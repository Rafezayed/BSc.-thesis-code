# -*- coding: utf-8 -*-
"""
Created on Fri May 18 23:08:23 2018

@author: Rafe Zayed
"""
import numpy as np
import itertools
import random
from exergyfunction import exergy

population_size=50
chromosome_size=2
geneset1=[i for i in range(150,380,10)]
geneset2=[i for i in range(12000000,33000000,100)]

mutation_rate=0.05
crossover_rate=0.95
generation=100


def summation(a,b):
    return (a+b)/(a*b)

#Creating fitness function

def fitness_array(population):
    fitness_array=[]
    for i in range(len(population)):
        fitness_array.append(exergy(population[i,0],population[i,1]))
    
    fitness_array=np.array(fitness_array)
    return fitness_array


#Creating random population

def return_random_population(geneset1,geneset2,population_size):
    population=random.sample(set(itertools.product(geneset1,geneset2)),population_size)
    population=np.array(population)
    return population


#Arranging the population from best to worst fitness

def return_best_worst_population(population):
    fitness_array1=fitness_array(population)
    new_population=np.zeros(population.shape)
    new_fitness_array=np.zeros(fitness_array1.shape)
    worst_best=np.argsort(fitness_array1)
    best_worst=worst_best[::-1]
    row_counter=0
    for i in best_worst:
        new_population[row_counter,:]=population[i,:]
        new_fitness_array[row_counter]=fitness_array1[i]
        row_counter +=1
    return new_population[0],new_fitness_array[0]


#Linear ranked_selection method

def return_ranked_selected_population(population):
    ranked_population=[]
    fitness_of_given_population=fitness_array(population)

    sort=np.argsort(fitness_of_given_population)   #argshort return the indices of lower to high fitness chromosome.
    
    rank_population=np.zeros(fitness_of_given_population.shape)
    x=1
    for i in sort:
        rank_population[i]=x
        x=x+1
    fitness_score=[(x/sum(rank_population)) for x in rank_population]     
        
    
    for i in range(len(fitness_score)):
        n=int(fitness_score[i]*100)
        for j in range(n):
            ranked_population.append(population[i])
    return ranked_population


#crossovered population

def return_crossovered_child(ranked_selected_population):
    if  np.random.random()<crossover_rate:
        a=np.random.randint(0,len(ranked_selected_population))
        b=np.random.randint(0,len(ranked_selected_population))
        parent1=ranked_selected_population[a]
        #print("x",parent1)
        parent2=ranked_selected_population[b]
        #print("y",parent2)
        slicing_point=np.random.randint(0,chromosome_size)
       # print("a",parent1[:slicing_point])
        #print("b",parent2[slicing_point:])
        child=list(parent1[:slicing_point])+list(parent2[slicing_point:])
        
        #print("c",child)
        return child
    return 0
    
#Mutated population

def return_mutated_child(crossovered_child):
    for i in range(chromosome_size):
        if np.random.random()<mutation_rate:
            if i==0:
                crossovered_child[i]=np.random.choice(geneset1)
            else:
                crossovered_child[i]=np.random.choice(geneset2)
            
            
    return crossovered_child

#creating initial population

new_population =return_random_population(geneset1,geneset2,population_size)
print("initial population",new_population)

a,b=return_best_worst_population(new_population)
print("best",a,"fitness",b)
#print(new_population)
for i in range(generation):
    mate_pool=return_ranked_selected_population(new_population)
    
    last_population=[]
    
    for j in range(population_size):
        
        crossed_child=return_crossovered_child(mate_pool)
        #print("c",crossed_child)
        if crossed_child is 0:
            continue
        else:
            mutated_child=return_mutated_child(crossed_child)
            #print("m",mutated_child)
        last_population.append(mutated_child)
    new_population=np.array(last_population)
    
    
    a,b=return_best_worst_population(new_population)
    print('generation',i,"best",a,"fitness",b)