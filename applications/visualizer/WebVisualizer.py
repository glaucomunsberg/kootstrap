#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer, codecs, os, glob, json,traceback,sys
sys.path.append('../')

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from urlparse import urlparse, parse_qs



        
from system.Kootstrap import Kootstrap
from system.Metadata import Metadata


class S(BaseHTTPRequestHandler):
    
    _k                  = Kootstrap()
    
    folder_path_datasets    = _k.path_dataset()
    folder_path_models      = _k.path_model()
    folder_path_tests       = _k.path_test()
    
    
    folder_json_path    = _k.path_test()
    folder_log_path     = _k.path_log()
    
    files               = None
    file                = None
    time                = None
    json_file_name      = None
    logs_file_name      = None
    is_active           = False
    begin_at            = ""
    end_at              = ""
    epoch_total         = None
    epoch_current       = None
    classes_number      = None
    path_input_data     = None
    path_output_weight  = None
    target_size         = None
    batch_size          = None
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        
        query_components = parse_qs(urlparse(self.path).query)
        if not "model" in query_components and not "modelTests" in query_components and not "dataset" in query_components and not "modelTest" in query_components and not "test" in query_components:
            self.showIndex()
        elif "modelTest" in query_components:
            self.showModelTests(query_components["modelTests"],query_components["modelTest"])
        elif "modelTests" in query_components:
            self.showModelTests(query_components["modelTests"])
        elif "model" in query_components:
            self.showModel(query_components["model"])
        else:
            None
            
    def showIndex(self):        
        
        self._set_headers()
        f=codecs.open("manager/index.html", 'r')
        file_has_string = f.read()
        
        # datasets
        html_directories = ""
        directories = [dI for dI in os.listdir(self.folder_path_datasets) if os.path.isdir(os.path.join(self.folder_path_datasets,dI))]
        
        for directory in directories:
            #print 'DIR',directory
            dire = directory.encode("utf-8")
            html_directories += "<a href='/?dataset="+dire+"' class='collection-item'> "+dire+" </a>"
        file_has_string = file_has_string.replace("k_list_of_datasets",html_directories)
        
        # models
        html_directories = ""
        models = [dI for dI in os.listdir(self.folder_path_models) if os.path.isdir(os.path.join(self.folder_path_models,dI))]
        
        for model in models:
            #print 'DIR',model
            dire = model.encode("utf-8")
            html_directories += "<a href='/?model="+dire+"' class='collection-item'> "+dire+" </a>"
        file_has_string = file_has_string.replace("k_list_of_models",html_directories)
        
        # tests
        html_directories = ""
        tests = [dI for dI in os.listdir(self.folder_path_tests) if os.path.isdir(os.path.join(self.folder_path_tests,dI))]
        
        for test in tests:
            #print 'DIR',test
            dire = test.encode("utf-8")
            html_directories += "<a href='/?modelTests="+dire+"' class='collection-item'> "+dire+" </a>"
            
        file_has_string = file_has_string.replace("k_list_of_tests",html_directories)
        file_has_string = file_has_string.replace("k_version",self._k.config['version'].encode("utf-8"))
        file_has_string = file_has_string.replace("k_log_level",self._k.config['log_level'].encode("utf-8"))
        file_has_string = file_has_string.replace("k_train_size",str(self._k.config['train_proportional_size']).encode("utf-8"))
        file_has_string = file_has_string.replace("k_validation_size",str(self._k.config['validation_proportional_size']).encode("utf-8"))
        file_has_string = file_has_string.replace("k_test_size",str(self._k.config['test_proportional_size']).encode("utf-8"))
        
        self.wfile.write(file_has_string)
        
    def showModelTests(self,test_model):
        name_of_folder = test_model[0].encode("utf-8")
        self._set_headers()
        f=codecs.open("manager/showModelTests.html", 'r')
        file_has_string = f.read()
        
        # datasets
        html_directories = ""
        directories = [dI for dI in os.listdir(self.folder_path_tests+name_of_folder+"/") if os.path.isdir(os.path.join(self.folder_path_tests+name_of_folder+"/",dI))]
        
        for directory in directories:
            #print 'DIR',directory
            dire = directory.encode("utf-8")
            html_directories += "<a href='/?modelTest="+dire+"&modelTests="+name_of_folder+"' class='collection-item'> "+dire+" </a>"
        file_has_string = file_has_string.replace("k_list_of_tests_by_model",html_directories)
        file_has_string = file_has_string.replace("k_model_test",test_model[0].encode("utf-8"))
        
        self.wfile.write(file_has_string)
        
    def showModelTest(self,test_model,test):
        
        name_of_folder_model = test_model[0].encode("utf-8")
        name_of_folder_test  = test[0].encode("utf-8")
        
        self._set_headers()
        
        self.loss_data  = "["
        self.loss_label = "["
        self.acc_data   = "["
        self.acc_label  = "["
        self.time_label = "["
        self.time_data  = "[" 
        self.log_lines  = ""
        self.model_lines= ""
        
        folder = self.folder_json_path+name_of_folder_model+"/"+name_of_folder_test+"/"
        file   = folder+"metadata.json"
        #print "FOLDER:", folder
        
        if os.path.isfile():
            
            md_test = Metadata(file)
        else:
            self.loss_label+="]"
            self.acc_label+="]"
            self.time_label+="]"
            self.loss_data+="]"
            self.acc_data+="]"
            self.time_data+="]"
        
    def showModel(self,model):
        
        name_of_folder_model = model[0].encode("utf-8")
        
        self._set_headers()
        
        self.loss_data  = "["
        self.loss_label = "["
        self.acc_data   = "["
        self.acc_label  = "["
        self.time_label = "["
        self.time_data  = "[" 
        self.log_lines  = ""
        self.model_lines= ""
        self.k_list_classes = ""
        folder      = self.folder_path_models+name_of_folder_model+"/"
        path_file   = folder+"metadata.json"
        #print "FOLDER:", folder
        
        if os.path.isfile(path_file):
            
            
            md_model = Metadata(path_file)
            last_modifed_at = datetime.fromtimestamp(os.path.getctime(path_file)).strftime('%Y-%m-%d %H:%M:%S')
            
            
            # convert loss json to chartjs data
            for value in md_model.metadata['history_loss']:
                self.loss_data += str(value)+","
            self.loss_data+="]"
            for i in range(len(md_model.metadata['history_loss'])):
                self.loss_label += str(i)+","
            self.loss_label+="]"

            # convert loss json to chartjs data
            for value in md_model.metadata['history_acc']:
                self.acc_data += str(value)+","
            self.acc_data+="]"
            for i in range(len(md_model.metadata['history_acc'])):
                self.acc_label += str(i)+","
            self.acc_label+="]"

            # convert time json to chartjs data
            # try to old files not breack the executation
            try:
                for value in md_model.metadata['time_elapsed']:
                    self.time_data += str(value)+","

                for i in range(len(md_model.metadata['time_elapsed'])):
                    self.time_label += str(i)+","
            except:
                None
            self.time_data+="]"
            self.time_label+="]"

            # get the model inside the file
            # try to old files not breack the executation
            try:
                for layer in md_model.metadata['model_layers']:
                    
                    self.model_lines += "<tr> <td>{0}</td> <td>{1}</td> <td>{2}</td> </tr>".format(layer["layer"],layer["layer_name"],layer["layer_trainable"])
                    #self.model_lines += "<p>"+str(value)+"</p>"
            except:
                traceback.print_exc()
                self.model_lines+="<tr colspan='2'>No information about model</tr>"

            try:
                position = 0
                for class_name in md_model.metadata['classes']:
                    self.k_list_classes += "<a href='#' class='collection-item'> "+str(position)+" - "+class_name+" </a>"
                    position+=1
            except:
                None
                
            try:
                if md_model.metadata['active'] == True or md_model.metadata['active'] == "True":
                    self.is_active = True
            except:
                None

            try:
                self.begin_at = str(md_model.metadata['begin_at'])
            except:
                self.begin_at = "No information"

            try:
                self.end_at = str(md_model.metadata['end_at'])
            except:
                self.end_at = "No information"

            try:
                self.epoch_total = str(md_model.metadata['epoch_total'])
            except:
                self.epoch_total = -1

            try:
                self.epoch_current = str(md_model.metadata['epoch_current'])
            except:
                self.epoch_current = -1

            try:
                self.classes_number = str(md_model.metadata['classes_number'])
            except:
                self.classes_number = -1

            try:
                self.path_output_weight = str(md_model.metadata['path_output_weight'])
            except:
                self.path_output_weight = "No information"

            try:
                self.path_input_data = str(md_model.metadata['path_dataset'])
            except:
                self.path_input_data = "No information"

            try:
                self.target_size = str(md_model.metadata['target_size'])
            except:
                self.target_size = -1

            try:
                self.batch_size = str(md_model.metadata['batch_size'])
            except:
                self.batch_size = -1
                
            self.kootstrap_version  = str(md_model.metadata['kootstrap_version'])
            self.keras_version      = str(md_model.metadata['keras_version'])
            self.dataset_name       = str(md_model.metadata['train_dataset_name'])
            
        else:
            self.loss_label+="]"
            self.acc_label+="]"
            self.time_label+="]"
            self.loss_data+="]"
            self.acc_data+="]"
            self.time_data+="]"
        
        f=codecs.open("manager/showModel.html", 'r')
        file_has_string = f.read()
        file_has_string = file_has_string.replace("model_name",name_of_folder_model)
        file_has_string = file_has_string.replace("dataset_name",str(self.dataset_name))
        file_has_string = file_has_string.replace("k_list_classes",str(self.k_list_classes))
        file_has_string = file_has_string.replace("last_modification",str(last_modifed_at))
        file_has_string = file_has_string.replace("number_of_epochs",str(len(self.loss_label)))
        file_has_string = file_has_string.replace("loss_label",self.loss_label)
        file_has_string = file_has_string.replace("loss_data",self.loss_data)
        file_has_string = file_has_string.replace("acc_label",self.acc_label)
        file_has_string = file_has_string.replace("acc_data",self.acc_data)
        file_has_string = file_has_string.replace("time_label",self.time_label)
        file_has_string = file_has_string.replace("time_data",self.time_data)
        file_has_string = file_has_string.replace("log_lines",self.log_lines)
        file_has_string = file_has_string.replace("model_lines",self.model_lines)
        file_has_string = file_has_string.replace("end_at",self.end_at)
        file_has_string = file_has_string.replace("begin_at",self.begin_at)
        file_has_string = file_has_string.replace("epoch_total",self.epoch_total)
        file_has_string = file_has_string.replace("epoch_current",self.epoch_current)
        file_has_string = file_has_string.replace("classes_number",self.classes_number)
        file_has_string = file_has_string.replace("path_input_data",self.path_input_data)
        file_has_string = file_has_string.replace("path_output_weight",self.path_output_weight)
        file_has_string = file_has_string.replace("target_size",self.target_size)
        file_has_string = file_has_string.replace("target_size",self.target_size)
        file_has_string = file_has_string.replace("batch_size",self.batch_size)
        
    
        file_has_string = file_has_string.replace("keras_version",self.keras_version)
        file_has_string = file_has_string.replace("kootstrap_version",self.kootstrap_version)
        
        if self.is_active:
            file_has_string = file_has_string.replace("loader_action","document.querySelector(\"div[loader]\").style.display = \"\"")
        else:
            file_has_string = file_has_string.replace("loader_action","document.querySelector(\"div[loader]\").style.display = \"none\"")
        self.wfile.write(file_has_string)
        
    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>try get =]</h1></body></html>")
        
class WebVisualizer:
    
    def __init__(self):
        None
        
    def run(self,server_class=HTTPServer, handler_class=S, port=8000):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd'
        print 'open in browser http://localhost:'+str(port)
        httpd.serve_forever()