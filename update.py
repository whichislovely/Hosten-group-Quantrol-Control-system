from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import config

def sequence_tab(self):
    self.update_off()
    #Update expressions and evaluations   
    something_changed = True
    iterations = 0 
    iterations_limit = 100 #after the maximum number of iterations it will throw a warning message
    #this while loop is done to accomodate all mutual dependencies. It may happen that user will crash the program by introducing closed loops.
    while something_changed and iterations < iterations_limit:
        iterations += 1
        something_changed = False    
        for row, edge in enumerate(self.experiment.sequence):
            expression = self.sequence_table.item(row,3).text()
            try:
                (edge.evaluation, edge.for_python, edge.is_scanned) = self.decode_input(expression)
                if edge.id in self.experiment.variables: # in case of deleting an edge there is no self.experiment.variables[edge.id] since we delete it in oder to check whether it has been used anywhere or not
                    if self.experiment.variables[edge.id].is_scanned != edge.is_scanned or self.experiment.variables[edge.id].for_python != edge.for_python:
                        something_changed = True
                        self.experiment.variables[edge.id].is_scanned = edge.is_scanned
                        self.experiment.variables[edge.id].for_python = edge.for_python
            except:
                return "sequence table col 3, edge %d" %row
    #Update values
    #this while loop is done to accomodate all mutual dependencies. It may happen that user will crash the program by introducing closed loops.
    something_changed = True
    iterations = 0 
    iterations_limit = 100 #after the maximum number of iterations it will throw a warning message
    while something_changed and iterations < iterations_limit:
        iterations += 1
        something_changed = False
        for edge_index, edge in enumerate(self.experiment.sequence):
            #UPDATING EDGE VALUES (TIME)
            try:
                exec("edge.value = " + str(edge.evaluation))
                #check if any value has been changed
                if edge.id in self.experiment.variables and self.experiment.variables[edge.id].value != edge.value:
                    something_changed = True
                    self.experiment.variables[edge.id].value = edge.value
            except:
                return "time expression edge number %d"%edge_index
  
    self.experiment.sequence = sorted(self.experiment.sequence, key = lambda edge: edge.value)
    if iterations == iterations_limit:
        self.error_message("100 Iterations exceeded. Please check for potential loops when the time edge depends on itself.", "Warning!")
    #Update table
    for row, edge in enumerate(self.experiment.sequence):
        self.sequence_table.item(row, 1).setText(edge.name)
        self.sequence_table.item(row, 3).setText(edge.expression)
        self.sequence_table.item(row, 4).setText(str(edge.value))
    self.update_on()


def digital_tab(self, update_expressions_and_evaluations = True, update_values_and_table = True):
    self.update_off()
    #note that in order to display numbers you first need to convert them to string
    for channel_index in range(config.digital_channels_number):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].digital[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            table_item = self.digital_table.item(row,col)
            if channel.changed: #Channel state needs to be updated
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = table_item.text()
                    try:
                        (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(channel.expression)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                #Updating values and table
                if update_values_and_table:
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                    #Color coding the values
                    if channel.value == 1:
                        table_item.setBackground(self.green)
                    elif channel.value == 0:
                        table_item.setBackground(self.red)
                    else: # the value is out of the allowed range
                        return "digital channel %d, edge %d" %(channel_index, row)
                    table_item.setToolTip(str(channel.value))
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else: #Update the value according to the previously set state
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values and table entries
                if update_values_and_table:
                    channel.value = int(current_value)
                    table_item.setText(channel.expression + " ") # Updating digital table entries 
                    table_item.setToolTip(str(channel.value))
                #Color coding the values
                table_item.setBackground(self.white)   
                                 
    self.update_on()

def analog_tab(self, update_expressions_and_evaluations = True, update_values_and_table = True):
    '''
    This function updates expressions, evaluations, values and entries of analog table
    Used in analog_table_changed()
    '''
    self.update_off()
    #note that in order to display numbers you first need to convert them to string
    for channel_index in range(config.analog_channels_number):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].analog[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            table_item = self.analog_table.item(row,col)
            if channel.changed: #Channel state needs to be updated
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = table_item.text()
                    #If a number is convertible to float display only up to first 6 digits (micro volt level)
                    try:
                        channel.expression = str(int(float(channel.expression) * 1000000)/1000000)
                    except:
                        pass
                    try:
                        (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(channel.expression)
                    except:
                        return "analog channel %d, edge %d" %(channel_index, row)
                #Updating values and table
                if update_values_and_table:
                    #Check if the expression can be evaluated
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "analog channel %d, edge %d" %(channel_index, row)
                    #Color coding the values
                    if channel.value >= -9.9 and channel.value <= 9.9:
                        if channel.value != 0:
                            table_item.setBackground(self.green)
                        else:
                            table_item.setBackground(self.red)
                    else:
                        return "analog channel %d, edge %d" %(channel_index, row)
                    table_item.setText(channel.expression)
                    table_item.setToolTip(str(channel.value))
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else: #Update the value according to the previously set state
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values
                if update_values_and_table:
                    channel.value = current_value     
                    table_item.setText(current_expression + " ")  # Updating analog table entries                       
                    table_item.setToolTip(str(channel.value))
                #Color coding the values
                table_item.setBackground(self.white)                       

    self.update_on()

def dds_tab(self, update_expressions_and_evaluations = True, update_values_and_table = True):
    '''
    This function updates expressions, evaluations, values and entries of dds table
    Used in dds_table_changed()
    '''
    self.update_off()
    #note that in order to display numbers you first need to convert them to string
    for channel_index in range(config.dds_channels_number):
        for setting in range(4,-1,-1): #start an update from the state of the channel to properly update the color coding
            for row in range(2, self.sequence_num_rows+2): # plus 2 because of 2 rows used for title
                channel = self.experiment.sequence[row-2].dds[channel_index]
                # plus 4 is because first 4 columns are used by number, name, time of edge and separator and times 6 is becuase each channel has 5 columns and 1 separator
                col = channel_index * 6 + 4 + setting
                table_item = self.dds_table.item(row, col)
                exec("self.channel_entry = channel.%s" %self.setting_dict[setting])
                channel_entry = self.channel_entry
                if channel.changed: #Channel state needs to be updated
                    #Updating expressions and evaluations
                    if update_expressions_and_evaluations:
                        channel_entry.expression = table_item.text()
                        #If a value is convertible to float perform the conversion as Artiq parameters for dds channel are required to be floats not integers
                        try:
                            if setting == 0: #frequency
                                channel_entry.expression = str(float(channel_entry.expression)) #Was checked to have at least a 1 Hz level resolution
                            elif setting == 1: #amplitude
                                channel_entry.expression = str(int(float(channel_entry.expression)*1000)/1000) # Keep only up to 3rd digit (0.1234 --> 0.123)
                            elif setting == 2: #attenuation
                                channel_entry.expression = str(round(float(channel_entry.expression)/0.5)*0.5) #Round up to 0.5
                            elif setting == 3: #phase
                                channel_entry.expression = str(round(float(channel_entry.expression)/0.36)*0.36) # Keep only up to 3rd digit (0.1234 --> 0.123) of phase that is represented as 1 -- > 360. 0.001 --> 0.36 in degrees 
                            elif setting == 4: #state
                                channel_entry.expression = str(int(channel_entry.expression))
                        except:
                            pass
                        try:
                            (channel_entry.evaluation, channel_entry.for_python, channel_entry.is_scanned) = self.decode_input(channel_entry.expression)
                        except:
                            return "dds channel %d, edge %d" %(channel_index, row)
                    #Updating values and table entries
                    if update_values_and_table:
                        try:
                            exec("channel_entry.value =" + channel_entry.evaluation)
                        except:
                            return "dds channel %d, edge %d" %(channel_index, row)
                        #check if the value within allowed range
                        if channel_entry.value >= self.min_dict[setting] and channel_entry.value <= self.max_dict[setting]:
                            #Color coding the values
                            if channel.state.value == 1:
                                table_item.setBackground(self.green)
                            else:
                                table_item.setBackground(self.red)
                            #Updating the entry of table to convert to float or integer. (Only state is being converted to integer)
                            table_item.setText(channel_entry.expression)
                            table_item.setToolTip(str(channel_entry.value))
                        else:
                            return "dds channel %d, edge %d" %(channel_index, row)
                    #Saving the current state of the channel
                    current_expression = channel_entry.expression
                    current_evaluation = channel_entry.evaluation
                    current_value = channel_entry.value
                    current_for_python = channel_entry.for_python
                else: #Update the value according to the previously set state
                    #Updating expressions and evaluations
                    if update_expressions_and_evaluations:
                        channel_entry.expression = current_expression
                        channel_entry.evaluation = current_evaluation
                        channel_entry.for_python = current_for_python
                    #Updating dds table values and table entries
                    if update_values_and_table:
                        channel_entry.value = current_value
                        table_item.setText(current_expression + " ")  
                        table_item.setToolTip(str(channel_entry.value))
                        

    self.update_on()

def variables_tab(self):
    #creating the variables tab from self.experiment.new_variables object
    self.update_off()
    self.variables_table_row_count = len(self.experiment.new_variables)
    self.variables_table.setRowCount(self.variables_table_row_count)
    for row, variable in enumerate(self.experiment.new_variables):
        self.variables_table.setItem(row, 0, QTableWidgetItem(variable.name))
        if self.experiment.do_scan and variable.is_scanned:
            item = QTableWidgetItem("scanned")
            item.setFlags(Qt.NoItemFlags)
            self.variables_table.setItem(row, 1, item) 
        else:
            self.variables_table.setItem(row, 1, QTableWidgetItem(str(variable.value)))  
    self.update_on()

def scan_table(self):
    self.update_off()
    self.scan_table_parameters.setRowCount(len(self.experiment.scanned_variables))
    self.number_of_steps_input.setText(str(self.experiment.number_of_steps))
    for row, variable in enumerate(self.experiment.scanned_variables):
        self.scan_table_parameters.setItem(row,0, QTableWidgetItem(str(variable.name)))
        self.scan_table_parameters.setItem(row,1, QTableWidgetItem(str(variable.min_val)))
        self.scan_table_parameters.setItem(row,2, QTableWidgetItem(str(variable.max_val)))
    self.update_on()


def all_tabs(self, update_expressions_and_evaluations = True, update_values_and_tables = True):
    '''
    This function updates all tabs. It just calls an update of each tab one by one
    '''
    sequence_tab_return = sequence_tab(self)
    if (sequence_tab_return==None):
        digital_tab_return = digital_tab(self, update_expressions_and_evaluations, update_values_and_tables)
        if (digital_tab_return==None):
            analog_tab_return = analog_tab(self, update_expressions_and_evaluations, update_values_and_tables)
            if (analog_tab_return==None):
                dds_tab_return = dds_tab(self, update_expressions_and_evaluations, update_values_and_tables)        
                self.update_on()
                return dds_tab_return
            else:
                self.update_on()
                return analog_tab_return
        else:
            self.update_on()
            return digital_tab_return    
    else:
        variables_tab(self)
        self.update_on()
        return sequence_tab_return                

def from_object(self):
    '''
    This function rebuilds all tabs by looking at the self.experiment object
    It reassigns title names, refills every table
    It is used in the following functions:
        1) sequence_table_changed : requires rebuilding tables, reassigning of the title names is redundant
        2) load_sequence_button_clicked : when a new sequence is loaded everything should be built again
        3) delete_edge_button_clicked : after an edge has been deleted we need to rebuild the table
    Development : one can make a flag based rebuild of title names
    '''
    self.sequence_num_rows = len(self.experiment.sequence)
    self.update_off()
    #Setting the row count for each table
    self.sequence_table.setRowCount(self.sequence_num_rows)                     
    self.digital_table.setRowCount(self.sequence_num_rows)
    self.digital_dummy.setRowCount(self.sequence_num_rows)
    self.analog_table.setRowCount(self.sequence_num_rows)
    self.analog_dummy.setRowCount(self.sequence_num_rows)
    self.dds_table.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
    self.dds_dummy.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
    #Separator
    self.making_separator()
    #Update titles
    self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
    self.digital_dummy.setHorizontalHeaderLabels(self.experiment.title_digital_tab[0:3])
    self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
    self.analog_dummy.setHorizontalHeaderLabels(self.experiment.title_analog_tab[0:3])
    for i in range(config.dds_channels_number):
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.dds_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

    if config.allow_skipping_images:
        #Updating the "Skip images" button color
        if self.experiment.skip_images == False:
            self.skip_images_button.setStyleSheet("background-color : red; color : white")
        else:
            self.skip_images_button.setStyleSheet("background-color : green; color : white")

    #Populating the table
    for row, edge in enumerate(self.experiment.sequence):
        #displaying edge names and times        
        self.sequence_table.setItem(row,0, QTableWidgetItem(str(row)))
        self.sequence_table.setItem(row,1, QTableWidgetItem(edge.name))
        self.sequence_table.setItem(row,2, QTableWidgetItem(edge.id))
        self.sequence_table.setItem(row,3, QTableWidgetItem(edge.expression))
        self.sequence_table.setItem(row,4, QTableWidgetItem(str(edge.value)))

        self.digital_dummy.setItem(row,0, QTableWidgetItem(str(row)))
        self.digital_dummy.setItem(row,1, QTableWidgetItem(edge.name))
        self.digital_dummy.setItem(row,2, QTableWidgetItem(str(edge.value)))

        self.analog_dummy.setItem(row,0, QTableWidgetItem(str(row)))
        self.analog_dummy.setItem(row,1, QTableWidgetItem(edge.name))
        self.analog_dummy.setItem(row,2, QTableWidgetItem(str(edge.value)))

        self.dds_dummy.setItem(row+2,0, QTableWidgetItem(str(row)))
        self.dds_dummy.setItem(row+2,1, QTableWidgetItem(edge.name))
        self.dds_dummy.setItem(row+2,2, QTableWidgetItem(str(edge.value)))        
    #displaying digital channels
    for channel_index in range(config.digital_channels_number):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].digital[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            if channel.changed:
                self.digital_table.setItem(row, col, QTableWidgetItem(channel.expression))
                if channel.value == 1:
                    self.digital_table.item(row,col).setBackground(self.green)
                else:
                    self.digital_table.item(row,col).setBackground(self.red)
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else:
                self.digital_table.setItem(row, col, QTableWidgetItem(current_expression + " "))
                channel.expression = current_expression
                channel.evaluation = current_evaluation
                channel.for_python = current_for_python
                channel.value = current_value  
    #displaying analog channels
    for channel_index in range(config.analog_channels_number):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].analog[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            if channel.changed:
                self.analog_table.setItem(row, col, QTableWidgetItem(channel.expression))
                if channel.value == 0:
                    self.analog_table.item(row,col).setBackground(self.red)
                else:
                    self.analog_table.item(row,col).setBackground(self.green)
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else:
                self.analog_table.setItem(row, col, QTableWidgetItem(current_expression + " "))
                channel.expression = current_expression
                channel.evaluation = current_evaluation
                channel.for_python = current_for_python
                channel.value = current_value 
    #displaying dds channels
    for channel_index in range(config.dds_channels_number):
        for setting in range(5):
            for row in range(2, self.sequence_num_rows+2): # plus 2 because of 2 rows used for title
                channel = self.experiment.sequence[row-2].dds[channel_index]
                # plus 4 is because first 4 columns are used by number, name, time of edge and separator and times 6 is becuase each channel has 5 columns and 1 separator
                col = channel_index * 6 + 4 + setting
                exec("self.channel_entry = channel.%s" %self.setting_dict[setting])
                channel_entry = self.channel_entry
                if channel.changed: 
                    self.dds_table.setItem(row, col, QTableWidgetItem(channel_entry.expression))
                    if channel.state.value == 1:
                        self.dds_table.item(row, col).setBackground(self.green)
                    else:
                        self.dds_table.item(row, col).setBackground(self.red)
                    current_expression = channel_entry.expression
                    current_evaluation = channel_entry.evaluation
                    current_value = channel_entry.value
                    current_for_python = channel_entry.for_python
                else:
                    self.dds_table.setItem(row, col, QTableWidgetItem(channel_entry.expression + " "))
                    channel_entry.expression = current_expression
                    channel_entry.evaluation = current_evaluation
                    channel_entry.for_python = current_for_python
                    channel_entry.value = current_value
    #building variables table from the self.experiment.new_variables array
    variables_tab(self)
    # building scanned variables table from the self.experiment.scanned_variables array
    scan_table(self)
    self.update_on()                  