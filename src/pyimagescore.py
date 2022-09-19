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
import glob

class ResultCls():
        def __init__(self, name, score): 
                self.name = name
                self.score = score   
class Pyimagescore:
      
        def __init__(self):                                
               self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        def trace(self, stck):                
                self.log.lg(f"{stck.function} ({ stck.filename}-{stck.lineno})")

        # init
        @_trace_decorator
        @_error_decorator()
        def init(self):            
                self.trace(inspect.stack()[0])                

        @_trace_decorator        
        @_error_decorator()
        def write_to_result_file(self, text_file, pth, score):                                       
                text_file.write("#####################\n")                                                                
                text_file.write(f"{pth}\n")
                text_file.write(f"image ={pth}\n")
                text_file.write(f"score ={score}\n")

        @_trace_decorator
        @_error_decorator()
        def prepare_image(self, image):
                if image.mode != 'RGB':
                        image = image.convert("RGB")
                Transform = transforms.Compose([
                        transforms.Resize([224,224]),      
                        transforms.ToTensor(),
                        ])
                image = Transform(image)   
                image = image.unsqueeze(0)
                return image.to(self.device)

        @_trace_decorator
        @_error_decorator()
        def predict(self, image, model):
                image = self.prepare_image(image)
                with torch.no_grad():
                        preds = model(image)
                return r'%.2f' % preds.item()
        
        @_trace_decorator
        @_error_decorator()
        def class_and_write(self, reportArray):    
                # classement et ecriture résultats                
                reportArray.sort(key=lambda x: x.score, reverse=True)
                result_file_path =  f"{self.root_app}{os.path.sep}data{os.path.sep}results.txt"
                text_file = open(result_file_path, "w")     
                for report in reportArray:
                        self.write_to_result_file(text_file, report.name, report.score)                
                text_file.close() 

        @_trace_decorator
        @_error_decorator()
        def test(self):         
                theimages = list(glob.glob(os.path.join("data/images",'*.*')))
                print(theimages)                
                resnetfile = f"{self.root_app}{os.path.sep}data{os.path.sep}models{os.path.sep}{self.jsprms.prms['resnet_file']}"
                reportArray = []
                for img in theimages:
                        image = Image.open(img)
                        model = torchvision.models.resnet50()
                        # num_ftrs = model.fc.in_features
                        # model.fc = torch.nn.Linear(num_ftrs, 1000)
                        # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input                        
                        model.fc = torch.nn.Linear(in_features=2048, out_features=1)
                        model.load_state_dict(torch.load(resnetfile, map_location=self.device)) 
                        model.eval().to(self.device)
                        print(img)
                        score = self.predict(image, model)
                        report = ResultCls(name=os.path.basename(img), score = score)
                        reportArray.append(report)                        
                        print(f'Popularity score: {score}')
                        self.class_and_write(reportArray=reportArray)
        
        def init_main(self, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack()[0])
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)                        
                        # self.test = self.jsprms.prms['test']                                               
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
                        command = "test" if (nbargs == 1) else sys.argv[1]                        
                        # json parameters from file
                        jsonfile = "default" if (nbargs < 3) else sys.argv[2].lower()          
                        param = "default" if (nbargs < 4) else sys.argv[3].lower()                
                        print(f"command={command}") 
                        self.init_main(command, jsonfile) 
                        #logs
                        # for tests command = "test"
                        self.trace(inspect.stack()[0])     
                        self.driver = self.init_main(jsonfile)                        
                        print(command)                                                       
                        if (command=="test"):   
                                self.test()
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
       