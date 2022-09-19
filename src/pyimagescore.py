# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep

import utils.mylog as mylog
import utils.jsonprms as jsonprms
import utils.file_utils as file_utils
import utils.str_utils as str_utils
from utils.mydecorators import _error_decorator, _trace_decorator
import inspect

import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image


class Pyimagescore:
      
        def __init__(self):                                
               pass 
               

        def trace(self, stck):                
                self.log.lg(f"{stck.function} ({ stck.filename}-{stck.lineno})")

        # init
        @_trace_decorator
        @_error_decorator()
        def init(self):            
                self.trace(inspect.stack()[0])                
                pass

        def testo(self):         
                self.trace(inspect.stack()[0])
                
                try:     
                        
                        pass

                except Exception as e:
                        self.log.errlg(e)  
                        self.driver.close()
                        self.driver.quit()        

        def init_main(self, command, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack()[0])
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)                        
                        self.test = self.jsprms.prms['test']                                               
                        self.log.lg("=HERE WE GO=")
                        keep_log_time = self.jsprms.prms['keep_log_time']
                        keep_log_unit = self.jsprms.prms['keep_log_unit']
                        self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)                        
                except Exception as e:
                        self.log.errlg(f"Wasted, very wasted : {e}")
                        raise

        def main(self):                         
                try:
                        # InitBot
                        # args
                        nbargs = len(sys.argv)
                        command = "doreport" if (nbargs == 1) else sys.argv[1]
                        #command = "test" if (nbargs == 1) else sys.argv[1]
                        # json parameters from file
                        jsonfile = "default" if (nbargs < 3) else sys.argv[2].lower()          
                        param = "default" if (nbargs < 4) else sys.argv[3].lower()                
                        print(f"command={command}") 
                        self.init_main(command, jsonfile) 
                        #logs
                       
                        # for tests command = "test"
                        self.trace(inspect.stack()[0])     
                        self.driver = self.init()                        
                        print(command)                                                       
                        if (command=="test"):   
                                print(inspect.stack()[0])

                        self.log.lg("=THE END COMPLETE=")
                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        pass
                except Exception as e:

                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        self.log.errlg(e)                       
                        return False
                finally:
                        print("==>> DONE <<==")
       
        


              
               
    

        
                

        

