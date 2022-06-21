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
import update_sequence_related_tabs as update_tabs
import pickle
import update_expressions_evaluations as update_evaluations
import update_expressions
from datetime import datetime

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    class Edge:
        def __init__(self, name = "", id = 0, expression = 0, evaluation = 0, for_python = 0, value = 0, is_scanned = False):
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

        class Analog:
            #Object is used to describe analog channels' values
            def __init__(self, value = 0, expression = 0, evaluation = 0, changed = False):
                self.value = value
                self.expression = expression
                self.evaluation = evaluation
                self.changed = changed
                self.is_scanned = False

        class Digital:
            #Object is used to describe digital channels' values
            def __init__(self, value = 0, expression = 0, evaluation = 0, changed = False):
                self.value = value
                self.expression = expression
                self.evaluation = evaluation
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
                def __init__(self, value = 0.0, expression = 0.0, evaluation = 0.0, changed = False):
                    self.value = value
                    self.expression = expression
                    self.evaluation = evaluation
                    self.changed = changed   
                    self.is_scanned = False     

    class Experiment:
        def __init__(self):
            self.title_digital_tab = []
            self.title_analog_tab = []
            self.title_dds_tab = []
            self.sequence = None
            self.go_to_edge_num = -1
            self.new_variables = [] #this was decided to be a list in order to display the human defined variables
            self.variables = {}
            self.do_scan = False
            self.file_name = ""
            self.scanned_variables = [] #list of variables involved in a scan

    class Scanned_variable:
        def __init__(self, name, min_val, max_val, step):
            self.name = name
            self.min_val = min_val
            self.max_val = max_val
            self.step = step

    class Variable: # is for every variable human defined and default variables of a form id#
        def __init__(self, name, value, for_python, is_scanned = False):
            self.name = name
            self.value = value
            self.is_scanned = is_scanned
            self.for_python = for_python


    def __init__(self):
        super().__init__()
        #MAIN PAGE LAYOUT
        self.setWindowTitle("Experimental control application. Hosten Group")
        self.main_window = QTabWidget()
        self.setCentralWidget(self.main_window)
        self.setGeometry(0,0,1920,1200)
        
        declare_global_var.build(self)
        tabs.sequence_tab_build(self)
        tabs.digital_tab_build(self)
        tabs.analog_tab_build(self)
        tabs.dds_tab_build(self)
        tabs.variables_tab_build(self)
        
        
        #ADDING TABS TO MAIN WINDOW
        self.main_window.addTab(self.sequence_tab_widget, "Main")
        self.main_window.addTab(self.digital_tab_widget, "Digital")
        self.main_window.addTab(self.analog_tab_widget, "Analog")
        self.main_window.addTab(self.dds_tab_widget, "DDS")
        self.main_window.addTab(self.variables_tab_widget, "Variables")
        update_evaluations.do(self)
        update_tabs.do(self)
        


    #FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS
    #GENERAL FUNCTIONS

    def setColorCol(self, col):
        #this function takes the column number and first megres all columns and then paints its background
        #it is used for separating DDS channels but can be employed elsewhere is needed
        self.dds_table.setSpan(0, col, self.sequence_num_rows+2, 1)
        self.dds_table.setItem(0,col, QTableWidgetItem())
        self.dds_table.item(0, col).setBackground(QColor(100,100,100))


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

    def some_dummy_function():
        print("You called a dummy function")
        print("this one was added from PC")
        

    #SEQUENCE TAB RELATED
    def sequence_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            edge = self.experiment.sequence[row]
            table_item = self.sequence_table.item(row,col)
            if col == 3:
                if table_item.text() == "":
                    if row == 0:
                        self.error_message("You can not delete initial value! Only '0' or '1' are expected", "Initial value is needed!")
                        self.update_off()
                        table_item.setText(str(edge.expression))
                        self.update_on()
                    else:
                        self.update_off()
                        edge.expression = self.experiment.sequence[row-1].expression#previous edge
                        self.update_on()
                else:                        
                    try:
                        edge.expression = table_item.text()
                        (evaluation, for_python, is_scanned) = self.decode_input(edge.expression)
                        exec("self.value = " + str(edge.evaluation)) # this is done here to be able to assign value of the id# type variable
                        edge.evaluation = evaluation
                        edge.is_scanned = is_scanned
                        if edge.is_scanned:
                            edge.for_python = for_python
                        else:
                            exec("edge.for_python = " + for_python)
                        edge.value = self.value
                        variable_name = "id" + str(edge.id)
                        self.experiment.variables[variable_name] = self.Variable(name = variable_name, value = edge.value, for_python = edge.for_python, is_scanned = edge.is_scanned)
                    except:
                        self.error_message("Expression can not be evaluated", "Wrong entry")
            elif col == 1:           
                edge.name = table_item.text()
            update_evaluations.do(self)
            update_tabs.do(self)
        else:
            pass

    
    def save_sequence_button_clicked(self):
        if self.experiment.file_name == "":
            self.experiment.file_name = QFileDialog.getSaveFileName(self, 'Save File')[0]
            if self.experiment.file_name != "": #happens when no file name was given (canceled)
                try:
                    with open(self.experiment.file_name, 'wb') as file:
                        pickle.dump(self.experiment, file)
                    self.create_file_name_label()
                    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Sequence saved at %s" %self.experiment.file_name)
                except:
                    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Saving attempt was not successful")                
        else:
            with open(self.experiment.file_name, 'wb') as file:
                pickle.dump(self.experiment, file)
            self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Sequence saved at %s" %self.experiment.file_name)


    def load_sequence_button_clicked(self):
        self.experiment.file_name = QFileDialog.getOpenFileName(self, "Open File")[0]
        if self.experiment.file_name != "": #happens when no file name was given (canceled)
            try:
                with open(self.experiment.file_name, 'rb') as file:
                    self.experiment = pickle.load(file)
                self.sequence_num_rows = len(self.experiment.sequence)
                self.sequence = self.experiment.sequence
                self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
                self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
                #update the label showing the sequence that is being modified 
                self.create_file_name_label()
                #update the drop_down menu
                self.update_off()
                self.scan_drop_down.clear()
                self.scan_drop_down.addItem("None")
                for variable in self.experiment.new_variables:
                    self.scan_drop_down.addItem(variable.name)
                self.update_on()
                self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Sequence loaded from %s" %self.experiment.file_name)
            except:
                self.error_message('Could not load the file', 'Error')
            update_evaluations.do(self)
            update_tabs.do(self)

    def create_file_name_label(self):
        self.file_name_lable.setText(self.experiment.file_name)


    def find_unique_id(self):
        #this functions finds the smallest possible id number that is not used and returns it
        for id in range(10**4):
            dummy_name = "id" + str(id)
            if dummy_name not in self.experiment.variables:
                return id

        

    def insert_edge_button_clicked(self):   
        new_unique_id = self.find_unique_id()
        edge = self.experiment.sequence[-1] #I know that on line below and 3 lines below edge is edge is not the same as after appending edge still has the previous last edge (one before the last). But since they have the same values for simplicity I left it like this
        self.experiment.sequence.append(self.Edge("", id = new_unique_id, expression = edge.expression, evaluation = edge.evaluation, for_python = edge.for_python, value = edge.value))
        name = "id" + str(new_unique_id)
        self.experiment.variables[name] = self.Variable(name = name, value = edge.value, for_python = edge.for_python)
        update_evaluations.do(self)
        update_tabs.do(self)

    def delete_edge_button_clicked(self):
        try:
            row = self.sequence_table.selectedIndexes()[0].row()
            name = 'id' + str(self.experiment.sequence[row].id)
            if row == 0:
                self.error_message("You can not delete the starting edge", "Protected item")
            else:

                temp_value = self.experiment.variables[name].value #temp is used if we are not able to evaluate expressions and need to reassign the variable
                # here is change the value to something that can not be evaluated to see whether id# variable was used in any expression
                # if it is used, obviously some expressions can not be evaluated and I reassign the previous value using temp_value. Otherwise the return value of 
                # update_evaluations.do(self) will be None and I will delete the edge and corresponding id# variable
                self.experiment.variables[name].value = "something_that_can_not_be_evaluated"
                return_value = update_evaluations.do(self)
                if return_value == None:
                    del self.experiment.sequence[row]
                    del self.experiment.variables[name]
                    self.sequence_table.setCurrentCell(row-1, 0)
                    update_tabs.do(self)
                else:
                    self.experiment.variables[name].value = temp_value
                    update_evaluations.do(self)
                    self.error_message('The edge time value is used as a variable in %s.'%return_value, 'Can not delete used edge')
        except:
            self.error_message("Select the edge you want to delete", "No edge selected")


    def go_to_edge_button_clicked(self):
        try:
            edge_num = self.sequence_table.selectedIndexes()[0].row()
            self.experiment.go_to_edge_num = edge_num
            write_to_python.create_go_to_edge(self)
            self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Go to edge file generated")
            try:
                os.system("conda activate artiq_5 && artiq_run go_to_edge.py") 
                self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Went to edge")
            except:
                self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Went to edge")    
            update_tabs.do(self)
        except:
            self.error_message("Chose the edge you want the system to go","No edge selected")


    def run_experiment_button_clicked(self):
        #os.system('. /home/hostengroup/anaconda3/etc/profile.d/conda.sh; conda activate artiq; artiq_run new_first.py') this was useful for linux based computers
        try:
#            if self.experiment.do_scan:
#                min_value = float(self.scan_table_parameters.item(0,1).text())
#                max_value = float(self.scan_table_parameters.item(0,2).text())
#                step_value = int(self.scan_table_parameters.item(0,3).text())
#                var_name = self.scan_drop_down.currentText()
#                scan_iterable = np.linspace(min_value, max_value, step_value)
#                for value in scan_iterable:
#                    print("performing the scan of %s at value %f" %(var_name, value))
#                    self.experiment.variables[var_name] = value
#                    update_evaluations.do(self)
            file_name = write_to_python.create_experiment(self)
            os.system("conda activate artiq_5 && artiq_run %s" %file_name)        


#            else:
#                file_name = write_to_python.create_experiment(self)
#                self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Python file generated")
#                try:
#                    os.system("conda activate artiq_5 && artiq_run %s" %file_name)    
#                    if self.experiment.go_to_edge_num != -1: #undoing highlighting of the edge
#                        self.experiment.go_to_edge_num = -1 
#                        update_tabs.do(self)
#                    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Experiment started")
#                except:
#                    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Was not able to start experiment")
        except:
            self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Was not able to generate python file")

    def dummy_button_clicked(self):
        #print("new variables")
        #for item in self.experiment.new_variables:
        #    print("NAME: ", item.name, "VALUE", item.value)
        print("variables", self.experiment.variables)
        for key, item in self.experiment.variables.items():
            print("NAME", item.name, "VALUE", item.value, "PYTHON", item.for_python, "SCANNED", item.is_scanned)

        print("TIME")
        for item in self.experiment.sequence:
            print("name", item.name)
            print("value", item.value)
            print("evaluation", item.evaluation)
            print("for python", item.for_python)
        print()
        print()
        print()



    #the button is used to clear the logger         
    def clear_logger_button_clicked(self):
        self.logger.clear()

    def scan_table_parameters_changed(self, item):
        row = item.row()
        col = item.column()
        table_item = self.scan_table_parameters.item(row, col)
        if col == 0:
            pass
        elif col == 1:
            self.experiment.scanned_variables[row].min_val = float(table_item.text())
            for item in self.experiment.new_variables:
                if item.name == self.scan_drop_down.currentText():
                    item.value = self.experiment.scanned_variables[row].min_val #quick fix for updating the scanned variable value for sorting in time sequence
        elif col == 2:    
            self.experiment.scanned_variables[row].max_val = float(table_item.text())
        elif col == 3:    
            self.experiment.scanned_variables[row].step = float(table_item.text())
        update_evaluations.do(self)
        update_tabs.do(self)        
       

    #DIGITAL TAB RELATED
    def update_digital_table_header(self, index, name):
        if "\n" in self.experiment.title_digital_tab[index]:
            self.experiment.title_digital_tab[index] = self.experiment.title_digital_tab[index][0:3] + "\n" + name
        else:
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

    #this function checks for inputs whether they are integers or not and also if they are acceptable values (0 and 1) or not
    def digital_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            table_item = self.digital_table.item(row,col)
            channel = self.experiment.sequence[row].digital[col-4]
            if table_item.text() == "":
                if row == 0:
                    self.error_message("You can not delete initial value! Only '0' or '1' are expected", "Initial value is needed!")
                    self.update_off()
                    try:
                        table_item.setText(channel.expression)
                    except:
                        table_item.setText("")
                    self.update_on()
                else:
                    try:
                        channel.expression = self.experiment.sequence[row-1].digital[col-4].expression
                        channel.evaluation = self.experiment.sequence[row-1].digital[col-4].evaluation
                        channel.changed = False
                    except:
                        pass
            else:
                try:
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy = " + evaluation)
                    if (self.dummy == 0 or self.dummy == 1):
                        channel.expression = expression
                        channel.evaluation = evaluation
                        channel.value = int(self.dummy)
                        channel.is_scanned = is_scanned
                        if channel.is_scanned:
                            channel.for_python = for_python
                        else:
                            exec("channel.for_python =" + for_python)
                        channel.changed = True
                    else:
                        self.error_message("!!!Only value '1' or '0' are expected", "Wrong entry")
                except:
                    self.error_message("Expression can not be evaluated", "Wrong entry")
            update_tabs.do(self)
            update_expressions.do(self)


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
            channel = self.experiment.sequence[row].analog[channel]
            table_item = self.analog_table.item(row,col)
            if table_item.text() == "":
                if row == 0:
                    self.error_message("You can not delete initial value! Only values from '-10' to '10' are expected", "Initial value is needed!")
                    self.update_off()
                    try:
                        table_item.setText(channel.expression)
                    except: 
                        table_item.setText("")
                    self.update_on()
                else:
                    try:
                        channel.expression = self.experiment.sequence[row-1].analog[col-4].expression
                        channel.evaluation = self.experiment.sequence[row-1].analog[col-4].evaluation
                        channel.changed = False
                    except:
                        pass
            else:
                try:
                    expression = table_item.text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy_val =" + evaluation)
                    if (self.dummy_val <= 10 and self.dummy_val >= -10):
                        channel.expression = expression
                        channel.evaluation = evaluation
                        channel.is_scanned = is_scanned
                        if channel.is_scanned:
                            channel.for_python = for_python
                        else:
                            exec("channel.for_python =" + for_python)
                        channel.value = self.dummy_val
                        channel.changed = True
                    else:
                        self.error_message("Only values between '+10' and '-10' are expected", "Wrong entry")
                        self.update_off()
                        table_item.setText(channel.expression)
                        self.update_on()
                except:
                    self.error_message('Expression can not be evaluated', 'Wrong entry')

            update_tabs.do(self)
            update_expressions.do(self)

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
                    exec("self.dds_table.item(row,col).setText(self.experiment.sequence[edge_num].dds[channel].%s" %self.setting_dict[setting])
                    self.update_on()
                else:
                    self.experiment.sequence[edge_num].dds[channel].changed = False
            else:   #non empty entry case (input is not "")
                try:
                    expression = self.dds_table.item(row,col).text()
                    (evaluation, for_python, is_scanned) = self.decode_input(expression)
                    exec("self.dummy_val =" + evaluation)
                    maximum, minimum = self.max_dict[setting], self.min_dict[setting]
                    if (self.dummy_val <= maximum and self.dummy_val >= minimum): 
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.expression = expression" %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.evaluation = evaluation" %self.setting_dict[setting])
                        if is_scanned:
                            exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = for_python" %self.setting_dict[setting])
                        else:
                            exec("self.experiment.sequence[edge_num].dds[channel].%s.for_python = " + for_python %self.setting_dict[setting])
                        exec("self.experiment.sequence[edge_num].dds[channel].%s.value = self.dummy_val" %self.setting_dict[setting])
                        self.experiment.sequence[edge_num].dds[channel].changed = True
                    else:
                        self.error_message("Only values between %f and %f are expected" %(minimum, maximum), "Wrong entry")
                        self.update_off()
                        exec("self.dds_table.item(row,col).setText(str(self.experiment.sequence[edge_num].dds[channel].%s.expression))" %self.setting_dict[setting])
                        self.update_on()
                except:
                    self.error_message('Expression can not be evaluated', 'Wrong entry')            
            update_tabs.do(self)
            update_expressions.do(self)

    def dds_dummy_header_changed(self, item):
        if self.to_update:
            col = item.column()
            self.experiment.title_dds_tab[(col-4)//6 + 4] = self.dds_dummy_header.item(0,col).text() # title has 3 leading names
            update_tabs.do(self)

    def find_new_variable_name_unused(self):
        for i in range(1, 1000):
            name = "var_" + str(i)
            if name not in self.experiment.variables:
                return name

    def create_new_variable_clicked(self):
        variable_name = self.find_new_variable_name_unused()
        self.experiment.new_variables.append(self.Variable(variable_name, 0.0, 0.0))
        self.experiment.variables[variable_name] = self.Variable(variable_name, 0.0, 0.0)
        #update the drop-down menu for scanning
        self.scan_drop_down.addItem(variable_name)
        update_tabs.do(self)

    def remove_restricted_characters(self, text):
        to_remove = "~!@#$%^&*()-=/*+.?[]{;}:\|<>` "
        for character in to_remove:
            text = text.replace(character, "")
        return text


    def decode_input(self, text):
        print("decoding", text)
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
                    print(variable.name, variable.value, variable.is_scanned)
                    if variable.is_scanned:#if scanned assign the python form else assign the value
                        is_scanned = True
                        output_for_python += str(self.experiment.variables[current].for_python) + text[index]
                        print("HEY THERE", output_for_python)
                    else:
                        output_for_python += str(variable.value) + text[index]
                        print("hello", output_for_python)

                current = ""
                index += 1
            if text[index] != " ":
                current += text[index]
            index += 1
            if output_eval:
                print("output", output_eval, output_for_python)
        try: #check if a variable is a float
            float(current)
            output_eval += current
            output_for_python += current
        except:
            output_eval += "self.experiment.variables['" + current + "'].value"
            variable = self.experiment.variables[current]
            if variable.is_scanned:#if scanned assign the python form else assign the value
                is_scanned = True
                output_for_python += str(self.experiment.variables[current].for_python)
                #output_for_python += "self.experiment.variables['" + current + "'].for_python"
                print("HEY THERE", output_for_python)
            else:
                output_for_python += str(variable.value)
                print("hello", output_for_python)
            if output_eval:
                print("output", output_eval, output_for_python)
        print("FINAL", output_eval, output_for_python)
        return (output_eval, output_for_python, is_scanned) 

    def variables_table_changed(self, item):
        if self.to_update:
            row = item.row()
            col = item.column()
            variable = self.experiment.new_variables[row]
            table_item = self.variables_table.item(row,col)
            if col == 0: #variable name was changed
                dummy_name = self.remove_restricted_characters(table_item.text())
                if dummy_name[0:2] == "id" and dummy_name[2] in "0123456789":
                    self.error_message("Variable names starting with id and following with integers are reserved for default edge time variables", "Invalid variable name")
                elif dummy_name not in self.experiment.variables:
                    not_a_number = True
                    try:
                        float(dummy_name) #does not allow defining variable names that contains only integers without characters
                        not_a_number = False
                    except:
                        pass
                    if not_a_number: #following block is executed when the name of the variable is kind of a valid one
                        #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                        self.experiment.variables[variable.name].value = "something_that_can_not_be_evaluated"
                        return_value = update_evaluations.do(self)
                        if return_value != None:
                            self.experiment.variables[variable.name].value = variable.value
                            update_evaluations.do(self)
                            self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
                        else:
                            new_variable = self.Variable(name = dummy_name, value = variable.value, for_python = variable.for_python, is_scanned=False)
                            del self.experiment.variables[variable.name]
                            self.experiment.variables[dummy_name] = new_variable
                            variable.name = dummy_name
                            #update drop-down menu for scanning
                            self.scan_drop_down.setItemText(row + 1, dummy_name) #plus one because of None being the first element
                    else:
                        self.error_message('Variable name can not be in a form of a number', 'Invalid variable name')
                else:
                    self.error_message('Variable name is already used', 'Invalid variable name')
            elif col == 1: #variable value was changed
                #variable.value is used as a back up if evaluation is not possible since we do not change self.experiment.new_variables to check if the variable is used or not
                self.experiment.variables[variable.name].value = float(table_item.text())
                return_value = update_evaluations.do(self)
                if return_value != None:
                    self.error_message("Evaluation is out of allowed range occured in %s. Variable value can not be assigned" %return_value, "Wrong entry")
                    self.experiment.variables[variable.name].value = variable.value 
                else:
                    variable.value = self.experiment.variables[variable.name].value
            update_expressions.do(self)
            update_evaluations.do(self)
            update_tabs.do(self)

    def delete_new_variable_clicked(self):
        row_selected = True
        try:
            row = self.variables_table.selectedIndexes()[0].row()
            name = self.variables_table.item(row,0).text()
            temp = self.experiment.variables[name] #used to be able to revert the process of deletion
            del self.experiment.variables[name]
            self.variables_table.setCurrentCell(row-1,0)
            return_value = update_evaluations.do(self)
            if return_value == None:
                del self.experiment.new_variables[row]
                #update drop-down menu for scanning
                self.scan_drop_down.removeItem(row + 1) #plus one because of None being the first element
                update_tabs.do(self)
            else:
                self.experiment.variables[name] = temp
                update_evaluations.do(self)
                self.error_message('The variable is used in %s.'%return_value, 'Can not delete used variable')
        except:
            self.error_message("Select the variable that needs to be deleted", "No variable selected")
            
    def scan_table_activated(self):
        self.experiment.do_scan = self.scan_table.isChecked()

    def scan_drop_down_changed(self):
        if self.to_update:
            #making all variables not scanned in case of reassignment of a scanned variable
            for item in self.experiment.new_variables:
                item.is_scanned = False
            self.experiment.scanned_variables = []
            #assigning new scanned variable
            for item in self.experiment.new_variables:
                if item.name == self.scan_drop_down.currentText():
                    self.experiment.variables[item.name].is_scanned = True
                    self.experiment.scanned_variables.append(self.Scanned_variable(item.name, 0,0,0))
                    #item.value = float(self.scan_table_parameters.item(0, 1).text()) we do not change the value of new_variable and will use that when we turn off the scan
                    self.experiment.variables[item.name].value = item.value
                    self.experiment.variables[item.name].for_python = item.name
            update_expressions.do(self)

        
def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

run()