from unittest import result
import GeneticAlgorithm as GA
import numpy as np
from StackMaker import *
from DataManager import *
import json
#from main import*
class hssp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        hssp.Amount = amount
        hssp.Weights = weights
class ssp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        ssp.Amount = amount
        ssp.Weights = weights
class smp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        smp.Amount = amount
        smp.Weights = weights
class mp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        mp.Amount = amount
        mp.Weights = weights
class mlp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        mlp.Amount = amount
        mlp.Weights = weights
class lp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        lp.Amount = amount
        lp.Weights = weights
class lhp:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        lhp.Amount = amount
        lhp.Weights = weights
        
class etc:
    Amount = 0
    Weights = []
    def __init__(self, amount, weights) -> None:
        etc.Amount = amount
        etc.Weights = weights


class Boxes:
    hssp = hssp(0, [])
    smp = smp(0, [])
    ssp = ssp(0, [])
    mp = mp(0, [])
    mlp = mlp(0, [])
    lp = lp(0, [])
    lhp = lhp(0, [])
    etc = etc(0, [])
    def __init__(self, hssp=None, smp=None, ssp=None, mp=None, mlp=None, lp=None, lhp=None, etc=None) -> None:
        Boxes.hssp = hssp
        Boxes.smp = smp
        Boxes.ssp = ssp
        Boxes.mp = mp
        Boxes.mlp = mlp
        Boxes.lp = lp
        Boxes.lhp = lhp
        Boxes.etc = etc

def execute(hssp_amount, ssp_amount, smp_amount, mlp_amount, mp_amount, lp_amount, lhp_amount, etc_amount, ssp_weights, smp_weights, hssp_weights, mp_weights, mlp_weights, lp_weights, lhp_weights, etc_weights, container_type):
    dummy_parcels = {
        'ssp' : ssp_amount,
        'smp' : smp_amount, 
        'hssp' : hssp_amount, 
        'mlp' : mlp_amount, 
        'mp' : mp_amount, 
        'lp' : lp_amount,
        'lhp' : lhp_amount,
        'etc' : etc_amount
    }
    dummy_weights = {
        'ssp' : ssp_weights,
        'smp' : smp_weights,
        'hssp' : hssp_weights,
        'mlp' : mlp_weights,
        'mp' : mp_weights,
        'lp' : lp_weights,
        'lhp' : lhp_weights, 
        'etc' : etc_weights
    }

    stack_maker = StacksMaker(dummy_parcels, dummy_weights)
    stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
    ga = GA.GeneticAlgorithm(stacks, container_type, {**same_type_stacking, **mix_type_stacking})
    result = ga.execute()
    #best_chrom_data = DataManager.to_json(population[chromosome_scores.index(max(chromosome_scores))], "c5")
    return result