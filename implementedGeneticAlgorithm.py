import math
from geneticAlgorithm import GeneticAlgorithm

class FitnessFunctionImplementationOfGA(GeneticAlgorithm):
	def fitnessFunction(self,x,y,z):
		exp_x = math.exp(-x)
		f0 = 2 * x * z * exp_x
		f1 = -2 * pow(y,3)
		f2 = pow(y,2) 
		f3 = -3 * pow(z,3)
		f = f0 + f1 +f2 + f3
		ObjFunctionValue = f
		return ObjFunctionValue

