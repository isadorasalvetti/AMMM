/*********************************************
 * OPL 12.6.0.0 Model
 * Author: Isadora
 * Creation Date: Jun 2, 2018 at 7:37:41 PM
 *********************************************/

 // Packages
 int nP = ...; //number of packges
 range P = 1..nP; //all packages
 int Pw[p in P] = ...;
 int PyD[p in P] = ...;
 int PxD[p in P] = ...;
 int PiPj[p1 in P][p2 in P] = ...; //p1 and p2 are incompatible
 
 //Trucks
 int nT = ...;
 int maxXDim = ...;
 int maxYDim = ...;
 range T = 1..nT;
 range X = 1..maxXDim;
 range Y = 1..maxYDim;
 int TwMax = ...;
  
 //Decision
 dvar boolean usedT [t in T];
 dvar boolean PnT [p in P][t in T]; //package P is in truck T
 dvar boolean Pbl [p in P][x in X][y in Y]; //package p is in bottom cell x, y
 dvar boolean Pxy [p in P][x in X][y in Y]; //package occupies cell x, y
 dvar int z; //load of the highest loaded truck.
 
 //Object
 minimize z + TwMax * sum(t in T) usedT[t];
 
 //Constrains
 subject to {
 	//each package must be placed in a truck
 	forall(p in P)
 	  sum(t in T) PnT[p][t] == 1;
 	  
 	//truck capacity cannot be exceeded
 	forall (t in T)
 	  sum (p in P) Pw[p]*PnT[p][t]  <= TwMax;
 	  
 	//some packages are incompatible
 	forall (p1 in P, p2 in P, t in T)
 	  PnT[p1][t] + PnT[p2][t] <= 2 - PiPj[p1][p2];
	  
 	//packages cannot overllap
 	forall (x in X, y in Y, t in T)
 	  forall (p1 in P, p2 in P: p1 < p2)
 	     PnT[p1][t] + Pbl[p1][x][y] + 
 	     PnT[p2][t] + Pbl[p2][x][y] <= 3;
 	  
 	//set package dimension/ position in truck
	forall(p in P) {
	  (sum(x in X: x <= maxXDim - PxD[p] + 1)
	   sum(y in Y: y <= maxYDim - PyD[p] + 1) 
	      Pbl[p,x,y]) == 1; 
	      
	  (sum(x in X: x > maxXDim - PxD[p] + 1)
	   sum(y in Y: y > maxYDim - PyD[p] + 1) 
	      Pbl[p,x,y]) == 0;
	}
	
	forall(p in P, x in X, y in Y) {
	  (sum(i in X: (x - PxD[p] + 1 <= i <= x))
	   sum(j in Y: (y - PyD[p] + 1 <= j <= y)) 
	      Pbl[p,i,j]) == Pxy[p,x,y];	
	}

	//set usedT if a package is placed in the truck
	forall (t in T, p in P) usedT[t] >= PnT[p][t];
	
	//set z = weight of the max loaded 
	forall (t in T)
	  sum (p in P) PnT[p][t]*Pw[p] <= z;
 }
 
 execute {
	writeln("= = = = = = = = = = = = = =");
	writeln("= = = Trucks' layouts = = =");
	writeln("= = = = = = = = = = = = = =");
}