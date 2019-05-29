import sys
import json
import random
import requests
import numpy as np
import matplotlib.pyplot as plt

from random import randint
from deap import base
from deap import creator
from deap import tools
from PIL import Image

from random import sample
from functools import partial

json_file='heroStats.json'
json_data=open(json_file)
dataset = json.load(json_data)

json_file2='counters.json'
json_data2=open(json_file2)
dataset2 = json.load(json_data2)


xglobal = []
yglobal = []
maxGlobal = 0
geracaoGlobal = 0
gglobal = 0
gglobalTemp = 0

####### Variaveis Importantes #######
# Numero de heros
numheros = 5
# Quantidade de heros presentes na base de dados
qtheros = 121
# Populacao Total
populacao = 20
# Probabilidade De Um Individuo Sofrer Mutacao
probmut = 0.5
# Probabilidade De Dois Individuos Cruzarem
probcross = 0.5
# Quantidade maxima de Geracoes
numgeracoes = 100
# Melhor resultado possivel da funcao de avaliacao
resulfunc = 100.0

#####################################

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def getHeroName(individual):
    namesIndividual=[]
    for id_hero in individual:
        for data in dataset:
            if data['id']==id_hero:
                namesIndividual.append(str(data['localized_name']).lower())
    return namesIndividual

def checkCounters(individual):
    namesIndividual = getHeroName(individual)
    totalCounters=0
    for n in namesIndividual:
        for counters in dataset2[n]:
        	if dataset2[n][counters] > 0:
        		totalCounters += dataset2[n][counters] 
    return totalCounters

def checkTeam(individual):
	team = False
	sup = 0
	hc = 0
	if not team:
		for id_hero in individual:
			for data in dataset:
				if data['id'] == id_hero:
					for r in data['roles']:
						if r == "Support":
							sup = 1
						elif r == "Carry":
							hc = 1
						elif sup == 1 and hc == 1:
							team=True
							return team
	print (team)
	return team 


# Essa funcao tem como objetivo validar que os heros nao
# se repitam dentro do conjunto
def validaFilho(vetor):
    for i, e in enumerate(vetor):
        for j, f in enumerate(vetor):
                if i is j:
                    pass
                elif e == f:
                    while e == f:
                        tmp = 0
                        f = randint(0,qtheros-1)
                        for g2 in vetor:
                            if f == g2:
                                tmp = 1
                            if tmp == 1:
                                f = e
                    vetor[i] = f
    return vetor

gen_idx = partial(sample, range(qtheros), numheros)

toolbox.register("inputs", gen_idx)

# Structure initializers
#                         define 'individual' to be an individual
toolbox.register("individual", tools.initIterate, creator.Individual, 
    toolbox.inputs)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# funcao de fitness
def evalOneMax(individual):
    game = sys.argv[1]
    strategy = sys.argv[2]
    checkCounters(individual)
    checkTeam_out = checkTeam(individual)
    # f(x) = Somatorio(Initiator) + Somatorio(attack) + Somatorio(move_speed)
    if strategy == 'gank':
        print("----------------------------------")
        print(individual)
        fitvalue=0
        initiator=0
        attack=0
        speed=0
        team_composition=20
        if game == 'dota':
            for id_hero in individual:
                for data in dataset:
                    if checkTeam_out == False:
                        team_composition=0

                    elif data['id']==id_hero:
                        print(str(data['localized_name'].lower()))
                        attack = attack + data['base_attack_max']
                    
                        speed = speed + data['move_speed']
                        #print("velocidade ", speed)
                        for r in data['roles']:
                            if r == "Initiator":
                                initiator=initiator+10
                            else:
                                initiator=initiator-5
            
            fitvalue=(attack+speed+initiator)-team_composition
            
            fitvalue = (float(fitvalue)*100)/(2075)
            print ('team fitness = ' +str(fitvalue))
        elif game == 'lol':
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        else:
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        return fitvalue,

    elif strategy == 'teamfight':
        print("----------------------------------")
        print(individual)
        fitvalue=0
        carry=0
        strength=0
        atk_rate=0

        if game == 'dota':
            for id_hero in individual:
                for data in dataset:
                    if data['id']==id_hero:
                        print(str(data['localized_name']))
                        strength = strength + data['base_str']
                        #print("strength ", strength)
                        atk_rate = atk_rate + data['attack_rate']
                        #print("velocidade ", atk_rate)
                        for r in data['roles']:
                            if r == "Carry":
                                carry=carry+10
                            else:
                                carry=carry-5
                        
            fitvalue=strength+atk_rate+carry
            print(fitvalue)
            fitvalue = (float(fitvalue)*100)/(210)
            print ('team fitness = ' +str(fitvalue))
        elif game == 'lol':
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        else:
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        return fitvalue,

    elif strategy == 'pusher':
        print("----------------------------------")
        print(individual)
        pusher=0
        primary_attr=0
        fitvalue=0
        agi=0
        team_composition = 20
        if game == 'dota':
            for id_hero in individual:
                for data in dataset:
                    if data['id']==id_hero:
                        print(str(data['localized_name']))
                        agi=agi+data['base_agi']
                        
                        if data['primary_attr']=="str":
                            primary_attr=primary_attr+20
                        else:
                            primary_attr=primary_attr+1
                        
                        for r in data['roles']:
                        
                            if r == "Pusher":
                                pusher=pusher+10
                            else:
                                pusher= 0
            fitvalue = agi+pusher+primary_attr
            print (fitvalue)
            fitvalue = (float(fitvalue)-1)/(210-1)
            #print ('time fitness = ' +str(fitvalue))
        elif game == 'lol':
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        else:
            sys.exit('League Of Legends evaluation isn\'t working yet. =( ')
        return fitvalue,

#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

def main():

    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=populacao)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = probcross, probmut
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    
    # Begin the evolution
    while max(fits) < resulfunc and g < numgeracoes:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        gglobalTemp = g
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                child1 = validaFilho(child1)                        
                child2 = validaFilho(child2)

            # fitness values of the children
            # must be recalculated later
            del child1.fitness.values
            del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        # Responsavel por capturar em que geracao o melhor resultado
        # foi encontrado para o dado ser utilizado no grafico final.
        if max(fits) > maxGlobal:
            global maxGlobal
            global gglobal
            maxGlobal = max(fits)
            gglobal = gglobalTemp

        xglobal.append(max(fits))
        yglobal.append(g)

    best_ind = tools.selBest(pop, 1)[0]
    
    #get heros name
    best_ind_name =[]
    image_urls=[]
    for b in best_ind:
        for data in dataset:
            if data['id']==b:
                best_ind_name.append(str(data['localized_name']))
                image_urls.append(data['img'])


    print("Best individual is %s, %s" % (best_ind_name, best_ind.fitness.values))
    print("-- End of (successful) evolution --")


    #evolution plot
    fig, ax = plt.subplots()
    ax.plot(xglobal, yglobal, 'b--')
    style = dict(size=10, color='gray')
    plt.scatter(xglobal, yglobal, color='green')
    #txtTemp = '{} individuos\nMelhor solucao: {}\nGeracao {}\n{}'.format(populacao, best_ind.fitness.values[0], gglobal, best_ind)
    #ax.annotate(txtTemp, xy=(best_ind.fitness.values[0], gglobal), xytext=(best_ind.fitness.values[0]-4, gglobal-4),arrowprops=dict(facecolor='black', shrink=0.05))
    plt.xlabel('Fitness function value')
    plt.ylabel('Generation')
    plt.show()


    #the best team plot
    #it works just with internet
    images=[]
    for im in image_urls:
        images.append(Image.open(requests.get('https://api.opendota.com'+im, stream=True).raw))

    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('test.jpg')


    
if __name__ == "__main__":
    main()