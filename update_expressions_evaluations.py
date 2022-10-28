import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



def do(self):
    #this while loop is done to accomodate all mutual dependencies. It may happen that user will crash the program by introducing closed loops.
    something_changed = True
    iterations = 0 #after the maximum number of iterations it will throw a warning message
    while something_changed and iterations < 20:
        iterations += 1
        something_changed = False

        self.experiment.sequence = sorted(self.experiment.sequence, key = lambda edge: edge.value)

        for edge_index, edge in enumerate(self.experiment.sequence):
            #UPDATING EDGE VALUES (TIME)
            try:
                exec("edge.value = " + str(edge.evaluation))
                name = "id" + str(edge.id)
                if self.experiment.variables[name].value != edge.value:
                    something_changed = True
                    self.experiment.variables[name].value = edge.value
            except:
                return "time expression edge number %d"%edge_index
                
            for channel_index, sub_channel in enumerate(edge.digital):
                #UPDATING DIGITAL CHANNELS
                try:
                    exec("sub_channel.value = " + str(sub_channel.evaluation))
                except:
                    return "digital channel %d, edge %d" %(channel_index, edge_index)
                if sub_channel.value < 0 or sub_channel.value > 1:
                    return "digital channel %d, edge %d" %(channel_index, edge_index)
            
            for channel_index, sub_channel in enumerate(edge.analog):
                #UPDATING ANALOG CHANNELS
                try:
                    exec("sub_channel.value = " + str(sub_channel.evaluation))
                except:
                    return "analog channel %d, edge %d" %(channel_index, edge_index)
                if sub_channel.value < -10 or sub_channel.value > 10:
                    return "analog channel %d, edge %d" %(channel_index, edge_index)
        
            for channel_index, sub_channel in enumerate(edge.dds):
                #UPDATING DDS CHANNELS
                try:
                    exec("sub_channel.frequency.value = " + str(sub_channel.frequency.evaluation))
                except:
                    return "DDS channel %d edge %d, frequency value" %(channel_index, edge_index)
                if sub_channel.frequency.value < 0 or sub_channel.frequency.value > 800:
                    return "DDS channel %d edge %d, frequency value" %(channel_index, edge_index)
                try:
                    exec("sub_channel.amplitude.value = " + str(sub_channel.amplitude.evaluation))
                except:
                    return "DDS channel %d edge %d, amplitude value" %(channel_index, edge_index)
                if sub_channel.amplitude.value < 0 or sub_channel.amplitude.value > 1:
                    return "DDS channel %d edge %d, amplitude value" %(channel_index, edge_index)           
                try:
                    exec("sub_channel.attenuation.value = " + str(sub_channel.attenuation.evaluation))
                except:
                    return "DDS channel %d edge %d, attenuation value" %(channel_index, edge_index)
                if sub_channel.attenuation.value < 0 or sub_channel.attenuation.value > 32:
                    return "DDS channel %d edge %d, attenuation value" %(channel_index, edge_index)
                try:
                    exec("sub_channel.phase.value = " + str(sub_channel.phase.evaluation))
                except:
                    return "DDS channel %d edge %d, channel state value" %(channel_index, edge_index)
                while sub_channel.phase.value < 0:
                    sub_channel.phase.value += 360
                sub_channel.phase.value = sub_channel.phase.value % 360
                exec("sub_channel.state.value = " + str(sub_channel.state.evaluation))
                if int(sub_channel.state.value) != 0 and int(sub_channel.state.value) != 1:
                    return "DDS channel %d edge %d, channel state value" %(channel_index, edge_index)

                sub_channel.amplitude.value = float(sub_channel.amplitude.value)
                sub_channel.attenuation.value = float(sub_channel.attenuation.value)
                sub_channel.phase.value = float(sub_channel.phase.value)
                
        self.experiment.sequence = sorted(self.experiment.sequence, key = lambda edge: edge.value)
        for row in range(len(self.experiment.sequence)):
            key = "id" + str(self.experiment.sequence[row].id)
            self.experiment.variables[key].value = self.experiment.sequence[row].value

    if iterations == 4:
        self.error_message("Please check for potential loops when the time edge depends on itself.", "Warning!")

