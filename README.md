# Quantrol
Quantrol is a high level solution built on top of the open access Artiq infrastructure. It allows researchers to use most of the Artiq features without coding.
The current state of the GUI is adopted for the specific hardware used in Hosten group at Institure of Science and Technology Austria. However, it can be relatively easily adopted for any type of Sinara based hardware.

## Example of cooling sequence
Here is an example of the experimental description of the cooling sequence in Quantrol
![image](https://github.com/user-attachments/assets/8bad5e63-a737-473f-ac95-21885abd28a4)
![image](https://github.com/user-attachments/assets/1e735e6e-2473-488a-ad76-7f0c1559353c)
![image](https://github.com/user-attachments/assets/2079a59d-661d-4a17-992a-7f8632831262)

And a corresponding hardcoded version that Quantrol generates and runs is shown below:
![Code](https://github.com/user-attachments/assets/7194862f-944f-466b-b695-9390eb0d1008)
The Quantrol has 23 rows of a nice interpretable table instead of almost 300 lines of code that are hard to interpret.

## Python requirements
The GUI was written using python 9.x. At the time of writing this note, some PyQt features and syntax supported by python 9 are not supported by python >=10. 
	
At the time of writing this note, python has officially stopped distributing installers, and only has source files. 

Building python versions from source on windows can be a bit painful, so there is a neat package called pyenv which allows one to manage different python versions. 

See the github page of pyenv-win for more details.
https://github.com/pyenv-win/pyenv-win/blob/master/README.md#installation

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

### Starting Quantrol
Open VS Code, that is usually pinned to the task bar, or press Windows button and type VS code. Expand the VS code to the full size for easier navigation.

In the left top corner click the File tab and choose Open folder. Navigate to the Quantrol folder, that should be located on the Desktop.

After opening the Quantrol folder run the source_code.py file by clicking the run (triangle) in the right top corner. You should see the Quantrol application window.

### Quantrol application
![image](https://github.com/user-attachments/assets/f8e69350-b616-49ae-b183-730589f3ed4c)
Quantrol application window was not designed to be adaptive for different sizes. Only use it with the full screen (maximum allowed size). Most of the buttons and important things have user friendly descriptions. Hover the mouse over the element or a button of interest and the hint explaining its functionality will pop up as shown in the figure above. 

It is advised to read all the descriptions of each button before starting to work with Quantrol to avoid misuse and potential information loss!!!

The experimental sequence is being described in terms of time edges, each of which has the information of the changes that should be performed at different time stamps. Quantrol initializes itself with only single default Edge that can be overwritten by Save default button.

At the top left corner there are five different tabs. Quantrol initializes at the sequence tab by default and the user should go to different tabs to describe the experimental sequence.

### Sequence tab
To start experimental description press the Insert Edge button. You should see the new edge created as shown in the figure below.
![image](https://github.com/user-attachments/assets/a7f460fc-2058-4cb2-9c9e-c8e60cf969fa)
Each edge has a descriptive name, unique ID, time expression, and time value in ms. The name of the edge should tell the user the purpose of the edge. It can be something like "3D MOT loading start". Unique ID can be used to offset edges with respect to each other by using the corresponding ID as a variable in the time expression. Below you can see an example of edge "3D MOT loading end" being requested after 5000 ms following the "3D MOT loading start" edge with ID - id1. The edges are automatically being sorted in increasing order. It is therefore possible to stick edges between the previously defined ones. However, for easier interpretation it is advised to start experimental description from the beginning.
![image](https://github.com/user-attachments/assets/71033094-deef-4b22-a8dc-de971f39b8e0)
The edge following the default edge should not be requested at the same time as the default edge. Therefore first edge is at 1 ms. This is required to avoid requesting too many changes at single time stamp. More about it will be described later in this guide, but for more details please refer to the Artiq manual or ask someone more experienced.

As can be seen from the example above the time expression allows some mathematical expressions to be used. However, the user is not allowed to use brackets. In principle it allows basic addition, subtraction, multiplication, and division operations. More complicated expressions might cause issues as Quantrol allows using variables. Therefore, it is advised to keep it as simple as possible.

### Digital tab
![image](https://github.com/user-attachments/assets/feab481a-6f8c-4648-90a1-ff3d88746b34)
Digital tab is used to set the states of the digital channels at different time edges created in sequence tab. It allows only values 1 or 0 for high and low states of the channels. 

The color coding is used to help user quickly understand what sequence is supposed to do. The green color represents the states that user wants to turn ON, whereas red color is for turning OFF the channel. White background of the table entry means that there were no user requested changes at that particular time and the value represents the previously set state of the hardware. 

User can delete the edge by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

Digital channel titles can be updated by right clicking on them and typing in the name of the channel. In case the purpose of the channel was changed the default state should also be overwritten so the Quantrol will be initialized with the updated title names and default edge values.

### Analog tab
![image](https://github.com/user-attachments/assets/d0a67da4-990e-439f-b8ff-acaaf361f35f)
Analog tab is very similar to the Digital tab. The entries of analog tab represent the voltage in volts to be set to output from analog channels. 

It has very similar color coding scheme with green being non zero, red being zero, and white being the current state of the hardware without user request for changes. 

User can delete the edge by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

The precision of the analog channels was set to 1 micro volt. The user entry as a numeric value will be rounded up to the micro volt and the experimental description will be according to the value displayed in Quantrol. For example if the user tries to type in 0.123456789 it will be updated to 0.123456 and the python description will include 0.123456 instead of 0.123456789. 

Allowed values range for the analog channel are between -9.9 and 9.9 inclusive.

Title of the analog tab can be renamed same as in digital tab.

### DDS tab
![image](https://github.com/user-attachments/assets/7eb6bfce-6130-4eb9-937b-100f01884e44)
DDS tab is also similar to digital and analog tabs but a little more different. Each channel has five different self-explanatory names. State represents if the DDS channel should be ON or OFF

Green color of the edge means that the DDS channel should be turned ON, red color means that the DDS channel should be turned OFF, and white background just shows the current state of the DDS channel and means that the user did not request any changes at a given time.

User can delete the any edge parameter by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

Title names of the DDS channels can be modified as a simple texts.

### Description of DDS parameters
Frequency of the DDS should be within the 500 MHz range that is the half of the reference clock due to Nyquist criteria. Shortly, it requires at least two samples per cycle to reconstruct a desired output waveform. Approaching 400 MHz already shows a significant sideband.

Frequency of the DDS was measured to be up to 1 Hz level. However, the precision might be even better.

Amplitude of the DDS is between 1.0 and 0.0 with the precision of 0.001. It means if the user enters 0.123456789 it will be updated to 0.123. It was measured that the changes lower that can't be even registered on the spectrum analyzer.

Attenuation of the DDS is between 0.0 and 31.5 with the precision of 0.5. Lower attenuation will result in stronger output signals. Quantrol will round the user entries to the closest 0.5 step. For instance, 0.7 will be converted to 0.5 and 0.8 to 1. The reason for that is digital attenuation step being 0.5.

Phase of the DDS is between 0.0 and 360.0 with steps of 0.36 degrees as was empirically measured on oscilloscope.

State of the DDS turns the channel ON and OFF at 1 and 0 input values.

### Variables tab
![image](https://github.com/user-attachments/assets/22408a56-dd06-4bd7-a007-5b15d3bc0821)
Variables tab allows user to create new variables and then use them in parameters expressions. In the example above there are three new variables that are created by pressing Create new variable button. The last one was renamed into dt and its values was assigned to 10.0. Now this can be used for example to set a variable offset between time Edges as shown in the example below.
![image](https://github.com/user-attachments/assets/418cf9ce-b814-4914-a31f-2d54f3148bd0)
Now the user can change that time offset easily by changing the value of the dt variable in the variables tab. User can delete the unused variables by right clicking them in the variables tab and pressing Delete a variable button.

### Scanning variables
After a variable dt is created in the variables tab the user has an option to scan the variable. In order to do so, fist check the Scan checkbox in the sequence tab. Then press Add scanned variable button and rename it from None to the variable that needs to be scanned. Quantrol will not allow using variable names that has not been created in a variable tab. After that change the min and max values of the scan and enter the Number of steps. Quantrol will create an experimental sequence that will linearly space the variables between min and max values with number of points equal to the number of steps. In the example below it will make a scan for values 0, 1, 2, 3, 4, 5.
![image](https://github.com/user-attachments/assets/eb1988e3-b54c-4595-9592-e0417ed2cbe3)
Note that the value of the dt in the sequence tab changed from 10 to 0.0. This is done in order to be able to sort the time edges in the sequence tab. It was decided to leave the user the responsibility of making sure that during the scan, when scanned variable is used in time expression, the edges order will remain unaltered.

As written below the scan table it is also the user responsibility to make sure that the scan of the variables remains within the allowed values range. For example, if the variable Voff is used in the definition of analog channel as "Voff + 1.0" and the scan range is between 0 and 9 it falls out of the allowed range as 9 + 1 will be 10. In that case depending on the artiq version it might either ignore the request or throw an error and stop execution. Therefore, make sure that the variables scan range remains within allowed input values range.

### Go to Edge button
Go to edge button requires additional clarification compared to any other button. Although the names of the buttons appear as the same across multiple tabs their functionalities are a little different. Go to edge button is used to set the hardware state at the state described at the specific time stamp. It disregards whether the state requires any change at that particular time and will enforce each state as shown in the tables regardless of their colors. In order to go to the edge the user should press the edge row in the left part of the table as highlighted in the example below and then press Go to Edge button. Quantrol will create the go_to_edge.py experimental description and will run it to set the hardware. It is important to note that Go to Edge button will go to the last selected Edge at that particular tab. For example, if the user clicks the first edge in the sequence tab, then goes to the digital tab, selects there the second edge. The edge that the Go to Edge button will go when pressed will depend on the current tab. If the user is currently in the sequence tab it will go to the first edge and when the user goes to the digital tab and presses Go to Edge button it will go to the second edge. Shortly, Quantrol stores last selected edges in each tab and then goes there when the button is clicked at that tab.
![image](https://github.com/user-attachments/assets/65be40be-f3aa-4f43-bfb7-caf380ec1da3)

### Logger
![image](https://github.com/user-attachments/assets/7f777e27-cfc5-4182-9684-b94176cbcd76)
Pay attention to the logger. It says that after a power cycle of the sinara hardware the user should initialize it. This can be achieved by pressing Init. Hardware button. The logged might also say that the loading of the sequence was unsuccessful as well as run of the experiment. Although the logger is useful, VS Code terminal has more detailed information. There might be some errors that Quantrol logger does not catch.

### Saving sequences
The sequences should be saved in the Sequences folder which is located in the Quantrol folder. If there is no such folder existing please do create it and save sequences there. It is important as the GitHub repository for both cold atoms and hybrid experiment teams is the same. Quantrol was designed to be able to have common files to allow feature development for both setups at the same time and ignore the files that are specific to the experimental teams.

### Troubleshooting Quantrol
In case the user needs to troubleshoot the behavior of the Quantrol, first look at the VS Code terminal for warnings and errors. After that, check if the experimental description is correct. For example, for Init. hardware, Stop continuous run it is init_hardware.py, for Continuous run, Run experiment, Generate experiment, and Submit experiment it is run_experiment.py, and for Go_to_Edge it is go_to_edge.py. If the descriptions are correct, then check the direct output of the Quantrol. For example, if you want to turn ON the laser by driving an AOM with an RF signal and it didn't turn ON. Before blaming the Quantrol, check if it outputs what you requested. It might happen that the AOM drive amplifier is not powered making it impossible to drive the AOM from Quantrol. So always break down the process into smallest pieces and check every suspect one by one. It requires creative tests to isolate each of the components that might cause problem of the whole system operation. In most of the cases, Artiq guarantees all or nothing degree of precision. Therefore, if Quantrol generates correct experimental sequence descriptions, it is either the connection problem with the hardware or it might require a power cycle as some of the cards might be stuck in some weird state.

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
