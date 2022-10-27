self.experiment.new_variables are used to be able to show the used created variables 
in the variables tab. Also it is used to reassign the previous values of variables that
were used to be scanned after they are not scanned anymore 

self.experiment.variables is a dictionary that does not have ordering.
If we would only use self.experiment.variables the table showing user created variables 
would be shuffled each time any change was introduced.

self.experiment.scanned_variables is used to store the variables that are being scanned.
It is a lookup list to fill the scanning parameters table
