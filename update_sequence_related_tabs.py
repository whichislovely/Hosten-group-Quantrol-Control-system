import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def do(self):
    self.update_off()
    self.sequence_num_rows = len(self.experiment.sequence) 
    
    #filling variables table
    self.variables_table_row_count = len(self.experiment.new_variables)
    self.variables_table.setRowCount(self.variables_table_row_count)
    for index, variable in enumerate(self.experiment.new_variables):
        self.variables_table.setItem(index, 0, QTableWidgetItem(variable.name))
        if self.experiment.do_scan and variable.is_scanned:
            item = QTableWidgetItem("scanned")
            item.setFlags(Qt.NoItemFlags)
            self.variables_table.setItem(index, 1, item) 
        else:
            self.variables_table.setItem(index, 1, QTableWidgetItem(str(variable.value)))    

    #note that in order to display numbers you first need to convert them to string
    for row, edge in enumerate(self.experiment.sequence):
        #displaying edge names and times
        self.sequence_table.item(row, 0).setText(str(row))
        self.sequence_table.item(row, 1).setText(edge.name)
        self.sequence_table.item(row, 2).setText("id" + str(edge.id))
        self.sequence_table.item(row, 3).setText(edge.expression)
        self.sequence_table.item(row, 4).setText(str(edge.value))
        #DIGITAL TABLE
        self.digital_dummy.item(row, 0).setText(str(row))
        self.digital_dummy.item(row, 1).setText(edge.name)
        self.digital_dummy.item(row, 2).setText(str(edge.value))
        #ANALOG TABLE
        self.analog_dummy.item(row, 0).setText(str(row))
        self.analog_dummy.item(row, 1).setText(edge.name)
        self.analog_dummy.item(row, 2).setText(str(edge.value))
        #DIGITAL TABLE
        self.dds_dummy.item(row+2, 0).setText(str(row))
        self.dds_dummy.item(row+2, 1).setText(edge.name)
        self.dds_dummy.item(row+2, 2).setText(str(edge.value))

        #HIGHLIGHTING THE EDGE IN CASE OF GO TO EDGE BUTTON PRESSED
        if row == self.experiment.go_to_edge_num : 
            self.sequence_table.item(row,0).setBackground(self.green)
            self.sequence_table.item(row,1).setBackground(self.green)
            self.sequence_table.item(row,2).setBackground(self.green)
            self.sequence_table.item(row,3).setBackground(self.green)
            self.sequence_table.item(row,4).setBackground(self.green)
            self.digital_dummy.item(row,0).setBackground(self.green)
            self.digital_dummy.item(row,1).setBackground(self.green)
            self.digital_dummy.item(row,2).setBackground(self.green)
            self.analog_dummy.item(row,0).setBackground(self.green)
            self.analog_dummy.item(row,1).setBackground(self.green)
            self.analog_dummy.item(row,2).setBackground(self.green)
            self.dds_dummy.item(row+2,0).setBackground(self.green)
            self.dds_dummy.item(row+2,1).setBackground(self.green)
            self.dds_dummy.item(row+2,2).setBackground(self.green)

        #displaying digital channels
        for index, channel in enumerate(self.experiment.sequence[row].digital):
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = index + 4
            if channel.changed:
                if channel.value == 1:
                    self.digital_table.item(row,col).setBackground(self.green)
                else:
                    self.digital_table.item(row,col).setBackground(self.red)
            else:
                self.digital_table.item(row,col).setText(self.digital_table.item(row-1, col).text() + " ")                

        #displaying analog channels
        for index, channel in enumerate(self.experiment.sequence[row].analog):
            # plus 3 is because first 3 columns are used by number, name and time of edge
            col = index + 4
            if channel.changed == True:
                if channel.value == 1:
                    self.analog_table.item(row, col).setBackground(self.green)
                else:
                    self.analog_table.item(row, col).setBackground(self.red)
            else:
                self.analog_table.item(row, col).setText(self.analog_table.item(row-1, col).text() + " ")
                self.analog_table.item(row, col).setToolTip(str(self.experiment.sequence[row].analog[index].value))

        #displaying dds channels
        for index, channel in enumerate(self.experiment.sequence[row].dds):
            #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
            col = 4 + index * 6
            if channel.changed == True:
                if channel.state.value == 1:
                    for setting in range(5):
                        self.dds_table.item(row+2, col + setting).setBackground(self.green)
                else:
                    for setting in range(5):
                        self.dds_table.item(row+2, col + setting).setBackground(self.red)
            else:
                for setting in range(5):
                    exec("self.dds_table.item(row+2, col + setting).setText(str(self.experiment.sequence[row].dds[index].%s.expression) + ' ')" %self.setting_dict[setting])
                    exec("self.dds_table.item(row+2, col + setting).setToolTip(str(self.experiment.sequence[row].dds[index].%s.value))" %self.setting_dict[setting])                    

    # displaying scan parameters
    self.scan_table_parameters.setRowCount(len(self.experiment.scanned_variables))
    for row, variable in enumerate(self.experiment.scanned_variables):
        self.scan_table_parameters.setItem(row,0, QTableWidgetItem(str(variable.name)))
        self.scan_table_parameters.setItem(row,1, QTableWidgetItem(str(variable.min_val)))
        self.scan_table_parameters.setItem(row,2, QTableWidgetItem(str(variable.max_val)))
        
    self.update_on()