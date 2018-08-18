class Instance:
	def __init__(self, trucks, tx, ty, tw, nPackages, pX, pY, pW, incompatible):
		#Sample instance
		self.nTrucks = trucks
		self.xTruck = tx
		self.yTruck = ty
		self.wTruck = tw

		self.nPackages = nPackages
		self.pX = pX
		self.pY = pY
		self.pW = pW
		self.incompatible = incompatible