# Quantrol
Quantrol is a high level solution built on top of the open access Artiq infrastructure. It allows researchers to use most of the Artiq features without coding.
The current state of the GUI is adopted for the specific hardware used in Hosten group at Institure of Science and Technology Austria. However, it can be relatively easily adopted for other types of Sinara based hardware.

## Example of cooling sequence   
Here is an example of the experimental description of the cooling sequence in Quantrol  

![image](https://github.com/user-attachments/assets/8bad5e63-a737-473f-ac95-21885abd28a4)
![image](https://github.com/user-attachments/assets/1e735e6e-2473-488a-ad76-7f0c1559353c)
![image](https://github.com/user-attachments/assets/2079a59d-661d-4a17-992a-7f8632831262)

And a corresponding hardcoded version that Quantrol generates and runs is shown below.

![Code](https://github.com/user-attachments/assets/7194862f-944f-466b-b695-9390eb0d1008)

The Quantrol has 23 rows of a nice interpretable table instead of almost 300 lines of code that are hard to interpret.

## Python requirements
The GUI was written using python 9.x. At the time of writing this note, some PyQt features and syntax supported by python 9 are not supported by python >=10. 
	
At the time of writing this note, python has officially stopped distributing installers, and only has source files. 

Building python versions from source on windows can be a bit painful, so there is a neat package called pyenv which allows one to manage different python versions. 

See the github page of pyenv-win for more details.

https://github.com/pyenv-win/pyenv-win/blob/master/README.md#installation

## Repository versions
There are three branches in this repository. Quantrol.1.0 is a more stable version that has only the basic functionality of running experiments according to the edge-like structure of the description. Quantrol 2.0 is a newer version that was quickly done and hence might have some bugs. However, it includes features as derived variables, lookup variables, mirny card, and slow DDS. Main branch is the Quantrol.2.0 version and should be The latest updated.

## Installation
This program was built and has been used on Windows based OS. 
In order to get started simply copy the entire repository on your local machine. The program was tested with VS Code but other code editors might also work as well. Open the entire repository folder in VS Code to be able to use it properly.
Use Ctrl+Shift+P and type 'Python Interpreter'. Chose the python you want to use. It doesn't have to include Artiq to operate. Make sure that you close the terminal and open it again for changes to take action. You can type which python to make sure that the correct python is used.
In the terminal of VS Code type following command to install the required libraries:

pip install -r requirements.txt

Alternatively, you can open the requirements.txt file and the pop-up window will suggest you to configure the virtual environment. After downloading the required libraries copy your device_db.py into the same folder and edit the config.py file to match your hardware. Since there might be different versions of cards, the way Quantrol generates python like experimental descriptions can be modified in write_to_python.py file.

Once device_db.py and config.py are set, run the source.py in order to start the program. For the first time run there will be a warning that will create a Default state according to your config.py. This is normal and should not appear in the following runs.

# User guide
Quantrol is a user friendly interface that helps describing experimental sequences without coding. 
It allows using simple mathematical expressions, define variables, scan multiple variables in a 1D scan, use default variables such as id0, id1, ..., request derived variables through RPC, load a lookup lists, etc.

## Starting Quantrol
Open VS Code, that is usually pinned to the task bar, or press Windows button and type VS code. Expand the VS code to the full size for easier navigation.

In the left top corner click the File tab and choose Open folder. Navigate to the Quantrol folder, that should be located on the Desktop.

After opening the Quantrol folder run the source_code.py file by clicking the run (triangle) in the right top corner. You should see the Quantrol application window.

## Quantrol application

![image](https://github.com/user-attachments/assets/f8e69350-b616-49ae-b183-730589f3ed4c)

Quantrol application window was not designed to be adaptive for different sizes. Only use it with the full screen (maximum allowed size). It might not appear well on the laptops, therefore large lab screens should be used. Most of the buttons and important things have user friendly descriptions. Hover the mouse over the element or a button of interest and the hint explaining its functionality will pop up as shown in the figure above. 

It is advised to read all the descriptions of each button before starting to work with Quantrol to avoid misuse and potential information loss!!!

The experimental sequence is being described in terms of time Edges, each of which has the information of the changes that should be performed at different time stamps. Quantrol initializes itself with only single default Edge that can be overwritten by Save default button.

At the top left corner there are multiple tabs that will depend on the presence of different Sinara cards specified in the config.py. Quantrol initializes at the sequence tab by default and the user should go to different tabs to describe the experimental sequence.

## Sequence tab
To start experimental description press the Insert Edge button. You should see the new Edge created as shown in the figure below.

![image](https://github.com/user-attachments/assets/a7f460fc-2058-4cb2-9c9e-c8e60cf969fa)

Each Edge has a descriptive name, unique ID, time expression, and time value in ms. The name of the Edge should tell the user the purpose of the Edge. It can be something like "3D MOT loading start". Unique ID can be used to offset Edges with respect to each other by using the corresponding ID as a variable in the time expression. Below you can see an example of Edge "3D MOT loading end" being requested after 5000 ms following the "3D MOT loading start" Edge with ID - id1. The Edges are automatically being sorted in increasing order. It is therefore possible to stick Edges between the previously defined ones. However, for easier interpretation it is advised to start experimental description from top to bottom. In other words, from the beginning to the end.

![image](https://github.com/user-attachments/assets/71033094-deef-4b22-a8dc-de971f39b8e0)

The Edge following the default Edge should not be requested at the same time as the default Edge. Therefore first Edge is at 1 ms. This is required to avoid requesting too many changes at single time stamp. More about it will be described later in this guide, but for more details please refer to the Artiq manual or ask someone more experienced.

As can be seen from the example above the time expression allows some mathematical expressions to be used. However, the user is not allowed to use brackets. In principle it allows basic addition, subtraction, multiplication, and division operations. More complicated expressions might cause issues as Quantrol allows using variables. Therefore, it is advised to keep it as simple as possible.

## Digital tab

![image](https://github.com/user-attachments/assets/feab481a-6f8c-4648-90a1-ff3d88746b34)

Digital tab is used to set the states of the digital channels at different time Edges created in sequence tab. It allows only values 1 or 0 for high and low states of the channels. 

The color coding is used to help user quickly understand the purpose of the sequence. Green color represents the channels that user wants to turn ON, whereas red color is for turning OFF the channel. White background of the table entry means that there were no user requested changes at that particular time and the value represents the previously set state of the hardware. By hovering the mouse over the channel user can see it value.

User can delete the Edge by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

Digital channel titles can be updated by right clicking on them and typing in the name of the channel. In case the purpose of the channel was changed the default state should also be overwritten so the Quantrol will be initialized with the updated title names and default Edge values.

## Analog tab

![image](https://github.com/user-attachments/assets/d0a67da4-990e-439f-b8ff-acaaf361f35f)

Analog tab is very similar to the Digital tab. The entries of analog tab represent the voltage in volts to be set to output from analog channels. 

It has very similar color coding scheme with green being non zero, red being zero, and white being the current state of the hardware without user request for changes. 

User can delete the Edge by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

The precision of the analog channels was set to 1 micro volt. The user entry as a numeric value will be rounded up to the micro volt and the experimental description will be according to the value displayed in Quantrol. For example if the user tries to type in 0.123456789 it will be updated to 0.123456 and the python description will include 0.123456 instead of 0.123456789. 

Allowed values range for the analog channel are between -9.9 and 9.9 inclusive.

Titles of the analog tab can be renamed in a same way as in digital tab.

## DDS tab

![image](https://github.com/user-attachments/assets/7eb6bfce-6130-4eb9-937b-100f01884e44)

DDS tab is also similar to digital and analog tabs but a little more different. Each channel has five different parameters. 

Green color of the Edge means that the DDS channel should be turned ON, red color means that the DDS channel should be turned OFF, and white background just shows the current state of the DDS channel and means that the user did not request any changes at a given time.

User can delete the any Edge parameter by entering an empty ("") text as the input in order to remove any change requests from the particular channel at given time. Quantrol will automatically display the previously set state in the table. 

Title names of the DDS channels can be modified as a simple texts.

### Description of DDS parameters
Frequency of the DDS should be within half of the reference clock due to Nyquist criteria. Shortly, it requires at least two samples per cycle to reconstruct a desired output waveform. For our setup with 1 GHz reference clock frequencies the output close to 400 MHz already show significant sidebands.

Frequency precision of the DDS was measured to be up to 1 Hz level. However, the precision might be even better and therefore Quantrol does not regulate the user entry.

Amplitude of the DDS is between 1.0 and 0.0 with the precision of 0.001 that was verified impirically by measuring the signal amplitude on a spectrum analyzer. It means if the user enters 0.123456789 it will be updated to 0.123. It was implemented to prevent user from requesting more than the hardware can provide and being fooled assumging that the hardware is set to the precision beyond its capabilities.

Attenuation of the DDS is between 0.0 and 31.5 with the precision of 0.5. Lower attenuation will result in stronger output signals. Quantrol will round the user entries to the closest 0.5 step. For instance, 0.7 will be converted to 0.5 and 0.8 to 1. The reason for that is because digital attenuation of Sinara hardware allows smallest step to be 0.5.

Phase of the DDS is between 0.0 and 360.0 with steps of 0.36 degrees as was empirically measured on oscilloscope.

State of the DDS turns the channel ON and OFF at 1 and 0 input values.

## Mirny tab
Mirny tab has exactly the same appearance and functionality as DDS tab. It was adapted from DDS tab in order to quickly include the functionality of Mirny into Quantrol. However, AFAICT mirny only supports the frequency, attenuation and state parameters. Therefore, amp and phase are not being considered and in principle should be removed from mirny tab.

## Sampler tab
Sampler tab is used to request sampling by entring the variable name in the corresponding channel at the required time edge. There is a delay between the request of sampling and actual assignment to the variable before it can be used in parameter expression. It is a user responsibility to make sure that there is a sufficient delay. In our lab we found that 160 us is a sufficient delay, but this might depend on different factors. An example of requesting to assign the S2 channel value to the transmission variable is shown below

![image](https://github.com/user-attachments/assets/831efbb9-fc4a-4573-943e-0b36b5c1dd33)

## Variables tab

![image](https://github.com/user-attachments/assets/794fcc86-e001-4754-a35d-02e983e059d4)

Variables tab allows user to create constant, derived, and lookup variables and them in parameters expressions. Their purpose and application example will be described in details below.

### Constant variables
In the example above there are three constant variables that are created by pressing Create new variable button. The second one was renamed to dt and its value was assigned to 10.0. Since this are constant variables their values allow only integers and floating numbers as an input. After declaring dt variable, it can be used in the sequence time expressions or any channel state description. For example to set a variable offset between time Edges as shown in the example below.

![image](https://github.com/user-attachments/assets/61f5ab39-a416-4ed0-988d-b4fa8bd52e61)


It allows user to change the time offset easily by changing the value of the dt variable in the variables tab. Same variables can be used in multiple places. For example, the user can create a constant variable "state" for several channels that should turn ON and OFF together and then toggle their state in variables tab. User can delete the unused variables by right clicking them in the variables tab and pressing Delete variable button.

Third variable in the constant variables table that is called input_a is indicated of being sampled. It was specified in the Sampler tab as shown below.

![image](https://github.com/user-attachments/assets/6be2c466-9590-4b83-9f7a-f944b86409e0)

That sampled variable can now be used as a variable in the expression. One can set the output of analog channel to be "- input_a * 2" to output some proportional feedback. For more compled feedback signals the sampled variable can be used as an argument in derived variables and lookup variables tables.

### Derived variables
Derived varible is a variable that is used to assign the return from the remote procedure call of an arbitrarily complex function. In the example shown below derived_shift variable will take input_a as an argument to calculate cosine of input_a through RPC. Edge id is the time edge at which the user wants to request the RPC call. Note that the delay required between the request and response can vary depending on the communication lattency and computational complexity of the calculation. It is a user responsibility to adjust the delay before derived_shift can be used to avoid Underflow errors. Simply increase the delay until it reliably executes without errors.

![image](https://github.com/user-attachments/assets/61f5ab39-a416-4ed0-988d-b4fa8bd52e61)

Below is the analog tab where we use the derived variable derived_shift to output the 0-th analog channel. The Cyan color indicating that the channel is a derived variable.

![image](https://github.com/user-attachments/assets/1d0ae330-cd3f-4ec0-af50-de5f80ec1eef)


The result of the sequence execution in terms of the python like description is shown below excluding the default edge for better interpretation.

![image](https://github.com/user-attachments/assets/3e910a31-6080-4dcb-9279-104daeac9a66)

Due to the communication lattencies of about 250 us we developed a lookup variables in order to allow faster real time responses/

### Lookup variables
Lookup variable is a variable that takes in a sampled variable as argument, converts it into the index and accesses value at that index in the lookup list. In order to load the lookup list for the lookup variable first right click the variable and then click Load lookup list button. Then navigate to the corresponding mat file that contains an array and press ok. The exact conversion of the input into the index of the lookup list should be done in the "def decode_input(self):" function in the source_code.py. The lookup list resolution should be done accordingly together with the input to index conversion. Quantrol will save the array state at the moment of loading lookup list. Later when the python description is being generated a corresponding array will be saved in the ./temp lookup variables folder and loaded to the core. An example of the use is shown below.

![image](https://github.com/user-attachments/assets/54011577-c749-427b-8ed7-7d7a7aeb6d5c)

And the corresponding python description is as following.

![image](https://github.com/user-attachments/assets/57a18ea9-be33-4b64-b089-173e060efb57)

## Slow DDS
Slow DDS tab is used for the urukul cards that do not have the digital switch capabilities. Such urukul cards can be spotted in the device_db.py as having no "ttl_urukul#_sw#". It can be used as a regular function generator and do not guarantee the time presision. In the example below there are four slow dds channels with parameters same as normal DDS. The button is used to create experimental description and set the states of slow DDS channels. Note that Quantrol uses artiq_run that will interrupt the current running experiment. So press Set slow DDS states when sure that no experiment is running.

![image](https://github.com/user-attachments/assets/ca24620a-edd0-4d4e-8c17-0e32e5338b52)


## Scanning variables
After a constant variable dt is created in the variables tab the user has an option to scan the variable. In order to do so, fist check the Scan checkbox in the sequence tab. Then press Add scanned variable button and rename it from None to the variable that needs to be scanned. Quantrol will not allow using variable names that has not been created in the variable tab. After that change the min and max values of the scan and enter the Number of steps. Quantrol will create an experimental sequence that will linearly span the variables values between its min and max values inclusively with number of steps. In the example below it will make a scan for values 0, 1, 2, 3, 4, 5.

![image](https://github.com/user-attachments/assets/eb1988e3-b54c-4595-9592-e0417ed2cbe3)

Note that the value of the dt in the sequence tab changed from 10 to 0.0. This is done in order to be able to sort the time Edges in the sequence tab. It was decided to leave the user the responsibility of making sure that during the scan, when scanned variable is used in time expression, the Edges order will remain unaltered.

As written below the scan table it is also the user responsibility to make sure that the scan of the variables remains within the allowed values range. For example, if the variable Voff is used in the definition of analog channel as "Voff + 1.0" and the scan range is between 0 and 9 it falls out of the allowed range as 9 + 1 will be 10. In that case depending on the artiq version it might either ignore the request or throw an error and stop execution. Therefore, make sure that the variables scan range remains within allowed input values range.

## Go to Edge button
Go to Edge button requires additional clarification compared to any other button. Although the names of the buttons appear as the same across multiple tabs their functionalities are a little different. Go to Edge button is used to set the hardware state at the state described at the specific time stamp. It disregards whether the state requires any change at that particular time and will enforce each state as shown in the tables regardless of their colors. In order to go to the Edge, the user should press the Edge row in the left part of the table as highlighted in the example below and then press Go to Edge button. Quantrol will create the go_to_edge.py experimental description and will run it to set the hardware. It is important to note that Go to Edge button will go to the last selected Edge at that particular tab. For example, if the user clicks the first Edge in the sequence tab, then goes to the digital tab, selects there the second Edge. The Edge that the Go to Edge button will go when pressed will depend on the current tab. If the user is currently in the sequence tab it will go to the first Edge and when the user goes to the digital tab and presses Go to Edge button it will go to the second Edge. Shortly, Quantrol stores last selected Edges in each tab and then goes there when the button is clicked at that tab. The Edge will be highlighted by green color to let the user know which Edge the hardware was set to.

![image](https://github.com/user-attachments/assets/65be40be-f3aa-4f43-bfb7-caf380ec1da3)

## Logger

![image](https://github.com/user-attachments/assets/7f777e27-cfc5-4182-9684-b94176cbcd76)

Pay attention to the logger. It says that after a power cycle of the sinara hardware the user should initialize it. This can be achieved by pressing Init. Hardware button. The logged might also say that the loading of the sequence was unsuccessful as well as run of the experiment. Although the logger is useful, VS Code terminal has more detailed information. There might be some errors that Quantrol logger does not catch.

## Saving sequences
In Hosten lab the sequences should be saved in the Sequences folder which is located in the Quantrol folder. If there is no such folder existing please do create it and save sequences there. It is important as the GitHub repository for both cold atoms and hybrid experiment teams is the same. Quantrol was designed to be able to have common files to allow feature development for both setups at the same time and ignore the files that are specific to the experimental teams.

## Troubleshooting Quantrol
In case the user needs to troubleshoot the behavior of the Quantrol, first look at the VS Code terminal for warnings and errors. After that, check if the experimental description is correct. For example, for Init. hardware, Stop continuous run buttons it is init_hardware.py, for Continuous run, Run experiment, Generate experiment, and Submit experiment buttons it is run_experiment.py, and for Go to Edge button it is go_to_edge.py. If the descriptions are correct, then check the direct output of the Quantrol. For example, if you want to turn ON the laser by driving an AOM with an RF signal and it didn't turn ON. Before blaming the Quantrol, check if it outputs what you requested. It might happen that the AOM drive amplifier is not powered, making it impossible to drive the AOM from Quantrol. So always break down the process into smallest components and check every suspect one by one. It requires creative tests to isolate each of the components that might disrupt the operation of the whole system. However, in most of the cases, Artiq guarantees all or nothing degree of precision. Therefore, if Quantrol generates correct experimental sequence descriptions, it is either the connection problem with the hardware or it might require a power cycle as some of the cards might be stuck in some weird state.

## Default state
Default state has all channel values changed. In other words, it is required to set the hardware in the default state for each channel. It was observed that the digital channels have limited number of channels that can be changed at a time to be 8. Therefore there is a 5 ms delay between assigning the first 8 channels and another 8 channels in out setup. In case you have more than 16 channels Quantrol will introduce 5 ms delays between each 8 digital channels. Keep this in mind when running the sequence continuously. It is possible to optimize those delays in the write_to_python.py file for your setup. 

It was also observed that in our setup the first analog channel following 16 digital channels is not assigned. The issue was resolved by adding 5 ns delay between the last eight digital channels assignment and analog channels for Zotino card. It is adviced to check the functionality of the Quantrol setting the default Edge values as it is the most demanding in terms of the number of channels at a time.

## Additional features
Quantrol can be used to generate python like experimental descriptions with a limited amount of features. Anything beyond of Quantrol capabilities can be hardcoded by modifying the generated run_experiment.py. For example, it is possible to create a 1D multiparameter scan using Quantrol. After that, the user can change the number of steps for each iterable object create by Quantrol, add additional for loops and easily make a multidimensional scan much.

## MSYS2 clang64 and conda
Initially the Quantrol was developed for conda package manager. Later after realizing that Artiq is going to deprecate conda based maintenance it was quickly adopted for MSYS2 clang64. In order to use it move the entire contents of the Quantrol repository to the location where msys2 is installed. In our case it is "C:\msys64\home\hostenlab". Then, specify in the config.py file that your package_manager = 'clang64'. Quantrol then will invoke clang64 file and run corresponding files with artiq_run. There should be better ways of doing this, but it was beyond my scope of expertise.

# Developer guide
The operation of Quantrol should be understood from several levels. First, using the table description of the experimental sequence, Quantrol creates an object self.experiment that contains different parameters to fully describe the sequence. After that according to the self.experiment object write_to_python will create python like description of the experimental sequence. Finally, using artiq_run Quantrol will run the experiment in the corresponding environment. For conda based environments it will invoke environment specified in the config.py and artiq_run it. For clang it will run the batch files that invoke clang64 and artiq_run it there.

Chart describing its self.experiment parameters and their descriptions is shown below. Purple blocks are objects, yellow blocks are the parameters of objects, and green blocks are descriptions of those parameters. This chart is not updated fully as during the last days of Quantrol developer (Whichislovely) he had many features to develop and could not modify this. However, it gives an overall idea of the structure and excluded parameters can be seen from the source_code.py. There are many descriptive comments.

![image](https://github.com/user-attachments/assets/961ba603-9d25-430d-8be5-7bb2a8c50788)

 ## Description of the logic behind some design decisions
 The user entered values are processed and stored in four forms 
	1) Expression used to evaluate the value
	2) Evaluation used in the python code to evaluate the value if it is not scanned and there is a specific value to be used for each variable in the expression
	3) Value of the parameter in case it is not scanned and there is a specific value to be used
	4) For python version that is going to be used in the python like description of the experimental sequence
The reason for evaluation being different from the expression is the ability of using the variables. Since the variable "delay" will be used as self.experiment.variables['delay'] there is a need of processing each variable accordingly and create an evaluation that can be executed to evaluate the parameter. The reason for having for_python is the ability of scanning variables. In case the parameter include a variable that is going to be scanned there is no specific value that is corresponding to that parameter. Instead the form such as scanned_variable_name is used as in the python like description there will be an iterable object that will be iterated over as "for a in self.a:". If the variable expression does not have any scanned variables, then the for_python is simply the value of the parameter.

## The need for variables and new_variables
Self.experiment.variables is a dictionary of all variables including the default variables that are created when the new Edge is being inserted (id0, id1, etc.). The use of dictionaries is good for faster retrieval of the variable values. However, it does not preserve any ordering that is required in rebuilding the variables tab. Otherwise, each time the variable is being created the order will be randomly changing, that might be confusing for the user. I could have used ordered dictionary, but self.experiment.new_variables proved to be useful to store the ordered user defined variables is handy when the variable is being scanned. When a variable is chosen to be scanned its value for the sorting of sequence table is being assigned to be the minimum value of the scanning range. However, after the tests with the scan one would like to retrieve the value of the variable that was used prior to scanning it. Self.experiment.new_variables comes handy as variables previous values can be easily retrieved from there.

## Updating of the for_python
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
The file is generated and updated by Quantrol. It is a python like desciprion of the experiment that initializes the hardware and sets its state to the defaul Edgee values. The user should initialize the hardware every time after power cycling Sinara hardware. In order to add different objects modify the write_to_python.py file.

## License
This is an open source project that was developed for the use in Hosten group (https://hostenlab.pages.ist.ac.at/). It was made public as we believed that other groups might benefit from what we have built.
Please keep in mind that there might still be minor bugs. We would appreciate your input on making Quantrol better.
