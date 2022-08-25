import copy
import json
import random
#import matplotlib.pyplot as plt
import parcels
import os
from collections import Counter
from sys import platform
''' Stack class '''


class Stack:
    def __init__(self, parcel_members, weight_each, stack_height, stack_width, stack_length, stack_name):
        self.members = parcel_members
        self.weight_each = weight_each
        self.height = stack_height
        self.width = stack_width
        self.length = stack_length
        self.name = stack_name
        self.area = self.width * self.length
        self.volume = self.area * self.height
        self.id = self.gen_id()
    def gen_id(self):
        password = ''
        char_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        for len in range(128):
            random_char = random.choice(char_seq)
            password += random_char
        list_pass = list(password)
        random.shuffle(list_pass)
        id = ''.join(list_pass)
        return id

''' Stacks Making Section '''


class StacksMaker:
    same_type_stacks_amount = None
    mix_type_stacks_amount = None
    stack_zero = Stack([], weight_each={
        'fl_1': [0]
    }, stack_height=0, stack_width=0, stack_length=0, stack_name=0)

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
                mix_type_stacks[202] += 1
                self.parcels['smp'] -= 2
                self.parcels['etc'] -= 1
            elif self.parcels['ssp'] >= 2 and self.parcels['etc'] >= 1:
                mix_type_stacks[203] += 1
                self.parcels['ssp'] -= 2
                self.parcels['etc'] -= 1
            elif self.parcels['etc'] >= 2 and self.parcels['lhp'] >= 1:
                mix_type_stacks[204] += 1
                self.parcels['etc'] -= 2
                self.parcels['lhp'] -= 1
            elif self.parcels['hssp'] >= 3 and self.parcels['mp'] >= 1:
                mix_type_stacks[205] += 1
                self.parcels['hssp'] -= 3
                self.parcels['mp'] -= 1
            elif self.parcels['smp'] >= 6 and self.parcels['mlp'] >= 1:
                mix_type_stacks[206] += 1
                self.parcels['smp'] -= 6
                self.parcels['mlp'] -= 1
            elif self.parcels['lp'] >= 2 and self.parcels['lhp'] >= 1:
                mix_type_stacks[207] += 1
                self.parcels['lp'] -= 2
                self.parcels['lhp'] -= 1
            elif self.parcels['smp'] >= 6 and self.parcels['mp'] >= 1:
                mix_type_stacks[208] += 1
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
                    stack_name=name,
                    stack_height=stack_info[2],
                    stack_width=stack_info[0], stack_length=stack_info[1], parcel_members=stack_members, weight_each=self.find_weight(name))
                stacks.append(copy.deepcopy(stack_obj))
        return stacks.copy()

    def find_weight(self, stack_name):
        weight = {}
        for key, value in parcels.Info.get_stack_members(stack_name).items():
            weight_per_fl = list()
            for x in range(len(value)):
                append_value = self.parcels_weight[value[x]][0]
                weight_per_fl.append(append_value)
            weight[key] = weight_per_fl
        return weight

    def execute(self):
        same_type_stacks, mix_type_stacks, remaining_parcels = self.make_stacks()
        stacks_obj = self.make_objects(same_type_stacks, mix_type_stacks)
        stacks_obj.append(StacksMaker.stack_zero)
        return stacks_obj, remaining_parcels, same_type_stacks, mix_type_stacks


''' Genetic Algorithm or GA section '''


def generate_initial_population(remaining_stacks: list) -> list:
    pop = list()
    _backup_remaining_stacks = remaining_stacks.copy()
    for _ in range(100):
        chrom = list()
        chrom_id = list()
        # if len(remaining_stacks) < 33:
        #     print("< 33")
        #     for x in remaining_stacks:
        #         chrom.append(copy.deepcopy(x))
        #     for _ in range(33 - len(remaining_stacks)):
        #         chrom.append(copy.deepcopy(StacksMaker.stack_zero))
        # elif len(remaining_stacks) >= 33 :
        for _ in range(33):
            rand_gene = random.choice(remaining_stacks)
            #     for j in _backup_remaining_stacks:
            #         if j.id not in chrom_id:
            while rand_gene.id in chrom_id:
                #print(rand_gene.id)
                rand_gene = random.choice(remaining_stacks)
                if rand_gene.name == 0:
                    break
            chrom_id.append(rand_gene.id)
            chrom.append(copy.deepcopy(rand_gene))
            
            # chrom.append(copy.deepcopy(rand_gene))
            # removed_index = _backup_remaining_stacks.index(rand_gene)
            # _backup_remaining_stacks.pop(removed_index)
        pop.append(chrom)
        #_backup_remaining_stacks = remaining_stacks.copy()
    return pop


def get_fitness_values(population: list, container_info : list) -> list:
    print("In getting fitness values")
    fitness_values = list()
    priority_values = 1 / 7
    for x in population:
        #print(f"Container_Width = {container_info[0]}")
        container_area = container_info[0] * container_info[1]
        biggest_stack_info = parcels.Info.get_stack_info(106)
        maximum_area = (biggest_stack_info[0] * biggest_stack_info[1]) * len(x)
        maximum_length = biggest_stack_info[1] * 11
        maximum_width = biggest_stack_info[0] * 3
        maximum_estimated_weight = 100000
        maximum_balancing_weight = int(100000 / 3) # a container can be divided into 3 sections
        standard_balancing_weight_value = int(container_info[3] / 3)
        area = 1 - abs(container_area - get_area(x)) / maximum_area
        length_chrom = get_length(x)
        width_chrom = get_width(x)
        height_chrom = get_height(x)
        maximum_height = 2.31
        duplicated_genes = get_duplicated_genes(x)
        # area_chrom = get_area(x)
        # weight_chrom = get_weight(x)
        # weight_balancing_score_chrom = get_weight_balancing(x)[1]
        if length_chrom > container_info[1]:
            length = (1 - abs(container_info[1] - length_chrom) / maximum_length) / 2
        else :
            length = 1 - abs(container_info[1] - length_chrom) / maximum_length
        if width_chrom > container_info[0]:
            width = (1 - abs(container_info[0] - get_width(x)) / maximum_width) / 2
        else :
            width = (1 - abs(container_info[0] - get_width(x)) / maximum_width)
        if height_chrom > container_info[2]:
            height = ((1 - abs(container_info[2] - height_chrom)) / maximum_height) / 2
        else :
            height = ((1 - abs(container_info[2] - height_chrom)) / maximum_height)
        if duplicated_genes > 33:
            duplicated_genes_count = ((1 - abs(0 - duplicated_genes)) / 33) / 2
        else :
            duplicated_genes_count = ((1 - abs(0 - duplicated_genes)) / 33)
        weight = 1 - abs(container_info[3] - get_weight(x)) / maximum_estimated_weight
        weight_balancing_score = 1 - \
            abs(standard_balancing_weight_value - get_weight_balancing(x)[1]) / maximum_balancing_weight
        #print(area, length, width)
        # fitness_values.append(-abs((((28.44 - area)) * priority_values[0])) + (
        #     (12 - length) * priority_values[1]) + ((2.37 - width) * priority_values[2]) + (((21700 - weight)/1000) * priority_values[3]) + ((weight_balancing_score / 1000) * priority_values[4]))
        fitness_values.append((area * priority_values) + (length * priority_values) + (
            width * priority_values) + (height * priority_values) + (duplicated_genes_count * priority_values) +(weight * priority_values) + (weight_balancing_score * priority_values))
    return fitness_values


def selection(population: list, fitness_values: list) -> list:
    offspring_selection = list()
    for _ in range(30):
        max_idx = fitness_values.index(max(fitness_values))
        offspring_selection.append(population[max_idx])
        fitness_values[max_idx] = -99
    print("Done Selection")
    return offspring_selection


def one_point_crossover(offspring_selection: list):
    offspring_crossover = list()
    uniform_positions = list()
    # uniform_rate_range = (1, random.randint(1, 10))
    # uniform_positions_count = random.randint(uniform_rate_range[0], int(len(offspring_selection[0]) * uniform_rate_range[1]))
    for _ in range(10):
        random_value = random.randint(0, 32)
        while random_value in uniform_positions:
            random_value = random.randint(0, 32)
        uniform_positions.append(random_value)
    for i in range(len(offspring_selection)):
        child_one = copy.deepcopy(offspring_selection[i])
        child_two = copy.deepcopy(
            offspring_selection[(len(offspring_selection) - 1) - i])
        for x in uniform_positions:
            temp_c_one = child_two[x]
            temp_c_two = child_one[x]
            child_one[x] = temp_c_one
            child_two[x] = temp_c_two
        offspring_crossover.append(child_one)
        offspring_crossover.append(child_two)
    # for i in range(len(offspring_selection)):
    #     cross_point = random.randint(0, 32)
    #     parent_one_left = offspring_selection[i][0:cross_point]
    #     parent_one_right = offspring_selection[i][cross_point:]
    #     parent_two_left = offspring_selection[len(
    #         offspring_selection) - 1 - i][0:cross_point]
    #     parent_two_right = offspring_selection[len(
    #         offspring_selection) - 1 - i][cross_point:]

    #     new_child_one = parent_one_left + parent_two_right
    #     new_child_two = parent_one_right + parent_two_left

    #     offspring_crossover.append(new_child_one)
    #     offspring_crossover.append(new_child_two)
    print("Done crossover")
    return offspring_crossover

def runcx(offspring_selection : list):
    offspring_crossover = list()
    for idx, v in enumerate(offspring_selection):
        if idx + 1 == len(offspring_crossover):
            break
        parent_one = v
        parent_two = offspring_selection[idx + 1]
        child_one, child_two = cxPartialyMatched(parent_one, parent_two)
        offspring_crossover.append(child_one)
        offspring_crossover.append(child_two)
    return offspring_crossover
def cxPartialyMatched(ind1, ind2):
    """Executes a partially matched crossover (PMX) on the input individuals.
    The two individuals are modified in place. This crossover expects
    :term:`sequence` individuals of indices, the result for any other type of
    individuals is unpredictable.
    :param ind1: The first individual participating in the crossover.
    :param ind2: The second individual participating in the crossover.
    :returns: A tuple of two individuals.
    Moreover, this crossover generates two children by matching
    pairs of values in a certain range of the two parents and swapping the values
    of those indexes. For more details see [Goldberg1985]_.
    This function uses the :func:`~random.randint` function from the python base
    :mod:`random` module.
    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
       salesman problem", 1985.
    """
    size = 33
    # p1, p2 = [0] * size, [0] * size

    # # Initialize the position of each indices in the individuals
    # for i in range(size):
    #     ind1[i] = i
    #     ind2[i] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2]] = temp2, temp1
        ind2[i], ind2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2

def adaptive_mutation(offspring_crossover: list, fitness_values: list, stacks : list, container_info : list) -> list:
    offspring_mutation = list()
    standard_rate = 0.11
    container_length = container_info[1]
    container_width = container_info[0]
    container_weight = container_info[3]
    avg_fitness_value = sum(fitness_values) / len(fitness_values)
    for _ in range(10):
        random_chrom = random.choice(offspring_crossover)
        if get_fitness_by_one(random_chrom, container_info) > avg_fitness_value:
            standard_rate = 0.15
        for _ in range(int(standard_rate * 33)):
            if get_length(random_chrom) > container_length or get_width(random_chrom) > container_width or get_weight(random_chrom) > container_weight:
                to_mutate_value = copy.deepcopy(StacksMaker.stack_zero)
            else :
                to_mutate_value = copy.deepcopy(random.choice(stacks))
                if is_all_zero(random_chrom):
                    is_in_mutated_chrom = False
                else :
                    is_in_mutated_chrom = True
                while is_in_mutated_chrom:
                    for j in random_chrom:
                        if j.id == to_mutate_value.id:
                            to_mutate_value = copy.deepcopy(random.choice(stacks))
                            break
                        else :
                            is_in_mutated_chrom = False
                # while to_mutate_value in random_chrom:
                #    to_mutate_value = copy.deepcopy(random.choice(stacks))
            random_position = random.randint(0, 32)
            streak = 0
            if not is_all_zero(random_chrom):
                print("Not zeros ")
                while random_chrom[random_position].name == 0:
                    if streak == len(random_chrom):
                        break
                    random_position = random.randint(0, 32)
                    streak += 1
            else :
                print("ALL ZEROS")
            random_chrom[random_position] = to_mutate_value
        random_position_one = random.randint(0, 32)
        random_position_two = random.randint(0, 32)
        random_position_three = random.randint(0, 32)
        random_position_one_swap = random.randint(0, 32)
        random_position_two_swap = random.randint(0, 32)
        random_position_three_swap = random.randint(0, 32)

        random_chrom[random_position_one], random_chrom[random_position_two], random_chrom[random_position_three] = random_chrom[
            random_position_one_swap], random_chrom[random_position_two_swap], random_chrom[random_position_three_swap]
        print('Done mutation')
        offspring_mutation.append(random_chrom.copy())
    return offspring_mutation


def get_fitness_by_one(chrom, container_info):
    priority_values = 1 / 7
    container_area = container_info[0] * container_info[1]
    biggest_stack_info = parcels.Info.get_stack_info(106)
    maximum_area = (biggest_stack_info[0] * biggest_stack_info[1]) * len(chrom)
    maximum_length = biggest_stack_info[1] * 11
    maximum_width = biggest_stack_info[0] * 3
    maximum_estimated_weight = 100000
    maximum_balancing_weight = int(100000 / 3) # a container can be divided into 3 sections
    standard_balancing_weight_value = int(container_info[3] / 3)
    area = 1 - abs(container_area - get_area(chrom)) / maximum_area
    length_chrom = get_length(chrom)
    width_chrom = get_width(chrom)
    height_chrom = get_height(chrom)
    maximum_height = 2.31
    duplicated_genes = get_duplicated_genes(chrom)
    if length_chrom > container_info[1]:
        length = (1 - abs(container_info[1] - length_chrom) / maximum_length) / 2
    else :
        length = 1 - abs(container_info[1] - length_chrom) / maximum_length
    if width_chrom > container_info[0]:
        width = (1 - abs(container_info[0] - get_width(chrom)) / maximum_width) / 2
    else :
        width = (1 - abs(container_info[0] - get_width(chrom)) / maximum_width)
    if height_chrom > container_info[2]:
        height = (1 - abs(container_info[2] - height_chrom) / maximum_height) / 2
    else :
        height = (1 - abs(container_info[2] - height_chrom) / maximum_height)
    if duplicated_genes > 33:
        duplicated_genes_count = ((1 - abs(0 - duplicated_genes)) / 33) / 2
    else :
        duplicated_genes_count = ((1 - abs(0 - duplicated_genes)) / 33)
    weight = 1 - abs(container_info[3] - get_weight(chrom)) / maximum_estimated_weight
    weight_balancing_score = 1 - \
        abs(standard_balancing_weight_value - get_weight_balancing(chrom)[1]) / maximum_balancing_weight
    final_score = (area * priority_values) + (length * priority_values) + (width * priority_values) + (height * priority_values) + (duplicated_genes_count * priority_values)+(
        weight * priority_values) + (weight_balancing_score * priority_values)
    return final_score

def is_all_zero(chrom):
    zero_count = 0
    for j in chrom:
        if j.name == 0:
            zero_count += 1
    if zero_count == len(chrom):
        return True
    else :
        return False

def is_all_chrom_zero(pop):
    pop_length = len(pop)
    zero_chrom_count = 0
    for j in pop:
        zero_count = 0
        for x in j:
            if x.name == 0:
                zero_count += 1
        if zero_count == len(pop[0]):
            zero_chrom_count += 1
    if zero_chrom_count == pop_length:
        return True
    else :
        return False
def get_height(chrom):
    highest = chrom[0].height
    for x in chrom:
        if x.height > highest:
            highest = x.height
    return highest

def get_weight(chrom):
    sum_weight = 0
    for x in chrom:
        for k, v in x.weight_each.items():
            sum_weight += sum(v)
    return sum_weight


def get_length(chrom):
    parcels_count = {
        101: 0,
        102: 0,
        103: 0,
        104: 0,
        105: 0,
        106: 0,
        201: 0,
        202: 0,
        203: 0,
        204: 0,
        205: 0,
        206: 0,
        207: 0,
        208: 0,
        0: 0
    }
    for x in chrom:
        parcels_count[x.name] += 1
    result_length = 0
    is_only_small_types = (parcels_count[104] + parcels_count[105] + parcels_count[106] + parcels_count[204] +
                           parcels_count[205] + parcels_count[206] + parcels_count[207] + parcels_count[208] == 0)
    if is_only_small_types:
        result_length = get_length_small_types(chrom)
    else:
        lengths = [
            [chrom[0].length, chrom[1].length, chrom[2].length],
            [chrom[3].length, chrom[4].length, chrom[5].length],
            [chrom[6].length, chrom[7].length, chrom[8].length],
            [chrom[9].length, chrom[10].length, chrom[11].length],
            [chrom[12].length, chrom[13].length, chrom[14].length],
            [chrom[15].length, chrom[16].length, chrom[17].length],
            [chrom[18].length, chrom[19].length, chrom[20].length],
            [chrom[21].length, chrom[22].length, chrom[23].length],
            [chrom[24].length, chrom[25].length, chrom[26].length],
            [chrom[27].length, chrom[28].length, chrom[29].length],
            [chrom[30].length, chrom[31].length, chrom[32].length]
        ]
        for x in lengths:
            result_length += max(x)
    return result_length


def get_length_small_types(chrom):
    x1, x2, x3 = [chrom[0].length,
                  chrom[3].length,
                  chrom[6].length,
                  chrom[9].length,
                  chrom[12].length,
                  chrom[15].length,
                  chrom[18].length,
                  chrom[21].length,
                  chrom[24].length,
                  chrom[27].length,
                  chrom[30].length],   [chrom[1].length,
                                        chrom[4].length,
                                        chrom[7].length,
                                        chrom[10].length,
                                        chrom[13].length,
                                        chrom[16].length,
                                        chrom[19].length,
                                        chrom[22].length,
                                        chrom[25].length,
                                        chrom[28].length,
                                        chrom[31].length],     [chrom[2].length,
                                                                chrom[5].length,
                                                                chrom[8].length,
                                                                chrom[11].length,
                                                                chrom[14].length,
                                                                chrom[17].length,
                                                                chrom[20].length,
                                                                chrom[23].length,
                                                                chrom[26].length,
                                                                chrom[29].length,
                                                                chrom[32].length]

    all_length = [sum(x1), sum(x2, sum(x3))]
    return max(all_length)

def get_duplicated_genes(chrom):
    chrom_id = list()
    duplicated_genes_count = 0
    for j in chrom:
        chrom_id.append(j.id)
    zero_id = None
    for j in chrom:
        if j.name == 0:
            zero_id = j.id
            break
    res = Counter(chrom_id)
    for k, v in res.items():
        res[k] -= 1
    res[zero_id] = 0
    duplicated_genes_count = sum(list(res.values()))
    return duplicated_genes_count

def get_width(chrom):
    widths = [
        sum([chrom[0].width, chrom[1].width, chrom[2].width]),
        sum([chrom[3].width, chrom[4].width, chrom[5].width]),
        sum([chrom[6].width, chrom[7].width, chrom[8].width]),
        sum([chrom[9].width, chrom[10].width, chrom[11].width]),
        sum([chrom[12].width, chrom[13].width, chrom[14].width]),
        sum([chrom[15].width, chrom[16].width, chrom[17].width]),
        sum([chrom[18].width, chrom[19].width, chrom[20].width]),
        sum([chrom[21].width, chrom[22].width, chrom[23].width]),
        sum([chrom[24].width, chrom[25].width, chrom[26].width]),
        sum([chrom[27].width, chrom[28].width, chrom[29].width]),
        sum([chrom[30].width, chrom[31].width, chrom[32].width]),
    ]
    # print(widths)
    return max(widths)


def get_area(chrom):
    area = 0
    for x in chrom:
        area += x.area
    return area


def get_weight_balancing(chrom):
    weight_section = [0, 0, 0]
    sections_index_ending = [10, 21, 32]
    sum_weight = 0
    chrom_arr = []
    cnt = 0
    sub_chrom = list()
    for x in chrom:
        if cnt == 3:
            chrom_arr.append(copy.deepcopy(sub_chrom))
            cnt = 0
            sub_chrom.clear()
        sub_chrom.append(x.name)
    _back_up_chrom = copy.deepcopy(chrom)
    for _ in range(chrom_arr.count([0, 0, 0])):
        zero_index = chrom_arr.index([0, 0, 0])
        _back_up_chrom.append(_back_up_chrom.pop(zero_index))
        chrom_arr.sort(key=[0, 0, 0].__eq__)
    for _ in range(len(chrom)):
        if _ in sections_index_ending:
            weight_section[int(str(_)[1])] += sum_weight
            sum_weight = 0
        for k, v in _back_up_chrom[_].weight_each.items():
            sum_weight += sum(v)
    balancing_score = 0
    balancing_standard = sum(weight_section) / len(weight_section)
    for j in weight_section:
        balancing_score += balancing_standard - j
    return weight_section, balancing_score


def visualizing_result(chrom):
    cnt = 0
    for x in chrom:
        if cnt == 3:
            print()
            cnt = 0
        print(x.name, end=" ")
        cnt += 1

def get_remaining_stacks(optimal_chrom : list, remaining_stacks : list):
    for x in optimal_chrom:
        if x.name == 0:
            pass
        else :
            for j in remaining_stacks:
                if x.id == j.id:
                    remaining_stacks.remove(j)

    return remaining_stacks

def is_remain_validated(chrom : list, remaining_stacks : list):
    is_valid = True
    for x in chrom:
        if x not in remaining_stacks:
            is_valid = False
    return is_valid

def run_two(container_id : str, parcels_data : dict, weights : dict, first_run=False, remaining_stacks_input=None):
    if first_run:
        stack_maker = StacksMaker(parcels_data, weights)
        stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
        stacks.append(copy.deepcopy(StacksMaker.stack_zero))
        remaining_stacks = stacks.copy()
    else :
        remaining_stacks = remaining_stacks_input.copy()
    pop = generate_initial_population(remaining_stacks.copy())
    # if is_all_chrom_zero(pop):
    #     print("All chroms are zeros.")
    #     body = {'Status' : 2}
    #     return [body, remaining_stacks.copy()]
    prev_score = 0
    score_streak = 0
    scores_to_plot = list()
    gens = list()
    container_data = parcels.Info.get_container_info(container_id)
    container_data.append(parcels.Info.get_container_weight(container_id))
    for x in range(2500):
        if platform == 'linux' or platform == 'darwin':
            os.system("clear")
        else :
            os.system('cls')
        #print(len(stacks))
        fitness_values = get_fitness_values(pop, container_data)
        print(f"Running @ Generation {x+1}")
        print(f'Fitness Value = {max(fitness_values)}')
        # for i in pop[fitness_values.index(max(fitness_values))]:
        #     print(i.name)
        length = get_length(pop[fitness_values.index(max(fitness_values))])
        width = get_width(pop[fitness_values.index(max(fitness_values))])
        area = get_area(pop[fitness_values.index(max(fitness_values))])
        print(area, width, length)
        print(get_duplicated_genes(pop[fitness_values.index(max(fitness_values))]))
        visualizing_result(pop[fitness_values.index(max(fitness_values))])
        weight_section = get_weight_balancing(
            pop[fitness_values.index(max(fitness_values))])[0]
        print(f"\n{weight_section}")
        if prev_score == max(fitness_values):
            if score_streak > 50:
                break
            else:
                score_streak += 1
        else:
            score_streak = 0
        offspring_selection = selection(pop, fitness_values)
        offspring_crossover = one_point_crossover(offspring_selection)
        #offspring_crossover = runcx(offspring_selection)
        offspring_mutation = adaptive_mutation(
            offspring_crossover, fitness_values, remaining_stacks.copy(), container_data)
        pop = offspring_selection + offspring_crossover + offspring_mutation
        prev_score = max(fitness_values)
        scores_to_plot.append(max(fitness_values))
        gens.append(x+1)
        #print(len(stacks))
    body = make_arr_response(pop[fitness_values.index(max(fitness_values))], container_id)
    remaining_stacks = get_remaining_stacks(pop[fitness_values.index(max(fitness_values))], remaining_stacks.copy())
    #remaining_parcels = get_remaining_parcels(pop[fitness_values.index(max(fitness_values))], parcels_data.copy())
    #print(is_remain_validated(pop[fitness_values.index(max(fitness_values))], stacks.copy()))
    # print(len(remaining_stacks))
    # plt.plot(gens, scores_to_plot)
    # plt.show()
    # to_json(body)
    return [body, remaining_stacks.copy()]
def run(containers_arr : list, parcels_data : dict, weights : dict):
    global remaining_stacks
    global container_data
    con_index = 0
    stack_maker = StacksMaker(parcels_data, weights)
    stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
    stacks.append(copy.deepcopy(StacksMaker.stack_zero))
    remaining_stacks = stacks.copy()
    bodies = list()
    while len(remaining_stacks) > 18:
        scores_to_plot = list()
        gens = list()
        pop = generate_initial_population(stacks)
        prev_score = 0
        score_streak = 0
        container_data = parcels.Info.get_container_info(containers_arr[con_index])
        container_data.append(parcels.Info.get_container_weight(containers_arr[con_index]))
        for x in range(1000):
            os.system('clear')
            os.system('cls')
            fitness_values = get_fitness_values(pop, container_data)
            print(f"Running @ Generation {x+1}")
            print(f'Fitness Value = {max(fitness_values)}')
            # for i in pop[fitness_values.index(max(fitness_values))]:
            #     print(i.name)
            length = get_length(pop[fitness_values.index(max(fitness_values))])
            width = get_width(pop[fitness_values.index(max(fitness_values))])
            area = get_area(pop[fitness_values.index(max(fitness_values))])
            print(area, width, length)
            visualizing_result(pop[fitness_values.index(max(fitness_values))])
            weight_section = get_weight_balancing(
                pop[fitness_values.index(max(fitness_values))])[0]
            print(f"\n{weight_section}")
            if prev_score == max(fitness_values):
                if score_streak > 250:
                    break
                else:
                    score_streak += 1
            else:
                score_streak = 0
            offspring_selection = selection(pop, fitness_values)
            offspring_crossover = one_point_crossover(offspring_selection)
            offspring_mutation = adaptive_mutation(
                offspring_crossover, fitness_values, container_info=container_data, stacks=remaining_stacks.copy())
            pop = offspring_selection + offspring_crossover + offspring_mutation
            prev_score = max(fitness_values)
            scores_to_plot.append(max(fitness_values))
            gens.append(x+1)
        body = make_arr_response(pop[fitness_values.index(max(fitness_values))], containers_arr[con_index])
        bodies.append(body)
        remaining_stacks = get_remaining_stacks(pop[fitness_values.index(max(fitness_values))], remaining_stacks)
        if con_index + 1 > len(containers_arr) - 1:
            con_index = 0
        else :
            con_index += 1
    to_json(bodies)

def is_duplicated_appeared(chrom):
    elements_counted = None
    chrom_id = list()
    for j in chrom:
        chrom_id.append(j.id)

    elements_counted = Counter(chrom_id)
    for k, v in elements_counted.items():
        elements_counted[k] -= 1
    if sum(list(elements_counted.values())) == 0:
        return False
    else :
        return True

def clean_duplicated_values(chrom):
    duplicated_key = None
    chrom_id = list()
    for j in chrom:
        chrom_id.append(j.id)
    elements_count = Counter(chrom_id)
    for k, v in elements_count.items():
        if v > 0:
            duplicated_key = k
            break

    duplicated_count = 0
    for x, j in enumerate(chrom):
        if j.id == duplicated_key and duplicated_count != 0:
            chrom[x] = StacksMaker.stack_zero

    chrom_name = [
        [chrom[0].name, chrom[1].name, chrom[2].name],
        [chrom[3].name, chrom[4].name, chrom[5].name],
        [chrom[6].name, chrom[7].name, chrom[8].name],
        [chrom[9].name, chrom[10].name, chrom[11].name],
        [chrom[12].name, chrom[13].name, chrom[14].name],
        [chrom[15].name, chrom[16].name, chrom[17].name],
        [chrom[18].name, chrom[19].name, chrom[20].name],
        [chrom[21].name, chrom[22].name, chrom[23].name],
        [chrom[24].name, chrom[25].name, chrom[26].name],
        [chrom[27].name, chrom[28].name, chrom[29].name],
        [chrom[30].name, chrom[31].name, chrom[32].name],
    ]
    return chrom_name
    

def make_arr_response(chrom, container_id):
    stacks_count = 0
    stacks_info = []
    chrom_arr_2 = [
        [chrom[0].name, chrom[1].name, chrom[2].name],
        [chrom[3].name, chrom[4].name, chrom[5].name],
        [chrom[6].name, chrom[7].name, chrom[8].name],
        [chrom[9].name, chrom[10].name, chrom[11].name],
        [chrom[12].name, chrom[13].name, chrom[14].name],
        [chrom[15].name, chrom[16].name, chrom[17].name],
        [chrom[18].name, chrom[19].name, chrom[20].name],
        [chrom[21].name, chrom[22].name, chrom[23].name],
        [chrom[24].name, chrom[25].name, chrom[26].name],
        [chrom[27].name, chrom[28].name, chrom[29].name],
        [chrom[30].name, chrom[31].name, chrom[32].name],
    ]
    if is_duplicated_appeared(chrom):
       chrom_arr_2 = clean_duplicated_values(chrom.copy())
    for _ in range(chrom_arr_2.count([0, 0, 0])):
        chrom_arr_2.sort(key=[0, 0, 0].__eq__)
    stacks_counted = {
        101 : 0,
        102 : 0,
        103 : 0,
        104 : 0,
        105 : 0,
        106 : 0,
        201 : 0,
        202 : 0, 
        203 : 0,
        204 : 0,
        205 : 0,
        206 : 0,
        207 : 0,
        208 : 0,
    }
    for x in chrom_arr_2:
        for z in x:
            #print(type(z))
            if z != 0:
                stacks_counted[z] += 1
    for j in chrom:
        if j.name != 0:
            #if stacks_counted[j.name] != 0:
                stacks_info.append({
                    "StackType" : j.name,
                    "StackWidth" : round(j.width, 2),
                    "StackLength" : round(j.length, 2),
                    "StackHeight" : round(j.height, 2),
                    "StackArea" : round(j.area, 2),
                    "StackVolume" : round(j.volume, 2),
                    "StackWeight" : get_stack_weight(j.weight_each)
                })
                stacks_count += 1
                #stacks_counted[j.name] = 0
    total_parcels = get_total_parcels(chrom)
    body = {
        "ArrangementPattern" : chrom_arr_2,
        'ContainerTotalArea' : get_area(chrom),
        "ContainerTotalWeight" : get_weight(chrom),
        "ContainerType" : container_id,
        "StacksInformation" : stacks_info,
        "StacksCounted" : stacks_count,
        "StacksName" : list(stacks_counted.keys()),
        "StacksAmount" : list(stacks_counted.values()),
        "TotalParcelsUsageName" : list(total_parcels.keys()),
        "TotalParcelsUsageAmount" : list(total_parcels.values())
    }
    return body

def get_total_parcels(chrom):
    parcels = {
        "ssp" : 0,
        'smp' : 0,
        'hssp' : 0,
        'mp' : 0,
        'mlp' : 0,
        'lhp' : 0,
        'lp' : 0,
        'etc' : 0,
    }
    print(chrom[0].members)
    for x in chrom:
        if type(x.members) is dict:
            for k, v in x.members.items():
                for c in v:
                    parcels[c] += 1
    return parcels
def get_stack_weight(stack_weight_each : dict):
    weight = 0
    for k, v in stack_weight_each.items():
        weight += sum(v)
    return weight

def to_json(bodies):
    sub_chrom = list()
    chrom_arr = list()
    cnt = 0
    # for x in chrom:
    #     if cnt == 3:
    #         chrom_arr.append(sub_chrom.copy())
    #         sub_chrom.clear()
    #         cnt = 0
    #     sub_chrom.append(x.name)
    #     cnt += 1
    # chrom_arr_2 = [
    #     [chrom[0].name, chrom[1].name, chrom[2].name],
    #     [chrom[3].name, chrom[4].name, chrom[5].name],
    #     [chrom[6].name, chrom[7].name, chrom[8].name],
    #     [chrom[9].name, chrom[10].name, chrom[11].name],
    #     [chrom[12].name, chrom[13].name, chrom[14].name],
    #     [chrom[15].name, chrom[16].name, chrom[17].name],
    #     [chrom[18].name, chrom[19].name, chrom[20].name],
    #     [chrom[21].name, chrom[22].name, chrom[23].name],
    #     [chrom[24].name, chrom[25].name, chrom[26].name],
    #     [chrom[27].name, chrom[28].name, chrom[29].name],
    #     [chrom[30].name, chrom[31].name, chrom[32].name],
    # ]
    # for _ in range(chrom_arr_2.count([0, 0, 0])):
    #     chrom_arr_2.sort(key=[0, 0, 0].__eq__)
    body = {
        "Response" : {
            "Containers" : []
        }
    }
    body['Response']['Containers'].append(bodies)
    json_file = open("outputs.json", 'a')
    json_file.write(json.dumps(body))
def get_remaining_parcels(chrom : list, remaining_parcels : dict):
    for x in chrom:
        if x.name == 0:
            pass
        else :
            members = parcels.Info.get_stack_members(x.name)
            for k, v in members.items():
                for l in v:
                    remaining_parcels[l] -= 1
    return remaining_parcels
if __name__ == '__main__':
    dummy_parcels = {
        'ssp': 100,
        'smp': 100,
        'hssp': 100,
        'mlp': 100,
        'mp': 100,
        'lp': 200,
        'lhp': 200,
        'etc': 100
    }
    dummy_weights = {
        'ssp': [10],
        'smp': [10],
        'hssp': [10],
        'mlp': [10],
        'mp': [10],
        'lp': [10],
        'lhp': [10],
        'etc': [10]
    }
    con_index = 0
    containers_arr = ["Small", "Large"]
    response, remaining_stacks = run_two(containers_arr[con_index], dummy_parcels, dummy_weights, first_run=True)
    con_index += 1
    test_arr_responses = list()
    while len(remaining_stacks) > 24:
        response, remaining_stacks = run_two(containers_arr[con_index], dummy_parcels, dummy_weights, remaining_stacks_input=remaining_stacks.copy())
        if con_index + 1 > len(containers_arr) - 1:
            con_index = 0
        else :
            con_index += 1
        test_arr_responses.append(response)
    print(test_arr_responses)
    # run(["Small", "Large"], dummy_parcels, dummy_weights)
    # # stack_maker = StacksMaker(dummy_parcels, dummy_weights)
    # stacks, remaining_parcels, same_type_stacking, mix_type_stacking = stack_maker.execute()
    # stacks.append(copy.deepcopy(StacksMaker.stack_zero))
    # pop = generate_initial_population(stacks)
    # prev_score = 0
    # score_streak = 0
    # scores_to_plot = list()
    # gens = list()
    # container_data = parcels.Info.get_container_info("Large")
    # container_data.append(parcels.Info.get_container_weight("Large"))
    # for x in range(2500):
    #     os.system('cls')
    #     os.system('clear')
    #     print(len(stacks))
    #     fitness_values = get_fitness_values(pop, container_data)
    #     print(f"Running @ Generation {x+1}")
    #     print(f'Fitness Value = {max(fitness_values)}')
    #     # for i in pop[fitness_values.index(max(fitness_values))]:
    #     #     print(i.name)
    #     length = get_length(pop[fitness_values.index(max(fitness_values))])
    #     width = get_width(pop[fitness_values.index(max(fitness_values))])
    #     area = get_area(pop[fitness_values.index(max(fitness_values))])
    #     print(area, width, length)
    #     visualizing_result(pop[fitness_values.index(max(fitness_values))])
    #     weight_section = get_weight_balancing(
    #         pop[fitness_values.index(max(fitness_values))])[0]
    #     print(f"\n{weight_section}")
    #     if prev_score == max(fitness_values):
    #         if score_streak > 250:
    #             break
    #         else:
    #             score_streak += 1
    #     else:
    #         score_streak = 0
    #     offspring_selection = selection(pop, fitness_values)
    #     offspring_crossover = one_point_crossover(offspring_selection)
    #     offspring_mutation = adaptive_mutation(
    #         offspring_crossover, fitness_values, stacks.copy(), container_data)
    #     pop = offspring_selection + offspring_crossover + offspring_mutation
    #     prev_score = max(fitness_values)
    #     scores_to_plot.append(max(fitness_values))
    #     gens.append(x+1)
    #     print(len(stacks))
    # body = make_arr_response(pop[fitness_values.index(max(fitness_values))], "Large")
    # remaining_stacks = get_remaining_stacks(pop[fitness_values.index(max(fitness_values))], stacks.copy())
    # #print(is_remain_validated(pop[fitness_values.index(max(fitness_values))], stacks.copy()))
    # print(len(remaining_stacks))
    # plt.plot(gens, scores_to_plot)
    # plt.show()
    # to_json(body)
    # '''
    # container => [101, {}]
    # container => [stack_name, weight_each]
    # '''
