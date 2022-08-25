import copy
from distutils.util import copydir_run_2to3
import parcels
from Stack import *
import random


class StacksMaker:
    same_type_stacks_amount = None
    mix_type_stacks_amount = None
    stack_zero = Stack([], weight_each={"fl_1" : [0]}, stack_height=0, stack_width=0, stack_length=0, stack_name=0)

    def __init__(self, parcels, parcels_weight):
        self.parcels = parcels
        self.parcels_weight = parcels_weight

    def make_stacks(self):
        same_type_stacks = {
            'ssp': 0,
            'smp': 0,
            'hssp': 0,
            'mlp': 0,
            'mp': 0,
            'lp': 0,
            'lhp': 0,
            'etc': 0
        }
        mix_type_stacks = {
            201: 0,
            202: 0,
            203: 0,
            204: 0,
            205: 0,
            206: 0,
            207: 0,
            208: 0
        }
        value_mod_same_type = [2, 3, 4, 2, 3, 3]
        # making same-type stacking (101 - 106)
        idx = 0
        for stack_name, value in self.parcels.items():
            if idx >= len(value_mod_same_type):
                break
            stack_count = (value // value_mod_same_type[idx])
            same_type_stacks[stack_name] += stack_count
            self.parcels[stack_name] -= (stack_count *
                                         value_mod_same_type[idx])
            idx += 1
        while True:
            if self.parcels['smp'] >= 2 and self.parcels['hssp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['smp'] -= 2
                self.parcels['hssp'] -= 1
            elif self.parcels['smp'] >= 2 and self.parcels['etc'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['smp'] -= 2
                self.parcels['etc'] -= 1
            elif self.parcels['ssp'] >= 2 and self.parcels['etc'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['ssp'] -= 2
                self.parcels['etc'] -= 1
            elif self.parcels['etc'] >= 2 and self.parcels['lhp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['etc'] -= 2
                self.parcels['lhp'] -= 1
            elif self.parcels['hssp'] >= 3 and self.parcels['mp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['hssp'] -= 3
                self.parcels['mp'] -= 1
            elif self.parcels['smp'] >= 6 and self.parcels['mlp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['smp'] -= 6
                self.parcels['mlp'] -= 1
            elif self.parcels['lp'] >= 2 and self.parcels['lhp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['lp'] -= 2
                self.parcels['lhp'] -= 1
            elif self.parcels['smp'] >= 6 and self.parcels['mp'] >= 1:
                mix_type_stacks[201] += 1
                self.parcels['smp'] -= 6
                self.parcels['mp'] -= 1
            else:
                break
        same_type_stacks_fixed = {
            101: same_type_stacks['hssp'],
            102: same_type_stacks['smp'],
            103: same_type_stacks['ssp'],
            104: same_type_stacks['mp'],
            105: same_type_stacks['mlp'],
            106: same_type_stacks['lp']
        }
        StacksMaker.same_type_stacks_amount = same_type_stacks_fixed
        StacksMaker.mix_type_stacks_amount = mix_type_stacks
        return same_type_stacks_fixed, mix_type_stacks, self.parcels

    def make_objects(self, same_type_stacks, mix_type_stacks):
        stacks = []
        stacks_combined = {**same_type_stacks, **mix_type_stacks}
        for name, value in stacks_combined.items():
            stack_info = parcels.Info.get_stack_info(name)
            stack_members = parcels.Info.get_stack_members(name)
            for _ in range(value):
                stack_obj = Stack(
                    stack_name=(name),
                    stack_height=stack_info[2],
                    stack_width=stack_info[0], stack_length=stack_info[1], parcel_members=stack_members, weight_each=self.find_weight(name))
                stacks.append((stack_obj))
        return stacks

    def find_weight(self, stack_name):
        weight = {}
        for key, value in parcels.Info.get_stack_members(stack_name).items():
            weight_per_fl = list()
            for x in range(len(value)):
                #append_value = self.parcels_weight[value[x]][0]
                # print(value[x], len(self.parcels_weight[value[x]]))
                # if len(self.parcels_weight[value[x]]) == 1:
                #     append_value = self.parcels_weight[value[x]][0]
                #     self.parcels_weight[value[x]].pop(0)
                # else :
                #     index = self.parcels_weight[value[x]].index(append_value)
                #     self.parcels_weight[value[x]].pop(index)

                if value[x] == 'ssp' :
                    min_range = 5
                    max_range = 15
                elif value[x] == 'smp':
                    min_range = 5
                    max_range = 50
                elif value[x] == 'hssp':
                    min_range = 12
                    max_range = 50
                elif value[x] == 'mlp':
                    min_range = 20
                    max_range = 50
                elif value[x] == 'mp':
                    min_range = 28
                    max_range = 50
                elif value[x] == 'lp' or value[x] == 'lhp':
                    min_range = 37
                    max_range = 50
                weight_per_fl.append(random.randint(min_range, max_range))
            weight[key] = weight_per_fl
        return weight

    def execute(self):
        same_type_stacks, mix_type_stacks, remaining_parcels = self.make_stacks()
        stacks_obj = self.make_objects(same_type_stacks, mix_type_stacks)
        stacks_obj.append(StacksMaker.stack_zero)
        return stacks_obj, remaining_parcels, same_type_stacks, mix_type_stacks

if __name__ == '__main__':
    dummy_parcels  = {
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
        'ssp' : [10],
        'smp' : [10],
        'hssp' : [10],
        'mlp' : [10],
        'mp' : [10],
        'lp' : [10],
        'lhp' : [10], 
        'etc' : [10]
    }
    stack_maker = StacksMaker(dummy_parcels, dummy_weights)
    stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
    for x in stacks:
        print(x.name)
