import math
from geneticAlgorithm import GeneticAlgorithm

class ImplementedGeneticAlgorithm(GeneticAlgorithm):

	def fitnessFunction(self,x,y,z):
		exp_x = math.exp(x)
		f0 = 2*x*z*exp_x
		#print('f0',f0)
		f1 = -2*pow(y,3)
		#print('f1',f1)
		f2 =  pow(y,2) 
		#print('f2',f2)
		f3 = -3* pow(z,3)
		#print('f3',f3) 
		f = f0 + f1 +f2 + f3
		ObjFunctionValue = f
		return ObjFunctionValue


a = ImplementedGeneticAlgorithm()
a.execute(10,4,50,10)

