# Quantrol

Quantrol is a high level solution built on top of the open access Artiq infrastructure. It allows researchers to use most of the Artiq features without coding.
The current state of the GUI is adopted for the specific hardware used in Hosten group at Institure of Science and Technology Austria. However, it can be relatively easily adopted for any type of Sinara based hardware.

## Installation

This program was built and has been used on Windows based OS. 
In order to get started simply copy the entire repository on your local machine. The program was tested with VS Code but other code editors might also work as well. Open the entire repository folder in VS Code to be able to use it properly.
Use Ctrl+Shift+P and type Python Interpreter. Chose the python you want to use. Make sure that you close the terminal and open it again for changes to take action. You can type which python to make sure that the correct python is used.
In the terminal of VS Code type following command to install the required libraries:

pip install -r requirements.txt

Alternatively, you can open the requirements.txt file and the pop-up window will suggest you to configure the virtual environment. After downloading the required libraries copy your device_db.py into the same folder and edit the config.py file to match your hardware. Since there might be different versions of cards, the way Quantrol generates python like experimental descriptions can be modified in write_to_python.py file.

Once device_db.py and config.py are set, run the source.py in order to start the program.

## User guide
Quantrol is a user friendly interface that helps describing experimental sequences without coding. 
It allows using simple mathematical expressions, define variables, scan multiple variables in a 1D scan, use default variables such as id0, id1, ... etc.

In order to describe the sequence user introduces time edges where the changes in the hardware state are required. 

In order to use or scan a variable, one first needs to create it in a variables tab. After that the user can add defined variables in mathematical expressions or Scanning table.

The color coding of the channel state is used for better visualization of the sequence. White background values show the previously set values and hence the current state of the hardware. Green and red background specifies the changes user introduced at a specific time edge.

The program was not optimized for adaptive resizing and was designed for the full window size use only.
Most of the important buttons have some descriptions. Simply hover the mouse of the button and read it carefully before using Quantrol.
![image](https://github.com/user-attachments/assets/77d4592d-d760-41c6-a12e-1dfd2940d377)
Experimental description is done in a form of a table of time edges. Each edge describes what changes in the digital, analog, and DDS outputs should be performed. An example of the far detuned cooling is shown below.
![digital](https://github.com/user-attachments/assets/49c4bad1-39ee-48b5-829e-0a4c9cdb46df)


And a corresponding hardcoded version that Quantrol generates and runs is shown below:
![Code](https://github.com/user-attachments/assets/7194862f-944f-466b-b695-9390eb0d1008)


## Developer guide
The entire description will all parameters is stored in an object self.experiment. Chart describing its parameters and their descriptions is shown below. Purple blocks are objects, yellow blocks are the parameters of objects, and green blocks are descriptions of those parameters.

![image](https://github.com/user-attachments/assets/961ba603-9d25-430d-8be5-7bb2a8c50788)


 ### Description of the logic behind some design decisions
 The user entered values are processed and stored in four forms 
	1) Expression used to evaluate the value
	2) Evaluation used in the python code to evaluate the value if it is not scanned and there is a specific value to be used for each variable in the expression
	3) Value of the parameter in case it is not scanned and there is a specific value to be used
	4) For python version that is going to be used in the python like description of the experimental sequence
The reason for evaluation being different from the expression is the ability of using the variables. Since the variable "delay" will be used as self.experiment.variables['delay'] there is a need of processing each variable accordingly and create an evaluation that can be executed to evaluate the parameter. The reason for having for_python is the ability of scanning variables. In case the parameter include a variable that is going to be scanned there is no specific value that is corresponding to that parameter. Instead the form such as scanned_variable_name is used as in the python like description there will be an iterable object that will be iterated over as "for a in self.a:". If the variable expression does not have any scanned variables, then the for_python is simply the value of the parameter.

### The need for variables and new_variables
Self.experiment.variables is a dictionary of all variables including the default variables that are created when the new edge is being inserted (id0, id1, etc.). The use of dictionaries is good for faster retrieval of the variable values. However, it does not preserve any ordering that is required in rebuilding the variables tab. Otherwise, each time the variable is being created the order will be randomly changing, that might be confusing for the user. I could have used ordered dictionary, but self.experiment.new_variables proved to be useful to store the ordered user defined variables is handy when the variable is being scanned. When a variable is chosen to be scanned its value for the sorting of sequence table is being assigned to be the minimum value of the scanning range. However, after the tests with the scan one would like to retrieve the value of the variable that was used prior to scanning it. Self.experiment.new_variables comes handy as variables previous values can be easily retrieved from there.

### Updating of the for_python
For_python is only being updated only when the run experiment button is pressed. This was done to avoid decoding of each expression present in the experimental sequence to find out if the expression including the scanned variable or not. Since the for_python is only used when the python like description is being generated. This might confuse the developer as some of the for_python values might appear as not being updated.

## Description of the files and their relation to each other
The program consists of several files that will be described in this section. 

### config.py
The config file contains the information that is specific to the hardware. The contents have self-explanatory names. Number of channels, name of artiq environment, analog card type can be set in a config file.

### source_code.py
The main file is the source_code.py It initializes the artiq server, communicates with the scheduler, creates and displays the main window, defines used objects such as self.experiment, self.edge, ... etc. And finally, it has many utility functions that are used when buttons are clicked or entries are changed.

### tabs.py
The tabs.py is a file that is used to build all tabs. It has a description of tables, buttons and their relative orientations. 

### update.py
The update.py is a file that consists of fairly optimized udpating functions that are required in different cases. 

### write_to_python.py
The write_to_python.py is a file that consists of functions required to generate the python like description of the experimental sequence.

### run_experiment.py 
The file is generated and updated by Quantrol. It is a python like description of the experimental sequence. In order to change the way it is being generated modify write_to_python.py file.

### go_to_edge.py
The file is generated and updated by Quantrol. It is a python like description of the experimental sequence that sets the hardware at a specific state. In order to change the way it is being generated modify write_to_python.py file.

### init_hardware.py
The file is generated and updated by Quantrol. It is a python like desciprion of the experiment that initializes the hardware and sets its state to the defaul edge values. The user should initialize the hardware every time after power cycling Sinara hardware. In order to add different objects modify the write_to_python.py file.

## License
This is an open source project that was developed for the use in Hosten group (https://hostenlab.pages.ist.ac.at/). It was made public as we believed that other groups might benefit from what we have built.
Please keep in mind that there might still be minor bugs. We would appreciate your input on making Quantrol better.
