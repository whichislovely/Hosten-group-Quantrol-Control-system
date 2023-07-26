from os import error
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import write_to_python
import declare_global_var  
import tabs
import pickle
from datetime import datetime
from copy import deepcopy
import update
import time
import threading

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    class Edge:
        def __init__(self, name = "", id = "id0", expression = "0", evaluation = 0, for_python = 0, value = 0, is_scanned = False):
            self.is_scanned = False
            self.expression = expression
            self.evaluation = evaluation
            self.value = value   
            self.name = name
            self.id = id
            self.is_scanned = is_scanned
            self.for_python = for_python
            self.analog = [self.Analog() for i in range(32)]
            self.digital = [self.Digital() for i in range(16)]
            self.dds = [self.DDS() for i in range(12)]

        class Digital:
            #Object is used to describe digital channels' values
            def __init__(self, value = 0, expression = "0", evaluation = 0, for_python = 0, changed = False):
                self.value = value
                self.expression = expression
                self.evaluation = evaluation
                self.for_python = for_python
                self.changed = changed
                self.is_scanned = False

        class Analog:
            #Object is used to describe analog channels' values
            def __init__(self, value = 0, expression = "0", evaluation = 0, for_python = "0", changed = False):
                self.value = value
                self.expression = expression
                self.evaluation = evaluation
                self.for_python = for_python
                self.changed = changed
                self.is_scanned = False

        class DDS:
            def __init__(self, state = 0.0, changed = False):
                self.frequency = self.Object()
                self.amplitude = self.Object()
                self.attenuation = self.Object()
                self.phase = self.Object()
                self.state = self.Object()
                self.changed = changed

            class Object:
                #Object is used to describe analog, digital channels' values as well as DDSs' frequency, amplitude, attenuation and phase
                def __init__(self, value = 0.0, expression = "0.0", evaluation = 0.0, changed = False):
                    self.value = value
                    self.expression = expression
                    self.evaluation = evaluation
                    self.changed = changed   
                    self.is_scanned = False     
                    self.for_python = evaluation

    class Experiment:
        def __init__(self):
            self.title_digital_tab = []
            self.title_analog_tab = []
            self.title_dds_tab = []
            self.sequence = None #list of edges
            self.go_to_edge_num = -1
            self.new_variables = [] #this was decided to be a list in order to display the human defined variables
            self.variables = {}
            self.do_scan = False
            self.number_of_steps = 1
            self.file_name = ""
            self.scanned_variables = [] #list of variables involved in a scan
            self.scanned_variables_count = 0
            self.continously_running = False # it is a flag indicating whether the experiment is being

    class Scanned_variable:
        def __init__(self, name, min_val, max_val):
            self.name = name
            self.min_val = min_val
            self.max_val = max_val

    class Variable: # is for every human defined variable and default variables of a form id#
        def __init__(self, name, value, for_python, is_scanned = False):
            self.name = name
            self.value = value
            self.is_scanned = is_scanned
            self.for_python = for_python
            
    class CustomThread(threading.Thread):
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
        self.setWindowTitle("Experimental control application. Hosten Group")
        self.main_window = QTabWidget()
        self.setCentralWidget(self.main_window)
        self.setGeometry(0,30,1920,1200)
        
        declare_global_var.build(self)
        tabs.sequence_tab_build(self)
        tabs.digital_tab_build(self)
        tabs.analog_tab_build(self)
        tabs.dds_tab_build(self)
        tabs.variables_tab_build(self)
        
        
        #ADDING TABS TO MAIN WINDOW
        self.main_window.addTab(self.sequence_tab_widget, "Sequence")
        self.main_window.addTab(self.digital_tab_widget, "Digital")
        self.main_window.addTab(self.analog_tab_widget, "Analog")
        self.main_window.addTab(self.dds_tab_widget, "DDS")
        self.main_window.addTab(self.variables_tab_widget, "Variables")
        self.to_update = True
        
        #starting artiq server (artiq_master)

        self.server_thread = self.CustomThread(target=os.system, args=["conda activate artiq_5 && artiq_master"])
        self.server_thread.start()  
        # server_thread = threading.Thread(target=os.system, args=["conda activate artiq_5 && artiq_master"])
        # server_thread.start()  

        


    #FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS
    #GENERAL FUNCTIONS
    
    def message_to_logger(self, message):
        #this function receives a message and then displays it with date and time 
        self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + message)
        
    def making_separator(self):
        #Spanning the cells to avoid colouring each cell separately
        if self.sequence_num_rows > 1: # to avoid having a warning that single cell span won't be added
            self.digital_table.setSpan(0,3, self.sequence_num_rows , 1)
            self.analog_table.setSpan(0,3, self.sequence_num_rows , 1)
        else:
            pass
        # gray coloured separating line digital tab
        self.digital_table.setItem(0,3, QTableWidgetItem())
        self.digital_table.item(0,3).setBackground(self.gray)
        # gray coloured separating line analog tab
        self.analog_table.setItem(0,3, QTableWidgetItem())
        self.analog_table.item(0,3).setBackground(self.gray)
        # gray coloured separating line dds tab
        self.dds_dummy.setSpan(0,3, self.sequence_num_rows + 2, 1)
        self.dds_dummy.setItem(0,3, QTableWidgetItem())
        self.dds_dummy.item(0,3).setBackground(self.gray)
        # gray coloured separating line dds tab
        for i in range(12):
            self.dds_table.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
            self.dds_table.setItem(0,6*i + 3, QTableWidgetItem())
            self.dds_table.item(0, 6*i + 3).setBackground(self.gray)

    def setColorCol(self, col):
        #this function takes the column number and first megres all rows and then paints its background
        #it is used for separating DDS channels but can be employed elsewhere is needed
        self.dds_table.setSpan(0, col, self.sequence_num_rows+2, 1)
        self.dds_table.setItem(0,col, QTableWidgetItem())
        self.dds_table.item(0, col).setBackground(self.gray)

    def update_on(self):
        self.to_update = True

    def update_off(self):
        self.to_update = False

    def error_message(self, text, title):
        msg = QMessageBox()
        msg.setFont(QFont('Arial', 14))
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle(title)
        msg.exec_()
    
    #SEQUENCE TAB RELATED
    def sequence_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            edge = self.experiment.sequence[row]
            table_item = self.sequence_table.item(row,col)
            if col == 3: # edge time expression changed
                if table_item.text() == "":
                    if row == 0: #default channel can not be deleted
                        self.error_message("You can not delete initial value! Only positive values are expected", "Initial value is needed!")
                        self.update_off()
                        table_item.setText(str(edge.expression))
                        self.update_on()
                    else: # if not default channel apply changes 
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
                        (evaluation, for_python, is_scanned) = self.decode_input(expression)
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
            elif col == 1: # edge name changed
                edge.name = table_item.text()

    
    def save_sequence_button_clicked(self):
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
        temp_file_name = QFileDialog.getOpenFileName(self, "Open File")[0]
        if temp_file_name != "": #happens when no file name was given (canceled)
            try:
                with open(temp_file_name, 'rb') as file:
                    self.experiment = pickle.load(file)
                self.sequence_num_rows = len(self.experiment.sequence)
                self.update_off()
                self.scan_table.setChecked(self.experiment.do_scan)
                #update the label showing the sequence that is being modified 
                self.experiment.file_name = temp_file_name
                self.create_file_name_label()
                update.from_object(self)
                self.message_to_logger("Sequence loaded from %s" %self.experiment.file_name)
            except:
                self.error_message('Could not load the file.', 'Error')
            self.update_on()

    def create_file_name_label(self):
        self.file_name_lable.setText(self.experiment.file_name)


    def find_unique_id(self):
        #this functions finds the smallest possible id number that is not used and returns it
        for id in range(10**4):
            unique_id = "id" + str(id)
            if unique_id not in self.experiment.variables:
                return unique_id
        
    def insert_edge_button_clicked(self):   
        #appending a new edge with a unique id
        new_unique_id = self.find_unique_id()
        new_edge = deepcopy(self.experiment.sequence[-1]) #copying the last edge
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
        self.dds_dummy.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name         row = self.sequence_num_rows - 1
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
        self.update_on()

    def delete_edge_button_clicked(self):
        try:
            row = self.sequence_table.selectedIndexes()[0].row()
            name = self.experiment.sequence[row].id
            if row == 0:
                self.error_message("You can not delete the starting edge", "Protected item")
            else:
                backup = deepcopy(self.experiment.variables[name]) #backup is a variable copy in case we would need to restore changes and not allow deleting edge
                #the following is a check whether the edge has been used somewhere. First we delete a corresponding variable and then try to evaluate all the entries
                del self.experiment.variables[name]
                return_value = update.all_tabs(self)
                if return_value == None:
                    del self.experiment.sequence[row]
                    self.sequence_table.setCurrentCell(row-1, 0)
                    update.from_object(self)
                else:
                    self.experiment.variables[name] = backup
                    self.error_message('The edge time value is used as a variable in %s.'%return_value, 'Can not delete used edge')
        except:
            self.error_message("Select the edge you want to delete", "No edge selected")

    def set_color_of_the_edge(self, set_color, edge_num):
        #this function is used by update_go_to_edge_color in order to highlight or unhighlight the edge
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
        # this function is called to put the control system into a particular edge state. 
        # all channels parameters are being set (DDS, ANALOG, DIGITAL).
        try:                
            write_to_python.create_go_to_edge(self)
            self.message_to_logger("Go to edge file generated")
            try:
                if os.system("conda activate artiq_5 && artiq_client submit go_to_edge.py") == 0:
                    self.message_to_logger("Went to edge")
                    edge_num = self.sequence_table.selectedIndexes()[0].row()
                    #unhighlighting the previously highlighted edge if it was previously highlighted
                    if self.experiment.go_to_edge_num != -1:
                        self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                    #highlighting newly selected edge to go
                    self.set_color_of_the_edge(self.green, edge_num)
                    self.experiment.go_to_edge_num = edge_num
                else:
                    self.message_to_logger("Couldn't go to edge")        
            except:
                self.message_to_logger("Couldn't go to edge")    
        except:
            self.error_message("Chose the edge you want the system to go","No edge selected")

    def count_scanned_variables(self):
        #this function iterates over all scanned variables that are not "None" and assigns the total count to 
        #self.experiment.scanned_variables_count. The function does not return anything
        count = 0
        for variable in self.experiment.scanned_variables:
            if variable.name != "None":
                count += 1
        self.experiment.scanned_variables_count = count

    def run_experiment_button_clicked(self): 
        self.count_scanned_variables()

        try:
            write_to_python.create_experiment(self)
            self.message_to_logger("Python file generated")
            try:
                #initialize environment and submit the experiment to the scheduler
                submit_experiment_thread = threading.Thread(target=os.system, args=["conda activate artiq_5 && artiq_client submit run_experiment.py"])
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


    def dummy_button_clicked(self):
        # print(self.server_thread.is_alive())
        # print(self.server_thread._return)
        current_experiment = self.CustomThread(target=os.system, args=["conda activate artiq_5 && artic_client scheduler.rid"])


    #    print("analog channel values")
    #    for edge in self.experiment.sequence:
    #        for ind, channel in enumerate(edge.analog):
    #            print("Channel", ind, "val", channel.value, "evaluation", channel.evaluation)
    #    print("scanned_variables")
    #    for item in self.experiment.scanned_variables:
    #        print(item.name, item.min_val, item.max_val)
    #    print("new variables")
    #    for item in self.experiment.new_variables:
    #        print(item.name, item.value, item.is_scanned)
        # for key, item in self.experiment.variables.items():
        #     print("var", item.name, "is_scanned", item.is_scanned, "for_python", item.for_python)
        # for ind, edge in enumerate(self.experiment.sequence):
        #     print("edge", ind)
        #     print("    chanel", ind,"evaluation", edge.evaluation, "for_python", edge.for_python, "scanned", edge.is_scanned)
        # print("END")

    def save_sequence_as_button_clicked(self):
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
        self.count_scanned_variables()
        
        try:
            write_to_python.create_experiment(self, run_continuous=True)
            self.message_to_logger("Python file generated")
            try:
                #initialize environment and submit the experiment to run continuously unless it is stopped
                submit_run_continuously_thread = threading.Thread(target=os.system, args=["conda activate artiq_5 && artiq_client submit run_experiment.py"])
                submit_run_continuously_thread.start()
                #unhighlighting the previously highlighted edge
                if self.experiment.go_to_edge_num != -1:
                    self.set_color_of_the_edge(self.white, self.experiment.go_to_edge_num)
                    self.experiment.go_to_egde_num = -1
                
                #needs to be done ---> logging the start of the experiment only if it was started without errors. Checking experiment stages
                self.message_to_logger("Experiment started")
            except:
                self.message_to_logger("Was not able to start experiment")
        except:
            self.message_to_logger("Was not able to generate python file")
        
        
        
    def stop_continuous_run_button_clicked(self):
        #stops continuous run
        #maybe try to find out the current experiment rid instead of using the last one? scheduler.rid might do the job
        try:
            with open('last_rid.pyon', 'r') as file:
                rid_of_the_last_scheduled_experiment = file.read()
        
            thread_stop_continuous_run = threading.Thread(target=os.system, args=["conda activate artiq_5 && artiq_client delete %s -g" %rid_of_the_last_scheduled_experiment])
            thread_stop_continuous_run.start()
            self.message_to_logger("Continuous run stopped")
        except:
            self.message_to_logger("Could not stop the continuous run")

    #the button is used to clear the logger         
    def clear_logger_button_clicked(self):
        self.logger.clear()

    def scan_table_checked(self):
        #NEED TO LOOK INTO THIS
        #check the scanned states of variables
        if self.to_update:
            self.experiment.do_scan = self.scan_table.isChecked()
            if self.experiment.do_scan == False:
                #reassign the variables to the pre scanning values using self.experiment.new_variables
                for item in self.experiment.new_variables:
                    self.experiment.variables[item.name].value = item.value
                    #there is no need to manually making the variables is_scanned attribute False since it is done in decode_input as self.experiment.do_scan is false
            else:
                for variable in self.experiment.scanned_variables:
                    self.experiment.variables[variable.name].value = variable.min_val
            update.all_tabs(self)
            update.variables_tab(self)
        

    def add_scanned_variable_button_pressed(self):
        self.experiment.scanned_variables.append(self.Scanned_variable("None", 0, 0))
        update.scan_table(self)

    def delete_scanned_variable_button_pressed(self):
        try:
            row = self.scan_table_parameters.selectedIndexes()[0].row()
            variable = self.experiment.scanned_variables[row]
            index = self.index_of_a_new_variable(variable.name)
            if index != None: #this is done to avoid trying to access "None" variable
                #reverting the value and scanning state of the variable that is not scanned anymore
                self.experiment.variables[variable.name].is_scanned = False
                self.experiment.variables[variable.name].value = self.experiment.new_variables[index].value #make the value of variable to the previous before being scanned
                self.experiment.new_variables[index].is_scanned = False
                self.experiment.variables[variable.name].for_python = self.experiment.variables[variable.name].value
            del self.experiment.scanned_variables[row]
            update.variables_tab(self)
            update.scan_table(self)
            update.all_tabs(self)
            if row != 0:
                self.scan_table_parameters.setCurrentCell(row-1, 0)
        except:
            self.error_message("Select the variable that needs to be deleted", "No variable selected")

    def number_of_steps_input_changed(self):
        #a check whether the text can be evaluated
        if self.to_update: 
            try:
                expression = self.number_of_steps_input.text()
                (evaluation, for_python, is_scanned) = self.decode_input(expression)
                exec("self.value = " + str(evaluation))
                if isinstance(self.value, int): #check whether it is an integer
                    if self.value > 0: #check whether it is a positive integer
                        self.experiment.number_of_steps = self.value
                    else:
                        self.error_message("Only positive integers larger than 0 are allowed", "Wrong entry")    
                else:
                    self.error_message("Only integer values for number of steps are allowed", "Wrong entry")
            except:
                self.error_message("Expression can not be evaluated", "Wrong entry")
            self.update_off()
            self.number_of_steps_input.setText(str(self.experiment.number_of_steps))
            self.update_on()

    def index_of_a_new_variable(self, name):
        #this function takes a variable name and checks whether it is in a previously human defined variables or not
        #in case it is found returns its index otherwise returns None
        index = None
        for ind, variable in enumerate(self.experiment.new_variables):
            if variable.name == name:
                index = ind
                break
        return index

    def already_scanned(self, name):
        '''Takes a variable name as an input and checks whether there exists a scanned variable with the same name.
            Returns True is case of dublicates and False otherwise'''
        for variable in self.experiment.scanned_variables:
            if variable.name == name:
                return True
        return False

    def scan_table_parameters_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.scan_table_parameters.item(row, col)
            variable = self.experiment.scanned_variables[row]
            if col == 0: #name of the scanned variable changed
                new_variable_name = self.remove_restricted_characters(table_item.text())
                table_item.setText(new_variable_name)
                if self.already_scanned(new_variable_name): #check if the given variable is defined previously or not
                    self.error_message("The variable name you entered was already used for scanning.", "Scanning variable dublicate")
                else: # if entered name does not have dublicates then we proceed on checking whether the varible name is defined in Variables tab
                    index = self.index_of_a_new_variable(new_variable_name)
                    if index != None:
                        prev_index = self.index_of_a_new_variable(variable.name)
                        if prev_index != None: #make the value of variable to the previous before being scanned.
                            #reverting the values to before scanning values and scanning states of the previous variable
                            self.experiment.variables[variable.name].value = self.experiment.new_variables[prev_index].value 
                            self.experiment.variables[variable.name].is_scanned = False 
                            self.experiment.variables[variable.name].for_python = self.experiment.variables[variable.name].value
                            self.experiment.new_variables[prev_index].is_scanned = False
                        #updating the values and scanning states of the new scanning  variable
                        variable.name = new_variable_name
                        self.experiment.variables[variable.name] = self.Variable(variable.name, variable.min_val, variable.min_val, True) #add a new variable with updated name
                        self.experiment.variables[variable.name].for_python = variable.name
                        self.experiment.new_variables[index].is_scanned = True
                    else: # if index == None it means that the variable name entered is not defined in a variables tab
                        self.error_message("The variable name you entered was not defined in variables tab", "Not defined variable")
                        self.update_off()
                        table_item.setText(variable.name)
                        self.update_on()
                self.count_scanned_variables()
            elif col == 1: #min_val of the scanned variable changed
                variable.min_val = float(table_item.text())
                if self.scan_table_parameters.item(row, 0).text() != "None": # this makes sure that we do not have to deal with "None" named variable
                    # we use the min values in order to use in sorting of the sequence tab
                    self.experiment.variables[variable.name].value = float(table_item.text())
            elif col == 2: #max_val of the scanned variable changed
                variable.max_val = float(table_item.text())
            
            update.all_tabs(self)
            update.variables_tab(self)
            update.scan_table(self)       
        else:
            pass

        
    #DIGITAL TAB RELATED
    def update_digital_table_header(self, index, name):
        if "\n" in self.experiment.title_digital_tab[index]:
            self.experiment.title_digital_tab[index] = self.experiment.title_digital_tab[index][0:3] + "\n" + name
        else: # this can be completely removed. Needs a test
            self.experiment.title_digital_tab[index] += "\n" + name
        self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
        self.dialog.accept()


    def digital_table_header_clicked(self, logicalIndex):
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
            button_update.clicked.connect(lambda:self.update_digital_table_header(index, value_input.text()))
            button_cancel.clicked.connect(lambda: self.dialog.reject())
            self.dialog.setWindowTitle("Custom name for the channel") 
            self.dialog.exec_()
        else:
            pass

    #this function checks for inputs whether they are integers or not and also if they are acceptable values (0 and 1) or not
    def digital_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.digital_table.item(row,col)
            channel = self.experiment.sequence[row].digital[col-4]
            if table_item.text() == "":
                if row == 0: #default edge 
                    self.error_message("You can not delete initial value! Only '0' or '1' are expected", "Initial value is needed!")
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                else:
                    #this can be removed as it is done in update.digital_tab(self)
                    self.update_off()
                    table_item.setBackground(self.white)
                    self.update_on()
                    channel.changed = False
                    update.digital_tab(self)
            else:
                try: #Checking whether the expression can be evaluated and the value is within allowed range
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy = " + evaluation)
                    if (self.dummy == 0 or self.dummy == 1):
                        channel.expression = expression
                        channel.evaluation = evaluation
                        channel.value = self.dummy
                        channel.changed = True
                        update.digital_tab(self)
                    else:
                        self.update_off()
                        table_item.setText(channel.expression)
                        self.update_on()
                        self.error_message("!!!Only value '1' or '0' are expected", "Wrong entry")
                except:
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                    self.error_message("Expression can not be evaluated", "Wrong entry")


    #ANALOG TABLE RELATED
    def update_analog_table_header(self, index, name):
        if "\n" in self.experiment.title_analog_tab[index]:
            self.experiment.title_analog_tab[index] = self.experiment.title_analog_tab[index][0:3] + "\n" + name
        else:
            self.experiment.title_analog_tab[index] += "\n" + name
        self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
        self.dialog.accept()


    def analog_table_header_clicked(self, logicalIndex):
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
        if self.to_update:
            row = item.row()
            col = item.column()
            channel = self.experiment.sequence[row].analog[col - 4]
            table_item = self.analog_table.item(row,col)
            if table_item.text() == "":
                if row == 0: # default edge
                    self.error_message("You can not delete initial value! Only values from '-10' to '10' are expected", "Initial value is needed!")
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                else:
                    channel.changed = False
                    #this could be removed as it is being done in the update.analog_tab(self)
                    self.update_off()
                    table_item.setBackground(self.white)
                    self.update_on()
                    update.analog_tab(self)
            else:
                try:
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy =" + evaluation)
                    if (self.dummy <= 10 and self.dummy >= -10):
                        channel.expression = expression
                        channel.evaluation = evaluation
                        channel.value = self.dummy
                        channel.is_scanned = is_scanned
                        channel.for_python = for_python 
                        channel.changed = True
                        update.analog_tab(self)
                    else:
                        self.update_off()
                        table_item.setText(channel.expression)
                        self.update_on()
                        self.error_message("Only values between '+10' and '-10' are expected", "Wrong entry")
                except:
                    self.update_off()
                    table_item.setText(channel.expression)
                    self.update_on()
                    self.error_message('Expression can not be evaluated', 'Wrong entry')

    #DDS TAB RELATED
    def dds_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            edge_num = row - 2
            channel = (col - 4)//6 #4 columns for edge and separation. division by 5 channel settings and 1 separation
            setting = col - 4 - 6 * channel # the number is a sequential value of setting. Frequency is 0, Amplitude 1, attenuation 2, phase 3, state 4
            if self.dds_table.item(row,col).text() == "": #empty entry case (input is "")
                if edge_num == 0:
                    self.error_message("You can not delete initial value!", "Initial value is needed!")
                    self.update_off()
                    exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                else:
                    #Removing background color
                    self.update_off()
                    #this can be removes as it is done in update.dds_tab(self)
                    for index_setting in range(5):
                        self.dds_table.item(row, channel*6 + 4 + index_setting).setBackground(self.white)
                    self.experiment.sequence[edge_num].dds[channel].changed = False
                    self.update_on()
                    update.dds_tab(self)
            else:   #non empty entry case (input is not "")
                try:
                    expression = self.dds_table.item(row,col).text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy_val =" + evaluation)
                    maximum, minimum = self.max_dict[setting], self.min_dict[setting]
                    if (self.dummy_val <= maximum and self.dummy_val >= minimum): 
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.expression = expression" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.evaluation = evaluation" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.value = self.dummy_val" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        self.experiment.sequence[edge_num].dds[channel].changed = True
                        update.dds_tab(self)
                    else:
                        self.error_message("Only values between %f and %f are expected" %(minimum, maximum), "Wrong entry")
                        self.update_off()
                        exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                        self.update_on()
                except:
                    self.update_off()
                    exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                    self.update_on()
                    self.error_message('Expression can not be evaluated', 'Wrong entry')            

    def dds_dummy_header_changed(self, item):
        if self.to_update:
            col = item.column()
            self.experiment.title_dds_tab[(col-4)//6 + 4] = self.dds_dummy_header.item(0,col).text() # title has 3 leading names and a separator

    def find_new_variable_name_unused(self):
        for i in range(1, 1000):
            name = "var_" + str(i)
            if name not in self.experiment.variables:
                return name

    def create_new_variable_clicked(self):
        variable_name = self.find_new_variable_name_unused()
        self.experiment.new_variables.append(self.Variable(variable_name, 0.0, 0.0))
        self.experiment.variables[variable_name] = self.Variable(variable_name, 0.0, 0.0)
        #HERE SHOULD BE UPDATE VARIABLES TABLE
        update.variables_tab(self)

    def decode_input(self, text):
        index = 0
        output_eval = ""
        output_for_python = ""
        current = ""
        is_scanned = False
        while index < len(text):
            if text[index] == "-" or text[index] == "+" or text[index] == "/" or text[index] == "*":
                current.replace(" ", "")
                try: #check if a variable is a float
                    float(current)
                    output_eval += current + text[index]
                    output_for_python += current + text[index]
                except:
                    output_eval += "self.experiment.variables['" + current + "'].value" + text[index]
                    variable = self.experiment.variables[current]
                    if self.experiment.do_scan and variable.is_scanned:#if scanned assign the python form else assign the value
                        is_scanned = True
                        output_for_python += str(self.experiment.variables[current].for_python) + text[index]
                    else:
                        output_for_python += str(variable.value) + text[index]
                current = ""
                index += 1
            if text[index] != " ":
                current += text[index]
            index += 1
        try: #check if a variable is a float
            float(current)
            output_eval += current
            output_for_python += current
        except:
            output_eval += "self.experiment.variables['" + current + "'].value"
            variable = self.experiment.variables[current]
            if self.experiment.do_scan and variable.is_scanned:#if scanned assign the python form else assign the value
                is_scanned = True
                output_for_python += str(self.experiment.variables[current].for_python)
            else:
                output_for_python += str(variable.value)
        try:
            exec("self.temp =" + output_for_python)
            output_for_python = str(self.temp)
        except:
            pass
        return (output_eval, output_for_python, is_scanned) 

    def remove_restricted_characters(self, text):
        to_remove = "~!@#$%^&*()-=/*+.?[]{;}:\|<>` "
        for character in to_remove:
            text = text.replace(character, "")
        return text

    def variables_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            variable = self.experiment.new_variables[row]
            table_item = self.variables_table.item(row,col)
            if col == 0: #variable name was changed
                new_name = self.remove_restricted_characters(table_item.text())
                if new_name[0:2] == "id" and new_name[2] in "0123456789":
                    self.error_message("Variable names starting with id and following with integers are reserved for default edge time variables", "Invalid variable name")
                elif new_name not in self.experiment.variables:
                    not_a_number = True
                    try:
                        float(new_name) #does not allow defining variable names that contains only integers without characters
                        not_a_number = False
                    except:
                        pass
                    if not_a_number: #following block is executed when the name of the variable is kind of a valid one
                        #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                        backup = deepcopy(self.experiment.variables[variable.name])
                        del self.experiment.variables[variable.name]
                        return_value = update.all_tabs(self) # we need to update value. In other words evaluate evaluations. No need to udpage expressions
                        if return_value == None:
                            self.experiment.variables[new_name] = backup
                            self.experiment.variables[new_name].name = new_name
                            self.experiment.variables[new_name].is_scanned = False
                            variable.name = new_name
                        else:
                            self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
                            self.experiment.variables[backup.name] = backup
                            self.update_off()
                            table_item.setText(backup.name)
                            self.update_on()
                    else:
                        self.error_message('Variable name can not be in a form of a number', 'Invalid variable name')
                else:
                    self.error_message('Variable name is already used', 'Invalid variable name')
            elif col == 1: #variable value was changed
                #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                try:
                    self.experiment.variables[variable.name].value = float(table_item.text())
                    return_value = update.all_tabs(self, update_expressions_and_evaluations=False) # we do not need to update expressions only update values.
                    if return_value == None:
                        variable.value = self.experiment.variables[variable.name].value
                    else:
                        self.error_message("Evaluation is out of allowed range occured in %s. Variable value can not be assigned" %return_value, "Wrong entry")
                        self.experiment.variables[variable.name].value = variable.value 
                        self.update_off()
                        table_item.setText(str(variable.value))
                        self.update_on()
                        update.all_tabs(self, update_expressions_and_evaluations=False)
                except:
                    self.error_message("Only integers and floating numbers are allowed.", "Wrong entry")


    def delete_new_variable_clicked(self):
        try:
            row = self.variables_table.selectedIndexes()[0].row()
            name = self.variables_table.item(row,0).text()
            backup = deepcopy(self.experiment.variables[name]) #used to be able to revert the process of deletion
            del self.experiment.variables[name]
            self.variables_table.setCurrentCell(row-1,0)
            return_value = update.all_tabs(self, update_expressions_and_evaluations=False) #we need to update only values not expressions
            if return_value == None:
                del self.experiment.new_variables[row]
                update.variables_tab(self)
            else:
                self.experiment.variables[name] = backup
                update.all_tabs(self) # May be not needed. Check this later
                self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
        except:
            self.error_message("Select the variable that needs to be deleted", "No variable selected")



def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

if __name__ == "__main__":
    run()