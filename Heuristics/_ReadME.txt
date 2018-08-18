ISADORA SALVETTI AND SANA JABEEN
AMMM - 2018

Run instructions:
Data must be generated first, by running InstanceGenerator.py.

Parameters for instance generation can be changed by changing the parameters of the call:
GenerateData(number_of_trucks, xTruck, yTruck, wTruck)

The new instance will be stored in Instance.pickle

Each run will overwrite the previous instance.
Generated instance is displayed on console with LoadData()
(SolutionGenerator will also output it to .txt, adapted for CPLEX, while generating a solution.)

///

SolutionGenerator.py will generate solutions for the current instance.

Changing the call 
GRASP(number_of_runs, alpha, file_to_save_output) 
will change the parameters for the solver.

