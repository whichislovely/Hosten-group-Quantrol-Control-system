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
                if col == 4:
                    print("row", row-2, "channel", channel_index, "setting", self.setting_dict[setting] )
                    print(table_item.background().color() == self.green)
    self.update_on()