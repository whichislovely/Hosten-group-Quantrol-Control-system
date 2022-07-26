import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def do(self):
    self.update_off()
    self.sequence_num_rows = len(self.experiment.sequence) 
    #EVALUATING TIMES WITH GIVEN EXPRESSIONS
#    print(self.experiment.variables)
#    for row in range(self.sequence_num_rows):
#        exec("self.sequence[row].time =" + str(self.sequence[row].evaluation))
#        print(row, self.sequence[row].evaluation)

#    self.sequence = sorted(self.sequence, key = lambda edge: edge.time)
#    for row in range(self.sequence_num_rows):
#        self.sequence[row].number = row
#       key = "id" + str(self.sequence[row].id)
#        self.experiment.variables[key] = self.sequence[row].time


    self.sequence_table.setRowCount(self.sequence_num_rows)                     
    self.digital_table.setRowCount(self.sequence_num_rows)
    self.digital_dummy.setRowCount(self.sequence_num_rows)
    self.analog_table.setRowCount(self.sequence_num_rows)
    self.analog_dummy.setRowCount(self.sequence_num_rows)
    self.dds_table.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
    self.dds_dummy.setRowCount(self.sequence_num_rows+2) #2 first rows are used for title name 
    
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
    
    self.variables_table_contents = [0] * self.variables_table_row_count
    for row in range(self.variables_table_row_count):
        self.variables_table_contents[row] = self.variables_table.item(row, 0).text()
    #additional assignment for the DDS table title of columns
    for i in range(3):
        self.dds_table.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_table.item(0,i).setTextAlignment(Qt.AlignCenter)
    for i in range(3):
        self.dds_dummy.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_dummy.item(0,i).setTextAlignment(Qt.AlignCenter)
    self.dds_dummy.setSpan(0,3, self.sequence_num_rows + 2, 1)
    self.dds_dummy.setItem(0,3, QTableWidgetItem())
    self.dds_dummy.item(0,3).setBackground(QColor(100,100,100))

    for i in range(12):
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        self.dds_table.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
        self.dds_table.setItem(0,6*i + 3, QTableWidgetItem())
        self.dds_table.item(0, 6*i + 3).setBackground(QColor(100,100,100))
        self.dds_table.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_table.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_table.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_table.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_table.setItem(1,6*i+8, QTableWidgetItem('state'))



    #note that in order to display numbers you first need to convert them to string
    for row in range(self.sequence_num_rows):
        #displaying edge names and times        
        self.sequence_table.setItem(row,0, QTableWidgetItem(str(row)))
        self.sequence_table.setItem(row,1, QTableWidgetItem(str(self.experiment.sequence[row].name)))
        self.sequence_table.setItem(row,2, QTableWidgetItem(str(self.experiment.sequence[row].id)))
        self.sequence_table.setItem(row,3, QTableWidgetItem(str(self.experiment.sequence[row].expression)))
        self.sequence_table.setItem(row,4, QTableWidgetItem(str(self.experiment.sequence[row].value)))

        self.digital_dummy.setItem(row,0, QTableWidgetItem(str(row)))
        self.digital_dummy.setItem(row,1, QTableWidgetItem(str(self.experiment.sequence[row].name)))
        self.digital_dummy.setItem(row,2, QTableWidgetItem(str(self.experiment.sequence[row].value)))

        self.analog_dummy.setItem(row,0, QTableWidgetItem(str(row)))
        self.analog_dummy.setItem(row,1, QTableWidgetItem(str(self.experiment.sequence[row].name)))
        self.analog_dummy.setItem(row,2, QTableWidgetItem(str(self.experiment.sequence[row].value)))

        self.dds_dummy.setItem(row+2,0, QTableWidgetItem(str(row)))
        self.dds_dummy.setItem(row+2,1, QTableWidgetItem(str(self.experiment.sequence[row].name)))
        self.dds_dummy.setItem(row+2,2, QTableWidgetItem(str(self.experiment.sequence[row].value)))
        if self.experiment.go_to_edge_num == row:
            self.sequence_table.item(row,0).setBackground(QColor(37,211,102))
            self.sequence_table.item(row,1).setBackground(QColor(37,211,102))
            self.sequence_table.item(row,2).setBackground(QColor(37,211,102))
            self.sequence_table.item(row,3).setBackground(QColor(37,211,102))
            self.sequence_table.item(row,4).setBackground(QColor(37,211,102))
            self.digital_dummy.item(row,0).setBackground(QColor(37,211,102))
            self.digital_dummy.item(row,1).setBackground(QColor(37,211,102))
            self.digital_dummy.item(row,2).setBackground(QColor(37,211,102))
            self.analog_dummy.item(row,0).setBackground(QColor(37,211,102))
            self.analog_dummy.item(row,1).setBackground(QColor(37,211,102))
            self.analog_dummy.item(row,2).setBackground(QColor(37,211,102))
            self.dds_dummy.item(row+2,0).setBackground(QColor(37,211,102))
            self.dds_dummy.item(row+2,1).setBackground(QColor(37,211,102))
            self.dds_dummy.item(row+2,2).setBackground(QColor(37,211,102))

        #displaying ttl channels
        for channel in range(16):
            # plus 4 is because first 4 columns are used by number, name, time of edge and separator
            col = channel + 4
            if self.experiment.sequence[row].digital[channel].is_scanned == False:
                if (self.experiment.sequence[row].digital[channel].value == 0 or self.experiment.sequence[row].digital[channel].value == 1):
                    if self.experiment.sequence[row].digital[channel].changed == False:
                        self.experiment.sequence[row].digital[channel].expression = self.experiment.sequence[row-1].digital[channel].expression
                    self.digital_table.setItem(row, col, QTableWidgetItem(str(self.experiment.sequence[row].digital[channel].expression) + " "))
                    if self.experiment.sequence[row].digital[channel].changed == True:              
                        if self.experiment.sequence[row].digital[channel].value == 1:
                                self.digital_table.item(row, col).setBackground(QColor(37,211,102))
                        if self.experiment.sequence[row].digital[channel].value == 0:
                                self.digital_table.item(row, col).setBackground(QColor(247,120,120))

                else:
                    self.error_message("Only value '1' or '0' are expected", "Wrong variable value at Digital table row" + str(row) + "channel" + str(channel))
                    self.update_off()
                    try:
                        self.digital_table.item(row,col).setText(self.experiment.sequence[row].digital[channel])
                    except:
                        self.digital_table.item(row,col).setText("")
                    self.update_on()
            else:
                self.digital_table.setItem(row, col, QTableWidgetItem(str(self.experiment.sequence[row].digital[channel].expression) + " "))


                
        #making a separation between first 3 columns and list of channels
        if self.sequence_num_rows > 1:
            self.digital_table.setSpan(0,3, self.sequence_num_rows , 1)
        self.digital_table.setItem(0,3, QTableWidgetItem())
        self.digital_table.item(0,3).setBackground(QColor(100,100,100))

        #displaying analog channels
        for index, channel in enumerate(self.experiment.sequence[row].analog):
            # plus 3 is because first 3 columns are used by number, name and time of edge
            col = index + 4
            if channel.changed == True:
                dummy_item = QTableWidgetItem(str(channel.expression))
                dummy_item.setToolTip(str(channel.value))
                self.analog_table.setItem(row, col, dummy_item)
                if channel.value == 0:
                    self.analog_table.item(row, col).setBackground(QColor(247,120,120))
                else:
                    self.analog_table.item(row, col).setBackground(QColor(37,211,102))                    
            else:
                self.experiment.sequence[row].analog[index].expression = self.experiment.sequence[row-1].analog[index].expression
                self.experiment.sequence[row].analog[index].value = self.experiment.sequence[row-1].analog[index].value
                dummy_item = QTableWidgetItem(str(channel.expression) + " ")
                dummy_item.setToolTip(str(channel.value))
                self.analog_table.setItem(row, col, dummy_item)
        if self.sequence_num_rows > 1:
            self.analog_table.setSpan(0,3, self.sequence_num_rows , 1)
        self.analog_table.setItem(0,3, QTableWidgetItem())
        self.analog_table.item(0,3).setBackground(QColor(100,100,100))

        #displaying dds channels
        for index, channel in enumerate(self.experiment.sequence[row].dds):
            #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
            col = 4 + index * 6
            if channel.changed == True:
                #frequency
                dummy_item = QTableWidgetItem(str(channel.frequency.expression))
                dummy_item.setToolTip(str(channel.frequency.value))
                self.dds_table.setItem(row+2, col, dummy_item)
                if channel.state.value == 0:
                    self.dds_table.item(row+2,col).setBackground(QColor(247,120,120))
                else:
                    self.dds_table.item(row+2,col).setBackground(QColor(37,211,102))
                #amplitude
                dummy_item = QTableWidgetItem(str(channel.amplitude.expression))
                dummy_item.setToolTip(str(channel.amplitude.value))
                self.dds_table.setItem(row+2, col+1, dummy_item)
                if channel.state.value == 0:
                    self.dds_table.item(row+2,col+1).setBackground(QColor(247,120,120))
                else:
                    self.dds_table.item(row+2,col+1).setBackground(QColor(37,211,102))
                #attenuation
                dummy_item = QTableWidgetItem(str(channel.attenuation.expression))
                dummy_item.setToolTip(str(channel.attenuation.value))
                self.dds_table.setItem(row+2, col+2, dummy_item)
                if channel.state.value == 0:
                    self.dds_table.item(row+2,col+2).setBackground(QColor(247,120,120))
                else:
                    self.dds_table.item(row+2,col+2).setBackground(QColor(37,211,102))
                #phase
                dummy_item = QTableWidgetItem(str(channel.phase.expression))
                dummy_item.setToolTip(str(channel.phase.value))
                self.dds_table.setItem(row+2, col+3, dummy_item)
                if channel.state.value == 0:
                    self.dds_table.item(row+2,col+3).setBackground(QColor(247,120,120))
                else:
                    self.dds_table.item(row+2,col+3).setBackground(QColor(37,211,102))
                #state
                dummy_item = QTableWidgetItem(str(channel.state.expression))
                dummy_item.setToolTip(str(channel.state.value))
                self.dds_table.setItem(row+2, col+4, dummy_item)
                if channel.state.value == 0:
                    self.dds_table.item(row+2,col+4).setBackground(QColor(247,120,120))
                else:
                    self.dds_table.item(row+2,col+4).setBackground(QColor(37,211,102))
            else:
                #frequency
                channel.frequency.expression = self.experiment.sequence[row-1].dds[index].frequency.expression
                channel.frequency.evaluation = self.experiment.sequence[row-1].dds[index].frequency.evaluation
                channel.frequency.value = self.experiment.sequence[row-1].dds[index].frequency.value
                dummy_item = QTableWidgetItem(str(channel.frequency.expression)+" ")
                dummy_item.setToolTip(str(channel.frequency.value))
                self.dds_table.setItem(row+2, col, dummy_item)
                #amplitude
                channel.amplitude.expression = self.experiment.sequence[row-1].dds[index].amplitude.expression
                channel.amplitude.evaluation = self.experiment.sequence[row-1].dds[index].amplitude.evaluation
                channel.amplitude.value = self.experiment.sequence[row-1].dds[index].amplitude.value
                dummy_item = QTableWidgetItem(str(channel.amplitude.expression)+" ")
                dummy_item.setToolTip(str(channel.amplitude.value))
                self.dds_table.setItem(row+2, col+1, dummy_item)
                #attenuation
                channel.attenuation.expression = self.experiment.sequence[row-1].dds[index].attenuation.expression
                channel.attenuation.evaluation = self.experiment.sequence[row-1].dds[index].attenuation.evaluation
                channel.attenuation.value = self.experiment.sequence[row-1].dds[index].attenuation.value
                dummy_item = QTableWidgetItem(str(channel.attenuation.expression)+" ")
                dummy_item.setToolTip(str(channel.attenuation.value))
                self.dds_table.setItem(row+2, col+2, dummy_item)
                #phase
                channel.phase.expression = self.experiment.sequence[row-1].dds[index].phase.expression
                channel.phase.evaluation = self.experiment.sequence[row-1].dds[index].phase.evaluation
                channel.phase.value = self.experiment.sequence[row-1].dds[index].phase.value
                dummy_item = QTableWidgetItem(str(channel.phase.expression)+" ")
                dummy_item.setToolTip(str(channel.phase.value))
                self.dds_table.setItem(row+2, col+3, dummy_item)
                #state
                channel.state.expression = self.experiment.sequence[row-1].dds[index].state.expression
                channel.state.evaluation = self.experiment.sequence[row-1].dds[index].state.evaluation
                channel.state.value = self.experiment.sequence[row-1].dds[index].state.value
                dummy_item = QTableWidgetItem(str(channel.state.expression)+" ")
                dummy_item.setToolTip(str(channel.state.value))
                self.dds_table.setItem(row+2, col+4, dummy_item)

    self.scan_table_parameters.setRowCount(len(self.experiment.scanned_variables))
    for row, variable in enumerate(self.experiment.scanned_variables):
        self.scan_table_parameters.setItem(row,0, QTableWidgetItem(str(variable.name)))
        self.scan_table_parameters.setItem(row,1, QTableWidgetItem(str(variable.min_val)))
        self.scan_table_parameters.setItem(row,2, QTableWidgetItem(str(variable.max_val)))
        
        

    self.update_on()