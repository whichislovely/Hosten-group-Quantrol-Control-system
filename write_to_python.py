import os
from sympy import simplify
   

def create_experiment(self, run_continuous = False):
    '''
    Function is used to create the description of the experimental sequence.
    Python like description is saved as run_experiment.py
    run_continuous is used as a flag to indicate if the continuous run is required.
    '''
    
    #CREATING A FILE
    file_name = "run_experiment.py"
    if not os.path.exists(file_name):
        with open(file_name, 'w'): pass

    #IMPORT AND BUILD FUNCTIONS
    file = open(file_name,'w')
    indentation = ""
    file.write(indentation + "from artiq.experiment import *\n\n")
    file.write(indentation + "from numpy import linspace\n\n")
    file.write(indentation + "class " + file_name[:-3] + "(EnvExperiment):\n")
    indentation += "    "
    file.write(indentation + "def build(self):\n")
    indentation += "    "
    file.write(indentation + "self.setattr_device('core')\n")
    for _ in range(3):
        file.write(indentation + "self.setattr_device('urukul%d_cpld')\n" %_) 
        for i in range(4):
            file.write(indentation + "self.setattr_device('urukul%d_ch%d')\n" %(_,i)) 
    for _ in range(16):
        file.write(indentation + "self.setattr_device('ttl%d')\n" %_)
    file.write(indentation + "self.setattr_device('zotino0')\n")
    
    if run_continuous:
        file.write(indentation + "self.setattr_device('scheduler')\n")

    # If scan is needed prepare the variables
    if self.experiment.do_scan == True and self.experiment.scanned_variables_count > 0:
        #iterating over valid (not "None") scanned variables and creating an array to be used as a collection of names
        var_names = ""
        for_zipping = ""
        for variable in self.experiment.scanned_variables:
            if variable.name != "None":
                file.write(indentation + "self.%s = linspace(%f, %f, %d)\n"%(variable.name, variable.min_val, variable.max_val, self.experiment.number_of_steps))
                var_names += variable.name + ", "
                for_zipping += "self." + variable.name + ", "
    file.write("\n")
    indentation = indentation[:-4]

    # Overwriting the run method
    file.write(indentation + "@kernel\n")
    file.write(indentation + "def run(self):\n")
    indentation += "    "
    file.write(indentation + "self.core.reset()\n")
    file.write(indentation + "self.core.break_realtime()\n")
    if self.experiment.do_scan == True and self.experiment.scanned_variables_count > 0:
        # this delay needs to be optimized. It may depend on scanning parameters as well
        file.write(indentation + "delay(5*s)\n") 
    else:
        file.write(indentation + "delay(10*ms)\n") # this delay is added since our reference clock is 1GHz and self.core.break_realtime moves it forward by 15000 clock cycles
    
    # file.write(indentation + "self.zotino0.init()\n")
    # file.write(indentation + "self.urukul0_cpld.init()\n")
    # file.write(indentation + "self.urukul0_ch0.init()\n")
    # file.write(indentation + "self.urukul0_ch1.init()\n")
    # file.write(indentation + "self.urukul0_ch2.init()\n")
    # file.write(indentation + "self.urukul0_ch3.init()\n")
    # file.write(indentation + "self.urukul1_cpld.init()\n")
    # file.write(indentation + "self.urukul1_ch0.init()\n")
    # file.write(indentation + "self.urukul1_ch1.init()\n")
    # file.write(indentation + "self.urukul1_ch2.init()\n")
    # file.write(indentation + "self.urukul1_ch3.init()\n")
    # file.write(indentation + "self.urukul2_cpld.init()\n")
    # file.write(indentation + "self.urukul2_ch0.init()\n")
    # file.write(indentation + "self.urukul2_ch1.init()\n")
    # file.write(indentation + "self.urukul2_ch2.init()\n")
    # file.write(indentation + "self.urukul2_ch3.init()\n")

    # This is used to trigger the camera 10 times and discard those images
    file.write(indentation + "self.ttl8.off()\n")
    file.write(indentation + "self.ttl9.off()\n")
    file.write(indentation + "delay(100*ms)\n")

    if self.experiment.skip_images:
        file.write(indentation + "for _ in range(10):\n")
        indentation += "    "
        file.write(indentation + "self.ttl8.on()\n")
        file.write(indentation + "self.ttl9.on()\n")
        file.write(indentation + "delay(100*ms)\n")
        file.write(indentation + "self.ttl8.off()\n")
        file.write(indentation + "self.ttl9.off()\n")
        file.write(indentation + "delay(100*ms)\n")
        
        indentation = indentation[:-4]

    # Create an infinite while loop if needs to run continuously
    if run_continuous:
        file.write(indentation + "while True:\n")
        indentation += "    "
        file.write(indentation + "if self.scheduler.check_pause():\n")
        file.write(indentation + "    break\n")
        file.write(indentation + "else:\n")
        indentation += "    "
        file.write(indentation + "delay(10*ms)\n")


    # If scan is needed 
    if self.experiment.do_scan == True and self.experiment.scanned_variables_count > 0:
        #making a scanning loop 
        #introduce a flag for multi and single variable scan
        if self.experiment.scanned_variables_count > 1:
            file.write(indentation + "for %s in zip(%s):\n" %(var_names[:-2], for_zipping[:-2]))
        else:
            file.write(indentation + "for %s in %s:\n" %(var_names[:-2], for_zipping[:-2]))        
        indentation += "    "

 
    self.delta_t = 0



    #flag_init is used to indicate that there is no need for a delay calculation for the first row
    flag_init = 0
    for edge in range(self.sequence_num_rows):
        file.write(indentation + "#Edge number " + str(edge) + " name of edge: " + self.experiment.sequence[edge].name + "\n")
        if flag_init == 0: # in the first iteration it does not need to do anything as delta_t is assigned to 0
            flag_init = 1
        else:
            #Brackets are needed to take into account that for_python can be a mathematical expression with signs
            self.delta_t = str(simplify("(" + str(self.experiment.sequence[edge].for_python) + ")" + "-" + "(" + str(self.experiment.sequence[edge-1].for_python) + ")"))
            # self.delta_t = "(" + str(self.experiment.sequence[edge].for_python) + ")" + "-" + "(" + str(self.experiment.sequence[edge-1].for_python) + ")"
            try: #this try is used to try evaluating the expression. It will only be able to do so in case it is scanned
                exec("self.delta_t = " + self.delta_t)
            except:
                pass
        #ADDING A DELAY
        if self.delta_t != 0:
            file.write(indentation + "delay((" + str(self.delta_t) + ")*ms)\n")

        #DIGITAL CHANNEL CHANGES
        for index, channel in enumerate(self.experiment.sequence[edge].digital):
            if edge == 0 and index == 8: #adding a 5 ms delay to make changes into TTL channels
                file.write(indentation + "delay(5*ms)\n")

            if channel.changed == True:
                if channel.value == 1:
                    file.write(indentation + "self.ttl" + str(index) + ".on()\n") 
                else:
                    file.write(indentation + "self.ttl" + str(index) + ".off()\n") 

        #ANALOG CHANNEL CHANGES
        flag_zotino_change_needed = False      
        for index, channel in enumerate(self.experiment.sequence[edge].analog):
            if channel.changed == True:
                flag_zotino_change_needed = True
                if channel.is_scanned:
                    file.write(indentation + "self.zotino0.write_dac(%d, channel.for_python)\n" %index)
                else:
                    file.write(indentation + "self.zotino0.write_dac(%d, %.4f)\n" %(index, channel.value))
                
                # file.write(channel.for_python + ")\n")
        if flag_zotino_change_needed:
            file.write(indentation + "self.zotino0.load()\n")

        #DDS CHANNEL CHANGES
        for index, channel in enumerate(self.experiment.sequence[edge].dds):
            if channel.changed == True:
                urukul_num = int(index // 4)
                channel_num = int(index % 4)
                file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set_att(" + str(channel.attenuation.for_python) + "*dB) \n")    
                file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set(frequency = " + str(channel.frequency.for_python) + "*MHz, amplitude = " + str(channel.amplitude.for_python) + ", phase = " + str(channel.phase.for_python) + ")\n")    
                if channel.state.value == 1:
                    file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.on() \n")
                else:
                    file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.off() \n")
        
    if run_continuous:
        file.write(indentation + "self.core.wait_until_mu(now_mu())\n")
                
    file.close()


def create_go_to_edge(self, to_default = False):
    '''
    Function is used to write a description of experiment that will go to the edge selected in a tab.
    The description is saved as go_to_edge.py   
    The flag to_default is used to be able to go to default edge in the init_hardware function
    '''

    if to_default:
        # Set the edge value to default edge
        edge = 0
        file_name = "init_hardware.py"
    else:
        # The edge is defined by the currently selected tab as a last selected row in that tab
        if self.main_window.currentIndex() == 0:
            edge = self.sequence_table.selectedIndexes()[0].row()
        elif self.main_window.currentIndex() == 1:
            edge = self.digital_dummy.selectedIndexes()[0].row()    
        elif self.main_window.currentIndex() == 2:
            edge = self.analog_dummy.selectedIndexes()[0].row()    
        elif self.main_window.currentIndex() == 3:
            edge = self.dds_dummy.selectedIndexes()[0].row() - 2 # because top 2 rows are used for title
        file_name = "go_to_edge.py"

    self.experiment.go_to_edge = edge
    # Create a file if it is missing
    if not os.path.exists(file_name):
        with open(file_name, 'w'): pass
    file = open(file_name,'w')
    
    # Importing libraries and overwriting the build method
    indentation = ""
    file.write(indentation + "from artiq.experiment import *\n\n")
    file.write(indentation + "class " + file_name[:-3] + "(EnvExperiment):\n")
    indentation += "    "
    file.write(indentation + "def build(self):\n")
    indentation += "    "
    file.write(indentation + "self.setattr_device('core')\n")
    for _ in range(3):
        file.write(indentation + "self.setattr_device('urukul%d_cpld')\n" %_) 
        for i in range(4):
            file.write(indentation + "self.setattr_device('urukul%d_ch%d')\n" %(_,i)) 
    for _ in range(16):
        file.write(indentation + "self.setattr_device('ttl%d')\n" %_)
    file.write(indentation + "self.setattr_device('zotino0')\n")
    file.write("\n")
    indentation = indentation[:-4]
    
    # Overwriting the run method
    file.write(indentation + "@kernel\n")
    file.write(indentation + "def run(self):\n")
    indentation += "    "
    file.write(indentation + "self.core.reset()\n")
    file.write(indentation + "self.core.break_realtime()\n")
    file.write(indentation + "delay(5*ms)\n")
    
    # file.write(indentation + "self.zotino0.init()\n")
    # file.write(indentation + "self.urukul0_cpld.init()\n")
    # file.write(indentation + "self.urukul0_ch0.init()\n")
    # file.write(indentation + "self.urukul0_ch1.init()\n")
    # file.write(indentation + "self.urukul0_ch2.init()\n")
    # file.write(indentation + "self.urukul0_ch3.init()\n")
    # file.write(indentation + "self.urukul1_cpld.init()\n")
    # file.write(indentation + "self.urukul1_ch0.init()\n")
    # file.write(indentation + "self.urukul1_ch1.init()\n")
    # file.write(indentation + "self.urukul1_ch2.init()\n")
    # file.write(indentation + "self.urukul1_ch3.init()\n")
    # file.write(indentation + "self.urukul2_cpld.init()\n")
    # file.write(indentation + "self.urukul2_ch0.init()\n")
    # file.write(indentation + "self.urukul2_ch1.init()\n")
    # file.write(indentation + "self.urukul2_ch2.init()\n")
    # file.write(indentation + "self.urukul2_ch3.init()\n")
  
    # Assigning digital channels
    for index, channel in enumerate(self.experiment.sequence[edge].digital):
        if index == 8: #adding a 5 ms delay to make changes for more than 8 TTL channels. There is a limit of the buffer size
            file.write(indentation + "delay(5*ms)\n")
        if channel.value == 0:
            file.write(indentation + "self.ttl" + str(index) + ".off()\n")
        elif channel.value == 1:
            file.write(indentation + "self.ttl" + str(index) + ".on()\n")        

    # Assigning analog channels
    for index, channel in enumerate(self.experiment.sequence[edge].analog):
        file.write(indentation + "self.zotino0.write_dac(%d, %.4f)\n" %(index, channel.value))
    file.write(indentation + "self.zotino0.load()\n")
    
    # Assigning DDS channels
    for index, channel in enumerate(self.experiment.sequence[edge].dds):
        urukul_num = int(index // 4)
        channel_num = int(index % 4)
        file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set_att(" + str(channel.attenuation.value) + "*dB) \n")    
        file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".set(frequency = " + str(channel.frequency.value) + "*MHz, amplitude = " + str(channel.amplitude.value) + ", phase = " + str(channel.phase.value) + ")\n")    
        if channel.state.value == 1:
            file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.on() \n")
        elif channel.state.value == 0:
            file.write(indentation + "self.urukul" + str(urukul_num) + "_ch" + str(channel_num) + ".sw.off() \n")                

    file.close()