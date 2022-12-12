from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime


#this is needed for making some rows or columns read only
#Example : delegate = ReadOnlyDelegate(self)
#          self.edges_table.setItemDelegateForColumn(2,delegate)
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        #print("createEditor event fired")
        return

def sequence_tab_build(self):
    #SEQUENCE TAB WIDGET
    self.sequence_tab_widget = QWidget()
    self.sequence_lable = QLabel(self.sequence_tab_widget)
    self.sequence_lable.setText("Timing Sequence")
    self.sequence_lable.setFont(QFont('Arial', 14))
    self.sequence_lable.setGeometry(85, 0, 200, 30)
    #file_name label
    self.file_name_lable = QLabel(self.sequence_tab_widget)
    self.file_name_lable.setFont(QFont('Arial', 10))
    self.file_name_lable.setGeometry(275, 2, 600, 30)
    #SEQUENCE TAB LAYOUT
    self.sequence_table = QTableWidget(self.sequence_tab_widget)
    width_of_table = 805
    self.sequence_table.setGeometry(QRect(0, 30, width_of_table, 1070))                                                #size of the table
    sequence_num_columns = 5
    self.sequence_table.setColumnCount(sequence_num_columns)
    self.sequence_table.setRowCount(1)
    self.sequence_table.setHorizontalHeaderLabels(["#", "Name","ID", "Time expression","Time (ms)"])
    self.sequence_table.verticalHeader().setVisible(False)
    self.sequence_table.horizontalHeader().setFixedHeight(60)
    self.sequence_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.sequence_table.setFont(QFont('Arial', 12))
    self.sequence_table.setColumnWidth(0,103)
    self.sequence_table.setColumnWidth(1,200)
    self.sequence_table.setColumnWidth(2,100)
    self.sequence_table.setColumnWidth(3,200)
    self.sequence_table.setColumnWidth(4,200)
    self.sequence_table.itemChanged.connect(self.sequence_table_changed)
    delegate = ReadOnlyDelegate(self)
    self.sequence_table.setItemDelegateForColumn(0,delegate)
    self.sequence_table.setItemDelegateForColumn(2,delegate)
    self.sequence_table.setItemDelegateForColumn(4,delegate)
    #Setting the default values 
    self.sequence_table.setItem(0, 0, QTableWidgetItem("0"))
    self.sequence_table.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.sequence_table.setItem(0, 2, QTableWidgetItem(self.experiment.sequence[0].id))
    self.sequence_table.setItem(0, 3, QTableWidgetItem(self.experiment.sequence[0].expression))
    self.sequence_table.setItem(0, 4, QTableWidgetItem(str(self.experiment.sequence[0].value)))
    #button to save current sequence
    self.save_sequence_button = QPushButton(self.sequence_tab_widget)
    self.save_sequence_button.setFont(QFont('Arial', 14))
    self.save_sequence_button.setGeometry(width_of_table + 50, 50, 200, 30)
    self.save_sequence_button.setText("Save sequence")
    self.save_sequence_button.clicked.connect(self.save_sequence_button_clicked)
    #button to load new sequence
    self.load_sequence_button = QPushButton(self.sequence_tab_widget)
    self.load_sequence_button.setFont(QFont('Arial', 14))
    self.load_sequence_button.setGeometry(width_of_table + 50, 100, 200, 30)
    self.load_sequence_button.setText("Load sequence")
    self.load_sequence_button.clicked.connect(self.load_sequence_button_clicked)
    #button to insert edge
    self.insert_edge_button = QPushButton(self.sequence_tab_widget)
    self.insert_edge_button.setFont(QFont('Arial', 14))
    self.insert_edge_button.setGeometry(width_of_table + 50, 150, 200, 30)
    self.insert_edge_button.setText("Insert Edge")
    self.insert_edge_button.clicked.connect(self.insert_edge_button_clicked)
    #button to delete edge
    self.delete_edge_button = QPushButton(self.sequence_tab_widget)
    self.delete_edge_button.setFont(QFont('Arial', 14))
    self.delete_edge_button.setGeometry(width_of_table + 50, 200, 200, 30)
    self.delete_edge_button.setText("Delete Edge")
    self.delete_edge_button.clicked.connect(self.delete_edge_button_clicked)
    #go to edge
    self.go_to_edge_button = QPushButton(self.sequence_tab_widget)
    self.go_to_edge_button.setFont(QFont('Arial', 14))
    self.go_to_edge_button.setGeometry(width_of_table + 50, 250, 200, 30)
    self.go_to_edge_button.setText("Go to Edge")
    self.go_to_edge_button.clicked.connect(self.go_to_edge_button_clicked)
    #run experiment
    self.run_experiment_button = QPushButton(self.sequence_tab_widget)
    self.run_experiment_button.setFont(QFont('Arial', 14))
    self.run_experiment_button.setGeometry(width_of_table + 50, 300, 200, 30)
    self.run_experiment_button.setText("Run experiment")
    self.run_experiment_button.clicked.connect(self.run_experiment_button_clicked)

    #dummy button for checking 
    self.dummy_button = QPushButton(self.sequence_tab_widget)
    self.dummy_button.setFont(QFont('Arial', 14))
    self.dummy_button.setGeometry(width_of_table + 50, 350, 200, 30)
    self.dummy_button.setText("Dummy button")
    self.dummy_button.clicked.connect(self.dummy_button_clicked)

    #button to save current sequence as
    self.save_sequence_as_button = QPushButton(self.sequence_tab_widget)
    self.save_sequence_as_button.setFont(QFont('Arial', 14))
    self.save_sequence_as_button.setGeometry(width_of_table + 50, 400, 200, 30)
    self.save_sequence_as_button.setText("Save sequence as")
    self.save_sequence_as_button.clicked.connect(self.save_sequence_as_button_clicked)

    #show logger of the program
    self.logger = QPlainTextEdit(self.sequence_tab_widget)
    self.logger.setFont(QFont("Arial", 12))
    self.logger.setGeometry(width_of_table + 50, 800, 1000, 300)
    self.logger.setReadOnly(True)
    self.logger.appendPlainText("Welcome to the Hosten lab! Hope you enjoy your stay here :)")
    self.logger.appendPlainText("")
    self.logger.appendPlainText(datetime.now().strftime("%D %H:%M:%S - ") + "Program initialized")
    #clear logger button
    self.clear_logger_button = QPushButton(self.sequence_tab_widget)
    self.clear_logger_button.setFont(QFont("Arial", 14))
    self.clear_logger_button.setGeometry(width_of_table + 50, 750, 200, 30)
    self.clear_logger_button.setText("Clear logger")
    self.clear_logger_button.clicked.connect(self.clear_logger_button_clicked)

    #Table of parameters
    self.scan_table_parameters = QTableWidget()
    self.scan_table_parameters.setColumnCount(3)
    self.scan_table_parameters.setRowCount(0)
    self.scan_table_parameters.verticalHeader().setVisible(False)
    self.scan_table_parameters.setFont(QFont("Arial", 14))
    self.scan_table_parameters.setHorizontalHeaderLabels(["Variable","Min value", "Max value"])
    self.scan_table_parameters.setColumnWidth(0,250)
    self.scan_table_parameters.setColumnWidth(1,200)
    self.scan_table_parameters.setColumnWidth(2,200)
    self.scan_table_parameters.itemChanged.connect(self.scan_table_parameters_changed)
    #ADD SCANNED VARIABLE BUTTON
    self.add_scanned_variable_button = QPushButton()
    self.add_scanned_variable_button.setFont(QFont('Arial', 14))
    self.add_scanned_variable_button.resize(200, 50)
    self.add_scanned_variable_button.setText("Add scanned variable")
    self.add_scanned_variable_button.clicked.connect(self.add_scanned_variable_button_pressed)#this should be modified

    #DELETE SCANNED VARIABLE BUTTON
    self.delete_scanned_variable_button = QPushButton()
    self.delete_scanned_variable_button.setFont(QFont('Arial', 14))
    self.delete_scanned_variable_button.setText("Delete scanned variable")
    self.delete_scanned_variable_button.clicked.connect(self.delete_scanned_variable_button_pressed)#this should be modified

    #STEP SIZE INPUT
    self.number_of_steps_label = QLabel()
    self.number_of_steps_label.setText("Number of steps")
    self.number_of_steps_input = QLineEdit()
    self.number_of_steps_input.editingFinished.connect(self.number_of_steps_input_changed)
    self.number_of_steps_input.setText("1")

    #HORIZONTAL LAYOUT
    hBox = QHBoxLayout()
    temp = QWidget()
    hBox.addWidget(self.add_scanned_variable_button)
    hBox.addWidget(self.delete_scanned_variable_button)     
    hBox.addWidget(self.number_of_steps_label)
    hBox.addWidget(self.number_of_steps_input)
    temp.setLayout(hBox)
    #SCAN PARAMETERS
    self.scan_table = QGroupBox(self.sequence_tab_widget)
    self.scan_table.setTitle("Scan")
    self.scan_table.setCheckable(True)
    self.scan_table.setChecked(False)
    self.scan_table.setFont(QFont("Arial", 14))
    self.scan_table.move(1100, 30)
    #self.scan_table.setGeometry(1100, 30, 675, 250)
    self.scan_table.toggled.connect(self.scan_table_checked)
    vBox = QVBoxLayout()
    self.scan_table.setLayout(vBox)
    vBox.addWidget(temp)
    vBox.addWidget(self.scan_table_parameters)



# DIGITAL TAB
def digital_tab_build(self):
    self.digital_tab_num_cols = 16 + 4    
    self.digital_and_analog_table_column_width = 130
    #DIGITAL TAB WIDGET
    self.digital_tab_widget = QWidget()
    digital_lable = QLabel(self.digital_tab_widget)
    digital_lable.setText("Digital channels")
    digital_lable.setFont(QFont('Arial', 14))
    digital_lable.setGeometry(85, 0, 400, 30)
    
    #DIGITAL TAB LAYOUT
    self.digital_table = QTableWidget(self.digital_tab_widget)
    self.digital_table.setGeometry(QRect(0, 30, 1905, 1070))  
    self.digital_table.setColumnCount(self.digital_tab_num_cols)
    self.digital_table.setRowCount(1) 
    self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
    self.digital_table.verticalHeader().setVisible(False)
    self.digital_table.horizontalHeader().setFixedHeight(60)
    self.digital_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.digital_table.setFont(QFont('Arial', 16))
    self.digital_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.digital_table.horizontalHeader().setMinimumSectionSize(0)
    self.digital_table.setColumnWidth(0,50)
    self.digital_table.setColumnWidth(1,180)
    self.digital_table.setColumnWidth(2,105)
    self.digital_table.setColumnWidth(3,5)
    self.digital_table.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(4):
        exec("self.digital_table.setItemDelegateForColumn(%d,delegate)" %_)
    #self.digital_table.setItemDelegateForRow(0, delegate)
    for i in range(4, self.digital_tab_num_cols):
        exec("self.digital_table.setColumnWidth(%d,%d)" % (i, self.digital_and_analog_table_column_width))
    #Filling the DIGITAL table
    for index, channel in enumerate(self.experiment.sequence[0].digital):
        col = index + 4
        self.digital_table.setItem(0, col, QTableWidgetItem(channel.expression))
        if channel.value == 1:
            self.digital_table.item(0, col).setBackground(self.green)
        else:
            self.digital_table.item(0, col).setBackground(self.red)
    #Binding functions
    self.digital_table.itemChanged.connect(self.digital_table_changed)
    self.digital_table.horizontalHeader().sectionClicked.connect(self.digital_table_header_clicked)



    #Dummy table that will display edge number, name and time and will be fixed
    self.digital_dummy = QTableWidget(self.digital_tab_widget)
    self.digital_dummy.setGeometry(QRect(0.5, 30, 327, 1053))
    self.digital_dummy.setColumnCount(3)
    self.digital_dummy.setRowCount(1)
    self.digital_dummy.setHorizontalHeaderLabels(self.experiment.title_digital_tab[0:3])
    self.digital_dummy.verticalHeader().setVisible(False)
    self.digital_dummy.horizontalHeader().setFixedHeight(60)
    self.digital_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.digital_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.digital_dummy.setFont(QFont('Arial', 12))
    self.digital_dummy.setColumnWidth(0,50)
    self.digital_dummy.setColumnWidth(1,180)
    self.digital_dummy.setColumnWidth(2,100)
    self.digital_dummy.setFrameStyle(QFrame.NoFrame)
    #Setting the left part of the DIGITAL table (edge number, name, time)
    self.digital_dummy.setItem(0, 0, QTableWidgetItem("0"))
    self.digital_dummy.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.digital_dummy.setItem(0, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))
    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.digital_dummy.setItemDelegateForColumn(%d,delegate)" %_)
        
    self.digital_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.digital_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

#ANALOG TAB
def analog_tab_build(self):
    self.analog_tab_num_cols = 32 + 4    
    #ANALOG TAB WIDGET
    self.analog_tab_widget = QWidget()
    #ANALOG LABLE
    analog_lable = QLabel(self.analog_tab_widget)
    analog_lable.setText("Analog channels")
    analog_lable.setFont(QFont('Arial', 14))
    analog_lable.setGeometry(85, 0, 400, 30)


    #ANALOG TAB LAYOUT
    self.analog_table = QTableWidget(self.analog_tab_widget)
    self.analog_table.setGeometry(QRect(0, 30, 1905, 1070))  
    self.analog_table.setColumnCount(self.analog_tab_num_cols) 
    self.analog_table.setRowCount(1)
    self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
    self.analog_table.verticalHeader().setVisible(False)
    self.analog_table.horizontalHeader().setFixedHeight(60)
    self.analog_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.analog_table.setFont(QFont('Arial', 16))
    self.analog_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.analog_table.horizontalHeader().setMinimumSectionSize(0)
    self.analog_table.setColumnWidth(0,50)
    self.analog_table.setColumnWidth(1,180)
    self.analog_table.setColumnWidth(2,105)
    self.analog_table.setColumnWidth(3,5)
    self.analog_table.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(4):
        exec("self.analog_table.setItemDelegateForColumn(%d,delegate)" %_)
    #self.analog_table.setItemDelegateForRow(0,delegate)
    for i in range(4, self.analog_tab_num_cols):
        exec("self.analog_table.setColumnWidth(%d,%d)" % (i,self.digital_and_analog_table_column_width))
    #Filling the default values
    for index, channel in enumerate(self.experiment.sequence[0].analog):
        # plus 3 is because first 3 columns are used by number, name and time of edge
        col = index + 4
        self.analog_table.setItem(0, col, QTableWidgetItem(channel.expression))
        self.analog_table.item(0, col).setToolTip(str(channel.value))
        if channel.value == 1:
            self.analog_table.item(0, col).setBackground(self.green)
        else:
            self.analog_table.item(0, col).setBackground(self.red)
    
    self.analog_table.itemChanged.connect(self.analog_table_changed)
    self.analog_table.horizontalHeader().sectionClicked.connect(self.analog_table_header_clicked)

    #Dummy table that will display edge number, name and time and will be fixed
    self.analog_dummy = QTableWidget(self.analog_tab_widget)
    self.analog_dummy.setGeometry(QRect(0.5,30, 327,1053))
    self.analog_dummy.setColumnCount(3)
    self.analog_dummy.setRowCount(1)
    self.analog_dummy.setHorizontalHeaderLabels(self.experiment.title_analog_tab[0:3])
    self.analog_dummy.verticalHeader().setVisible(False)
    self.analog_dummy.horizontalHeader().setFixedHeight(60)
    self.analog_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.analog_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.analog_dummy.setFont(QFont('Arial', 12))
    self.analog_dummy.setColumnWidth(0,50)
    self.analog_dummy.setColumnWidth(1,180)
    self.analog_dummy.setColumnWidth(2,100)
    self.analog_dummy.setFrameStyle(QFrame.NoFrame)
    #Setting the left part of the analog table
    self.analog_dummy.setItem(0, 0, QTableWidgetItem("0"))
    self.analog_dummy.setItem(0, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.analog_dummy.setItem(0, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))    

    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.analog_dummy.setItemDelegateForColumn(%d,delegate)" %_)

    self.analog_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.analog_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

def dds_tab_build(self):
    self.dds_tab_num_cols = 6*12 + 3
    #DDS TABLE WIDGET
    self.dds_tab_widget = QWidget()
    #DDS LABLE
    dds_lable = QLabel(self.dds_tab_widget)
    dds_lable.setText("Dds channels")
    dds_lable.setFont(QFont('Arial', 14))
    dds_lable.setGeometry(85, 0, 400, 30)
    self.sequence_num_rows = len(self.experiment.sequence)
    
    #DDS TAB LAYOUT
    self.dds_table = QTableWidget(self.dds_tab_widget)
    self.dds_table.setGeometry(QRect(0.5, 30, 1905, 1070))
    self.dds_table.setColumnCount(self.dds_tab_num_cols)
    self.dds_table.horizontalHeader().setMinimumHeight(50)
    self.dds_table.verticalHeader().setVisible(False)
    self.dds_table.horizontalHeader().setVisible(False)
    self.dds_table.setRowCount(3) # 5 is an arbitrary number we just need to have rows in order to span them
    self.dds_table.horizontalHeader().setMinimumSectionSize(0)
    self.dds_table.setFont(QFont('Arial', 12))
    self.dds_table.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.dds_table.setColumnWidth(0,50)
    self.dds_table.setColumnWidth(1,180)
    self.dds_table.setColumnWidth(2,100)
    self.dds_table.setColumnWidth(3,5)

    delegate = ReadOnlyDelegate(self)
    #SHAPING THE TABLE
    for i in range(12):
        self.dds_table.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.dds_table.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.dds_table.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.dds_table.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable
    
    #making first three columns verticaly wider to fit with header 
    for i in range(3):
        self.dds_table.setSpan(0, i, 2, 1)
        self.dds_table.setItemDelegateForColumn(i,delegate)
    #Filling the default values of DDS table
    for index, channel in enumerate(self.experiment.sequence[0].dds):
        #plus 4 is because first 4 columns are used by number, name, time and separator(dark grey line)
        col = 4 + index * 6  
        for setting in range(5):
            exec("self.dds_table.setItem(2, col + setting, QTableWidgetItem(str(channel.%s.expression)))" %self.setting_dict[setting])
            exec("self.dds_table.item(2, col + setting).setToolTip(str(channel.%s.value))" %self.setting_dict[setting])
            self.dds_table.item(2, col + setting).setBackground(self.green)


    self.dds_table.itemChanged.connect(self.dds_table_changed)

    #Dummy table that will display edge number, name and time and will be fixed (LEFT SIDE OF THE TABLE)
    self.dds_dummy = QTableWidget(self.dds_tab_widget)
    self.dds_dummy.setGeometry(QRect(0.5,30,335,1053))
    self.dds_dummy.setColumnCount(4)
    self.dds_dummy.setRowCount(3)
    self.dds_dummy.horizontalHeader().setMinimumHeight(50)
    self.dds_dummy.verticalHeader().setVisible(False)
    self.dds_dummy.horizontalHeader().setVisible(False)
    self.dds_dummy.horizontalHeader().setMinimumSectionSize(0)
    self.dds_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.dds_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_dummy.setFont(QFont('Arial', 12))
    self.dds_dummy.setColumnWidth(0,50)
    self.dds_dummy.setColumnWidth(1,180)
    self.dds_dummy.setColumnWidth(2,100)
    self.dds_dummy.setColumnWidth(3,5)
    self.dds_dummy.setFrameStyle(QFrame.NoFrame)

    #making first three columns vertically wider to fit with header 
    for i in range(3):
        self.dds_dummy.setSpan(0, i, 2, 1)
        self.dds_dummy.setItemDelegateForColumn(i,delegate)
    #Filling the left part of the DDS table
    self.dds_dummy.setItem(2, 0, QTableWidgetItem("0"))
    self.dds_dummy.setItem(2, 1, QTableWidgetItem(self.experiment.sequence[0].name))
    self.dds_dummy.setItem(2, 2, QTableWidgetItem(str(self.experiment.sequence[0].value)))


    #Dummy horizontal header (TOP SIDE OF THE TABLE)
    self.dds_dummy_header = QTableWidget(self.dds_tab_widget)
    self.dds_dummy_header.setGeometry(QRect(0.5,30,1905,60))
    self.dds_dummy_header.setColumnCount(self.dds_tab_num_cols)
    self.dds_dummy_header.horizontalHeader().setMinimumHeight(50)
    self.dds_dummy_header.verticalHeader().setVisible(False)
    self.dds_dummy_header.horizontalHeader().setVisible(False)
    self.dds_dummy_header.setRowCount(2) 
    self.dds_dummy_header.horizontalHeader().setMinimumSectionSize(0)
    self.dds_dummy_header.horizontalHeader().setFont(QFont('Arial', 12))
    self.dds_dummy_header.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_dummy_header.setFont(QFont('Arial', 12))
    self.dds_dummy_header.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS 
    self.dds_dummy_header.setColumnWidth(0,50) 
    self.dds_dummy_header.setColumnWidth(1,180)
    self.dds_dummy_header.setColumnWidth(2,100)

    #SHAPING THE TABLE
    for i in range(12):
        self.dds_dummy_header.setSpan(0,4 + 6*i, 1, 5) # stretching the title of the channel
        self.dds_dummy_header.setColumnWidth(3 + 6*i, 5) # making separation line thin
        self.dds_dummy_header.setColumnWidth(8 + 6*i, 45) # making state column smaller
        self.dds_dummy_header.setItemDelegateForColumn(3 + 6*i,delegate) #making separation line uneditable

    self.dds_dummy_header.setItemDelegateForRow(1, delegate) #making row number 2 uneditable

    #populating headers and separators
    for i in range(12):
        #separator
        self.dds_dummy_header.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
        self.dds_dummy_header.setItem(0,6*i + 3, QTableWidgetItem())
        self.dds_dummy_header.item(0, 6*i + 3).setBackground(QColor(100,100,100))
        #headers Channel
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        #headers Channel attributes (f, Amp, att, phase, state)
        self.dds_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

    self.dds_dummy_header.itemChanged.connect(self.dds_dummy_header_changed)

    #Making fixed corner (TOP LEFT SIDE OF THE TABLE)
    self.dds_fixed = QTableWidget(self.dds_tab_widget)
    self.dds_fixed.setGeometry(QRect(0.5,30, 335,60))
    self.dds_fixed.setColumnCount(4)
    self.dds_fixed.horizontalHeader().setMinimumHeight(50)
    self.dds_fixed.verticalHeader().setVisible(False)
    self.dds_fixed.horizontalHeader().setVisible(False)
    self.dds_fixed.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_fixed.horizontalHeader().setMinimumSectionSize(0)
    self.dds_fixed.setRowCount(2) 
    self.dds_fixed.setFont(QFont('Arial', 12))
    self.dds_fixed.setFrameStyle(QFrame.NoFrame)
    #SHAPING THE FIRST 3 COLUMNS
    self.dds_fixed.setColumnWidth(0,50)
    self.dds_fixed.setColumnWidth(1,180)
    self.dds_fixed.setColumnWidth(2,100)
    self.dds_fixed.setColumnWidth(3,5)
    #making first three columns vertically wider to fit with header 
    for i in range(4):
        self.dds_fixed.setSpan(0, i, 2, 1)
        self.dds_fixed.setItemDelegateForColumn(i,delegate)
    #Separator
    self.dds_fixed.setItem(0,3, QTableWidgetItem())
    self.dds_fixed.item(0,3).setBackground(QColor(100,100,100))
    #populating edge number, name and time
    for i in range(3):
        self.dds_fixed.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_fixed.item(0,i).setTextAlignment(Qt.AlignCenter)

    #MAKING VERTICAL SCROLL BARS COMMON FOR DDS TABLE
    self.dds_tables = [self.dds_table,self.dds_dummy,self.analog_table,self.analog_dummy, self.digital_table, self.digital_dummy, self.sequence_table]

    def move_other_scrollbars_vertical(idx,bar):
        scrollbars = {tbl.verticalScrollBar() for tbl in self.dds_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.dds_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dds_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.dds_tables:
        scrollbar = tbl.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_vertical(idx, bar))

    #MAKING HORIZONTAL SCROLL BARS COMMON FOR DDS TABLE
    self.dds_dummy_tables = [self.dds_table,self.dds_dummy_header]

    def move_other_scrollbars_horizontal(idx,bar):
        scrollbars = {tbl.horizontalScrollBar() for tbl in self.dds_dummy_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.dds_dummy_header.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dds_dummy_header.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.dds_dummy_tables:
        scrollbar = tbl.horizontalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars_horizontal(idx, bar))

    self.making_separator()


def variables_tab_build(self):
    #VARIABLES TAB WIDGET
    self.variables_tab_widget = QWidget()
    #VARIABLES LABLE
    variables_lable = QLabel(self.variables_tab_widget)
    variables_lable.setText("Variables")
    variables_lable.setFont(QFont('Arial', 14))
    variables_lable.setGeometry(85, 0, 1000, 30)

    #VARIABLES TAB LAYOUT
    self.variables_table = QTableWidget(self.variables_tab_widget)
    width_of_table_variables = 400
    self.variables_table.setGeometry(QRect(0, 30, width_of_table_variables, 1070))                                                #size of the table
    variables_num_columns = 2 #2 for proof of concept
    self.variables_table.setColumnCount(variables_num_columns)
    self.variables_table.setHorizontalHeaderLabels(["Variable", "Value"])
    self.variables_table.verticalHeader().setVisible(False)
    self.variables_table.horizontalHeader().setFixedHeight(50)
    self.variables_table.horizontalHeader().setFont(QFont('Arial', 12))
    self.variables_table.setFont(QFont('Arial', 12))
    self.variables_table.setColumnWidth(0,200)
    self.variables_table.setColumnWidth(1,198)
    #button to create new variable
    self.create_new_variable = QPushButton(self.variables_tab_widget)
    self.create_new_variable.setFont(QFont('Arial', 14))
    self.create_new_variable.setGeometry(width_of_table_variables + 50, 40, 200, 30)
    self.create_new_variable.setText("Create new variable")
    self.create_new_variable.clicked.connect(self.create_new_variable_clicked)
    #when table contents are changed
    self.variables_table.itemChanged.connect(self.variables_table_changed)
    #button to delete a variable
    self.delete_variable = QPushButton(self.variables_tab_widget)
    self.delete_variable.setFont(QFont('Arial', 14))
    self.delete_variable.setGeometry(width_of_table_variables + 50, 90, 200, 30)
    self.delete_variable.setText("Delete a variable")
    self.delete_variable.clicked.connect(self.delete_new_variable_clicked)






    

