## Optimization And Heuristic Algorithm for Packages to Truck Problem

* FIB - AMMM 2018
* Isadora Salvetti and Sana Jabeen

Final project for Algorithmic Methods for Mathematical Models.

# Problem Definition

A logistic company require an efficient way to place the P number of packages in to T number of trucks such that each truck have same length XTruck and width YTruck and the capacity WTruck. In the same way the packages have also XDim length, YDim width and wp weight, which is unique for all the packages. There are some constraints such that, the packages cannot be rotated when placed in the truck thus, a 5X3 package cannot be placed in 3X4 truck. However, the packages cannot be placed over each other. Furthermore, there are some pair of packages P1 and P2 that should not be placed in the same truck. For this purpose we are using a boolean matrix incomp[P1][P2] such that if incomp[P1][P2] is equal to 1, this means that the packages are not in the same truck which ensure the constraint. The Goal of this project is to find the distribution of packages into the trucks, so that minimal number of trucks used and to reduce the load of the highest loaded truck.

wTruck  number of used trucks + load of the truck with the highest load * modifier

# Contents
* ILP Model and dataset
* Heuristics

Written in python, comprised of an intance generator and a solver.
