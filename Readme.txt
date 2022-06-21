self.experiment.new_variables are used solely to be able to show the used created variables 
in the variables tab. self.experiment.variables is a dictionary that does not have ordering.
If we would only use self.experiment.variables the table showing user created variables 
would be shuffled each time any change was introduced. Hey hey hey
