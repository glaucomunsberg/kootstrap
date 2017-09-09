#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, csv, os
import matplotlib
matplotlib.use('Agg') # fixing -X screen
import matplotlib.pyplot as plt

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from tester.Tester import Tester
    
    
class TopClass:
    
    path_csv            = None
    path_destiny        = None
    number_of_tops      = None
    number_of_classes   = None
    
    name_file_top_classes   = None
    file_name_top_classes   = None
    
    _name_files         = None
    _logger             = None
    
    def __init__(self,path_csv, path_destiny,number_of_tops,number_of_classes,logger=None):
        
        if logger == None:
            self._logger = Logger('TopClass')
        else:
            self._logger = logger
        
        self.path_predictions_csv   = path_csv
        self.path_destiny           = path_destiny
        self.number_of_tops         = number_of_tops
        self.number_of_classes      = number_of_classes
        
        self.file_name_top_classes  = self.path_destiny+"top_"+str(number_of_tops)+"_by_image.csv"
        self.name_file_top_classes  = "top_"+str(number_of_tops)+"_by_image.csv"
        
        self._name_files            = []
    def start(self):
        
        num_row         = 0
        num_coll        = 0
        array_values    = []
        array_position  = []
        file_out_csv    = open(self.file_name_top_classes,'w')
        with open(self.path_predictions_csv ,'r') as csvfile:
            reader_csv = csv.reader(csvfile, delimiter=';')
            
            # for each row we create a array the number of classes
            #   and possible best values 
            for indx, row in enumerate(reader_csv):
                self._name_files.append(row[1])
                if indx > 0:
                    array_values.append([0.0]*self.number_of_tops)
                    array_position.append([0]*self.number_of_tops)
                    
        with open(self.path_predictions_csv ,'r') as csvfile:
            reader_csv = csv.reader(csvfile, delimiter=';')    
            # for each row in file
            #   if row == header
            #       create the hearder with the name of classes
            #   else
            #       for each coll in row
            #           if the value is great the each values in array of row
            #               change the min position and value for corrent value
            for row in reader_csv:
                
                if num_row % 1000 == 0:
                    self._logger.info("TopClass: Processed {0} rows".format(num_row))
                    print 'TopClass: Process '+str(num_row)+" rows",
                
                if num_row == 0: 
                    the_header = "image name;"
                    for colum in row:
                        if num_coll != self.number_of_classes+2 and num_coll > 1:
                            the_header += colum+";"
                        num_coll+=1
                    the_header += os.linesep
                    file_out_csv.write(the_header)
                else:
                    for collum in row:
                        #print 'num_row->',num_row
                        if num_coll <= self.number_of_classes and num_coll > 1 :
                            the_max_value = float(max(array_values[num_row-1]))
                            the_min_value = float(min(array_values[num_row-1]))
                            the_value = float(collum)
                            if the_value > the_min_value:
                                the_position = array_values[num_row-1].index(the_min_value)
                                array_values[num_row-1][the_position] = the_value
                                array_position[num_row-1][the_position] = num_coll
                        else:
                            None
                            #print 'Coll->',num_coll
                        num_coll+=1
                num_row += 1
                num_coll = 0
                
            num_row = 0
            # for each classe
            #   if position is on positions
            #       value is one (top)
            #   else
            #       value is zero 
            for num, positions in enumerate(array_position):
                the_values = ""
                
                #print 'Positions',positions
                #print 'Values   ',array_values[num]
                the_values+= self._name_files[num+1]+";"
                for i in range(self.number_of_classes+1):
                    if i != 0:
                        if i in positions:
                            the_values  += "1;"
                        else:
                            the_values  += "0;"            
                the_values += os.linesep
                file_out_csv.write(the_values)

            file_out_csv.close()
            self._logger.info("TopClass: Finished!")
            
class TopHistogram:
    
    _logger                 = None
    
    path_predictions_csv    = None
    path_destiny            = None
    
    number_of_tops          = None
    number_of_classes       = None
    number_limit_to_y       = None
    
    save_csv                = None
    save_png                = None
    save_list_image         = None
    
    title                   = None
    
    file_name_out_csv       = None
    file_name_out_png       = None
    file_name_out_list_csv  = None
    
    
    def __init__(self,args,path_csv,path_destiny,number_of_classes,logger=None):
        
        if logger == None:
            self._logger = Logger('TopClass')
        else:
            self._logger = logger
            
        if args.save_histogram_to_csv == "true":
            self.save_csv   = True
        else:
            self.save_csv   = False
            
        if args.save_histogram_to_png == "true":
            self.save_png   = True
        else:
            self.save_png   = False
            
        if args.save_list_image == "true":
            self.save_list_image = True
        else:
            self.save_list_image = False
        
        self.number_of_tops         = args.number_of_tops
        self.number_limit_to_y      = args.number_limit_to_y
        self.title                  = args.title
        
        self.path_predictions_csv   = path_csv
        self.path_destiny           = path_destiny
        self.number_of_classes      = number_of_classes
        
        self.file_name_out_csv      = self.path_destiny+"top_"+str(args.number_of_tops)+"_histogram.csv"
        self.file_name_out_png      = self.path_destiny+"top_"+str(args.number_of_tops)+"_histogram.png"
        self.file_name_out_list_csv = self.path_destiny+"top_"+str(args.number_of_tops)+"_histogram_list.csv"
        
    def start(self):
        
        num_row = 0
        num_coll= 0
        array_titles = []
        array_values = []
        array_images = {}
        if self.save_csv:
            file_out_csv    = open(self.file_name_out_csv,'w')
            
        if self.save_list_image:
            file_name_out_list_csv    = open(self.file_name_out_list_csv,'w') 
        
        with open(self.path_predictions_csv,'r') as csvfile:
            reader_csv = csv.reader(csvfile,delimiter=';')
            for row in reader_csv:
                if num_row % 1000 == 0:
                    self._logger.info("TopHistogram: Processed {0} rows".format(num_row))
                    print 'TopHistogram: Processed',num_row,'rows'
                if num_row == 0:
                    the_header_csv = ""
                    classes_names = []
                    for colum in row:
                        if num_coll != self.number_of_classes+1:
                            the_header_csv += colum+";"
                            classes_names.append(colum)
                            if num_coll != 0:
                                array_titles.append(num_coll)
                                #array_titles.append(the_header_csv)
                            array_values.append(0)
                        num_coll+=1
                    the_header_csv += os.linesep
                    if self.save_csv:
                        file_out_csv.write(the_header_csv)
                else:
                    for position,collum in enumerate(row):
                        if num_coll== 0:
                            array_values[num_coll] = row[0]  
                        elif num_coll != self.number_of_classes+1:
                            top_value = int(collum)
                            array_values[num_coll]  += top_value
                            if top_value == 1:
                                if array_titles[position] in array_images:
                                    array_images[array_titles[position]].append(row[0])
                                else:
                                    array_images[array_titles[position]]= [row[0]]
                                
                        num_coll+=1
                num_row += 1
                num_coll = 0
            print 'TopHistogram: Processed',num_row,'rows'
        the_values = ""
        for value in array_values:
            the_values += str(value)+";"
        the_values += os.linesep
        
        if self.save_csv:
            file_out_csv.write(the_values)
            file_out_csv.close()
            
        if self.save_png:
            plt.grid(True)
            plt.xlabel('Per class')
            plt.ylabel('Number of Images')
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.plot(array_titles, array_values[1:], label='Activations')
            ax.grid(True,linestyle="dashed")
            ax.set_xlabel("Per class", fontsize=10)
            ax.set_ylabel("Number of Images", fontsize=12)

            if self.number_limit_to_y != -1:
                ax.set_xlim([0,len(array_titles)])
                ax.set_ylim([0,self.number_limit_to_y])

            plt.title(self.title)
            ax.legend()
            fig.savefig(self.file_name_out_png)
            
        if self.save_list_image:
            
            # cal the collum and number of rows
            num_of_collums = len(array_images)
            num_of_rows = -1
            for classes in array_images.iterkeys():
                if len(array_images[classes]) > num_of_rows:
                    num_of_rows = len(array_images[classes])
            
            list_of_images = ""
            for classe in array_images.iterkeys():
                list_of_images += classes_names[classe-1]+";"
            list_of_images+= os.linesep
            for i in range(num_of_rows):
                for classe in array_images.iterkeys():
                    #print 'i,class,value',i,classe,array_images[classe][i]
                    if i < len(array_images[classe]):
                        list_of_images+= array_images[classe][i]+";"
                    else:
                        list_of_images+= ";"
                list_of_images+= os.linesep
                
            file_name_out_list_csv.write(list_of_images)
            file_name_out_list_csv.close()