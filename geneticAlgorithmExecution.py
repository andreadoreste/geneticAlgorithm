from implementedGeneticAlgorithm import FitnessFunctionImplementationOfGA

#numberOfIterations = [100,200,300,500,1000]

#for i in numberOfIterations:
#	a = FitnessFunctionImplementationOfGA()
#	a.execute(20,4,i,10,4,4,0.5,'results_{}.txt'.format(i))


numberOfPopulation = [20,50,100,200,500]

for i in numberOfPopulation:
	a = FitnessFunctionImplementationOfGA()
	a.execute(i,4,350,10,4,4,0.5,'results_{}_population.txt'.format(i))