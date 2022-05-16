from abc import ABC, abstractmethod
import numpy as np
import time

class GeneticAlgorithm(ABC):

	def __init__(self):
		self.population = []
		self.populationScore = []
		self.maxValue = [None,None]


	@abstractmethod
	def fitnessFunction(self,x,y,z):
		pass

	
	def setPopulation(self,populationNumber):
		for i in range(populationNumber):
			chromossome = np.random.uniform(0,100,3) 
			self.population.append(chromossome) 
			chromossomeScore = self.fitnessFunction(
				chromossome[0],chromossome[1],chromossome[2])
			self.populationScore.append([chromossomeScore,i])


	def evaluatePopulation(self):
		self.populationScore.sort(reverse=False)
		
		choosenChromossomeIt = self.populationScore[-1]
		chromossomeItScore = choosenChromossomeIt[0]
		chromossomeItPosition =  choosenChromossomeIt[1]
		chromossomeIt = self.population[chromossomeItPosition]

		self.maxValue = [chromossomeItScore, chromossomeItPosition, chromossomeIt]


	def tournamentSelection(self, kIndividuals=3):
		generator = np.random.default_rng()
		selection = generator.choice(len(self.population),kIndividuals, replace=False)
		
		maximumParentScore = 0
		for i in selection:
			parentScoreByIteration = self.fitnessFunction(
				self.population[i][0],self.population[i][1],self.population[i][2])
			
			if (parentScoreByIteration > maximumParentScore):
				selectedParent = i
				maximumParentScore = parentScoreByIteration
				
		return selectedParent


	def selectParents(self, numberOfParents,kIndividuals=3):
		selectedParentsIndex = []
		selectedParents = []
		for i in range(numberOfParents):
			parentI = self.tournamentSelection(kIndividuals)
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


	# kChildren= number of children
	def setOffSpring(self, selectedParentsIndex, kChildren, threshold =0.5,):
		offSpring = []
		while (len(offSpring)<kChildren):
			generator = np.random.default_rng()
			parentsForCrossoverIndex = generator.choice(
				selectedParentsIndex,2,replace=False)
			
			probabilityOfDoingCrossOver = np.random.uniform(0,1)
			if probabilityOfDoingCrossOver > threshold:
				offSpringI = self.crossOver(parentsForCrossoverIndex[0],parentsForCrossoverIndex[1])
				for i in offSpringI:
					offSpring.append(i)
			else:
				for i in parentsForCrossoverIndex:	
					offSpring.append(self.population[i].copy())
			
		return offSpring


	def mutation(self, child, maxMutationValue = 1):
		for i in range(len(child)):
			generator = np.random.default_rng()
			mutationValue = generator.uniform(-maxMutationValue,maxMutationValue)

			if(child[i]+ mutationValue<100):
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


	def execute(self,populationNumber, numberOfParents,numberOfIterations, maxNumberOfRepetition=10 ,kIndividuals=3,k=4, crossOverThr = 0.5, fileName = 'results'):
		file = open("{}.txt".format(fileName),"a")
		file.write(
            f'Population Number: {populationNumber}, Number of Parents: {numberOfParents}, Number of Iterations: {numberOfIterations}, Number of Children: {k} \n \n')
		
		start = time.time()	
		
		iteration = 0
		numberOfRepetition = 0
		self.setPopulation(populationNumber)
		
		while ((iteration<numberOfIterations and numberOfRepetition < maxNumberOfRepetition)):
			file.write(f'iteration:{iteration} \n')

			previousIterationScore = self.maxValue[0]
			self.evaluatePopulation()
			
			file.write(
                f'Minimum Value: Score = {self.maxValue[0]}, x = {self.maxValue[2][0]}, y = {self.maxValue[2][1]}, z={self.maxValue[2][2]}, Position in Population={self.maxValue[1]} \n')
			
			parentsIndex = self.selectParents(numberOfParents,kIndividuals)
			offSpring = self.setOffSpring(parentsIndex,k,crossOverThr)
			children = self.setMutants(offSpring)
			
			self.setNewPopulation(children[0],children[1])
			
			if (self.maxValue[0] == previousIterationScore):
				numberOfRepetition= numberOfRepetition+1
			else:
				numberOfRepetition = 0 
			
			file.write(f'number of repetition: {numberOfRepetition} \n')
			iteration= iteration + 1
			
		end = time.time()
		file.write(f'Total time of Execution:{end - start} \n')	
		file.close()		
		return self.maxValue


