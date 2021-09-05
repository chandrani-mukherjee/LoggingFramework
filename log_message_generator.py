import logging
import os
import random
import zmq
from datetime import datetime
from time import sleep
# pip install Faker
from faker import Faker
from faker.providers import BaseProvider
# pip install pyzmq


random.seed = 0
Faker.seed = 0

logging.basicConfig()
_logger = logging.getLogger('test')
_logger.setLevel(logging.DEBUG)

class ModuleProvider(BaseProvider):

    def __init__(self):
        pass

    def module_name(self):
        return random.choice(['evse', 'ocpp', 'slac'])

    def module_state(self):
        # Random states are not really reasonable, but this is just for testing.
        return random.choice(['initializing', 'idle', 'charging', 'finalizing'])

    def module_output(self):
        # Make stdout have 2/3 probability.
        stream = random.choice(['stdout', 'stdout', 'stderr'])
        message = 'Something happened.'
        return (stream, message)


class ModuleEVSE(object):
    def __init__(self):
        pass

    @staticmethod
    def buildJson(moduleClass):
        log_output =  ModuleProvider().module_output()
        msg = {       
        "module" :  moduleClass.lstrip("Module"), \
        "timestamp" :  datetime.now().isoformat(), \
        "state" :  ModuleProvider().module_state(), \
        "log-stream" : log_output[0], \
        "log-message" :   log_output[1]
        }   

        return msg


class ModuleOCPP(object):
    def __init__(self):
        pass

    @staticmethod
    def buildJson(moduleClass):
        log_output =  ModuleProvider().module_output()
        msg = {       
        "module" :  moduleClass.lstrip("Module"), \
        "timestamp" :  datetime.now().isoformat(), \
        "state" :  ModuleProvider().module_state(), \
        "log-stream" : log_output[0], \
        "log-message" :   log_output[1]
        }

        return msg   


class ModuleSLAC(object):
    def __init__(self):
        pass

    @staticmethod
    def buildJson(moduleClass):
        log_output =  ModuleProvider().module_output()
        msg = {       
        "module" :  moduleClass.lstrip("Module"), \
        "timestamp" :  datetime.now().isoformat(), \
        "state" :  ModuleProvider().module_state(), \
        "log-stream" : log_output[0], \
        "log-message" :   log_output[1]
        }   

        return msg



class JsonBuilder:
    def __init__(self):
        self.name2class = {"ModuleSLAC":ModuleSLAC,"ModuleOCPP":ModuleOCPP,"ModuleEVSE":ModuleEVSE}

    def buildJson(self,moduleClass):
        print("moduleClass {0}".format(moduleClass))
        #inst = moduleClass()
        return self.name2class[moduleClass]().buildJson(moduleClass)

# A singletone class for initializing the socket  
class SockerInitiator:

    __instance = None
    def __init__(self):
        if SockerInitiator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            context = zmq.Context()
            socket = context.socket(zmq.PUB)
            socket.bind("tcp://*:5555")
            self.sock = socket
            SockerInitiator.__instance = self
    
    #Need to use this method to get the instance for this class
    @staticmethod
    def getinstance(*args, **kwargs):
        if SockerInitiator.__instance == None:
           SockerInitiator()
        return   SockerInitiator.__instance  
            
# A Generator class for generating Log Messages           
class MsgGenerator:

    def __init__(self): 
        #Get the initial Module Name and call its corresponding class to create the JSON response
        moduleName = ModuleProvider().module_name()
        moduleName = moduleName.upper()
        moduleClass = "Module" + moduleName
        jsonuilderObj = JsonBuilder()
        self.msg = jsonuilderObj.buildJson(moduleClass)
       
    #Calling next on the current class object will call this function which is a generator
    def __iter__(self):
        while True:
            yield self.msg
            moduleName = ModuleProvider().module_name()
            moduleName = moduleName.upper()
            moduleClass = "Module" + moduleName
            jsonuilderObj = JsonBuilder()
            self.msg = jsonuilderObj.buildJson(moduleClass)
            





#1. Call the socket class and get the object
#2. Generate a msg
#3. Send the Msg
if __name__ == '__main__':
    sockInit = SockerInitiator()
    msgiter =iter( MsgGenerator())
    i = 0
    while True:
        msg = next(msgiter)
        _logger.debug(msg)
        sockInit.sock.send_json(msg)
        sleep(random.uniform(0, 30))
        i += 1



    

