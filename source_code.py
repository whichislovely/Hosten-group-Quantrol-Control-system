'''
    |||||||   ||    ||    ||    ||    ||  ||||||||  ||||||    |||||   ||
    ||   ||   ||    ||   ||||   |||   ||     ||     ||   ||  ||   ||  ||
    ||   ||   ||    ||  ||  ||  || || ||     ||     ||   ||  ||   ||  ||
    ||   ||   ||    ||  ||||||  ||  | ||     ||     ||||||   ||   ||  ||
    ||   ||   ||    ||  ||  ||  ||   |||     ||     ||  ||   ||   ||  ||
    ||||||||   ||||||   ||  ||  ||    ||     ||     ||   ||   |||||   ||||||
          ||

Quantrol is used as a high level solution built on top of artiq infrastructure to allow scientists to use precise
timing control system with no prerequisite of coding. It features an easy to interpret table based experimental
sequence description, variables use and scan, input values allowed range check and many more.

Author  :   Vyacheslav Li 
Email   :   vyacheslav.li.1991@gmail.com
Date    :   07.30.2024
Version :   1.0
Contact :   https://hostenlab.pages.ist.ac.at/contact/
'''

from os import error
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import write_to_python
import tabs
import pickle
from datetime import datetime
from copy import deepcopy
import update
import threading
import config

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    '''
    Main window that includes everything that needs to be displayed to the user
    '''
    class Edge:
        '''
        An object that is used to describe the time edge of experimental sequence
        Attributes description:
            expression  :   Mathematical expression used to describe the time edge
            evaluation  :   Expression that can be executed in python to evaluate the time edge. 
                            In case there is a scanned variable in the expression its minimum value is assigned to
                            be able to sort the sequence. It is a user responsibility to make sure that the sequence
                            of time edges will never be changed during the scan
            value       :   Time value of the edge. In case there is no scanned variable it is just the value, otherwise
                            it is a value of the expression evaluated with the minimum value of the scanned variable
            name        :   Descriptive name of the time edge to help user understand the purpose of the edge
            id          :   Unique id in the form of id0, id1, etc. It is used to let the user know what default variable
                            can be used to quickly use the value of this time edge. For example, one can offset the 
                            next time edge with respect to the previous one using "id1 + 5"
            is_scanned  :   Flag indicating if the time edge requires scanning. Even if there is a single scanned variable
                            in the edge expression, the edge becomes scanned as it is supposed to be changing at different
                            scan steps
            for_python  :   The version of the time edge description that is used in the python like experimental sequence
                            generation. It is only used in write_to_python.py and only updated when the run_experiment_button_clicked
            analog      :   List of Analog objects used to describe the state of the analog channel
            digital     :   List of Digital objects used to describe the state of the digital channel
            dds         :   List of DDS objects used to describe the state of the dds channel
            mirny       :   List of DDS objects used to describe the state of the mirny channel
            sampler     :   List of sampler channel parameters. 0 indicates that there is no requested input read. Other than 0 it can be a
                            variable name that will be used for storing the value of the input
            derived_variable_requested      :   Index of the derived variable for non zero values. -1 corresponds to no derived variables requested
                                                
        '''
        def __init__(self, name = "", id = "id0", expression = "0", evaluation = 0, for_python = 0, value = 0, is_scanned = False, derived_variable_requested = -1):
            self.expression = expression
            self.evaluation = evaluation
            self.value = value   
            self.name = name
            self.id = id
            self.is_scanned = is_scanned
            self.for_python = for_python
            self.digital = [self.Digital() for i in range(config.digital_channels_number)]
            self.analog = [self.Analog() for i in range(config.analog_channels_number)]
            self.dds = [self.DDS() for i in range(config.dds_channels_number)]
            self.mirny = [self.DDS() for i in range(config.mirny_channels_number)]
            self.sampler = ['0']*8
            self.derived_variable_requested = derived_variable_requested


        class Digital:
            '''
            An object that is used to describe the state of the digital channel
            Attributes description:
                expression  :   Mathematical expression used to describe the state of digital channel
                evaluation  :   Expression that can be executed in python to evaluate the state of digital channel
                value       :   The value of the digital channel
                for_python  :   The version of the digital channel state description that is used in the python like experimental sequence
                                generation. It is only used in write_to_python.py and only updated when the run_experiment_button_clicked
                changed     :   Flag indicating if the digital channel is required to be changed at this time edge
                is_scanned  :   Flag indicating if the digital channel state requires scanning. Even if there is a single scanned variable
                                in the expression, the channel becomes scanned as it is supposed to be changing at different
                                scan steps
            '''
            def __init__(self, expression = "0", evaluation = 0, value = 0, for_python = 0, changed = True, is_scanned = False):
                self.expression = expression
                self.evaluation = evaluation
                self.value = value
                self.for_python = for_python
                self.changed = changed
                self.is_scanned = is_scanned


        class Analog:
            '''
            An object that is used to describe the state of the analog channel
            Attributes description:
                expression  :   Mathematical expression used to describe the state of analog channel
                evaluation  :   Expression that can be executed in python to evaluate the state of analog channel
                value       :   The value of the analog channel
                for_python  :   The version of the analog channel value description that is used in the python like experimental sequence
                                generation. It is only used in write_to_python.py and only updated when the run_experiment_button_clicked
                changed     :   Flag indicating if the analog channel is required to be changed at this time edge
                is_scanned  :   Flag indicating if the analog channel state requires scanning. Even if there is a single scanned variable
                                in the expression, the channel becomes scanned as it is supposed to be changing at different
                                scan steps
            '''            
            def __init__(self, expression = "0", evaluation = 0, value = 0, for_python = "0", changed = True, is_scanned = False):
                self.expression = expression
                self.evaluation = evaluation
                self.value = value
                self.for_python = for_python
                self.changed = changed
                self.is_scanned = is_scanned
                self.is_sampled = False


        class DDS:
            '''
            An object that is used to describe the state of the dds channel
            Attributes description:
                frequency    :   An object that is used to describe the frequency state of the dds channel
                amplitude    :   An object that is used to describe the amplitude state of the dds channel
                attenuation  :   An object that is used to describe the attenuation state of the dds channel
                phase        :   An object that is used to describe the phase state of the dds channel
                state        :   An object that is used to describe the ON/OFF state of the dds channel
                changed      :   Flag indicating if the dds channel is required to be changed at this time edge                
            '''
            def __init__(self, state = 0, changed = True):
                self.frequency = self.Object()
                self.amplitude = self.Object()
                self.attenuation = self.Object()
                self.phase = self.Object()
                self.state = self.Object()
                self.changed = changed

        
            class Object:
                '''
                An object that is used to describe the state of the dds channel parameters
                Attributes description:
                    expression  :   Mathematical expression used to describe the dds channel parameter
                    evaluation  :   Expression that can be executed in python to evaluate the dds channel parameter
                    value       :   The value of the dds channel parameter
                    for_python  :   The version of the dds parameter description that is used in the python like experimental sequence
                                    generation. It is only used in write_to_python.py and only updated when the run_experiment_button_clicked
                    changed     :   Flag indicating if the dds channel parameter is required to be changed at this time edge. If any of the
                                    dds parameters is required to be changed the state is going to be updated at this time edge
                    is_scanned  :   Flag indicating if the dds channel parameter requires scanning. Even if there is a single scanned variable
                                    in the expression, the channel parameter becomes scanned as it is supposed to be changing at different
                                    scan steps
                '''
                def __init__(self, expression = "0.0", evaluation = 0.0, value = 0.0, changed = True, is_scanned = False):
                    self.expression = expression
                    self.evaluation = evaluation
                    self.for_python = evaluation
                    self.value = value
                    self.changed = changed   
                    self.is_scanned = is_scanned     

        
    class Experiment:
        '''
        An object that is used to describe the entire experimental sequence, title names and state of the GUI
        Attributes description:
            title_digital_tab           :   List of the String type title names used in digital tab
            title_analog_tab            :   List of the String type title names used in analog tab
            title_dds_tab               :   List of the String type title names used in dds tab
            title_sampler_tab           :   List of the String type title names used in sampler tab
            sequence                    :   List of Edge objects describing the experimental sequence at different time stamps
            go_to_edge_num              :   Number of the edge specified to go when pressing go_to_edge button. Initialized at -1
                                            for easy check in case none of the edges has been selected yet
            new_variables               :   List of user defined variables. Used to build the variables tab and retieve the values 
                                            assigned before scanning a variable
            derived_variables           :   List of Derived_variables. Used to be able to use sampled variables in more complex functions 
                                            to allow feedback
            names_of_derived_variables  :   Set of the derived variables names. Useful to check if a variable is a derived variable
            variables                   :   Dictionary of all variables. Used to look up the values of the variables in the execution of
                                            evaluation
            sampler_variables           :   Set of variable names used for being used in a samlper
            do_scan                     :   Flag indicating if the scan is needed to be done
            number_of_steps             :   Number of steps specificed in the Scan table parameters. Default value is 1
            file_name                   :   The name of the experimental sequence. When the program is initialized the name is an empty String.
                                            Once the save_sequence button is clicked the user needs to specify the location and name of the file.
                                            Used to display the name of the sequence to let user know the purpose of the sequence.
            scanned_variables           :   List of scanned variables. Used in the write_to_python.py to generate the proper iterables for the scan
            scanned_varbiales_count     :   Number of scanned variables. Used to ignore the scan tick in case of 0 specified scanned variables.
                                            User can create several scanning variables with None as names
            continuously_running        :   Flag indicating if the continuous run is required
            slow_dds                    :   List of SLOW_DDS objects that describe the state of the slow dds output
        '''  
        def __init__(self):
            self.title_digital_tab = []
            self.title_analog_tab = []
            self.title_dds_tab = []
            self.title_mirny_tab = []
            self.title_sampler_tab = []
            self.title_slow_dds_tab = []
            self.sequence = [] 
            self.go_to_edge_num = -1
            self.new_variables = [] 
            self.variables = {}
            self.sampler_variables = set()
            self.derived_variables = []
            self.names_of_derived_variables = set()
            self.do_scan = False
            self.number_of_steps = 1
            self.file_name = ""
            self.scanned_variables = [] 
            self.scanned_variables_count = 0
            self.continously_running = False 
            self.slow_dds = [self.SLOW_DDS() for i in range(config.slow_dds_channels_number)]


        class SLOW_DDS:
            '''
            An object that is used to describe the state of the slow dds channel
            Attributes description:
                frequency    :   An object that is used to describe the frequency state of the dds channel
                amplitude    :   An object that is used to describe the amplitude state of the dds channel
                attenuation  :   An object that is used to describe the attenuation state of the dds channel
                phase        :   An object that is used to describe the phase state of the dds channel
                state        :   An object that is used to describe the ON/OFF state of the dds channel
            '''
            def __init__(self, frequency = 0.0, amplitude = 0.0, attenuation = 0.0, phase = 0.0, state = 0):
                self.frequency = frequency
                self.amplitude = amplitude
                self.attenuation = attenuation
                self.phase = phase
                self.state = state


    class Derived_variable:
        '''
        An object that is used to describe the derived variable parameters
        Attributes description:
            name        :   Name of the scanned variable
            arguments   :   List of agruments for the function used to derive the variable
            function    :   String of the python description of the function to derive the variable
        ''' 
        def __init__(self, name, arguments, edge_id, function):
            self.name = name
            self.arguments = arguments
            self.edge_id = edge_id
            self.function = function
            
              
    class Scanned_variable:
        '''
        An object that is used to describe the scanned variable parameters
        Attributes description:
            name        :   Name of the scanned variable
            min_val     :   Minimum value assigned to the scanned variable
            max_val     :   Maximum value assigned to the scanned variable
        ''' 
        def __init__(self, name, min_val, max_val):
            self.name = name
            self.min_val = min_val
            self.max_val = max_val


    class Variable: 
        '''
        An object that is used to describe all variables in self.experiment.variables decitionary
        Attributes description:
            name        :   Name of the variable
            value       :   Values of the variable. In case the variable is scanned its minimum values is assigned as its value
            is_scanned  :   Flag indicating if the variable is scanned
            for_python  :   The version of the variable description that is used in the python like experimental sequence
                            generation. It is only used in write_to_python.py and only updated when the run_experiment_button_clicked
        '''         
        def __init__(self, name, value, for_python, is_scanned = False, is_derived = False):
            self.name = name
            self.value = value
            self.for_python = for_python
            self.is_scanned = is_scanned
            self.is_derived = is_derived
            
            
    class CustomThread(threading.Thread):
        '''
        An object that is used to initialize parallel threads
        '''    
        def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
            super().__init__(group, target, name, args, kwargs, daemon=daemon)        
            self._return = None

            
        def run(self):
            try:
                if self._target:
                    self._return = self._target(*self._args, **self._kwargs)
            finally:
                # Avoid a refcycle if the thread is running a function with
                # an argument that has a member that points to the thread.
                del self._target, self._args, self._kwargs                
            

    def __init__(self):
        super().__init__()
        #MAIN PAGE LAYOUT
        self.setWindowTitle("Quantrol. %s Group" %config.research_group_name)
        self.main_window = QTabWidget()
        self.setCentralWidget(self.main_window)
        self.setGeometry(0,30,1920,1200)
        
        #Declaring global variables
        self.experiment = self.Experiment()
        self.sequence_num_rows = 1
        self.setting_dict = {0:"frequency", 1:"amplitude", 2:"attenuation", 3:"phase", 4:"state"}
        self.max_dict_dds = {0: 500, 1: 1, 2: 31.5, 3: 360, 4: 1} 
        self.min_dict_dds = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0} 
        self.max_dict_mirny = {0: 6800, 1: 1, 2: 31.5, 3: 360, 4: 1} #max and min needs to be checked 
        self.min_dict_mirny = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}  #max and min needs to be checked 
        self.to_update = False
        self.green = QColor(37,211,102)
        self.red = QColor(247,120,120)
        self.grey = QColor(100,100,100)
        self.white = QColor(255,255,255)
        self.yellow = QColor(255, 255, 0)
        self.cyan = QColor(0, 255, 255)
        self.experiment.variables['id0'] = self.Variable(name = "id0", value = 0.0, for_python = 0.0)
        self.experiment.variables[''] = self.Variable(name = '', value = 0.0, for_python = 0.0)   #in order to be able to process expressions like -5 we need to have it as first item in decode will be "" that should be 0    
        self.experiment.sequence = [self.Edge("Default")]
        
        self.init_default_values() #Reads the default state file and initializes the values
        tabs.sequence_tab_build(self)
        if config.digital_channels_number > 0:
            tabs.digital_tab_build(self)
        if config.analog_channels_number > 0:
            tabs.analog_tab_build(self)
        if config.dds_channels_number > 0:
            tabs.dds_tab_build(self)
        if config.sampler_channels_number > 0:
            tabs.sampler_tab_build(self)
        if config.mirny_channels_number > 0:
            tabs.mirny_tab_build(self)
        if config.slow_dds_channels_number > 0:
            tabs.slow_dds_tab_build(self)
        tabs.variables_tab_build(self)
        self.making_separator()
       
        #ADDING TABS TO MAIN WINDOW
        self.main_window.addTab(self.sequence_tab_widget, "Sequence")
        self.main_window.addTab(self.digital_tab_widget, "Digital")
        self.main_window.addTab(self.analog_tab_widget, "Analog")
        self.main_window.addTab(self.dds_tab_widget, "DDS")
        self.main_window.addTab(self.mirny_tab_widget, "Mirny")
        self.main_window.addTab(self.sampler_tab_widget, "Sampler")
        self.main_window.addTab(self.variables_tab_widget, "Variables")
        self.main_window.addTab(self.slow_dds_tab_widget, "Slow DDS")
        self.to_update = True
        
    '''
    ||||||  ||    ||  ||    ||  |||||| |||||||| ||||||   |||||   ||    ||  ||||||||  ||  ||  ||
    ||      ||    ||  |||   ||  ||  ||    ||      ||    ||   ||  |||   ||  ||    ||  ||  ||  ||
    ||      ||    ||  || || ||  ||        ||      ||    ||   ||  || || ||    ||      ||  ||  ||
    ||||||  ||    ||  ||  | ||  ||        ||      ||    ||   ||  ||  | ||      ||    ||  ||  ||
    ||      ||    ||  ||   |||  ||  ||    ||      ||    ||   ||  ||   |||  ||    ||
    ||       ||||||   ||    ||  ||||||    ||    ||||||   |||||   ||    ||  ||||||||  ||  ||  ||
    '''
    
    def init_default_values(self):
        '''
        The function downloads the default state and initializes it by assigning the current experimental
        to the default values
        '''
        incompatible = False
        try:
            with open("./default/default", 'rb') as file:
                default_experiment = pickle.load(file)
            if (len(default_experiment.sequence[0].digital) == config.digital_channels_number) and (len(default_experiment.sequence[0].analog) == config.analog_channels_number) and (len(default_experiment.sequence[0].dds) == config.dds_channels_number) and (len(default_experiment.sequence[0].sampler) == config.sampler_channels_number) and (len(default_experiment.sequence[0].mirny) == config.mirny_channels_number) and (len(default_experiment.slow_dds) == config.slow_dds_channels_number):
                pass
            else:
                incompatible = True
                default_experiment.sequence[0].digital[1000000000] #Causing an error
            #reassign the default values to the current self.experiment object
            self.experiment.sequence[0] = deepcopy(default_experiment.sequence[0])
            self.experiment.title_digital_tab = deepcopy(default_experiment.title_digital_tab)
            self.experiment.title_analog_tab = deepcopy(default_experiment.title_analog_tab)
            self.experiment.title_dds_tab = deepcopy(default_experiment.title_dds_tab)
            self.experiment.title_mirny_tab = deepcopy(default_experiment.title_mirny_tab)
            self.experiment.title_sampler_tab = deepcopy(default_experiment.title_sampler_tab)
            self.experiment.title_slow_dds_tab = deepcopy(default_experiment.title_slow_dds_tab)
        except:
            self.experiment.sequence[0] = self.Edge(name="Default")
            if config.digital_channels_number > 0:
                self.experiment.title_digital_tab = ["#", "Name", "Time (ms)", ""] + [f"D{i}" for i in range(config.digital_channels_number)]
            if config.analog_channels_number > 0:
                self.experiment.title_analog_tab = ["#", "Name", "Time (ms)", ""] + [f"A{i}" for i in range(config.analog_channels_number)]
            if config.dds_channels_number > 0:
                self.experiment.title_dds_tab = ["#", "Name", "Time (ms)", ""] + [f"DDS{i}" for i in range(config.dds_channels_number)]            
            if config.mirny_channels_number > 0:
                self.experiment.title_mirny_tab = ["#", "Name", "Time (ms)", ""] + [f"M{i}" for i in range(config.mirny_channels_number)]            
            if config.sampler_channels_number > 0:
                self.experiment.title_sampler_tab = ["#", "Name", "Time (ms)", ""] + [f"S{i}" for i in range(config.sampler_channels_number)]            
            if config.dds_channels_number > 0:
                self.experiment.title_slow_dds_tab = ["#", "Name", "Time (ms)", ""] + [f"slow DDS{i}" for i in range(config.dds_channels_number)]            
            if incompatible:
                self.error_message('Default file is incompatible. Initializing the DEFAULT default values and updating the default file.', 'Error')
            else:
                self.error_message('Default file is not found. Initializing the DEFAULT default values and updating the default file.', 'Error')
            os.makedirs("./default", exist_ok=True)
            with open("./default/default", 'wb') as file:
                pickle.dump(self.experiment, file)

    

    def message_to_logger(self, message):
        '''
        The function is taking a message in terms of the String and displays it into the logger with the current time stamp
        where the time is the system time now
        '''
        self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + message)
        

    def making_separator(self):
        '''
        The function does include a separator in the table that is coloured in dark grey for better visual separation across all tabs
        Fucntion is called each time the new edge is being incerted
        '''
        #making the separation rows a single column
        if self.sequence_num_rows > 1: # to avoid having a warning that single cell span won't be added
            self.digital_table.setSpan(0,3, self.sequence_num_rows, 1)
            self.analog_table.setSpan(0,3, self.sequence_num_rows, 1)
            self.sampler_table.setSpan(0,3, self.sequence_num_rows, 1)
        else:
            pass
        # grey coloured separating line digital tab
        self.digital_table.setItem(0,3, QTableWidgetItem())
        self.digital_table.item(0,3).setBackground(self.grey)
        # grey coloured separating line analog tab
        self.analog_table.setItem(0,3, QTableWidgetItem())
        self.analog_table.item(0,3).setBackground(self.grey)
        # grey coloured separating line dds tab
        self.dds_dummy.setSpan(0,3, self.sequence_num_rows + 2, 1)  
        self.dds_dummy.setItem(0,3, QTableWidgetItem())
        self.dds_dummy.item(0,3).setBackground(self.grey)
        # grey coloured separating line in dds tab between channels
        for i in range(config.dds_channels_number):
            self.dds_table.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
            self.dds_table.setItem(0,6*i + 3, QTableWidgetItem())
            self.dds_table.item(0, 6*i + 3).setBackground(self.grey)
        # grey coloured separating line mirny tab
        self.mirny_dummy.setSpan(0,3, self.sequence_num_rows + 2, 1)  
        self.mirny_dummy.setItem(0,3, QTableWidgetItem())
        self.mirny_dummy.item(0,3).setBackground(self.grey)
        # grey coloured separating line in mirny tab between channels
        for i in range(config.mirny_channels_number):
            self.mirny_table.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
            self.mirny_table.setItem(0,6*i + 3, QTableWidgetItem())
            self.mirny_table.item(0, 6*i + 3).setBackground(self.grey)
        # grey coloured separating line sampler tab
        self.sampler_table.setItem(0,3, QTableWidgetItem())
        self.sampler_table.item(0,3).setBackground(self.grey)
     


    def update_on(self):
        '''
        Function that sets the self.to_update to true. It was created to make the code more readable
        '''
        self.to_update = True


    def update_off(self):
        '''
        Function that sets the self.to_update to false. It was created to make the code more readable
        '''
        self.to_update = False


    def error_message(self, text, title):
        '''
        Function that takes text and title and creates an error pop up message with the provided title and text
        '''
        msg = QMessageBox()
        msg.setFont(QFont('Arial', 14))
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle(title)
        msg.exec_()
 

    def decode_input(self, text):
        '''
        Function is used to decode the user input in a form of a simple mathematical expression. It interprets chunks of text 
        until the next mathematical operator or the end of the text.
        '''
        index = 0
        output_eval = ""
        output_for_python = ""
        current = ""
        is_scanned = False
        is_sampled = False
        is_derived = False
        text = text.replace(" ", "") # removing spaces
        text += "+" #Adding a plus in the end of the text in order to avoid typing additional operation for the last element
        while index < len(text):
            #Adding the next character
            current += text[index]
            index += 1
            if text[index] == "-" or text[index] == "+" or text[index] == "/" or text[index] == "*":
                current.replace(" ", "")
                try: #If the current convertible to float type of value
                    float_current = float(current)
                    output_eval += str(float_current) + text[index]
                    output_for_python += str(float_current) + text[index]
                except: #If the current is a variable name
                    output_eval += "self.experiment.variables['" + current + "'].value" + text[index]
                    variable = self.experiment.variables[current]
                    if self.experiment.do_scan and variable.is_scanned:#if scanned assign the python form else assign the value
                        is_scanned = True
                        output_for_python += str(self.experiment.variables[current].for_python) + text[index]
                    elif current in self.experiment.sampler_variables: #if sampled assign the name itself
                        output_for_python += "%s" %current + text[index]
                        is_sampled = True
                    elif variable.is_derived: #if derived assign the name itself
                        output_for_python += "%s" %current + text[index]
                        is_derived = True
                    else:
                        output_for_python += str(variable.value) + text[index]
                current = ""
                index += 1
        # Removing all additional characters in the end. Making a+2+ into a+2
        output_eval = output_eval[:-1]
        output_for_python = output_for_python[:-1]
        # If for_python can be evaluated, then just store the value. Otherwise we keep the original form
        try:
            exec("self.temp =" + output_for_python)
            output_for_python = str(float(self.temp))
        except:
            pass
        # If evaluation can be evaluated, then store the value. Otherwise we keep the original form
        try:
            output_eval = str(float(output_eval))
        except:
            pass
        return (output_eval, output_for_python, is_scanned, is_sampled, is_derived) #Since we added an additional sign we need to remove it


    def remove_restricted_characters(self, text):
        '''
        Function is used to remove the restricted characters from the variable names.
        It takes the initial name as a String input and returns the Sring of the modified text
        '''
        to_remove = "~!@#$%^&*()-=/*+.?[]{;}:\|<>` "
        for character in to_remove:
            text = text.replace(character, "")
        return text
    
    
    #SEQUENCE TAB RELATED FUNCTIONS
    def sequence_table_changed(self, item):
        '''
        This function is triggered when the sequence table entry is changed. There are two possible locations of the change.
        column 1 corresponds to the change of the name of the edge
                This will just reassign the edge.name parameter to the new value.
        column 3 corresponds to the change of the time expression. There are two distinct cases for user entry
                1) when the entry is empty, then it will assign the previous edge values and update the table entries accordingly
                2) when the entru is not empty it will try to evaluate it and in case of positive result assign it to the edge
                   and update the table. Otherwise it will throw an error
        Function takes no inputs, item is an internal variable that has information of the row and column of the entry that has been changed
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            edge = self.experiment.sequence[row]
            table_item = self.sequence_table.item(row,col)
            if col == 1: # edge name changed
                edge.name = table_item.text()
                update.from_object(self)
            elif col == 3: # edge time expression changed
                if table_item.text() == "":
                    #previous edge values
                    edge.expression = self.experiment.sequence[row-1].expression#previous edge
                    edge.evaluation = self.experiment.sequence[row-1].evaluation#previous edge
                    edge.value = self.experiment.sequence[row-1].value#previous edge
                    edge.for_python = self.experiment.sequence[row-1].for_python#previous edge
                    #updating table entry
                    self.update_off()
                    table_item.setText(edge.expression)
                    self.update_on()
                else:                        
                    try:
                        expression = table_item.text()
                        (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                        exec("self.value = " + str(evaluation)) # this is done here to be able to assign value of the id# type variable
                        if self.value < 0: #restricting negative values for time
                            self.error_message("Negative values are not allowed", "Negative time value")
                            self.update_off()
                            table_item.setText(str(edge.expression))
                            self.update_on()
                        else:
                            edge.value = self.value
                            edge.evaluation = evaluation
                            edge.expression = expression
                            edge.for_python = for_python
                            edge.is_scanned = is_scanned
                            self.experiment.variables[edge.id] = self.Variable(name = edge.id, value = edge.value, for_python = edge.for_python, is_scanned = edge.is_scanned)
                            update.sequence_tab(self)
                            update.from_object(self)
                    except:
                        self.error_message("Expression can not be evaluated", "Wrong entry")
                        self.update_off()
                        table_item.setText(str(edge.expression))
                        self.update_on()                        

 
    def save_sequence_button_clicked(self):
        '''
        Function is used when the user wants to save the sequence. In there is no file corresponsing to the sequence displayed the 
        user needs to specify its location and name. Otherwise it will orverwrite the sequence that was opened
        '''
        if self.experiment.file_name == "":
            self.experiment.file_name = QFileDialog.getSaveFileName(self, 'Save File')[0]
            if self.experiment.file_name != "": #happens when no file name was given (canceled)
                try:
                    with open(self.experiment.file_name, 'wb') as file:
                        pickle.dump(self.experiment, file)
                    self.create_file_name_label()
                    self.message_to_logger("Sequence saved at %s" %self.experiment.file_name)
                except:
                    self.message_to_logger("Saving attempt was not successful")                
        else:
            with open(self.experiment.file_name, 'wb') as file:
                pickle.dump(self.experiment, file)
            self.message_to_logger("Sequence saved at %s" %self.experiment.file_name)


    def load_sequence_button_clicked(self):
        '''
        Function is used when the user wants to load the sequence. It triggers the folder explorer and lets the user choose 
        the file to open.
        '''
        loaded_file_name = QFileDialog.getOpenFileName(self, "Open File")[0]
        if loaded_file_name != "": #happens when no file name was given (canceled)
            try:
                with open(loaded_file_name, 'rb') as file:
                    self.experiment = pickle.load(file)
                #this was only created to avoid crushing when the old versions of experiments are loaded without the skip_images attribute
                if hasattr(self.experiment, 'skip_images'):
                    pass
                else:
                    self.experiment.skip_images = False
                    self.skip_images_button.setStyleSheet("background-color : red; color : white")

                self.sequence_num_rows = len(self.experiment.sequence)
                self.update_off()
                #update the state of the checkbox for doing the scan
                self.scan_table.setChecked(self.experiment.do_scan)
                #update the label showing the sequence that is being modified 
                self.experiment.file_name = loaded_file_name
                self.create_file_name_label()
                update.from_object(self)
                self.message_to_logger("Sequence loaded from %s" %self.experiment.file_name)
            except:
                self.error_message('Could not load the file.', 'Error')
            self.update_on()


    def create_file_name_label(self):
        '''
        Function was created to make the code more readable 
        '''
        self.file_name_lable.setText(self.experiment.file_name)


    def find_unique_id(self):
        '''
        Function iterates over the id numbers from id0, id1, etc. until it finds the smallest available id number and returns it
        '''
        for id in range(10**4):
            unique_id = "id" + str(id)
            if unique_id not in self.experiment.variables:
                return unique_id
        

    def insert_edge_button_clicked(self):   
        '''
        Function is used to insert a new edge. Its values are assigned to be the same as the values of the previous edge but empty name.
        Updating of the table here is done inplace. One could create a function in update.py that would do it but for now it is here.
        '''
        #appending a new edge with a unique id
        new_unique_id = self.find_unique_id()
        new_edge = deepcopy(self.experiment.sequence[-1]) #copying the last edge
        new_edge.derived_variable_requested = -1
        new_edge.id = new_unique_id
        new_edge.name = ""
        self.experiment.sequence.append(new_edge)
        self.sequence_num_rows += 1
        #creating a corresponding variable so one can use id# as a variable
        self.experiment.variables[new_edge.id] = self.Variable(name = new_edge.id, value = new_edge.value, for_python = new_edge.for_python)
        self.update_off()
        #adding a new row in all tabs
        self.sequence_table.setRowCount(self.sequence_num_rows)                     
        self.digital_table.setRowCount(self.sequence_num_rows)
        self.digital_dummy.setRowCount(self.sequence_num_rows)
        self.analog_table.setRowCount(self.sequence_num_rows)
        self.analog_dummy.setRowCount(self.sequence_num_rows)
        self.dds_table.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
        self.dds_dummy.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name    
        self.mirny_table.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
        self.mirny_dummy.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name    
        self.sampler_table.setRowCount(self.sequence_num_rows)     
        self.making_separator()
        row = self.sequence_num_rows - 1
        edge = self.experiment.sequence[row]
        #Setting the left part of the SEQUENCE table (edge number, name, expression, time)
        self.sequence_table.setItem(row, 0, QTableWidgetItem(str(row)))
        self.sequence_table.setItem(row, 1, QTableWidgetItem(edge.name))
        self.sequence_table.setItem(row, 2, QTableWidgetItem(edge.id))
        self.sequence_table.setItem(row, 3, QTableWidgetItem(edge.expression))
        self.sequence_table.setItem(row, 4, QTableWidgetItem(str(edge.value)))
        
        #Setting the left part of the DIGITAL table (edge number, name, time)
        self.digital_dummy.setItem(row, 0, QTableWidgetItem(str(row)))
        self.digital_dummy.setItem(row, 1, QTableWidgetItem(edge.name))
        self.digital_dummy.setItem(row, 2, QTableWidgetItem(str(edge.value)))
        #Setting DIGITAL table values
        for index, channel in enumerate(self.experiment.sequence[-1].digital):
            col = index + 4 #plus 4 is because first 4 columns are used by number, name, time of the edge and separator
            self.digital_table.setItem(row, col, QTableWidgetItem(channel.expression + " "))
            channel.changed = False

        #Setting the left part of the ANALOG table (edge number, name, time)
        self.analog_dummy.setItem(row, 0, QTableWidgetItem(str(row)))
        self.analog_dummy.setItem(row, 1, QTableWidgetItem(edge.name))
        self.analog_dummy.setItem(row, 2, QTableWidgetItem(str(edge.value)))
        #Setting ANALOG table values
        for index, channel in enumerate(self.experiment.sequence[-1].analog):
            # plus 3 is because first 3 columns are used by number, name and time of edge
            col = index + 4
            self.analog_table.setItem(row, col, QTableWidgetItem(channel.expression + " "))
            self.analog_table.item(row, col).setToolTip(str(channel.value))
            channel.changed = False

        #Setting the left part of the DDS table (edge number, name, time)
        self.dds_dummy.setItem(row+2, 0, QTableWidgetItem(str(row)))
        self.dds_dummy.setItem(row+2, 1, QTableWidgetItem(edge.name))
        self.dds_dummy.setItem(row+2, 2, QTableWidgetItem(str(edge.value)))
        #Setting DDS table values
        for index, channel in enumerate(self.experiment.sequence[-1].dds):
            #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
            for setting in range(5):
                col = 4 + index * 6 + setting
                dds_row = row + 2
                exec("self.dds_table.setItem(dds_row, col, QTableWidgetItem(str(channel.%s.expression) + ' '))" %self.setting_dict[setting])
                exec("self.dds_table.item(dds_row, col).setToolTip(str(channel.%s.value))" %self.setting_dict[setting])
            channel.changed = False
        #Setting the left part of the MIRNY table (edge number, name, time)
        self.mirny_dummy.setItem(row+2, 0, QTableWidgetItem(str(row)))
        self.mirny_dummy.setItem(row+2, 1, QTableWidgetItem(edge.name))
        self.mirny_dummy.setItem(row+2, 2, QTableWidgetItem(str(edge.value)))
        #Setting MIRNY table values
        for index, channel in enumerate(self.experiment.sequence[-1].mirny):
            #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
            for setting in range(5):
                col = 4 + index * 6 + setting
                dds_row = row + 2
                exec("self.mirny_table.setItem(dds_row, col, QTableWidgetItem(str(channel.%s.expression) + ' '))" %self.setting_dict[setting])
                exec("self.mirny_table.item(dds_row, col).setToolTip(str(channel.%s.value))" %self.setting_dict[setting])
            channel.changed = False
        #Setting the left part of the SAMPLER table (edge number, name, time)
        self.sampler_table.setItem(row, 0, QTableWidgetItem(str(row)))
        self.sampler_table.setItem(row, 1, QTableWidgetItem(edge.name))
        self.sampler_table.setItem(row, 2, QTableWidgetItem(str(edge.value)))
        #Setting SAMPLER table values
        for index, channel in enumerate(self.experiment.sequence[-1].sampler):
            col = index + 4 #plus 4 is because first 4 columns are used by number, name, time of the edge and separator
            self.sampler_table.setItem(row, col, QTableWidgetItem("0"))

        self.update_on()


    def delete_edge_button_clicked(self):
        '''
        Function is used when the user wants to delete selected edge. The user is not allowed to delete the default edge.
        The function is creating a backup version of the variable with corresponding id number and tries to update all tabs without that 
        variable. That way it is checking if the edge value has been used anywhere? In case of no problems it does execute the deletion
        and updates the table in each tab. Otherwise, the fucntion will reassign the variable and let the user know that the time edge is 
        being used at particular place.
        '''
        try:
            row = self.sequence_table.selectedIndexes()[0].row()
            name = self.experiment.sequence[row].id
            if row == 0: # corresponds to the default edge
                self.error_message("You can not delete the starting edge", "Protected item")
            else:
                backup = deepcopy(self.experiment.variables[name]) #backup is a variable copy in case we would need to restore changes and not allow deleting edge
                #the following is a check whether the edge has been used somewhere. First we delete a corresponding variable and then try to evaluate all the entries
                del self.experiment.variables[name]
                return_value = update.digital_analog_dds_mirny_tabs(self)
                if return_value == None: #no errors, means that the edge can be deleted
                    del self.experiment.sequence[row]
                    self.sequence_table.setCurrentCell(row-1, 0)
                    update.from_object(self) #updating all tables
                else:
                    self.experiment.variables[name] = backup
                    self.error_message('The edge time value is used as a variable in %s.'%return_value, 'Can not delete used edge')
        except:
            self.error_message("Select the edge you want to delete", "No edge selected")


    def set_color_of_the_edge(self, set_color, edge_num):
        '''
        Function is used to highlight or unhighlight the edge. For example, when the user wants the system to go_to_edge
        it will color it after successful execution. Or, when the user runs the sequence the highlighted edge should be unhighlighted
        '''
        self.to_update = False # this is done in order to avoid sequence table changed event
        self.sequence_table.item(edge_num,0).setBackground(set_color)
        self.sequence_table.item(edge_num,1).setBackground(set_color)
        self.sequence_table.item(edge_num,2).setBackground(set_color)
        self.sequence_table.item(edge_num,3).setBackground(set_color)
        self.sequence_table.item(edge_num,4).setBackground(set_color)
        self.digital_dummy.item(edge_num,0).setBackground(set_color)
        self.digital_dummy.item(edge_num,1).setBackground(set_color)
        self.digital_dummy.item(edge_num,2).setBackground(set_color)
        self.analog_dummy.item(edge_num,0).setBackground(set_color)
        self.analog_dummy.item(edge_num,1).setBackground(set_color)
        self.analog_dummy.item(edge_num,2).setBackground(set_color)
        self.dds_dummy.item(edge_num+2,0).setBackground(set_color)
        self.dds_dummy.item(edge_num+2,1).setBackground(set_color)
        self.dds_dummy.item(edge_num+2,2).setBackground(set_color)
        self.to_update = True        

    
    def go_to_edge_button_clicked(self):
        '''
        Function is used to set the hardware into a specific time edge state. User needs to click the edge before pressing the button.
        After a successful execution the edge will be highlighted in green. The function recognizes the tab that is being currently displayed
        and assigns the hardware to the state of the last selected edge in that particular tab.
        '''
        try:                
            if self.main_window.currentIndex() == 0:
                edge_num = self.sequence_table.selectedIndexes()[0].row()
            elif self.main_window.currentIndex() == 1:
                edge_num = self.digital_dummy.selectedIndexes()[0].row()    
            elif self.main_window.currentIndex() == 2:
                edge_num = self.analog_dummy.selectedIndexes()[0].row()    
            elif self.main_window.currentIndex() == 3:
                edge_num = self.dds_dummy.selectedIndexes()[0].row() - 2 # because top 2 rows are used for title   
            elif self.main_window.currentIndex() == 4:
                edge_num = self.mirny_dummy.selectedIndexes()[0].row() - 2 # because top 2 rows are used for title   
            write_to_python.create_go_to_edge(self, edge_num=edge_num)
            self.message_to_logger("Go to edge file generated")
            try:
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run go_to_edge.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["go_to_edge.bat"])
                submit_experiment_thread.start()
                self.message_to_logger("Went to edge")
                #unhighlighting the previously highlighted edge if it was previously highlighted
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                #highlighting newly selected edge to go
                self.set_color_of_the_edge(self.green, edge_num)
                self.experiment.go_to_edge_num = edge_num
            except:
                self.message_to_logger("Couldn't go to edge")    
        except:
            self.error_message("Chose the edge you want the system to go","No edge selected")


    def count_scanned_variables(self):
        '''
        Function iterates over all scanned variables that are not "None" and assigns the total count to 
        self.experiment.scanned_variables_count. The function does not return anything
        '''
        count = 0
        for variable in self.experiment.scanned_variables:
            if variable.name != "None":
                count += 1
        self.experiment.scanned_variables_count = count


    def run_experiment_button_clicked(self): 
        '''
        Function is used when the user wants to run the experiment. By calling update.digital_analog_dds_mirny_tabs(self) it updates every expression
        to make sure that all scanning variables are taken into account. After that it generates the run_experiment.py file and 
        submits the experimental description to the scheduler through artiq_run function.
        '''
        self.count_scanned_variables()
        update.digital_analog_dds_mirny_tabs(self) #updating all expressions in particular for_pythons of each parameter
        try:
            write_to_python.create_experiment(self)
            self.message_to_logger("Python file generated")
            try:
                #initialize environment and submit the experiment to the scheduler
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run run_experiment.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["run_experiment.bat"])
                submit_experiment_thread.start()
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                    self.experiment.go_to_edge_num = -1
                #needs to be done ---> logging the start of the experiment only if it was started without errors. Checking experiment stages
                self.message_to_logger("Experiment started")
            except:
                self.message_to_logger("Was not able to start experiment")
        except:
            self.message_to_logger("Was not able to generate python file")


    def init_hardware_button_clicked(self):
        '''
        Function is used to initialize the hardware at the default values. It generates the init_hardware.py file according to the
        default edge state and then sets the hardware in that state by running something similar to go_to_edge.py
        '''
        try:
            write_to_python.create_go_to_edge(self, edge_num=0, to_default=True)
            self.message_to_logger("Init_hardware.py file generated")
            try:
                #initialize environment and submit the experiment to the scheduler
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run init_hardware.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["init_hardware.bat"])
                submit_experiment_thread.start()
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                #Highlighting the default edge and setting the go_to_edge_num to the default edge value (0)
                self.experiment.go_to_edge_num = 0
                self.set_color_of_the_edge(self.green, 0)
                self.message_to_logger("Hardware initialized at the default edge.")
            except:
                self.message_to_logger("Was not able to initialize the hardware.")        
        except:
            self.message_to_logger("Was not able to generate init_hardware.py file")


    def generate_run_experiment_py_button_clicked(self):
        '''
        Function is used to generate the run_experiment.py according to the experimental descirption without
        running it. It is usefull for debugging purposes.
        '''
        update.digital_analog_dds_mirny_tabs(self) #specifically used to update for_python version of each parameter in the sequence
        try:
            write_to_python.create_experiment(self)
            self.message_to_logger("Python file generated")
        except:
            self.message_to_logger("Was not able to generate python file")


    def submit_run_experiment_py_button_clicked(self):
        '''
        Function is used to submit already existing run_experiment.py without updating it with the current state
        of the experimental description. Useful in case one needs to hard code some changes into the previously
        generated run_experiment.py file. For instance, making a 2D scan:
        
        self.a = np.linspace(a_min, a_max, number_of_steps_a)
        self.b = np.linspace(b_min, b_max, number_of_steps_b)
        
        for index_a in range(number_of_steps_a):
            for index_b in range(number_of_steps_b):
                self.ttl0(self.a[index_a])
                self.ttl1(self.b[index_b])
        '''
        file_name = "run_experiment.py"
        if os.path.exists(file_name):
            try:
                #initialize environment and submit the experiment to the scheduler
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run run_experiment.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["run_experiment.bat"])
                submit_experiment_thread.start()
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                    self.experiment.go_to_edge_num = -1
                #needs to be done ---> logging the start of the experiment only if it was started without errors. Checking experiment stages
                self.message_to_logger("Experiment started")
            except:
                self.message_to_logger("Was not able to start experiment")        
        else:
            self.message_to_logger("The file run_experiment.py is not found")
        
    def dummy_button_clicked(self):
        
        print("DERIVED VARIABLES")
        for variable in self.experiment.derived_variables:
            print(variable.name, variable.arguments, variable.function)
            
        ''' 
        Function is used to debug the program. Can be used to check the variables at different time stamps.
        Commented out examlpes might be usefull starting point. Usually debugging is done by printing values
        in the console of the VS Code and observing how parameters are being changed.
        '''
        # print("SAMPLER")
        # for edge in self.experiment.sequence:
        #     print(edge.name, edge.sampler)    

        # print(self.experiment.sampler_variables)

        # print("analog channel values")
        # for edge in self.experiment.sequence:
        #     for ind, channel in enumerate(edge.analog):
        #         print("Channel", ind, "val", channel.value, "evaluation", channel.evaluation, "for_python", channel.for_python)

        # print("NEW variables")
        # for item in self.experiment.new_variables:
        #     print("name: ", item.name, "value: ", item.value, "for python: ", item.for_python)
        
        print("VARIABLES")
        for key, item in self.experiment.variables.items():
            print("name: ", item.name, "value: ", item.value, "for python: ", item.for_python)

        # print("EDGES")
        # for ind, edge in enumerate(self.experiment.sequence):
        #     print("edge", ind)
        #     print("    chanel", ind,"evaluation", edge.evaluation, "for_python", edge.for_python, "scanned", edge.is_scanned)
        # print("END")

        # print("analog channel values")
        # for edge in self.experiment.sequence:
        #     for ind, channel in enumerate(edge.analog):
        #         print("Channel", ind, "val", channel.value, "evaluation", channel.evaluation)

        # print("scanned_variables")
        # for item in self.experiment.scanned_variables:
        #     print(item.name, item.min_val, item.max_val)
        
        # print("new variables")
        # for item in self.experiment.new_variables:
        #     print(item.name, item.value, item.is_scanned)


    def save_sequence_as_button_clicked(self):
        '''
        Function is used when the user wants to save the sequence as a separate file. It will not reassign the current file name
        but just create an additional copy of the current state of the self.experiment
        '''
        self.experiment.file_name = QFileDialog.getSaveFileName(self, 'Save File')[0] # always ask for filename
        if self.experiment.file_name != "": #self.experiment.file_name = ""happens when no file name was given (canceled)
            try:
                with open(self.experiment.file_name, 'wb') as file:
                    pickle.dump(self.experiment, file)
                self.create_file_name_label()
                self.message_to_logger("Sequence saved at %s" %self.experiment.file_name)
            except:
                self.message_to_logger("Saving attempt was not successful")
        else:
            self.message_to_logger("No file name was given. Saving unsuccessful")


    def continuous_run_button_clicked(self):
        '''
        Function is used when the user wants to run the specified experimental sequence continuously.
        It passes the run_continuous flag into the write_to_python.create_experiment and the rest is handled there
        '''
        self.count_scanned_variables()
        update.digital_analog_dds_mirny_tabs(self) #updating all expressions in particular for_pythons of each parameter
        try:
            write_to_python.create_experiment(self, run_continuous=True)
            self.message_to_logger("Python file generated")
            try:
                #initialize environment and submit the experiment to run continuously unless it is stopped
                if config.package_manager == "conda":
                    submit_run_continuously_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run run_experiment.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_run_continuously_thread = threading.Thread(target=os.system, args=["run_experiment.bat"])
                submit_run_continuously_thread.start()
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                    self.experiment.go_to_egde_num = 0
                
                #needs to be done ---> logging the start of the experiment only if it was started without errors. Checking experiment stages
                self.message_to_logger("Experiment started")
            except:
                self.message_to_logger("Was not able to start experiment")
        except:
            self.message_to_logger("Was not able to generate python file")
        
        
    def stop_continuous_run_button_clicked(self):
        '''
        Function is used when the user wants to stop continuous run. It will stop anything and run the init_hardware.py file
        '''
        self.dialog = QDialog()
        self.dialog.setGeometry(710, 435, 400, 120)
        self.dialog.setFont(QFont('Arial', 14))
        value_input = QLabel("Are you sure that you want to stop continuous run?")
        dialog_layout = QVBoxLayout()
        button_yes = QPushButton("Yes")
        button_no = QPushButton("No")
        dialog_layout.addWidget(value_input)
        dialog_buttons_layout = QHBoxLayout()
        dialog_buttons_layout.addWidget(button_yes)
        dialog_buttons_layout.addWidget(button_no)
        dialog_layout.addLayout(dialog_buttons_layout)
        self.dialog.setLayout(dialog_layout)
        button_yes.clicked.connect(lambda:self.stop_continuous_run())
        button_no.clicked.connect(lambda:self.dialog.reject())
        self.dialog.setWindowTitle("Warning!") 
        self.dialog.exec_()
 
    def stop_continuous_run(self):
        '''
        This function is used to trigger the event of button_yes for stop_continuous_run_button_clicked. When using it to accept the dialog and then
        having a flag of self.dialog.accepted in case the window was closed by clicking the close button at the 
        right top corner, the dialog was accepted by default.
        '''
        try:
            write_to_python.create_go_to_edge(self, edge_num=0, to_default=True)
            self.message_to_logger("Init_hardware.py file generated")
            try:
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && artiq_run init_hardware.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["init_hardware.bat"])
                submit_experiment_thread.start()
                self.message_to_logger("Experiment was stopped. Hardware is set to the default values")
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                #Highlighting the default edge and setting the go_to_edge_num to the default edge value (0)
                self.experiment.go_to_edge_num = 0
                self.set_color_of_the_edge(self.green, 0)
            except:
                self.message_to_logger("Could not stop the experiment.")
        except:
            self.message_to_logger("Could not generate init_hardware.py file")    
        self.dialog.accept()    


    def save_default_button_clicked(self):
        '''
        Function is used when the user wants to save the current state of the default edge. It first asks if the user is sure that
        it is needed to overwrite the default settings.
        '''
        #The pop-up window to preven use from accidentally overwriting the default settings
        self.dialog = QDialog()
        self.dialog.setGeometry(710, 435, 400, 120)
        self.dialog.setFont(QFont('Arial', 14))
        value_input = QLabel("Are you sure that you want to overwrite the default settings? Previous default settings will be lost!")
        dialog_layout = QVBoxLayout()
        button_update = QPushButton("Yes")
        button_cancel = QPushButton("No")
        dialog_layout.addWidget(value_input)
        dialog_buttons_layout = QHBoxLayout()
        dialog_buttons_layout.addWidget(button_update)
        dialog_buttons_layout.addWidget(button_cancel)
        dialog_layout.addLayout(dialog_buttons_layout)
        self.dialog.setLayout(dialog_layout)
        button_update.clicked.connect(lambda:self.saving_default())
        button_cancel.clicked.connect(lambda:self.dialog.reject())
        self.dialog.setWindowTitle("Warning!") 
        self.dialog.exec_()

 
    def saving_default(self):
        '''
        This function is used to trigger the event of button_yes for save_default_button_clicked. When using it to accept the dialog and then
        having a flag of self.dialog.accepted in case the window was closed by clicking the close button at the 
        right top corner, the dialog was accepted by default.
        '''
        
        try:
            with open("./default/default", 'wb') as file:
                pickle.dump(self.experiment, file)
            self.message_to_logger("Default saved at %s" %self.experiment.file_name)
        except:
            self.message_to_logger("Saving attempt was not successful")
        self.dialog.accept()
    
    def load_default_button_clicked(self):
        '''
        Function is used when the user wants to load the default settings. This can be used when loading the old versions of experiemnts
        to overwrite the titles and default states to the updated default values.
        '''
        self.update_off()
        try:
            with open("./default/default", 'rb') as file:
                default_experiment = pickle.load(file)
            #Reassign the default values to the current self.experiment object
            self.experiment.sequence[0] = deepcopy(default_experiment.sequence[0])
            self.experiment.title_digital_tab = deepcopy(default_experiment.title_digital_tab)
            self.experiment.title_analog_tab = deepcopy(default_experiment.title_analog_tab)
            self.experiment.title_dds_tab = deepcopy(default_experiment.title_dds_tab)
            update.from_object(self)
            self.message_to_logger("Default values loaded from %s" %self.experiment.file_name)
        except:
            self.error_message('Could not load the file.', 'Error')
        self.update_on()


    def clear_logger_button_clicked(self):
        '''
        The function is used to clear the logger
        '''
        self.logger.clear()


    def scan_table_checked(self):
        '''
        Function is used when the user checks/unchecks the scan table checkbox
        '''
        if self.to_update:
            self.experiment.do_scan = self.scan_table.isChecked()
            if self.experiment.do_scan == False:
                #User unchecked the scan. Reassign the variables to the pre scanning values using self.experiment.new_variables
                for item in self.experiment.new_variables:
                    self.experiment.variables[item.name].value = item.value
                    #there is no need for manually making the variables is_scanned attribute False since it is done in decode_input as self.experiment.do_scan is false
            else: #User checked the scan. Assign the scanned variables values to the minimum value. This is required in case they are used in edge time expression to allow sorting
                for variable in self.experiment.scanned_variables:
                    if variable.name != "None":
                        self.experiment.variables[variable.name].value = variable.min_val
            update.digital_analog_dds_mirny_tabs(self)
            update.variables_tab(self, derived_variables = False)
        

    def add_scanned_variable_button_pressed(self):
        '''
        Function is used when the user wants to add a scanned variable. It adds a variable with the name "None" and updates the 
        scan_table to display the changes
        '''
        self.experiment.scanned_variables.append(self.Scanned_variable("None", 0.0, 0.0))
        update.scan_table(self)


    def delete_scanned_variable_button_pressed(self):
        '''
        Function is used when the user wants to delete scanned variable.        
        '''
        try:
            row = self.scan_table_parameters.selectedIndexes()[0].row()
            variable = self.experiment.scanned_variables[row]
            index = self.index_of_a_new_variable(variable.name)
            if index != None: #this is done to avoid trying to access "None" variable
                #reverting the value and scanning state of the variable that is not scanned anymore
                self.experiment.variables[variable.name].is_scanned = False
                self.experiment.variables[variable.name].value = self.experiment.new_variables[index].value #Assign the value of variable to the previous value before being scanned
                self.experiment.new_variables[index].is_scanned = False
                self.experiment.variables[variable.name].for_python = self.experiment.variables[variable.name].value
            del self.experiment.scanned_variables[row]
            #First update the variables tab in order to update the values for evaluation in following update steps
            update.variables_tab(self, derived_variables = False)
            update.scan_table(self)
            update.digital_analog_dds_mirny_tabs(self)
            if row != 0:
                self.scan_table_parameters.setCurrentCell(row-1, 0)
        except:
            self.error_message("Select the variable that needs to be deleted", "No variable selected")


    def index_of_a_new_variable(self, name):
        '''
        Function is used to find the index of the user defined variable by the name. It takes the variable name and
        iterates over all user defined variables to find the match and return the index of that variable in case it
        is present and None otherwise.
        '''
        index = None
        for ind, variable in enumerate(self.experiment.new_variables):
            if variable.name == name:
                index = ind
                break
        return index


    def number_of_steps_input_changed(self):
        '''
        Function is used when the user changes the number of steps in the scan_table.
        Input field allows simple mathematical expressions but in the end only preserves the integer values.
        There is an error message that prevents user from entering an expression resulting in 0 or negative values.
        '''
        if self.to_update: 
            try:
                expression = self.number_of_steps_input.text()
                (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                exec("self.value = " + str(evaluation))
                if self.value > 0: #check whether it is a positive integer
                    self.experiment.number_of_steps = int(self.value)
                else:
                    self.error_message("Only positive integers larger than 0 are allowed", "Wrong entry")    
            except:
                self.error_message("Expression can not be evaluated", "Wrong entry")
            self.update_off()
            self.number_of_steps_input.setText(str(self.experiment.number_of_steps))
            self.update_on()


    def check_if_already_scanned(self, name):
        '''
        Function takes a variable name as an input and checks if it already exists in a scanned variables list.
        This is used to avoid providing two same scanned variable. Returns True in case of duplicates and False otherwise
        '''
        for variable in self.experiment.scanned_variables:
            if variable.name == name:
                return True
        return False


    def scan_table_changed(self, item):
        '''
        Function is used when the user changes parameter of a scan table.
        Function takes no inputs, item is an internal variable that has information of the row and column of the entry that has been changed
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.scan_table_parameters.item(row, col)
            variable = self.experiment.scanned_variables[row]
            if col == 0: #name of the scanned variable changed
                new_variable_name = self.remove_restricted_characters(table_item.text())
                table_item.setText(new_variable_name)
                if self.check_if_already_scanned(new_variable_name) == False: #Check if the given variable is defined previously or not
                    index = self.index_of_a_new_variable(new_variable_name)
                    if self.index_of_a_new_variable(new_variable_name) != None: #Check if the varible name is defined in Variables tab
                        if new_variable_name not in self.experiment.sampler_variables: #Check if the variable name is used for sampling
                            #Proceeding with changes
                            prev_index = self.index_of_a_new_variable(variable.name)
                            if prev_index != None: #make the value of variable to the previous before being scanned.
                                #reverting the values to before scanning values and scanning states of the previous variable
                                self.experiment.variables[variable.name].value = self.experiment.new_variables[prev_index].value 
                                self.experiment.variables[variable.name].is_scanned = False 
                                self.experiment.variables[variable.name].for_python = self.experiment.variables[variable.name].value
                                self.experiment.new_variables[prev_index].is_scanned = False
                            #updating the values and scanning states of the new scanning  variable
                            variable.name = new_variable_name
                            self.experiment.variables[variable.name].value = variable.min_val
                            self.experiment.variables[variable.name].for_python = "self." + variable.name + "[step]"
                            self.experiment.variables[variable.name].is_scanned = True
                            self.experiment.new_variables[index].is_scanned = True
                        else: #The variable name enteres is used in sampler tab
                            self.error_message("The variable name you entered was already used in sampler tab", "Used variable name")
                            self.update_off()
                            table_item.setText(variable.name)
                            self.update_on()                            
                    else: #The variable name entered is not defined in a variables tab
                        self.error_message("The variable name you entered was not defined in variables tab", "Not defined variable")
                        self.update_off()
                        table_item.setText(variable.name)
                        self.update_on()
                else:
                    self.error_message("The variable name you entered was already used for scanning.", "Scanning variable duplicate")
                self.count_scanned_variables()
            elif col == 1: #min_val of the scanned variable changed
                try:
                    variable.min_val = float(table_item.text())
                    table_item.setText(str(variable.min_val))
                    if self.scan_table_parameters.item(row, 0).text() != "None": # this makes sure that we do not have to deal with "None" named variable
                        # we use the min values in order to use in sorting of the sequence tab
                        self.experiment.variables[variable.name].value = variable.min_val
                except:
                    self.error_message("Expression can not be evaluated", "Wrong entry")
            elif col == 2: #max_val of the scanned variable changed
                try:
                    variable.max_val = float(table_item.text())
                    table_item.setText(str(variable.max_val))
                except:
                    self.error_message("Expression can not be evaluated", "Wrong entry")
            update.digital_analog_dds_mirny_tabs(self)
            update.variables_tab(self, derived_variables = False)
            update.scan_table(self)       
        else:
            pass


    def skip_images_button_clicked(self):
        '''
        Function is used to toggle the initial trigger of the camera 10 times due to the problem of image acquisition.
        '''
        self.experiment.skip_images = not self.experiment.skip_images
        if self.experiment.skip_images:
            #set the color of the button to green
            self.skip_images_button.setStyleSheet("background-color: green; color: white")
        else:
            #set the color of the button to red
            self.skip_images_button.setStyleSheet("background-color: red; color: white")

        
    #DIGITAL TAB RELATED FUNCTIONS
    def update_digital_table_header(self, index, name):
        '''
        Fucntion is used to update the digital table title name. It takes the index of the title and the name and updates it
        '''
        if name != "":
            self.experiment.title_digital_tab[index] = "D%d"%(index - 4) + "\n" + name
        else:
            self.experiment.title_digital_tab[index] = "D%d"%(index - 4)
        self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
        self.dialog.accept()


    def digital_table_header_clicked(self, logicalIndex):
        '''
        Function is used when the user wants to change the digital table title name by clicking it.
        ligicalIndex is the internal item of the digital table header that reflects the index of the header clicked.
        '''
        index = logicalIndex
        if index > 3:
            #Pop up window to allow user to enter the name of the digital title
            self.dialog = QDialog()
            self.dialog.setGeometry(710, 435, 400, 120)
            self.dialog.setFont(QFont('Arial', 14))
            value_input = QLineEdit()
            dialog_layout = QVBoxLayout()
            button_update = QPushButton("update")
            button_cancel = QPushButton("cancel")
            dialog_layout.addWidget(value_input)
            dialog_buttons_layout = QHBoxLayout()
            dialog_buttons_layout.addWidget(button_update)
            dialog_buttons_layout.addWidget(button_cancel)
            dialog_layout.addLayout(dialog_buttons_layout)
            self.dialog.setLayout(dialog_layout)
            button_update.clicked.connect(lambda:self.update_digital_table_header(index, value_input.text()))
            button_cancel.clicked.connect(lambda:self.dialog.reject())
            self.dialog.setWindowTitle("Custom name for the channel") 
            self.dialog.exec_()
        else:
            pass


    def digital_table_changed(self, item):
        '''
        Function is used when the user changes the values in the digital table. It ensures that the expressions are integer values
        0 or 1. The user can delete the input and the function will assign the value of the previous edge and unhighlight the channel
        indicating that it should not be changed and will only display previously set value.
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.digital_table.item(row,col)
            channel = self.experiment.sequence[row].digital[col-4]
            if table_item.text() == "": #User deleted the value. The function will display the previously set state
                if row == 0: #default edge 
                    self.error_message("You can not delete initial value!", "Default value is protected!")
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                else:
                    channel.changed = False
                    update.digital_tab(self)
            else:   #User entered a new state
                try: 
                    #Checking whether the expression can be evaluated and the value is within allowed range
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                    exec("self.value = " + evaluation)
                    if (self.value == 0 or self.value == 1):
                        channel.changed = True
                        update.digital_tab(self)
                    else:
                        #Reverting back the previously accepted expression
                        self.update_off()
                        table_item.setText(str(channel.expression))
                        self.update_on()
                        self.error_message("Only value '1' or '0' are expected!", "Wrong entry!")
                except:
                    #Return the previously assigned value if the expression can not be evaluated
                    self.update_off()
                    if channel.changed:
                        table_item.setText(channel.expression)
                    else:
                        table_item.setText(str(channel.value))
                    self.update_on()
                    self.error_message("Expression can not be evaluated", "Wrong entry")


    #ANALOG TABLE RELATED
    def update_analog_table_header(self, index, name):
        '''
        Fucntion is used to update the analog table title name. It takes the index of the title and the name and updates it
        '''
        if name != "":
            self.experiment.title_analog_tab[index] = "A%d"%(index - 4) + "\n" + name
        else:
            self.experiment.title_analog_tab[index] = "A%d"%(index - 4)
        self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
        self.dialog.accept()


    def analog_table_header_clicked(self, logicalIndex):
        '''
        Function is used when the user wants to change the analog table title name by clicking it.
        ligicalIndex is the internal item of the analog table header that reflects the index of the header clicked.
        '''
        index = logicalIndex
        if index > 3:
            self.dialog = QDialog()
            self.dialog.setGeometry(710, 435, 400, 120)
            self.dialog.setFont(QFont('Arial', 14))
            value_input = QLineEdit()
            dialog_layout = QVBoxLayout()
            button_update = QPushButton("update")
            button_cancel = QPushButton("cancel")
            dialog_layout.addWidget(value_input)
            dialog_buttons_layout = QHBoxLayout()
            dialog_buttons_layout.addWidget(button_update)
            dialog_buttons_layout.addWidget(button_cancel)
            dialog_layout.addLayout(dialog_buttons_layout)
            self.dialog.setLayout(dialog_layout)
            button_update.clicked.connect(lambda:self.update_analog_table_header(index, value_input.text()))
            button_cancel.clicked.connect(lambda: self.dialog.reject())
            self.dialog.setWindowTitle("Custom name for the channel") 
            self.dialog.exec_()


    def analog_table_changed(self, item):
        '''
        Function is used when the user changes the values in the analog table. It ensures that the expressions are float values in the 
        range between -9.9 to +9.9. The user can delete the input and the function will assign the value of the previous edge and unhighlight the channel
        indicating that it should not be changed and will only display previously set value.
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            channel = self.experiment.sequence[row].analog[col - 4]
            table_item = self.analog_table.item(row,col)
            if table_item.text() == "": #User deleted the value. The function will display the previously set state
                if row == 0: # default edge
                    self.error_message("You can not delete initial value!", "Initial value is needed!")
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                else:
                    channel.changed = False
                    update.analog_tab(self)
            else: #User entered a new state
                try:
                    #Checking whether the expression can be evaluated and the value is within allowed range                    
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                    exec("self.value =" + evaluation)
                    if (self.value <= 9.9 and self.value >= -9.9):
                        channel.expression = expression
                        channel.evaluation = evaluation
                        channel.value = self.value
                        channel.is_scanned = is_scanned
                        channel.for_python = for_python 
                        channel.changed = True
                        update.analog_tab(self)
                    else:
                        #Reverting back the previously accepted expression                    
                        self.update_off()
                        table_item.setText(channel.expression)
                        self.update_on()
                        self.error_message("Only values between '+9.9' and '-9.9' are expected", "Wrong entry")
                except:
                    #Return the previously assigned value if the expression can not be evaluated                    
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                    self.error_message('Expression can not be evaluated', 'Wrong entry')


    #DDS TAB RELATED FUNCTIONS
    def dds_table_changed(self, item):
        '''
        Function is used when the user changes the values in the dds table. It ensures that the expressions can be evaluated in the
        allowed input values range. The user can delete the input and the function will assign the value of the previous edge and 
        unhighlight the channel indicating that it should not be changed and will only display previously set value.
        '''        
        if self.to_update:
            row = item.row()
            col = item.column()
            edge_num = row - 2
            channel = (col - 4)//6 #4 columns for edge and separation. division by 5 channel settings and 1 separation
            setting = col - 4 - 6 * channel # the number is a sequential value of setting. Frequency is 0, Amplitude 1, attenuation 2, phase 3, state 4
            if self.dds_table.item(row,col).text() == "": #User deleted the value. The function will display the previously set state
                if edge_num == 0: #Default edge
                    self.error_message("You can not delete initial value!", "Initial value is needed!")
                    self.update_off()
                    exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                else: #Other than a default edge
                    #Removing background color
                    self.update_off()
                    for index_setting in range(5):
                        self.dds_table.item(row, channel*6 + 4 + index_setting).setBackground(self.white)
                    self.experiment.sequence[edge_num].dds[channel].changed = False
                    self.update_on()
                    update.dds_tab(self)
            else:   #User entered a new input value
                try:
                    #Checking whether the expression can be evaluated and the value is within allowed range                     
                    expression = self.dds_table.item(row,col).text()
                    (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                    exec("self.dummy_val =" + evaluation)
                    maximum, minimum = self.max_dict_dds[setting], self.min_dict_dds[setting]
                    if (self.dummy_val <= maximum and self.dummy_val >= minimum): 
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.expression = expression" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.evaluation = evaluation" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.value = self.dummy_val" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        self.experiment.sequence[edge_num].dds[channel].changed = True
                        update.dds_tab(self)
                    else:
                        #Reverting back the previously accepted expression                            
                        self.error_message("Only values between %f and %f are expected" %(minimum, maximum), "Wrong entry")
                        self.update_off()
                        exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                        self.update_on()
                except:
                    #Return the previously assigned value if the expression can not be evaluated                       
                    self.update_off()
                    exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                    self.error_message('Expression can not be evaluated', 'Wrong entry')            


    def dds_dummy_header_changed(self, item):
        '''
        Function is used when the user wants to change the name of the dds title. 
        It overwrites the value of the corresponding title name in the experiment object so when it is saved the changes are persitent.
        '''
        if self.to_update:
            col = item.column()
            self.experiment.title_dds_tab[(col-4)//6 + 4] = self.dds_dummy_header.item(0,col).text() # title has 3 leading names and a separator


    #MIRNY TAB RELATED FUNCTIONS
    def mirny_table_changed(self, item):
        '''
        Function is used when the user changes the values in the mirny table. It ensures that the expressions can be evaluated in the
        allowed input values range. The user can delete the input and the function will assign the value of the previous edge and 
        unhighlight the channel indicating that it should not be changed and will only display previously set value.
        '''        
        if self.to_update:
            row = item.row()
            col = item.column()
            edge_num = row - 2
            channel = (col - 4)//6 #4 columns for edge and separation. division by 5 channel settings and 1 separation
            setting = col - 4 - 6 * channel # the number is a sequential value of setting. Frequency is 0, Amplitude 1, attenuation 2, phase 3, state 4
            if self.mirny_table.item(row,col).text() == "": #User deleted the value. The function will display the previously set state
                if edge_num == 0: #Default edge
                    self.error_message("You can not delete initial value!", "Initial value is needed!")
                    self.update_off()
                    exec("self.mirny_table.item(row,col).setText(str(self.experiment.sequence[edge_num].mirny[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                else: #Other than a default edge
                    #Removing background color
                    self.update_off()
                    for index_setting in range(5):
                        self.mirny_table.item(row, channel*6 + 4 + index_setting).setBackground(self.white)
                    self.experiment.sequence[edge_num].mirny[channel].changed = False
                    self.update_on()
                    update.mirny_tab(self)
            else:   #User entered a new input value
                try:
                    #Checking whether the expression can be evaluated and the value is within allowed range                     
                    expression = self.mirny_table.item(row,col).text()
                    (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                    exec("self.dummy_val =" + evaluation)
                    maximum, minimum = self.max_dict_mirny[setting], self.min_dict_mirny[setting]
                    if (self.dummy_val <= maximum and self.dummy_val >= minimum): 
                        exec("self.experiment.sequence[edge_num].mirny[channel].%s.expression = expression" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].mirny[channel].%s.evaluation = evaluation" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].mirny[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].mirny[channel].%s.value = self.dummy_val" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].mirny[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        self.experiment.sequence[edge_num].mirny[channel].changed = True
                        update.mirny_tab(self)
                    else:
                        #Reverting back the previously accepted expression                            
                        self.error_message("Only values between %f and %f are expected" %(minimum, maximum), "Wrong entry")
                        self.update_off()
                        exec("self.mirny_table.item(row,col).setText(str(self.experiment.sequence[edge_num].mirny[channel].%s.expression))" %self.setting_dict[setting])
                        self.update_on()
                except:
                    #Return the previously assigned value if the expression can not be evaluated                       
                    self.update_off()
                    exec("self.mirny_table.item(row,col).setText(str(self.experiment.sequence[edge_num].mirny[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                    self.error_message('Expression can not be evaluated', 'Wrong entry')            


    def mirny_dummy_header_changed(self, item):
        '''
        Function is used when the user wants to change the name of the mirny title. 
        It overwrites the value of the corresponding title name in the experiment object so when it is saved the changes are persitent.
        '''
        if self.to_update:
            col = item.column()
            self.experiment.title_mirny_tab[(col-4)//6 + 4] = self.mirny_dummy_header.item(0,col).text() # title has 3 leading names and a separator


    #SLOW_DDS TAB RELATED FUNCTIONS
    def slow_dds_table_changed(self, item):
        '''
        Function is used when the user changes the values in the slow_dds table. It ensures that the expressions can be evaluated in the
        allowed input values range. The user can delete the input and the function will assign the value of the previous edge and 
        unhighlight the channel indicating that it should not be changed and will only display previously set value.
        '''        
        if self.to_update:
            row = item.row()
            col = item.column()
            channel = (col - 1)//6 #4 columns for edge and separation. division by 5 channel settings and 1 separation
            setting = col - 1 - 6 * channel # the number is a sequential value of setting. Frequency is 0, Amplitude 1, attenuation 2, phase 3, state 4
            if row == 2: #Table entry was changed
                if self.slow_dds_table.item(row,col).text() == "": #User deleted the value. The function will display the previously set state
                    self.error_message("You can not delete the value!", "Some value is required!")
                    self.update_off()
                    exec("self.slow_dds_table.item(row,col).setText(str(self.experiment.slow_dds[channel].%s))" %self.setting_dict[setting])
                    self.update_on()
                else:   #User entered a new input value
                    try:
                        #Checking whether the expression can be evaluated and the value is within allowed range                     
                        expression = self.slow_dds_table.item(row,col).text()
                        (evaluation, for_python, is_scanned, is_sampled, is_derived) = self.decode_input(expression)
                        exec("self.dummy_val =" + evaluation)
                        maximum, minimum = self.max_dict_dds[setting], self.min_dict_dds[setting]
                        if (self.dummy_val <= maximum and self.dummy_val >= minimum): 
                            exec("self.experiment.slow_dds[channel].%s = self.dummy_val" %self.setting_dict[setting])
                            for parameter in range(5): # THIS SHOULD BE DONE
                                if self.experiment.slow_dds[channel].state == 1:
                                    self.slow_dds_table.item(row,(col - 1)//6 * 6 + parameter).setBackground(self.green)
                                else:
                                    self.slow_dds_table.item(row,(col - 1)//6 * 6 + parameter).setBackground(self.red)
                        else:
                            #Reverting back the previously accepted expression                            
                            self.error_message("Only values between %f and %f are expected" %(minimum, maximum), "Wrong entry")
                            self.update_off()
                            exec("self.slow_dds_table.item(row,col).setText(str(self.experiment.slow_dds[channel].%s))" %self.setting_dict[setting])
                            self.update_on()
                    except:
                        #Return the previously assigned value if the expression can not be evaluated                       
                        self.update_off()
                        exec("self.slow_dds_table.item(row,col).setText(str(self.experiment.slow_dds[channel].%s))" %self.setting_dict[setting])
                        self.update_on()
                        self.error_message('Expression can not be evaluated', 'Wrong entry')            
            elif row == 0: #Channel title was changed
                self.experiment.title_slow_dds_tab[(col)//6 + 4] = self.slow_dds_table.item(0,col).text() 


    def set_slow_dds_states_button_clicked(self):
        '''
        Function is used when the user requests to set the displayed values. It will generate the experimental description
        and artiq_run it to set only the states of the slow dds channels
        '''
        try:
            write_to_python.set_slow_dds_states(self)
            self.message_to_logger("Python file generated")
            try:
                #initialize environment and submit the experiment to the scheduler
                if config.package_manager == "conda":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate %s && set_slow_dds_states.py"%config.artiq_environment_name])
                elif config.package_manager == "clang64":
                    submit_experiment_thread = threading.Thread(target=os.system, args=["set_slow_dds_states.bat"])
                submit_experiment_thread.start()
                self.message_to_logger("Slow DDS states are set")
            except:
                self.message_to_logger("Was not able to set slow DDS states")
        except:
            self.message_to_logger("Was not able to generate python file")
    

    #VARIABLES TAB RELATED FUNCTIONS
    def find_new_variable_name_unused(self):
        '''
        Function itereates over the variable names of form var_1, var_2, etc. and returns the lowest available variable name
        '''
        for i in range(1, 1000):
            name = "var_" + str(i)
            if name not in self.experiment.variables:
                return name


    def delete_variable_button_clicked(self):
        '''
        Function is used when the user wants to delete the variable from the variables table.
        It checks if the variable is used in any expression by deleting it and trying to evaluate every expression.
        the backup is used in order to be able to revert the changes in case the variable is used somewhere.
        '''
        try:
            row = self.variables_table.selectedIndexes()[0].row()
            name = self.variables_table.item(row,0).text()
            if name not in self.experiment.sampler_variables: # Check if the variable is being sampled 
                #Checking if the variable is being scanned
                variable_scanned = False
                for variable in self.experiment.scanned_variables:
                    if name == variable.name:
                        variable_scanned = True
                        break
                if variable_scanned == False:
                    backup = deepcopy(self.experiment.variables[name]) #used to be able to revert the process of deletion
                    del self.experiment.variables[name]
                    self.variables_table.setCurrentCell(row-1,0)
                    return_value = update.digital_analog_dds_mirny_tabs(self) #we need to update only values not expressions
                    if return_value == None: #Variable can be deleted
                        del self.experiment.new_variables[row]
                        update.variables_tab(self)
                    else: #Variable can not be deleted. Reverting all changes back to previous state
                        self.experiment.variables[name] = backup
                        update.digital_analog_dds_mirny_tabs(self) 
                        update.variables_tab(self)
                        self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
                else:
                    self.error_message("The variable is scanned. Remove it from the scan table before deleting.", "Scanned variable")
            else:
                self.error_message("The variable is sampled. Remove it from the sampler tab before deleting.", "Sampled variable")
        except: #In case the user pressed delete variable button without selecting the variable that needs to be deleted
            self.error_message("Select the variable that needs to be deleted", "No variable selected")


    def create_new_variable_button_clicked(self):
        '''
        Function is used when the user wants to create a new user defined variable. It finds the lowest unused available variable name and 
        creates it with initial value of 0.0. It also creates the corresponding Variable objects  in new_variables and variables.
        '''
        variable_name = self.find_new_variable_name_unused()
        self.experiment.new_variables.append(self.Variable(variable_name, 0.0, 0.0))
        self.experiment.variables[variable_name] = self.Variable(variable_name, 0.0, 0.0)
        update.variables_tab(self, derived_variables = False)


    def variables_table_changed(self, item):
        '''
        Function is used when the user changes the values in the variables table. It makes sure that in case the name is changed
        the previous variable was not used in the expression of any parameter in the sequence. In case the previous variable is
        used in any epxression the function will let user know about the first occurence of that variable and revert the name. 
        It also makes sure that if the variable is used the expression when its value is changed the expression evaluation remains in the
        allowed parameters range.       
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            variable = self.experiment.new_variables[row]
            table_item = self.variables_table.item(row,col)
            if col == 0: #Variable name was changed
                if variable.name not in self.experiment.sampler_variables: # Check if the variable is being sampled 
                    #Checking if the variable is being scanned
                    variable_scanned = False
                    for item in self.experiment.scanned_variables:
                        if variable.name == item.name:
                            variable_scanned = True
                            break
                    if variable_scanned == False:
                        new_name = self.remove_restricted_characters(table_item.text())
                        #Restricting the user from using the reserved default variable names in the form of id1, id2, etc.
                        if new_name[0:2] == "id" and new_name[2] in "0123456789":
                            self.error_message("Variable names starting with id and following with integers are reserved for default edge time variables", "Invalid variable name")
                        elif new_name == "None": #Restricting the user from defining the variable name "None" as it is reserved by the Scan table
                            self.error_message("Variable name None is reserved by the scan table. Please choose another name", "Invalid variable name")
                            self.update_off()
                            table_item.setText(variable.name)       
                            self.update_on()             
                        elif new_name in self.experiment.variables:#Restricting the user from defining the variable name as already defined variable names to avoid having duplicates
                            self.error_message('Variable name is already used', 'Invalid variable name')
                            self.update_off()
                            table_item.setText(variable.name)       
                            self.update_on()                         
                        else: # The varibable name is almost among allowed, only the integer or float without other caracters should be checked.
                            only_numbers = False
                            try:
                                float(new_name) #does not allow defining variable names that contains only integers without characters
                                only_numbers = True
                            except:
                                pass
                            if only_numbers: #Restricting the user from defining a variable name using only numbers
                                self.update_off()
                                table_item.setText(variable.name)       
                                self.update_on()                         
                                self.error_message('Variable name can not be in a form of a number', 'Invalid variable name')
                            else:
                                #Allowed variable name. Now checking if it is used in any expression or not. It is done by deleting the variable and trying to evaluate every expression
                                #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                                backup = deepcopy(self.experiment.variables[variable.name])
                                del self.experiment.variables[variable.name]
                                return_value = update.digital_analog_dds_mirny_tabs(self) # we need to update value. In other words evaluate evaluations. No need to udpage expressions
                                if return_value == None: #The previous variable was not used anywhere and can be changed
                                    self.experiment.variables[new_name] = backup
                                    self.experiment.variables[new_name].name = new_name
                                    self.experiment.variables[new_name].is_scanned = False
                                    variable.name = new_name
                                    self.update_off()
                                    table_item.setText(variable.name)
                                    self.update_on()                            
                                else: #The previous variable was used somewhere. Reverting the name to the previous 
                                    self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
                                    self.experiment.variables[backup.name] = backup
                                    self.update_off()
                                    table_item.setText(backup.name)
                                    self.update_on()
                    else:
                        self.update_off()
                        table_item.setText(variable.name)
                        self.update_on()                          
                        self.error_message("The variable is scanned. Remove it from the scan table before changing its name.", "Scanned variable")
                else:
                    self.update_off()
                    table_item.setText(variable.name)
                    self.update_on()                      
                    self.error_message("The variable is sampled. Remove it from the sampler tab before changing its name.", "Sampled variable")
            elif col == 1: #variable value was changed
                #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                try:
                    #Checking if the new value resulting in the values allowed for each parameter it is used in
                    self.experiment.variables[variable.name].value = float(table_item.text())
                    return_value = update.digital_analog_dds_mirny_tabs(self) # we do not need to update expressions only update values.
                    if return_value == None: #The value can be updated
                        variable.value = self.experiment.variables[variable.name].value
                        table_item.setText(str(variable.value))
                        update.sequence_tab(self)
                        update.digital_analog_dds_mirny_tabs(self)
                        update.from_object(self)
                    else: #The value can not be updated, reverting every evaluation done before.
                        self.error_message("Evaluation is out of allowed range occured in %s. Variable value can not be assigned" %return_value, "Wrong entry")
                        self.experiment.variables[variable.name].value = variable.value 
                        self.update_off()
                        table_item.setText(str(variable.value))
                        self.update_on()
                        update.sequence_tab(self)
                        update.digital_analog_dds_mirny_tabs(self)
                        update.from_object(self)
                except: #Restricting the user from using anything but the integer values and floating numbers
                    self.update_off()
                    table_item.setText(str(variable.value))
                    self.update_on()
                    update.digital_analog_dds_mirny_tabs(self, update_expressions_and_evaluations=False)                    
                    self.error_message("Only integers and floating numbers are allowed.", "Wrong entry")


    def find_derived_variable_name_unused(self):
        '''
        Function itereates over the variable names of form derived_1, derived_2, etc. and returns the lowest available variable name
        '''
        for i in range(1, 1000):
            name = "derived_" + str(i)
            if name not in self.experiment.names_of_derived_variables:
                return name


    def create_derived_variable_button_clicked(self):
        '''
        Function is used when the user wants to create a new derived variable. It finds the lowest unused available variable name and 
        creates it with initial value of 0.0. It also create the corresponding Variable objects  in new_variables and variables.
        '''
        variable_name = self.find_derived_variable_name_unused()
        self.experiment.names_of_derived_variables.add(variable_name)
        self.experiment.derived_variables.append(self.Derived_variable(name = variable_name, edge_id = "", arguments = "", function = ""))
        self.experiment.variables[variable_name] = self.Variable(name = variable_name, value = 0.0, for_python = 0.0, is_derived = True)
        update.variables_tab(self, new_variables = False)


    def find_edge_index_by_id(self, id):
        '''
        Function is used to find the index of the edge by its id value. It iterates over all edges and returns the 
        index when the id matches the edge.id
        '''
        for index, edge in enumerate(self.experiment.sequence):
            if edge.id == id:
                return index


    def delete_derived_variable_button_clicked(self):
        '''
        Function is used when the user wants to delete the derived variable from the table.
        '''
        try:
            row = self.derived_variables_table.selectedIndexes()[0].row()
            if row == 0:
                self.error_message("You can not delete a dummy example", "Protected variable")
            else:
                print(1)
                name = self.derived_variables_table.item(row,0).text()
                edge_index = self.find_edge_index_by_id(self.derived_variables)
                self.experiment.sequence[edge_index].derived_variable_requested = 0
                self.experiment.names_of_derived_variables.remove(name)
                print(2)
                del self.experiment.derived_variables[row-1] # -1 is due to the dummy variable taking the first row
                print(3)
                del self.experiment.variables[name]
                print(4)
                update.variables_tab(self, new_variables = False)
        except: #In case the user pressed delete variable button without selecting the variable that needs to be deleted
            self.error_message("Select the variable that needs to be deleted", "No variable selected")

    def derived_variables_table_changed(self, item):
        '''
        Function is used when the user changes the values in the derived variables table. 
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            variable = self.experiment.derived_variables[row-1] # due to the dummy variable being 1st
            table_item_text = self.derived_variables_table.item(row,col).text()
            self.derived_variables_table.item(row,col).setText(table_item_text.replace(" ",""))
            if col == 0: #Variable name was changed
                del self.experiment.variables[variable.name]
                variable.name = table_item_text.replace(" ","")
                self.experiment.variables[variable.name] = self.Variable(name = variable.name, value = 0.0, for_python = 0.0, is_derived = True)
            if col == 1: #Variable arguments were changed
                variable.arguments = table_item_text.replace(" ","")
            if col == 2: #Variable execution edge was changed
                new_edge_id = table_item_text.replace(" ", "")
                if self.find_edge_index_by_id(new_edge_id) == None:
                    self.error_message("The edge id was not found. Please enter correct id value", "Wrong id entered")
                    self.derived_variables_table.item(row,col).setText(variable.edge_id)
                else:
                    if variable.edge_id != "":  #In case it was another id before we need to make that edge.derived_variable_requested to 0 which means that it is not requested
                        edge_index = self.find_edge_index_by_id(variable.edge_id)
                        self.experiment.sequence[edge_index].derived_variable_requested = -1
                    #Assigning the edge.derived_variable_requested value 
                    variable.edge_id = table_item_text.replace(" ","")
                    edge_index = self.find_edge_index_by_id(variable.edge_id)
                    self.experiment.sequence[edge_index].derived_variable_requested = row-1 # -1 because the dummy variable is the first one
            if col == 3: #Variable function was changed
                variable.function = table_item_text


    #SAMPLER TAB RELATED FUNCTIONS
    def update_sampler_table_header(self, index, name):
        '''
        Fucntion is used to update the sampler table title name. It takes the index of the title and the name and updates it
        '''
        if name != "":
            self.experiment.title_sampler_tab[index] = "S%d"%(index - 4) + "\n" + name
        else:
            self.experiment.title_sampler_tab[index] = "S%d"%(index - 4)        
        self.sampler_table.setHorizontalHeaderLabels(self.experiment.title_sampler_tab)
        self.dialog.accept()


    def sampler_table_header_clicked(self, logicalIndex):
        '''
        Function is used when the user wants to change the sampler table title name by clicking it.
        ligicalIndex is the internal item of the sampler table header that reflects the index of the header clicked.
        '''
        index = logicalIndex
        if index > 3:
            #Pop up window to allow user to enter the name of the sampler title
            self.dialog = QDialog()
            self.dialog.setGeometry(710, 435, 400, 120)
            self.dialog.setFont(QFont('Arial', 14))
            value_input = QLineEdit()
            dialog_layout = QVBoxLayout()
            button_update = QPushButton("update")
            button_cancel = QPushButton("cancel")
            dialog_layout.addWidget(value_input)
            dialog_buttons_layout = QHBoxLayout()
            dialog_buttons_layout.addWidget(button_update)
            dialog_buttons_layout.addWidget(button_cancel)
            dialog_layout.addLayout(dialog_buttons_layout)
            self.dialog.setLayout(dialog_layout)
            button_update.clicked.connect(lambda:self.update_sampler_table_header(index, value_input.text()))
            button_cancel.clicked.connect(lambda:self.dialog.reject())
            self.dialog.setWindowTitle("Custom name for the channel") 
            self.dialog.exec_()
        else:
            pass


    def sampler_table_changed(self, item):
        '''
        Function is used when the user changes the values in the sampler table. It ensures that the expressions are integer values
        0 or variable name defined in variables tab. The user can delete the input and the function will assign the value to 0 and unhighlight the channel
        '''
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.sampler_table.item(row, col)
            table_entry = self.sampler_table.item(row,col).text()
            channel = self.experiment.sequence[row].sampler[col-4]
            if table_entry == "" or table_entry == "0" or table_entry == "0.0": #User deleted the value or set it to 0. The function will assign 0 value
                if channel in self.experiment.sampler_variables: #if the previous value of the sampler was a variable we need to revert back the variables tab value and activate editing
                    self.experiment.sampler_variables.remove(channel)
                    update.variables_tab(self, derived_variables = False)
                self.update_off()
                table_item.setText("0")
                self.update_on()
            else: #User attempted to assign a variable name to the sampler input
                if table_entry in self.experiment.variables: #Check if the variable name is defined in the variables tab
                    if self.experiment.variables[table_entry].is_scanned == False: #Check if the variable name is not scanned
                        if table_entry not in self.experiment.sampler_variables:
                            #Remove the previous variable from the sampler variables if it was not 0 before the human entry
                            if channel in self.experiment.sampler_variables:
                                self.experiment.sampler_variables.remove(channel)
                            self.experiment.sequence[row].sampler[col-4] = table_entry #Updating the sampler value
                            self.experiment.sampler_variables.add(table_entry) #Adding a new variable to the sampler variables set
                            update.variables_tab(self, derived_variables = False)
                        else:
                            self.update_off()
                            table_item.setText(str(channel))
                            self.update_on()
                            self.error_message("Variable you entered is already used in sampler. Duplicates are not allowed.", "Reuse of the variable")        
                    else:
                        self.update_off()
                        table_item.setText(str(channel))
                        self.update_on()
                        self.error_message("Variable you entered is in the Scan table. First remove it from there.", "Scanned variable")        
                else:
                    self.update_off()
                    table_item.setText(str(channel))
                    self.update_on()
                    self.error_message("Variable you entered is not found in the variables table. First create the variable there.", "No variable found")
            update.sampler_tab(self)  
                

def run():
    '''
    Main function that starts the application and invokes the window
    '''
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


if __name__ == "__main__":
    run()