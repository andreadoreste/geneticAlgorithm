from abc import ABC, abstractmethod
import numpy as np
#import math
import time

class GeneticAlgorithm(ABC):

	def __init__(self):
		self.population = []
		self.populationScore = []
		self.maxValue = [None,None]

	@abstractmethod
	def fitnessFunction(self,x,y,z):
		pass

	#Initialize populuation randomly
	def setPopulation(self,populationNumber):

		for i in range(populationNumber):

			chromossome = np.random.uniform(0,100,3) 
			self.population.append(chromossome) 
			chromossomeScore = self.fitnessFunction(chromossome[0],chromossome[1],chromossome[2])
			self.populationScore.append([chromossomeScore,i])


		#self.populationScore.sort(reverse=False)
		#self.populationScore.sort()

	def evaluatePopulation(self):

		self.populationScore.sort(reverse=False)
		choosenChromossomeIt = self.populationScore[-1]
		chromossomeItScore = choosenChromossomeIt[0]
		chromossomeItPosition =  choosenChromossomeIt[1]
		chromossomeIt = self.population[chromossomeItPosition]

		self.maxValue = [chromossomeItScore, chromossomeItPosition, chromossomeIt]

	def tournamentSelection(self, k=3):
				
		generator = np.random.default_rng()
		selection = generator.choice(len(self.population),k, replace=False)
		
		# set the minimum value as infinit 
		minimumParentScore = 0
		for i in selection:
			parentScoreByIteration = self.fitnessFunction(self.population[i][0],self.population[i][1],self.population[i][2])
			
			if (parentScoreByIteration > minimumParentScore):
				selectedParent = i
				minimumParentScore = parentScoreByIteration
				
		return selectedParent

	def selectParents(self, numberOfParents):
		
		selectedParentsIndex = []
		selectedParents = []

		for i in range(numberOfParents):
			parentI = self.tournamentSelection()
			selectedParentsIndex.append(parentI)
			selectedParents.append(self.population[parentI])
		
		return selectedParentsIndex

	def crossOver(self, parentOneIndex, parentTwoIndex):
		parentOne = self.population[parentOneIndex]
		parentTwo = self.population[parentTwoIndex]
		childOne = parentOne.copy()
		childTwo = parentTwo.copy()

		generator = np.random.default_rng()
		genI = generator.integers(0,3)
		childOne[genI] = parentTwo[genI]
		childTwo[genI] = parentOne[genI]
		
		return [childOne,childTwo]

	# k= number of children
	def setOffSpring(self, selectedParentsIndex, k, threshold =0.5,):
		
		offSpring = []
		
		while (len(offSpring)<k):

			generator = np.random.default_rng()
			parentsForCrossoverIndex = generator.choice(selectedParentsIndex,2,replace=False)
			
			probabilityOfDoingCrossOver = np.random.uniform(0,1)
						
			if probabilityOfDoingCrossOver > threshold:

				offSpringI = self.crossOver(parentsForCrossoverIndex[0],parentsForCrossoverIndex[1])
				for i in offSpringI:
					offSpring.append(i)
			
			else:
				
				for i in parentsForCrossoverIndex:	
					offSpring.append(self.population[i].copy())
			
		return offSpring

	#default maxMutationValue = 0.01*100		
	def mutation(self, child, maxMutationValue = 1):
		
		for i in range(len(child)):
			generator = np.random.default_rng()
			mutationValue = generator.uniform(-maxMutationValue,maxMutationValue)
			child[i] = child[i] + mutationValue
		
		return child

	def setMutants(self, offSpring, maxMutationValue=1):
		listOfMutantsScore = []
		listOfMutants = []
		
		for i in offSpring:
			mutant = self.mutation(i,maxMutationValue)
			chromossomeScore = self.fitnessFunction(i[0],i[1],i[2])
			listOfMutants.append(mutant)
			listOfMutantsScore.append(chromossomeScore)
		
		return [listOfMutants,listOfMutantsScore]

	
	def setNewPopulation(self,children,childrenScore):
		
		for i in range(len(children)):
			
			oldParent = self.populationScore.pop(i)
			self.population.pop(oldParent[1])
			child = children.pop(0)
			childScore = childrenScore.pop(0)
			
			self.population.insert(oldParent[1],child)
			self.populationScore.insert(i,[childScore,oldParent[1]])


		
	def execute(self,populationNumber, numberOfParents,numberOfIterations, maxNumberOfRepetition=1 ,k=4, crossOverThr = 0.5, fileName = 'results'):
		
		file = open("{}.txt".format(fileName),"a")
		initialData = 'Population Number: {}, Number of Parents: {}, Number of Iterations: {}, Number of Children: {} \n \n'.format(populationNumber,numberOfParents,numberOfIterations,k)
		file.write(initialData)
		start = time.time()	
		iteration = 0
		numberOfRepetition = 0

		#initialize the population
		self.setPopulation(populationNumber)
		
		while ((iteration<numberOfIterations and numberOfRepetition < maxNumberOfRepetition)):
			
			file.write('iteration:{} \n'.format(iteration))

			previousIterationScore = self.maxValue[0]
			
			self.evaluatePopulation()
			
			file.write("Minimum Value: Score = {}, x = {}, y = {}, z={}, Position in Population={} \n".format(self.maxValue[0],self.maxValue[2][0],self.maxValue[2][1],self.maxValue[2][2],self.maxValue[1]))
			
			parentsIndex = self.selectParents(numberOfParents)
			offSpring = self.setOffSpring(parentsIndex,k,crossOverThr)
			children = self.setMutants(offSpring)
			
			self.setNewPopulation(children[0],children[1])
			
			if (self.maxValue[0] == previousIterationScore):
				numberOfRepetition= numberOfRepetition+1
			else:
				numberOfRepetition = 0 
			file.write("number of repetition: {} \n".format(numberOfRepetition))
			

			iteration= iteration + 1
			
		end = time.time()
		file.write("Total time of Execution:{} \n".format(end - start))		
		file.close()		
		return self.maxValue


