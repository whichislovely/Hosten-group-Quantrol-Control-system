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
    self.sequence_table.setHorizontalHeaderLabels(["#", "Name","ID", "Time expression","Time (ms)"])
    self.sequence_table.verticalHeader().setVisible(False)
    self.sequence_table.horizontalHeader().setFixedHeight(50)
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
    #self.sequence_table.setItemDelegateForRow(0,delegate)
    
    #button to save current sequence
    self.save_sequence_as_button = QPushButton(self.sequence_tab_widget)
    self.save_sequence_as_button.setFont(QFont('Arial', 14))
    self.save_sequence_as_button.setGeometry(width_of_table + 50, 50, 200, 30)
    self.save_sequence_as_button.setText("Save sequence")
    self.save_sequence_as_button.clicked.connect(self.save_sequence_button_clicked)
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

     #DROP DOWN MENU FOR VARIABLE SELECTION
    self.scan_drop_down = QComboBox()
    self.scan_drop_down.setFont(QFont("Arial", 14))
    self.scan_drop_down.setMinimumWidth(200)
    self.scan_drop_down.addItem("None")
    self.scan_drop_down.currentTextChanged.connect(self.scan_drop_down_changed)
    #Table of parameters
    self.scan_table_parameters = QTableWidget()
    self.scan_table_parameters.setColumnCount(4)
    self.scan_table_parameters.setRowCount(1)
    self.scan_table_parameters.verticalHeader().setVisible(False)
    self.scan_table_parameters.setFont(QFont("Arial", 14))
    self.scan_table_parameters.setHorizontalHeaderLabels(["Variable","Min value", "Max value", "Step"])
    self.scan_table_parameters.setColumnWidth(0,200)
    self.scan_table_parameters.setColumnWidth(1,150)
    self.scan_table_parameters.setColumnWidth(2,150)
    self.scan_table_parameters.setColumnWidth(3,150)
    self.scan_table_parameters.setItem(0,1, QTableWidgetItem(str(0)))
    self.scan_table_parameters.setItem(0,2, QTableWidgetItem(str(0)))
    self.scan_table_parameters.setItem(0,3, QTableWidgetItem(str(0)))
    self.scan_table_parameters.itemChanged.connect(self.scan_table_parameters_changed)
    #SCAN PARAMETERS
    self.scan_table = QGroupBox(self.sequence_tab_widget)
    self.scan_table.setTitle("Scan")
    self.scan_table.setCheckable(True)
    self.scan_table.setChecked(False)
    hBox = QHBoxLayout()
    self.scan_table.setLayout(hBox)
    hBox.addWidget(self.scan_table_parameters)
    self.scan_table.setFont(QFont("Arial", 14))
    self.scan_table.setGeometry(1100, 30, 675, 200)
    self.scan_table.toggled.connect(self.scan_table_checked)
    self.scan_table_parameters.setCellWidget(0,0,self.scan_drop_down)   


# DIGITAL TAB
def digital_tab_build(self):
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
    self.digital_table.setHorizontalHeaderLabels(self.experiment.title_digital_tab)
    self.digital_table.verticalHeader().setVisible(False)
    self.digital_table.horizontalHeader().setFixedHeight(50)
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
        exec("self.digital_table.setColumnWidth(%d,%d)" % (i, self.table_column_width))
    self.digital_table.itemChanged.connect(self.digital_table_changed)
    self.digital_table.horizontalHeader().sectionClicked.connect(self.digital_table_header_clicked)
    #Dummy table that will display edge number, name and time and will be fixed
    self.digital_dummy = QTableWidget(self.digital_tab_widget)
    self.digital_dummy.setGeometry(QRect(0.5, 30, 327, 1053))
    self.digital_dummy.setColumnCount(3)
    self.digital_dummy.setHorizontalHeaderLabels(self.experiment.title_digital_tab[0:3])
    self.digital_dummy.verticalHeader().setVisible(False)
    self.digital_dummy.horizontalHeader().setFixedHeight(50)
    self.digital_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.digital_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.digital_dummy.setFont(QFont('Arial', 12))
    self.digital_dummy.setColumnWidth(0,50)
    self.digital_dummy.setColumnWidth(1,180)
    self.digital_dummy.setColumnWidth(2,100)
    self.digital_dummy.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.digital_dummy.setItemDelegateForColumn(%d,delegate)" %_)

    self.digital_tables = [self.digital_table,self.digital_dummy]

    def move_other_scrollbars(idx,bar):
        scrollbars = {tbl.verticalScrollBar() for tbl in self.digital_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.digital_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.digital_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.digital_tables:
        scrollbar = tbl.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars(idx, bar))


#ANALOG TAB
def analog_tab_build(self):
    self.analog_tab_widget = QWidget()
    analog_lable = QLabel(self.analog_tab_widget)
    analog_lable.setText("Analog channels")
    analog_lable.setFont(QFont('Arial', 14))
    analog_lable.setGeometry(85, 0, 400, 30)


    #ANALOG TAB LAYOUT
    self.analog_table = QTableWidget(self.analog_tab_widget)
    self.analog_table.setGeometry(QRect(0, 30, 1905, 1070))  
    self.analog_table.setColumnCount(self.analog_tab_num_cols) 
    self.analog_table.setHorizontalHeaderLabels(self.experiment.title_analog_tab)
    self.analog_table.verticalHeader().setVisible(False)
    self.analog_table.horizontalHeader().setFixedHeight(50)
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
        exec("self.analog_table.setColumnWidth(%d,%d)" % (i,self.table_column_width))
    self.analog_table.itemChanged.connect(self.analog_table_changed)
    self.analog_table.horizontalHeader().sectionClicked.connect(self.analog_table_header_clicked)

    #Dummy table that will display edge number, name and time and will be fixed
    self.analog_dummy = QTableWidget(self.analog_tab_widget)
    self.analog_dummy.setGeometry(QRect(0.5,30, 327,1053))
    self.analog_dummy.setColumnCount(3)
    self.analog_dummy.setHorizontalHeaderLabels(self.experiment.title_analog_tab[0:3])
    self.analog_dummy.verticalHeader().setVisible(False)
    self.analog_dummy.horizontalHeader().setFixedHeight(50)
    self.analog_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.analog_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.analog_dummy.setFont(QFont('Arial', 12))
    self.analog_dummy.setColumnWidth(0,50)
    self.analog_dummy.setColumnWidth(1,180)
    self.analog_dummy.setColumnWidth(2,100)
    self.analog_dummy.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    for _ in range(3):
        exec("self.analog_dummy.setItemDelegateForColumn(%d,delegate)" %_)

    self.analog_tables = [self.analog_table,self.analog_dummy]

    def move_other_scrollbars(idx,bar):
        scrollbars = {tbl.verticalScrollBar() for tbl in self.analog_tables}
        scrollbars.remove(bar)
        for bar in scrollbars:
            bar.setValue(idx)
        
    self.analog_dummy.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.analog_dummy.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    for tbl in self.analog_tables:
        scrollbar = tbl.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda idx,bar=scrollbar: move_other_scrollbars(idx, bar))

def dds_tab_build(self):
    self.dds_tab_widget = QWidget()
    dds_lable = QLabel(self.dds_tab_widget)
    dds_lable.setText("Dds channels")
    dds_lable.setFont(QFont('Arial', 14))
    dds_lable.setGeometry(85, 0, 400, 30)
    self.sequence_num_rows = len(self.experiment.sequence)
    
    #dds TAB LAYOUT
    self.dds_table = QTableWidget(self.dds_tab_widget)
    self.dds_table.setGeometry(QRect(0.5, 30, 1905, 1070))
    self.dds_table.setColumnCount(self.dds_tab_num_cols)
    self.dds_table.horizontalHeader().setMinimumHeight(50)
    self.dds_table.verticalHeader().setVisible(False)
    self.dds_table.horizontalHeader().setVisible(False)
    self.dds_table.setRowCount(5) # 5 is an arbitrary number we just need to have rows in order to span them
    self.dds_table.horizontalHeader().setMinimumSectionSize(0)
    self.dds_table.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    #self.dds_table.setSpan(row,col, rowspan, colspan)
    for i in range(12):
        self.dds_table.setSpan(0,4 + 6*i, 1, 5)
        self.dds_table.setColumnWidth(3 + 6*i, 5)
        self.dds_table.setColumnWidth(8 + 6*i, 45)
        self.dds_table.setItemDelegateForColumn(3 + 6*i,delegate)
    #making first three columns wider to fit with header 
    for i in range(3):
        self.dds_table.setSpan(0, i, 2, 1)
        self.dds_table.setItemDelegateForColumn(i,delegate)

    self.dds_table.setFont(QFont('Arial', 12))
    self.dds_table.setColumnWidth(0,50)
    self.dds_table.setColumnWidth(1,180)
    self.dds_table.setColumnWidth(2,100)

    self.dds_table.itemChanged.connect(self.dds_table_changed)
    #self.dds_table.horizontalHeader().sectionClicked.connect(self.dds_table_header_clicked)

    #Dummy table that will display edge number, name and time and will be fixed
    self.dds_dummy = QTableWidget(self.dds_tab_widget)
    self.dds_dummy.setGeometry(QRect(0.5,30,335,1053))
    self.dds_dummy.setColumnCount(4)
    self.dds_dummy.horizontalHeader().setMinimumHeight(50)
    self.dds_dummy.verticalHeader().setVisible(False)
    self.dds_dummy.horizontalHeader().setVisible(False)
    self.dds_dummy.setRowCount(5) # 5 is an arbitrary number we just need to have rows in order to span them
    self.dds_dummy.horizontalHeader().setMinimumSectionSize(0)
    self.dds_dummy.horizontalHeader().setFont(QFont('Arial', 12))
    self.dds_dummy.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.dds_dummy.setFont(QFont('Arial', 12))
    self.dds_dummy.setColumnWidth(0,50)
    self.dds_dummy.setColumnWidth(1,180)
    self.dds_dummy.setColumnWidth(2,100)
    self.dds_dummy.setColumnWidth(3,5)

    #self.dds_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #self.dds_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    self.dds_dummy.setFrameStyle(QFrame.NoFrame)
    delegate = ReadOnlyDelegate(self)
    #making first three columns wider to fit with header 
    #self.dds_dummy.setSpan(row,col, rowspan, colspan)
    for i in range(3):
        self.dds_dummy.setSpan(0, i, 2, 1)
        self.dds_dummy.setItemDelegateForColumn(i,delegate)

    self.dds_tables = [self.dds_table,self.dds_dummy]

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

    #Dummy horizontal header 
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
    #self.dds_table.setSpan(row,col, rowspan, colspan)
    for i in range(12):
        self.dds_dummy_header.setSpan(0,4 + 6*i, 1, 5)
        self.dds_dummy_header.setColumnWidth(3 + 6*i, 5)
        self.dds_dummy_header.setColumnWidth(8 + 6*i, 45)
        self.dds_dummy_header.setItemDelegateForColumn(3 + 6*i,delegate)
    #making first three columns wider to fit with header 
    for i in range(3):
        self.dds_dummy_header.setSpan(0, i, 2, 1)
        self.dds_dummy_header.setItemDelegateForColumn(i,delegate)
    #populating edge number, name and time
    for i in range(3):
        self.dds_dummy_header.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_dummy_header.item(0,i).setTextAlignment(Qt.AlignCenter)

    #self.dds_dummy_header.setItemDelegateForRow(1, delegate)
    self.dds_table.setItemDelegateForRow(2, delegate)

    self.dds_dummy_header.setColumnWidth(0,50)
    self.dds_dummy_header.setColumnWidth(1,180)
    self.dds_dummy_header.setColumnWidth(2,100)

    

    #populating headers and separators
    for i in range(12):
        self.dds_dummy_header.setItem(0,6*i+4, QTableWidgetItem(str(self.experiment.title_dds_tab[i+4])))
        self.dds_dummy_header.item(0,6*i+4).setTextAlignment(Qt.AlignCenter)
        self.dds_dummy_header.setSpan(0, 6*i + 3, self.sequence_num_rows+2, 1)
        self.dds_dummy_header.setItem(0,6*i + 3, QTableWidgetItem())
        self.dds_dummy_header.item(0, 6*i + 3).setBackground(QColor(100,100,100))
        self.dds_dummy_header.setItem(1,6*i+4, QTableWidgetItem('f (MHz)'))
        self.dds_dummy_header.setItem(1,6*i+5, QTableWidgetItem('Amp (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+6, QTableWidgetItem('Att (dBm)'))
        self.dds_dummy_header.setItem(1,6*i+7, QTableWidgetItem('phase (deg)'))
        self.dds_dummy_header.setItem(1,6*i+8, QTableWidgetItem('state'))

    self.dds_dummy_header.itemChanged.connect(self.dds_dummy_header_changed)

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

    #Making fixed corner
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
    #making first three columns wider to fit with header 
    for i in range(4):
        self.dds_fixed.setSpan(0, i, 2, 1)
        self.dds_fixed.setItemDelegateForColumn(i,delegate)
    #populating edge number, name and time
    for i in range(3):
        self.dds_fixed.setItem(0,i, QTableWidgetItem(str(self.experiment.title_dds_tab[i])))
        self.dds_fixed.item(0,i).setTextAlignment(Qt.AlignCenter)
    
    self.dds_fixed.setColumnWidth(0,50)
    self.dds_fixed.setColumnWidth(1,180)
    self.dds_fixed.setColumnWidth(2,100)
    self.dds_fixed.setColumnWidth(3,5)
    self.dds_fixed.setItem(0,3, QTableWidgetItem())
    self.dds_fixed.item(0,3).setBackground(QColor(100,100,100))

    self.dds_fixed.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dds_fixed.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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






    

