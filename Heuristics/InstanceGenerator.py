import time
import random
import pickle
from Instance import Instance

'''
!Run notes at the bottom!

'''

class GenInstanceTest:
	def __init__(self):
		#Sample instance
		self.nTrucks = 10
		self.xTruck = 12
		self.yTruck = 10
		self.wTruck = 12

		self.nPackages = 5
		self.pX = [3, 2, 1, 4, 6]
		self.pY = [1, 6, 2, 3, 4]
		self.pW = [8, 6, 4, 2, 5]
		self.incompatible = [[False, False, False, False, False],
							 [False, False, False, False, False],
							 [False, False, False, False, False],
							 [False, False, False, False, False],
							 [False, False, False, False, False]]

class GenInstance:
	def GenerateData(self, trucks, tx, ty, tw):
		'''
		Generate data for the problem, making sure a solution is possible.
		Needs to have defined n of trucks, (trucks) x, y, w. Makes sure the packages fit, add a small margin.
		'''
		nTrucks = trucks
		xTruck = tx
		yTruck = ty
		wTruck = tw

		nPackages = 0
		pX = []
		pY = []
		pW = []

		packageToTrck = []

		#Generate packages to fit trucks:
		for t in range (0, trucks): 
			x, y, w, = 0, 0, 0
			while True:
				newX = random.randint((int)(tx/5), (int)(tx/2))
				newY = random.randint((int)(ty/5), (int)(ty/2))
				newW = random.randint((int)(tw/10), (int)(tw/5))
				x = x + newX
				y = y + newY
				w = w + newW

				#Attempt to find better values to fill the truck
				while (x >= xTruck and newX > 1):
					newX = newX - 1
					x = x -1

				while (y >= yTruck and newY > 1):
					newY = newY - 1
					y = y -1

				while (w >= wTruck and newW > 1):
					newW = newW - 1
					w = w -1

				if (newX < 2 or newY < 2 or newW < 2):
					break

				else:
					pX.append(newX)
					pY.append(newY)
					pW.append(newW)
					packageToTrck.append(t)

		nPackages = len(pX)
		incompatible = [[0 for i in range(nPackages)] for i in range(nPackages)]

		#Generate incompatible matrix:
		for p1 in range(nPackages):
			p2 = random.randint(0, nPackages-1)
			probability = random.randint(0, 100)
			if (probability < 20):
				if (p1 != p2 and packageToTrck[p1] != packageToTrck[p2]):
					incompatible[p1][p2] = 1
					incompatible[p2][p1] = 1

		inst = Instance(nTrucks, xTruck, yTruck, wTruck, nPackages, pX, pY, pW, incompatible)
		self.PickleData(inst)

	def PickleData(self, inst):
		pickle_out = open("Instance.pickle", "wb")
		pickle.dump(inst, pickle_out)

def LoadData():
	pickle_load = open("Instance.pickle", "rb")
	inst = pickle.load(pickle_load)
	print("--- Instance ---")
	print("Trucks: ", inst.nTrucks)
	print("x: ", inst.xTruck)
	print("y: ", inst.yTruck)
	print("z: ", inst.wTruck)
	print("Packages: ", inst.nPackages)
	print("x: ", inst.pW)
	print("y: ", inst.pY)
	print("z: ", inst.pW)
	print("Incompatible: ", inst.incompatible)

################
'''
Runing:
GenerateData(number_of_trucks, xTruck, yTruck, wTruck)
The new instance will be stored in Instance.pickle

Each run will overwrite the previous instance.
Generated instance is displayed on console with LoadData()
(SolutionGenerator will also output ot to .txt, adapted for CPLEX, 
while generating a solution.)

'''
################

generator = GenInstance()
generator.GenerateData(42, 25, 45, 31) #WILL OVERWRITE PREVIOUS DATA!
LoadData()
