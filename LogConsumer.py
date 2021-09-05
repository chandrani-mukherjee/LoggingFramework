import zmq
import asyncore
import socket
import json
import logging
from datetime import datetime
from urllib.parse import urlparse

logging.basicConfig()
_logger = logging.getLogger('AsyncoreLog')
_logger.setLevel(logging.DEBUG)

class HTTPClient(asyncore.dispatcher):

    def __init__(self, url):
        asyncore.dispatcher.__init__(self)
        self.name2class = {"SLAC":"handle_ModuleSLAC","OCPP":"handle_ModuleOCPP","EVSE":"handle_ModuleEVSE"}
        self.moduleMetas = {}
        self.context = zmq.Context()
        recvr = zmq.Socket(self.context, zmq.SUB)
        recvr.setsockopt(zmq.SUBSCRIBE,b'')
        self.set_socket(recvr)
        self.parsed_url = urlparse(url)
        self.connect("tcp://localhost:5555")   
        self.buffer = bytes('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' %
                            ("tcp://localhost",5555), 'ascii')

   
    def handle_ModuleSLAC(self,decodeMsg):
        _logger.debug("Inside handle_ModuleSLAC")
        with open("logSLACMsg",'w',encoding = 'utf-8') as fileSLAC:
            fileSLAC.write(decodeMsg)
        

    def handle_ModuleOCPP(self,decodeMsg):
        _logger.debug("Inside handle_ModuleOCPP")
        with open("logOCPPMsg",'w',encoding = 'utf-8') as fileOCPP:
            fileOCPP.write(decodeMsg)
        

    def handle_ModuleEVSE(self,decodeMsg):
        _logger.debug("Inside handle_ModuleEVSE")
        with open("logEVSEMsg",'w',encoding = 'utf-8') as fileEVSE:
            fileEVSE.write(decodeMsg)
        

    
    def set_socket(self, sock, map=None):
        self.socket = sock
        self._fileno = sock.getsockopt(zmq.FD)
        self.add_channel(map)        

    def handle_read_event(self):
        # check if really readable
        revents = self.socket.getsockopt(zmq.EVENTS)
        while revents & zmq.POLLIN:
            self.handle_read()
            revents = self.socket.getsockopt(zmq.EVENTS)

    def connect(self, *args):
        self.socket.connect(*args)
        self.connected = True

    def handle_close(self):
        #print("In handle close")
        self.close()
    
    def handle_expt_event(self) -> None:
        _logger.debug("Ignore Json related execptions")
    
    def handle_leastEmissiveModule(self,data):
        _logger.debug("The module did not respons for a long time", data)

    def handle_read(self):
        try:
            #Receive buffer size from socket stream
            logMsg = self.recv(8192)
            decodeMsg = logMsg.decode('utf-8')
            _logger.debug(decodeMsg)
            jsonObj = json.loads(decodeMsg)
            #Get the handler corresponding to the module
            metName = self.name2class[jsonObj["module"]]
            getattr(HTTPClient,str(metName))(self,decodeMsg)
            #Log the intial log time and last log time for each module
            if jsonObj["module"] not in self.moduleMetas.keys():
                self.moduleMetas[jsonObj["module"]] = {"logStartTime":jsonObj["timestamp"],"logEndTime":jsonObj["timestamp"]}
            else:
                self.moduleMetas[jsonObj["module"]]["logEndTime"] = jsonObj["timestamp"]
            
            #Sort the module metas with last received log time to trigger alert
            date_format = "%Y-%m-%dT%H:%M:%S.%f" 
            sortedMeta = sorted(self.moduleMetas.items(), key=lambda x: datetime.strptime(x[1]["logEndTime"],date_format))
            dateDiff = datetime.strptime(datetime.now().strftime(date_format),date_format) -  datetime.strptime(sortedMeta[0][1]["logEndTime"] ,date_format)
            if dateDiff.total_seconds() > 120:
                self.handle_leastEmissiveModule(sortedMeta[0][0])
              
        except Exception as e:
            _logger.debug("There was an exception " , str(e))
               

    def readable(self):
        _logger.debug("In readable")
        return True

    def writable(self):
        return False

    def handle_write(self):
       pass

if __name__ == '__main__':
    try:
        client = HTTPClient('tcp://localhost')
        asyncore.loop()
    except KeyboardInterrupt:
        asyncore.close_all()
    finally:
        _logger.debug("Program Finished")
