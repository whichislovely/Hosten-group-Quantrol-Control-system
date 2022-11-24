from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def digital_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, ):
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
                #Updating values
                if update_values:
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                # Updating digital table entries
                if update_table:
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
            else:
                # Updating digital table entries
                if update_table:
                    self.digital_table.item(row,col).setText(current_expression + " ")                
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values
                if update_values:
                    channel.value = current_value   
                                 
    self.update_on()

def analog_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, ):
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
                #Updating values
                if update_values:
                    try:
                        exec("channel.value = " + channel.evaluation)
                    except:
                        return "digital channel %d, edge %d" %(channel_index, row)
                # Updating analog table entries
                if update_table:
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
            else:
                # Updating digital table entries
                if update_table:
                    self.analog_table.item(row,col).setText(current_expression + " ")                
                #Updating expressions and evaluations
                if update_expressions_and_evaluations:
                    channel.expression = current_expression
                    channel.evaluation = current_evaluation
                    channel.for_python = current_for_python
                #Updating values
                if update_values:
                    channel.value = current_value     
    self.update_on()

def dds_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False):
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
                    if update_values:
                        try:
                            exec("channel_entry.value =" + channel_entry.evaluation)
                        except:
                            return "digital channel %d, edge %d" %(channel_index, row)
                    # Updating dds table entries
                    if update_table:
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
                else:
                    # Updating digital table entries
                    if update_table:
                        table_item.setText(current_expression + " ")                
                    #Updating expressions and evaluations
                    if update_expressions_and_evaluations:
                        channel_entry.expression = current_expression
                        channel_entry.evaluation = current_evaluation
                        channel_entry.for_python = current_for_python
                    #Updating values
                    if update_values:
                        channel_entry.value = current_value

    self.update_on()

def all_tabs(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, ):
    self.update_off()
    digital_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, )
    analog_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, )
    dds_tab(self, update_expressions_and_evaluations = False, update_values = False, update_table = False, )
    self.update_on()   


def from_object(self):
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
        self.sequence_table.setItem(row,2, QTableWidgetItem("id" + str(edge.id)))
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
              
