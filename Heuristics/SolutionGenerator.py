import time
import pickle
import random

'''
!Run notes at the bottom!

'''

###############
#Problem data:
###############
class Data:
	def __init__(self):
		pickle_load = open("Instance.pickle", "rb")
		data = pickle.load(pickle_load)

		self.nTrucks = data.nTrucks
		self.nPackages = data.nPackages
		
		#Trucks (int)
		self.xTruck = data.xTruck
		self.yTruck = data.yTruck
		self.wTruck = data.wTruck

		#Packages (int lists)
		self.pX = data.pX
		self.pY = data.pY
		self.pW = data.pW

		#Incompatibility list
		self.incomp = data.incompatible

		#List of packages
		self.P = []	

###############
#Store Solution:
###############
class Solution:
	def __init__(self, genSolution):
		self.pckgToTruck = genSolution.pckgToTruck
		self.trckToPackage = genSolution.trckToPackage
		self.pckgToPos = genSolution.pckgToPos
		self.greedyCostP = genSolution.greedyCostP
		self.greedyCostT = genSolution.greedyCostT

		#Create all empty truck layouts
		self.tLoad = genSolution.tLoad
		self.z = genSolution.z
		self.tLayout = genSolution.tLayout

		self.objective = genSolution.objective

###############
#Solution Generator:
###############
class Solvers:
	def __init__(self):
		self.log = open("Log.txt","a") #Log file.

		self.data = Data()
		self.pckgToTruck = [-1] * self.data.nPackages #List[pkage] = assigned truck, x, y
		self.trckToPackage = [ [] for i in range(self.data.nTrucks) ] #List[truck] = list of packages
		self.pckgToPos = [(-1, -1)] * self.data.nPackages #List[pkage] = bl package position
		self.objective = 999999999999 #Value of object function
		self.greedyCostP = [0] * self.data.nPackages #greedy cost of packages
		self.greedyCostT = [0] * self.data.nTrucks #greedy cost of trucks

		#Create all empty truck layouts
		self.tLoad = [0] * self.data.nTrucks #list[truck] = trucks current load
		self.z = 0 #load of the max loaded truck
		self.tLayout = [[[]]] #tLayout [t][x][y]
		for t in range (self.data.nTrucks):
			self.tLayout.append([])
			for x in range (self.data.xTruck):
				self.tLayout[t].append([])
				for y in range (self.data.yTruck):
					self.tLayout[t][x].append(-1)


	def reset(self):
		self.pckgToTruck = [-1] * self.data.nPackages #List[pkage] = assigned truck, x, y
		self.trckToPackage = [ [] for i in range(self.data.nTrucks) ] #List[truck] = list of packages
		self.pckgToPos = [(-1, -1)] * self.data.nPackages #List[pkage] = bl package position
		self.objective = 99999999999999 #Value of object function
		self.greedyCostP = [0] * self.data.nPackages #greedy cost of packages
		self.greedyCostT = [0] * self.data.nTrucks #greedy cost of trucks

		#Create all empty truck layouts
		self.tLoad = [0] * self.data.nTrucks #list[truck] = trucks current load
		self.z = 0 #load of the max loaded truck
		self.tLayout = [[[]]] #tLayout [t][x][y]
		for t in range (self.data.nTrucks):
			self.tLayout.append([])
			for x in range (self.data.xTruck):
				self.tLayout[t].append([])
				for y in range (self.data.yTruck):
					self.tLayout[t][x].append(-1)

	def setAsBest(self):
		genSolution = self.BestSolution
		self.pckgToTruck = genSolution.pckgToTruck
		self.trckToPackage = genSolution.trckToPackage
		self.pckgToPos = genSolution.pckgToPos
		self.greedyCostP = genSolution.greedyCostP
		self.greedyCostT = genSolution.greedyCostT

		#Create all empty truck layouts
		self.tLoad = genSolution.tLoad
		self.z = genSolution.z
		self.tLayout = genSolution.tLayout

		self.objective = genSolution.objective


	def checkData(self):
		print("Number of packages: ", self.data.nPackages)
		print("Number of trucks: ", self.data.nTrucks)
		print("Data of package 3;", " x:", self.data.P[3].pX, " y:", self.data.P[3].pY, " w:", self.data.P[3].pW )

	def printInstance(self, InstanceFile):

		#Write to file.
		f = open(InstanceFile,"w+")

		#Adapted for CPLEX:
		f.write("nT = {}; \n".format(self.data.nTrucks))
		f.write("nP = {}; \n".format(self.data.nPackages))
		f.write("maxXDim = {}; \n".format(self.data.xTruck))
		f.write("maxYDim = {}; \n".format(self.data.yTruck))
		f.write("TwMax = {}; \n\n".format(self.data.wTruck))

		f.write("PxD = {}; \n".format(self.data.pX))
		f.write("PyD = {}; \n".format(self.data.pY))
		f.write("Pw = {}; \n\n".format(self.data.pW))

		f.write("PiPj = {}; \n".format(self.data.incomp))
		f.close()
		
		'''
		f.write("\n--- Instance--- \n")
		f.write("Trucks: {} \n".format(self.data.nTrucks))
		f.write("Packages: {} \n".format(self.data.nPackages))
		f.write("Truck size: {}, {} \n".format(self.data.xTruck, self.data.yTruck))
		f.write("Truck weight: {} \n\n".format(self.data.wTruck))

		f.write("Packages X: {} \n".format(self.data.pX))
		f.write("Packages Y: {} \n".format(self.data.pY))
		f.write("Packages W: {} \n\n".format(self.data.pW))

		f.write("Incompatibility: {} \n".format(self.data.incomp))
		'''

	def printResults(self):
		'''
		PRINTING TO CONSOLE. NOT IN USE.
		print("\n--- Results---")
		print("Objective: ", self.objective)
		print("TrucksUsed: ", len(self.trckToPackage))
		print("Truck loads", self.tLoad)
		print("Z:", self.z)
		print("Packages to truck", self.pckgToTruck)
		print("Package positions", self.pckgToPos)
		print("Trucks", self.trckToPackage)
		print("\n\nTrucks layout: \n")
		for t in range (self.data.nTrucks):
			ts = ""
			for x in range (self.data.xTruck):
				for y in range (self.data.yTruck):
					if (self.tLayout[t][x][y] == -1):
						ts = ts + "*" + " "
					else:
						ts = ts + str(self.tLayout[t][x][y]) + " "

				if (self.tLayout[t][x][y] == -1):
					ts = ts + "*" + " "
				else:
					ts = ts + str(self.tLayout[t][x][y]) + " "
				ts = ts + "\n"
			ts = ts + "\n"
			print(ts)
		'''

		#Write to file.
		f = open(self.SolutionFile,"w+")

		f.write("Solver took: {} \n".format(self.executionTime))
		f.write("\n--- Instance--- \n")
		f.write("Trucks: {} \n".format(self.data.nTrucks))
		f.write("Packages: {} \n".format(self.data.nPackages))
		f.write("Truck size: {}, {} \n".format(self.data.xTruck, self.data.yTruck))
		f.write("Truck weight: {} \n".format(self.data.wTruck))
		f.write("\n--- Results--- \n")
		f.write("Objective: {} \n".format(self.objective))
		trckUsed = len(self.trckToPackage)
		f.write("TrucksUsed: {} \n".format(trckUsed))
		f.write("Truck loads: {} \n".format(self.tLoad))
		f.write("Z: {} \n".format(self.z))
		f.write("Packages to truck: {} \n".format(self.pckgToTruck))
		f.write("Package positions: {} \n".format(self.pckgToPos))
		f.write("Trucks: {} \n".format(self.trckToPackage))
		f.write("\nTrucks layout: \n")

		''''
		PRINTING TRUCK LAYOUTS = too slow, not in use
		for t in range (self.data.nTrucks):
			ts = ""
			for x in range (self.data.xTruck):
				for y in range (self.data.yTruck):
					if (self.tLayout[t][x][y] == -1):
						ts = ts + "**" + " "
					elif (self.tLayout[t][x][y] < 10):
						ts = ts + "0" + str(self.tLayout[t][x][y]) + " "
					else:
						ts = ts + str(self.tLayout[t][x][y]) + " "
				ts = ts + "\n"
			ts = ts + "\n"
			f.write(ts)
			'''

	'''
	CONSTRAINS.
	Do the package -> truck assigments if the assigment fulfills the constraints:
		1) No packages overlap -> check space
		2) Package fits the truck
		3) Max weight is not surpassed -> check weight
		4) Package is not in the same truck as an incompatible package -> check compatibility 

	(package, truck) pairs are chosen with no criteria.
	'''

	def checkCompatibility(self, p1, t): #Checks if there is an incompatible package in the truck
		if not t in self.trckToPackage:
			return True #return true if this is the first package assigned to truck
		for p2 in self.trckToPackage[t]: #check if the packages in this truck
			if (p1 != p2 and self.data.incompatible[p1][p2]):
				return False #return false if there is an incompatible package in the truck
		return True #return true if that is not the case

	def checkSpace(self, p, t): #Checks if there is space in the truck
		pY = self.data.pY[p]
		pX = self.data.pX[p]

		#Try to place package in x, y spot:
		for x in range (self.data.xTruck):
			for y in range (self.data.yTruck):
				if (self.tLayout[t][x][y] == -1): #Check if x, y spot is occupied.
					if (self.checkDimensions(t, x, y, pX, pY)):
						return (x, y)

		return (-1, -1) #No place was found. Return invalid position.

	def checkDimensions(self, t, x, y, pX, pY):
		for i in range(x, x+pX):  #Does this package fit if placed here? Check for overlaps.
			for j in range(y, y+pY):
				if (self.tLayout[t][i][j] != -1 or i >= self.data.xTruck - 1 or j >= self.data.yTruck - 1):
					return False
		return True #nothing went wrong. retirn true.

	def checkWeight (self, p, t):
		if (self.tLoad[t] <= self.data.wTruck - self.data.pW[p]):
			return True
		else:
			return False

	#UPDATE DATA - after an assigment is performed
	def updateObj(self):
		#Objective: min(numTrucksUsed + z), z being the highes load.
		usedTrucks = 0
		for t in self.trckToPackage:
			if (len(t)>0):
				usedTrucks += 1
		self.z = 0
		for load in self.tLoad: #for all trucks
			self.z = max(self.z, load) #z is max of z and this trucks load.
		obj = usedTrucks*self.data.wTruck + self.z
		return obj

	def checkAssignment(self, p, t):
		bl = self.checkSpace(p, t)
		if (bl[0] >= 0 and self.checkCompatibility(p, t) and self.checkWeight(p, t)):
			pY = self.data.pY[p]
			pX = self.data.pX[p]
			self.pckgToPos[p] = bl
			self.pckgToTruck[p] = t
			self.trckToPackage[t].append(p)
			self.objective = self.updateObj()
			self.tLoad[t] += self.data.pW[p]
			x, y = bl[0], bl[1]
			for i in range(x, x + pX):
				for j in range(y, y + pY):
					self.tLayout[t][i][j] = p
			return True
		else:
			return False

	def getGreedyCost(self):
		if (self.greedyCostP[0] == 0): #Same cost for all iterations. No need to recalculate.
			for p in range(self.data.nPackages): #Pick packages with biggest area/weight - prioritize area.
				areaP = self.data.pY[p] * self.data.pX[p]
				self.greedyCostP[p] = areaP * 100 + self.data.pW[p]

		'''
		As for trucks, always choose the first available one in the array, ensuring the solver attempts to fill
		the first trucks before moving down the array.

		'''

	'''
	SOLVERS
	'''
	def NaiveSolve(self):
		
		'''
		Assign packages to trucks by index.

		'''

		#Create list of unassigned packages
		unasignedPacks = []
		for p in range (self.data.nPackages):
			unasignedPacks.append(p) #create list of unassigned packages

		assignedPacks = 0
		for p in unasignedPacks:
			for t in range (self.data.nTrucks): #(p, t) -> package/ truck to be assigned.
				check = self.checkAssignment(p, t)
				if (check == True):
					assignedPacks = assignedPacks + 1
					break

		if (len(unasignedPacks) - assignedPacks > 1):
			print("Solution failed. Pacakges left: ", len(unasignedPacks) - assignedPacks)
		
		solution.printResults()

	def GRASP(self, maxRuns, a, solutionFile):
		'''
		- Greedy Constructive:
		- Define the greedy cost of each element in p.
		- Define the lists of candidates based on greedy cost =
		assign (p, t) -> p of lowest greedy cost, all trucks t, starting from the first ones in the array.
		- Add a random element from the list to the solution
		- Repeat until complete.

		- Local Search
		- Attempt to better the solution:
				- Reduce the number of used tricks
						-Find the truck with the least amount of packages and attempt to reassign those to a different truck
						(reduntand/ inneficient - method of package assigment makes it unlikelly that this would be possible)
				- Reduce the load of the highest loaded truck
						-Remove the smallest package from the truck with the highest load and attempt to place it in a truck
						with a small load.

		'''
		print("Grasp started")
		myTimeS = time.time() #Start timer
		self.BestSolution = Solution(self)
		self.getGreedyCost()

		self.SolutionFile = solutionFile #where to store solution
		for run in range (maxRuns):
			self.reset()
			self.constructive(a) #Look for a base solution
			print("Finish constructive")
			self.localSearch()
			print("Finish a set")

		myTimeE = time.time()
		self.executionTime = myTimeE - myTimeS
		print(self.executionTime)
		self.setAsBest()
		self.printResults()

	def constructive(self, a):
		'''
		Constructs a solution by assigning a packages to a truck based on a cost.
		Can be repeated multiple times, comparing the solutions and choosing the best objective.

		'''
		self.log.write("Constructive Solver. \n\n")
		
		#Prepare list of unassigned packages
		unasignedPacks = []
		for p in range (self.data.nPackages):
				unasignedPacks.append(p) #create list of unassigned packages
		if (a > 0 and a < 1):
			sortedCost = sorted(range(len(self.greedyCostP)), key=lambda k: self.greedyCostP[k])
		else:
			sortedCost = []
			for p in range (self.data.nPackages):
				sortedCost.append(p) #create list of unassigned packages

		continueLoop = True

		while (len(unasignedPacks) > 0 and continueLoop == True):
			#List of candidates
			candidateList = []

			if (a == 0): #If alpha is zero, ignore greedy cost.
				candidateList = unasignedPacks

			elif (a == 1): #If alpha is one, pick only the max cost elements
				maxCost = 0
				for p in range (len(sortedCost)):
					if (sortedCost[p] > maxCost):
						maxCost = self.greedyCostP[p]
						candidateList = []
						candidateList.append(p)
					elif (sortedCost[p] == maxCost):
						candidateList.append(p)
				#self.log.write("Alpha 1 candidates: {} \n".format(candidateList))

			else: #For other alphas, sort packages list accordingly.
				maxCost = self.greedyCostP[sortedCost[-1]] #min /max cost
				minCost = self.greedyCostP[sortedCost[0]]
				threshold = (1-a) * minCost + a * maxCost

				for p in sortedCost:
					if (len(unasignedPacks) < 2):
						candidateList.append(p) 
					elif (self.greedyCostP[p] <= threshold):
						candidateList.append(p)
					else:
						break
				#self.log.write("Alpha n candidates: {} \n".format(candidateList))

			#Prick a random assignment from the list:
			if (len(candidateList) > 0):
				aPack = random.randint(0, len(candidateList)-1)
				aPack = candidateList[aPack]

			for t in range(self.data.nTrucks): #(p, t) -> package/ truck to be assigned.
				check = self.checkAssignment(aPack, t)
				if (check == True):
					unasignedPacks.remove(aPack)
					sortedCost.remove(aPack)
					break
				elif (t == self.data.nTrucks - 1):
					print("Assigment on", p, " failed.")
					self.log.write("Snapshot (packages to truck): {} \n".format(self.pckgToTruck))
					return False

		if (continueLoop == True):
			self.log.write("Contructive Solution found.")
			self.log.write("Snapshot (packages to truck): {} \n".format(self.pckgToTruck))
			self.log.write("Objective: {} \n".format(self.objective))

			if (self.objective < self.BestSolution.objective): #If this run had a better objective, update solution.
				self.BestSolution = Solution(self)
				self.log.write("** Solution updated **\n\n")

		self.reset()
		return True


	def localSearch(self):
		'''
		Receives a complete solution.
		Find similar solutions: 

		Deassign a pair t/ package.
			Options to manage WEIGHT:
			- look for the trucks with the highest load.
			- look for the lightest package in the truck.
			- attempt to place it in a different truck.
			
			(Optimizing for truck usage should not be necessary with a good constructive solution.)
			Options to manage TRUCK USAGE:
			- find the emptiest truck.
			- check the load/ area of the packages in it.
			- examine if it is possible: is there empty space/ load available anywhere?
			- if NOT: do not proceed. Manage weight instead.
			- if YES: attempt to reassign the packages in the truck.
				-if it fails, discard solution and manage weight instead.
		'''

		self.log.write("Local Search Solver. \n\n")

		#Initial analizis - find the potentail candidate trucks/ packages
		lastUsedTruck = -1
		improvementFound = True

		while improvementFound:
			ptRmv = [] #Pair to remove

			#find truck
			for t in range (len(self.trckToPackage)):
				if (len(self.trckToPackage[t])>0):
					if (self.tLoad[t] == self.z):
						for p in self.trckToPackage[t]: #Pick viable packages:
							ptRmv.append((p, t))
				elif (lastUsedTruck==-1):
					lastUsedTruck = t
					break

			self.log.write("List of assignments in attempt: {} \n".format(ptRmv))
			if (len(ptRmv) < 1):
				break

			count = 0
			for tR in ptRmv:
				count += 1
				p, t = tR[0], tR[1]
				self.removePair(p, t)
				for tn in range(lastUsedTruck):
					if (t != tn):
						if (self.checkAssignment(p, tn)):
							if (self.objective < self.BestSolution.objective): #If this run had a better objective, update solution.
								self.BestSolution = Solution(self)
								self.printResults()
								self.log.write("Solution: {} found. \n".format(tryC))
								self.log.write("Snapshot (packages to truck): {} \n".format(self.pckgToTruck))
								self.log.write("Objective: {} \n".format(self.objective))
								self.log.write("** Solution updated **\n\n")
								break
					if (tn == lastUsedTruck):
						failure = self.checkAssignment(p, t)
						self.log.write("No reassignment possible for: {}, {} \n".format(p, tR))
						self.log.write("Reassigment was {} \n".format(failure))
				if (count == len(ptRmv)):
					improvementFound = False #No better solution was foud. Stop

	def removePair(self, p, t):
		#Removes pair package/truck.
		pY = self.data.pY[p]
		pX = self.data.pX[p]
		x, y = self.pckgToPos[p][0], self.pckgToPos[p][1]
		self.pckgToPos[p] = (-1, -1)
		self.pckgToTruck[p] = -1
		self.trckToPackage[t].remove(p)
		self.tLoad[t] -= self.data.pW[p]
		for i in range(x, x + pX):
			for j in range(y, y + pY):
				self.tLayout[t][i][j] = -1

################
'''
Running:
To generate new solution:
Call GRASP(number_of_runs, alpha, file_to_save_output) 

A instance must already have been generated and stored as
instance.pickle (see InstangeGenerator).

Some additional data is stored in log.txt

'''
################
print("Program started")
open('log.txt', 'w').close() #clear last log.

#Storing the solution results:
run1 = "solution_01.txt"
run2 = "solution_02.txt"
run3 = "solution_03.txt"
run4 = "solution_04.txt"
run5 = "solution_05.txt"
run6 = "solution_06.txt"

solve = Solvers()
solve.printInstance("MyInstance.txt")
runs = 90
#solve.GRASP(runs, 1, run1)
solve.GRASP(runs, .2, run2)
solve.GRASP(runs, .5, run3)
solve.GRASP(runs, .7, run4)
solve.GRASP(runs, 0, run5)
print("--Ended--")


run1 = "solution_501.txt"
run2 = "solution_502.txt"
run3 = "solution_503.txt"
run4 = "solution_504.txt"
run5 = "solution_505.txt"
run6 = "solution_506.txt"
runs = 5
solve.GRASP(runs, 1, run1)
solve.GRASP(runs, .2, run2)
solve.GRASP(runs, .5, run3)
solve.GRASP(runs, .7, run4)
solve.GRASP(runs, 0, run5)
print("--Ended--")

run1 = "solution_1001.txt"
run2 = "solution_1002.txt"
run3 = "solution_1003.txt"
run4 = "solution_1004.txt"
run5 = "solution_1005.txt"
run6 = "solution_1006.txt"
runs = 10
solve.GRASP(runs, 1, run1)
solve.GRASP(runs, .2, run2)
solve.GRASP(runs, .5, run3)
solve.GRASP(runs, .7, run4)
solve.GRASP(runs, 0, run5)
print("--Ended--")
