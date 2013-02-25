import random
import sys

# Declare our arrays and grab inputs
population = []
population_scores = []
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,? "
populaton_size = int(sys.argv[1])
target = sys.argv[2]
target_len = len(target)

# Got to have a random string generator
def generateRandomString(length):
	randString = ""
	for i in xrange(length):
		randString += charset[random.randint(0, len(charset)-1)]
	return randString

# Got to also have a random populator generator
def generateRandomPopulation(num, length):
	for i in xrange(num):
		population.append( generateRandomString(int(length)) )
		population_scores.append(0)

# Get the sum of the squares of the differences between a member and the target.
def getMemberScore(member):
	score = 0
	for i in xrange(target_len):
		score += (ord(target[i]) - ord(member[i]))**2
	return score

# Fill our population scores array with the current scores
def scorePopulation():
	for i in xrange(len(population)):
		population_scores[i] = getMemberScore( population[i] )

# Sort the two arrays (population and population_scores) in increasing order of their scores
def sortPopulation():
	global population
	global population_scores
	tmp = zip(population_scores, population)
	tmp.sort()
	population_scores = [i for (i, s) in tmp]
	population = [s for (i, s) in tmp]
	del( tmp )

# Choose the percantage of top members to mate (percent_parents), and choose a percentage
# of the population to kill off. Example: choose 0.50 and 0.20 respectively means that if
# we had 100 members in the population, we will only make using the top 50% of the population,
# and we will seek to mate 20 times, thus replacing 20% of the population with children.
def mateTopMembers(percent_parents, percent_deaths):
	availableOptions = int(len(population)*float((float(percent_parents)/100.0)))
	times = int(len(population)*float((float(percent_deaths)/100.0)))
	for i in xrange(times):
		parent1 = population[random.randint(0,availableOptions)]
		parent2 = population[random.randint(0,availableOptions)]
		cut = random.randint(0,target_len)
		child = parent1[:cut] + parent2[cut:]
		population[(len(population)-1)-i] = child
		population_scores[(len(population)-1)-i] = 0

# Cycle through the population and allow for some members to mutate through the generations.
def mutateMembers():
	# This variable is in percent
	chance_to_mutate = 4
	for i in xrange(len(population)):
		# Mutate only if XX%
		if random.randint(0,100) < chance_to_mutate:
			word = list(population[i])
			word[random.randint(0,len(word)-1)] = charset[random.randint(0,len(charset)-1)]
			population[i] = "".join(word)

# Start the show and let them evolve
def startEvolution(populaton_size, target_len):
	generateRandomPopulation(populaton_size, target_len)
	scorePopulation()
	sortPopulation()
	generation = 0
	# This will keep evolving the population so long as there is no member who has a score of 0
	# A score of 0 means that a member is equal to our target. So we can stop evolving.
	while( 0 not in population_scores ):
		mateTopMembers(80,20)
		mutateMembers()
		scorePopulation()
		sortPopulation()
		generation += 1
	print "Goal: " + target
	print "Done! Took: " + str(generation) + " generations!"

startEvolution(populaton_size, target_len)
