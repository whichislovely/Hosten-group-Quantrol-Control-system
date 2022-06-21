import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



def do(self):
    # checking each entry
    for row, edge in enumerate(self.experiment.sequence):
        #sequence table
        (edge.evaluation, edge.for_python, edge.is_scanned) = self.decode_input(self.sequence_table.item(row,3).text())
        name = "id" + str(edge.id)
        self.experiment.variables[name].evaluation = edge.evaluation
        self.experiment.variables[name].for_python = edge.for_python
        self.experiment.variables[name].is_scanned = edge.is_scanned
        #if edge.is_scanned == True:
        #    edge.time = edge.evaluation
        #else:
        #    exec("edge.time = " + str(edge.evaluation))

        #digital table
        for index in range(16):
            channel = edge.digital[index]
            col = index + 4
            
            (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(self.digital_table.item(row, col).text())
            #if channel.is_scanned == True:
            #    channel.value = channel.evaluation
            #else:
            #    exec("channel.value = " + str(channel.evaluation))

        #analog table
        for index in range(32):
            channel = edge.analog[index]
            col = index + 4
            (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(self.analog_table.item(row, col).text())

            #if channel.is_scanned == True:
            #    channel.value = channel.evaluation
            #else:
            #    exec("channel.value = " + str(channel.evaluation))

        #dds table
        for index in range(12):
            channel = edge.dds[index]
            dds_row = row + 2
            for setting in range(5):
                col = index * 6 + 4 + setting
                exec("(channel.%s.evaluation, channel.%s.for_python, channel.%s.is_scanned) = self.decode_input(self.dds_table.item(dds_row, col).text())" %(self.setting_dict[setting], self.setting_dict[setting], self.setting_dict[setting]))
                #exec("self.temp = channel.%s.is_scanned" %self.setting_dict[setting])
                #if self.temp == True:
                #    exec("channel.%s.value = channel.%s.evaluation" %(self.setting_dict[setting], self.setting_dict[setting]))
                #else:
                #    exec("self.temp_2 = channel.%s.evaluation" % self.setting_dict[setting])
                #    exec("channel.%s.value = "%self.setting_dict[setting] + str(self.temp_2))
        






