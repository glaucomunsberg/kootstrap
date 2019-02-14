#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, matplotlib, json, argparse
sys.path.append('../')

matplotlib.use('Agg')  # fixing -X screen
import matplotlib.pyplot as plt

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Helper import Helper


class Plot:

    _k = None
    _helper = None
    _args = None
    path_file = None


    def __init__(self, args):

        self._k = Kootstrap()
        self._helper = Helper()

        self._args = args

        if self._args.model_name is None:
            raise ValueError('arg --model_name need by setted')

        self.path_metadata_model_json = self._k.path_model() + self._args.model_name+"/metadata.json"


    def start(self):

        json_file = open(self.path_metadata_model_json, 'r').read()
        loaded_model_json = json.loads(json_file)

        loss = loaded_model_json['history_loss']
        acc = loaded_model_json['history_acc']

        array_loss_values = []
        array_loss_titles = []
        array_acc_values = []
        array_acc_titles = []

        value = 0
        for loss_item in loss:
            array_loss_values.append(loss_item)
            array_loss_titles.append(str(value))
            value += 1

        value = 0
        for acc_item in acc:
            array_acc_values.append(acc_item)
            array_acc_titles.append(str(value))
            value += 1

        path_destiny = self._k.path_model()+self._args.model_name+"/"
        serial_name = self._helper.getSerialNow()

        self.save(array_acc_titles, array_acc_values, 'Accuracity', 'Epochs', path_destiny+self._args.model_name+"_acc_"+serial_name+".png")
        self.save(array_loss_titles, array_loss_values, 'Loss', 'Epochs', path_destiny+self._args.model_name+"_loss_"+serial_name+".png")

    def save(self, array_titles, array_values, xlabel, ylabel, file_name_out_png):

        plt.grid(True)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(array_values, label=xlabel)
        ax.grid(True, linestyle="dashed")
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.autoscale(enable=True)

        #if self.number_limit_to_y != -1:
        #    ax.set_xlim([0, len(array_titles)])
        #    ax.set_ylim([0, self.number_limit_to_y])

        #plt.title(self._args.title)
        ax.legend()
        fig.savefig(file_name_out_png)