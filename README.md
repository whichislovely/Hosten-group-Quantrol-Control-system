# Quantrol

Quantrol is a high level solution built on top of the open access Artiq infrastructure. It allows researchers to use most of the Artiq features without coding.
The current state of the GUI is adopted for the specific hardware used in Hosten group at Institure of Science and Technology Austria. However, it can be relatively easily adopted for any type of Sinara based hardware.

## Installation

This program was built and has been used on Windows based OS. 
In order to get started simply copy the entire repository on your local machine. The program was tested with VS Code but other code editors might also work as well. Open the entire repository folder in VS Code to be able to use it properly.
In the terminal of VS Code type following command to install the required libraries:

pip install -r requirements.txt

Alternatively, you can open the requirements.txt file and the pop-up window will suggest you to configure the virtual environment. After downloading the required libraries copy your device_db.py into the same folder.
Run the source.py in order to start the program.

## User guide
Quantrol is a user friendly interface that helps describing experimental sequences without coding. 
It allows using mathematical expressions, define variable, scan multiple variables in a 1D scan, use default variables such as id0, id1, ... etc.

In order to describe the sequence user introduces time edges where the changes in the hardware state are required. 

In order to use or scan a variable, one first needs to create it in a variables tab. After that the user can add defined variables in mathematical expressions or Scanning table.
The color coding of the channel state is used for better visualization of the sequence. White background values show the previously set values and hence the current state of the hardware. Green and red background specifies the changes user introduced at a specific time edge.

The program was not optimized for adaptive resizing and was arranged for the full window size.

## Developer guide
The program consists of several files that will be described in this section. 

### source_code.py
The main file is the source_code.py It initializes the artiq server, communicates with the scheduler, creates and displays the main window, defines used objects such as self.experiment, self.edge, ... etc. And finally, it has many utility functions that are used when buttons are clicked or entries are changed.
### tabs.py
The tabs.py is a file that is used to build all tabs. It has a description of tables, buttons and their relative orientations. 
### update.py
The update.py is a file that consists of fairly optimized udpating functions that are required in different cases. 
### write_to_python.py
The write_to_python.py is a file that consists of functions required to generate the python like description of the experimental sequence.

## License
This is an open source project that was developed for the use in Hosten group (https://hostenlab.pages.ist.ac.at/). It was made public as we believed that other groups might benefit from what we have built.
Please keep in mind that there might still be minor bugs. We would appreciate your input on making Quantrol better.
