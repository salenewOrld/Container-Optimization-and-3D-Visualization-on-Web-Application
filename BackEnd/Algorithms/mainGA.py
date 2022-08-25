import GeneticAlgorithm as GA
import numpy as np
from StackMaker import *
from DataManager import *
from main import *
import json
dummy_parcels = {
    'ssp' : 100,
    'smp' : 500, 
    'hssp' : 800, 
    'mlp' : 100, 
    'mp' : 900, 
    'lp' : 300,
    'lhp' : 100,
    'etc' : 70
}
dummy_weights = {
    'ssp' : list(np.random.randint(1, 6, dummy_parcels['ssp'])),
    'smp' : list(np.random.randint(1, 9, dummy_parcels['smp'])),
    'hssp' : list(np.random.randint(1, 15, dummy_parcels['hssp'])),
    'mlp' : list(np.random.randint(1, 19, dummy_parcels['mlp'])),
    'mp' : list(np.random.randint(1, 25, dummy_parcels['mp'])),
    'lp' : list(np.random.randint(1, 60, dummy_parcels['lp'])),
    'lhp' : list(np.random.randint(1, 85, dummy_parcels['lhp'])), 
    'etc' : list(np.random.randint(1, 29, dummy_parcels['etc']))
}

stack_maker = StacksMaker(dummy_parcels, dummy_weights)
stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
ga = GA.GeneticAlgorithm(stacks, "c5")
population, chromosome_scores = ga.execute()
best_chrom_data = DataManager.to_json(population[chromosome_scores.index(max(chromosome_scores))], "c5")
print(json.dumps(best_chrom_data))