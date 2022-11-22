import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def build(self):
    self.experiment = self.Experiment()
    self.sequence_num_rows = 1
    self.setting_dict = {0:"frequency", 1:"amplitude", 2:"attenuation", 3:"phase", 4:"state"}
    self.max_dict = {0: 800, 1: 1, 2: 32, 3: 360, 4: 1} #max and min needs to be checked 
    self.min_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}  #max and min needs to be checked 
    self.to_update = False
    self.green = QColor(37,211,102)
    self.red = QColor(247,120,120)
    self.gray = QColor(100,100,100)
    self.white = QColor(255,255,255)
    

    self.experiment.sequence = [self.Edge("Default")]
    self.experiment.variables['id0'] = self.Variable(name = "id0", value = 0.0, for_python = 0.0)
    self.experiment.variables[''] = self.Variable(name = '', value = 0.0, for_python = 0.0)   #in order to be able to process expressions like -5 we need to have it as first item in decode will be "" that should be 0

    #INITIAL PARAMETERS
    for i in range(16):
        exec("self.experiment.sequence[0].digital[%d].changed = True" %i)
    for i in range(32):
        exec("self.experiment.sequence[0].analog[%d].changed = True" %i)
    for i in range(12):
        exec("self.experiment.sequence[0].dds[%d].changed = True" %i)
    

    #FROM HERE ON IT SHOULD BE MOVED TO DEFAULT
    self.experiment.title_digital_tab = ["#","Name","Time (ms)", ""]
    for _ in range(16):
        dummy_str = "D" + str(_) + "  "
        code = """self.experiment.title_digital_tab.append('%s')"""
        exec(code % dummy_str)  

    self.experiment.title_analog_tab = ["#","Name","Time (ms)", ""]
    for _ in range(32):
        dummy_str = "A" + str(_) + "  "
        code = """self.experiment.title_analog_tab.append('%s')"""
        exec(code % dummy_str) 

    self.experiment.title_dds_tab = ["#","Name","Time (ms)", ""]
    for _ in range(12):
        dummy_str = "DDS" + str(_) + "  "
        code = """self.experiment.title_dds_tab.append('%s')"""
        exec(code % dummy_str)  




    #assigning default values to channel values of a digital tab
    self.experiment.sequence[0].digital[8].value = 1
    self.experiment.sequence[0].digital[8].expression = "1"
    self.experiment.sequence[0].digital[8].evaluation = 1

    #assigning default values to channel names and values that won't change much
    self.experiment.title_digital_tab[0+4] += "\nX shutter"
    self.experiment.title_digital_tab[1+4] += "\nXqwp shutter"
    self.experiment.title_digital_tab[2+4] += "\nY shutter"
    self.experiment.title_digital_tab[3+4] += "\nYqwp shutter"
    self.experiment.title_digital_tab[4+4] += "\nZtop shutter"
    self.experiment.title_digital_tab[5+4] += "\nZbot shutter"
    self.experiment.title_digital_tab[6+4] += "\nRepump shutter"
    self.experiment.title_digital_tab[7+4] += "\nMOT B-fld switch"
    self.experiment.title_digital_tab[8+4] += "\nZ camera trig"
    self.experiment.title_digital_tab[9+4] += "\nX-Y camera trig"
    self.experiment.title_dds_tab[0+4] += "Repump offset"
    self.experiment.title_dds_tab[1+4] += "Cooling offset"
    self.experiment.title_dds_tab[2+4] += "RF offset for 3.6GHz (SSB1)"
    self.experiment.title_dds_tab[3+4] += "Seeded laser 5 AOM"
    self.experiment.title_dds_tab[4+4] += "Repump AOM"
    self.experiment.title_dds_tab[5+4] += "3D-XY MOT AOM"
    self.experiment.title_dds_tab[6+4] += "3D-Z MOT AOM"
    self.experiment.title_dds_tab[7+4] += "2D MOT AOM"
    self.experiment.title_dds_tab[8+4] += "2D PUSH AOM"
    self.experiment.title_dds_tab[9+4] += "Raman 1 AOM"
    self.experiment.title_dds_tab[10+4] += "Raman 2 AOM"
    #DDS0
    self.experiment.sequence[0].dds[0].frequency.value = 226.73083
    self.experiment.sequence[0].dds[0].frequency.evaluation = 226.73083
    self.experiment.sequence[0].dds[0].frequency.expression = 226.73083
    self.experiment.sequence[0].dds[0].amplitude.value = 0.9
    self.experiment.sequence[0].dds[0].amplitude.evaluation = 0.9
    self.experiment.sequence[0].dds[0].amplitude.expression = 0.9
    self.experiment.sequence[0].dds[0].state.value = 1.0
    self.experiment.sequence[0].dds[0].state.evaluation = 1.0
    self.experiment.sequence[0].dds[0].state.expression = 1.0
    #DDS1
    self.experiment.sequence[0].dds[1].frequency.value = 386.605
    self.experiment.sequence[0].dds[1].frequency.evaluation = 386.605
    self.experiment.sequence[0].dds[1].frequency.expression = 386.605
    self.experiment.sequence[0].dds[1].amplitude.value = 0.3
    self.experiment.sequence[0].dds[1].amplitude.evaluation = 0.3
    self.experiment.sequence[0].dds[1].amplitude.expression = 0.3
    self.experiment.sequence[0].dds[1].attenuation.value = 0.5
    self.experiment.sequence[0].dds[1].attenuation.evaluation = 0.5
    self.experiment.sequence[0].dds[1].attenuation.expression = 0.5
    self.experiment.sequence[0].dds[1].state.value = 1.0
    self.experiment.sequence[0].dds[1].state.evaluation = 1.0
    self.experiment.sequence[0].dds[1].state.expression = 1.0
    #DDS2
    self.experiment.sequence[0].dds[2].frequency.value = 182.65869
    self.experiment.sequence[0].dds[2].frequency.evaluation = 182.65869
    self.experiment.sequence[0].dds[2].frequency.expression = 182.65869
    self.experiment.sequence[0].dds[2].amplitude.value = 0.3
    self.experiment.sequence[0].dds[2].amplitude.evaluation = 0.3
    self.experiment.sequence[0].dds[2].amplitude.expression = 0.3
    self.experiment.sequence[0].dds[2].attenuation.value = 0.5
    self.experiment.sequence[0].dds[2].attenuation.evaluation = 0.5
    self.experiment.sequence[0].dds[2].attenuation.expression = 0.5
    self.experiment.sequence[0].dds[2].state.value = 1.0
    self.experiment.sequence[0].dds[2].state.evaluation = 1.0
    self.experiment.sequence[0].dds[2].state.expression = 1.0
    #DDS3
    self.experiment.sequence[0].dds[3].frequency.value = 80.0
    self.experiment.sequence[0].dds[3].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[3].frequency.expression = 80.0
    self.experiment.sequence[0].dds[3].amplitude.value = 0.2
    self.experiment.sequence[0].dds[3].amplitude.evaluation = 0.2
    self.experiment.sequence[0].dds[3].amplitude.expression = 0.2
    self.experiment.sequence[0].dds[3].attenuation.value = 0.0
    self.experiment.sequence[0].dds[3].attenuation.evaluation = 0.0
    self.experiment.sequence[0].dds[3].attenuation.expression = 0.0
    self.experiment.sequence[0].dds[3].state.value = 1.0
    self.experiment.sequence[0].dds[3].state.evaluation = 1.0
    self.experiment.sequence[0].dds[3].state.expression = 1.0
    #DDS4
    self.experiment.sequence[0].dds[4].frequency.value = 80.0
    self.experiment.sequence[0].dds[4].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[4].frequency.expression = 80.0
    self.experiment.sequence[0].dds[4].amplitude.value = 0.4
    self.experiment.sequence[0].dds[4].amplitude.evaluation = 0.4
    self.experiment.sequence[0].dds[4].amplitude.expression = 0.4
    self.experiment.sequence[0].dds[4].state.value = 1.0
    self.experiment.sequence[0].dds[4].state.evaluation = 1.0
    self.experiment.sequence[0].dds[4].state.expression = 1.0
    #DDS5
    self.experiment.sequence[0].dds[5].frequency.value = 80.0
    self.experiment.sequence[0].dds[5].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[5].frequency.expression = 80.0
    self.experiment.sequence[0].dds[5].amplitude.value = 0.2
    self.experiment.sequence[0].dds[5].amplitude.evaluation = 0.2
    self.experiment.sequence[0].dds[5].amplitude.expression = 0.2
    self.experiment.sequence[0].dds[5].state.value = 1.0
    self.experiment.sequence[0].dds[5].state.evaluation = 1.0
    self.experiment.sequence[0].dds[5].state.expression = 1.0
    #DDS6
    self.experiment.sequence[0].dds[6].frequency.value = 80.0
    self.experiment.sequence[0].dds[6].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[6].frequency.expression = 80.0
    self.experiment.sequence[0].dds[6].amplitude.value = 0.2
    self.experiment.sequence[0].dds[6].amplitude.evaluation = 0.2
    self.experiment.sequence[0].dds[6].amplitude.expression = 0.2
    self.experiment.sequence[0].dds[6].state.value = 1.0
    self.experiment.sequence[0].dds[6].state.evaluation = 1.0
    self.experiment.sequence[0].dds[6].state.expression = 1.0
    #DDS7
    self.experiment.sequence[0].dds[7].frequency.value = 80.0
    self.experiment.sequence[0].dds[7].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[7].frequency.expression = 80.0
    self.experiment.sequence[0].dds[7].amplitude.value = 0.25
    self.experiment.sequence[0].dds[7].amplitude.evaluation = 0.25
    self.experiment.sequence[0].dds[7].amplitude.expression = 0.25
    self.experiment.sequence[0].dds[7].state.value = 1.0
    self.experiment.sequence[0].dds[7].state.evaluation = 1.0
    self.experiment.sequence[0].dds[7].state.expression = 1.0
    #DDS8
    self.experiment.sequence[0].dds[8].frequency.value = 80.0
    self.experiment.sequence[0].dds[8].frequency.evaluation = 80.0
    self.experiment.sequence[0].dds[8].frequency.expression = 80.0
    self.experiment.sequence[0].dds[8].amplitude.value = 0.2
    self.experiment.sequence[0].dds[8].amplitude.evaluation = 0.2
    self.experiment.sequence[0].dds[8].amplitude.expression = 0.2
    self.experiment.sequence[0].dds[8].state.value = 1.0
    self.experiment.sequence[0].dds[8].state.evaluation = 1.0
    self.experiment.sequence[0].dds[8].state.expression = 1.0





