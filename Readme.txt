self.experiment.new_variables are used to be able to show the used created variables 
in the variables tab. Also it is used to reassign the previous values of variables that
were used to be scanned after they are not scanned anymore 

self.experiment.variables is a dictionary that does not have ordering.
If we would only use self.experiment.variables the table showing user created variables 
would be shuffled each time any change was introduced.

self.experiment.scanned_variables is used to store the variables that are being scanned.
It is a lookup list to fill the scanning parameters table

for_python is only used in write_to_python.create_experiment in the go_to_edge we use only values.

for_python is only updated when run experiment button is pressed. In other words, just before the 
actual python file needs to be generated. It saves time since we do not need to redecode expressions
but might be confusing for the developing person when for_python values do not correspond to correct values.

