from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def sequence_tab(self):
    self.update_off()
    #Update values
    #this while loop is done to accomodate all mutual dependencies. It may happen that user will crash the program by introducing closed loops.
    something_changed = True
    iterations = 0 #after the maximum number of iterations it will throw a warning message
    iterations_limit = 100
    while something_changed and iterations < iterations_limit:
        iterations += 1
        something_changed = False

        for edge_index, edge in enumerate(self.experiment.sequence):
            #UPDATING EDGE VALUES (TIME)
            try:
                exec("edge.value = " + str(edge.evaluation))
            except:
                return "time expression edge number %d"%edge_index

        for edge in self.experiment.sequence:
            if self.experiment.variables[edge.id].value != edge.value:
                something_changed = True
                self.experiment.variables[edge.id].value = edge.value

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
    for channel_index in range(16):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].digital[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            if channel.changed: 
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = self.digital_table.item(row,col).text()
                    (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(channel.expression)
                #Updating values and table
                if update_values_and_table:
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                    #Color coding the values
                    if channel.value == 1:
                        self.digital_table.item(row,col).setBackground(self.green)
                    else:
                        self.digital_table.item(row,col).setBackground(self.red)
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else: # We first need to update table entries, then evaluations and then values. Because not human entered values depend on previous human entered ones.
                # Updating digital table entries
                if update_values_and_table:
                    self.digital_table.item(row,col).setText(current_expression + " ")                
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values
                if update_values_and_table:
                    channel.value = current_value   
                                 
    self.update_on()

def analog_tab(self, update_expressions_and_evaluations = True, update_values_and_table = True):
    '''
    This function updates expressions, evaluations, values and entries of analog table
    Used in dds_table_changed()
    '''
    self.update_off()
    #note that in order to display numbers you first need to convert them to string
    for channel_index in range(32):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].analog[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            if channel.changed: 
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = self.analog_table.item(row,col).text()
                    (channel.evaluation, channel.for_python, channel.is_scanned) = self.decode_input(channel.expression)
                #Updating values and table
                if update_values_and_table:
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                    #Color coding the values
                    if channel.value != 0:
                        self.analog_table.item(row,col).setBackground(self.green)
                    else:
                        self.analog_table.item(row,col).setBackground(self.red)
                #Saving the current state of the channel
                current_expression = channel.expression
                current_evaluation = channel.evaluation
                current_value = channel.value
                current_for_python = channel.for_python
            else:# We first need to update table entries, then evaluations and then values. Because not human entered values depend on previous human entered ones.
                # Updating digital table entries
                if update_values_and_table:
                    self.analog_table.item(row,col).setText(current_expression + " ")                
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values
                if update_values_and_table:
                    channel.value = current_value     
    self.update_on()

def dds_tab(self, update_expressions_and_evaluations = True, update_values_and_table = True):
    '''
    This function updates expressions, evaluations, values and entries of dds table
    Used in dds_table_changed()
    '''
    self.update_off()
    #note that in order to display numbers you first need to convert them to string
    for channel_index in range(12):
        for setting in range(5):
            for row in range(2, self.sequence_num_rows+2): # plus 2 because of 2 rows used for title
                channel = self.experiment.sequence[row-2].dds[channel_index]
                # plus 4 is because first 4 columns are used by number, name, time of edge and separator and times 6 is becuase each channel has 5 columns and 1 separator
                col = channel_index * 6 + 4 + setting
                table_item = self.dds_table.item(row, col)
                exec("self.channel_entry = channel.%s" %self.setting_dict[setting])
                channel_entry = self.channel_entry
                if channel.changed: 
                    #Updating expressions and evaluations
                    if update_expressions_and_evaluations:
                        channel_entry.expression = table_item.text()
                        (channel_entry.evaluation, channel_entry.for_python, channel_entry.is_scanned) = self.decode_input(channel_entry.expression)
                    #Updating values
                    if update_values_and_table:
                        try:
                            exec("channel_entry.value =" + channel_entry.evaluation)
                        except:
                            return "digital channel %d, edge %d" %(channel_index, row)
                        #Color coding the values
                        if channel.state.value == 1:
                            table_item.setBackground(self.green)
                        else:
                            table_item.setBackground(self.red)
                    #Saving the current state of the channel
                    current_expression = channel_entry.expression
                    current_evaluation = channel_entry.evaluation
                    current_value = channel_entry.value
                    current_for_python = channel_entry.for_python
                else:# We first need to update table entries, then evaluations and then values. Because not human entered values depend on previous human entered ones.
                    # Updating digital table entries
                    if update_values_and_table:
                        table_item.setText(current_expression + " ")                
                    #Updating expressions and evaluations
                    if update_expressions_and_evaluations:
                        channel_entry.expression = current_expression
                        channel_entry.evaluation = current_evaluation
                        channel_entry.for_python = current_for_python
                    #Updating values
                    if update_values_and_table:
                        channel_entry.value = current_value

    self.update_on()

def all_tabs(self, update_expressions_and_evaluations = True, update_values_and_tables = True):
    '''
    This function updates all tabs. It just calls an update of each tab one by one
    
    Development : we need to include update variables tab and include it    
    '''
    self.update_off()
    sequence_tab(self)
    digital_tab(self, update_expressions_and_evaluations, update_values_and_tables)
    analog_tab(self, update_expressions_and_evaluations, update_values_and_tables)
    dds_tab(self, update_expressions_and_evaluations, update_values_and_tables)
    self.update_on()   

def from_object(self):
    '''
    This function rebuilds all tabs by looking at the self.experiment
    It reassigns title names, refills every table
    It is used in the following functions:
        1) sequence_table_changed : requires rebuilding tables, reassigning of the title names if redundant
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
    for i in range(12):
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.dds_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

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
    for channel_index in range(16):
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
    for channel_index in range(32):
        for row in range(self.sequence_num_rows):
            channel = self.experiment.sequence[row].analog[channel_index]
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel_index + 4
            if channel.changed:
                self.analog_table.setItem(row, col, QTableWidgetItem(channel.expression))
                if channel.value == 1:
                    self.analog_table.item(row,col).setBackground(self.green)
                else:
                    self.analog_table.item(row,col).setBackground(self.red)
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
    for channel_index in range(12):
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
    self.update_on()                
              