import copy
import random

from StackMaker import StacksMaker
import parcels


class GeneticAlgorithm:

    def __init__(self, container_id, remaining_parcels, stacks) -> object:
        self.informations = parcels.Info
        container_information = self.informations.get_container_info(
            container_id)
        self._container_id = container_id
        self._remaining_parcels = remaining_parcels
        self._stacks = stacks
        self.CONTAINER_WIDTH = container_information[0]
        self.CONTAINER_LENGTH = container_information[1]
        self.CONTAINER_HEIGHT = container_information[2]
        self.CONTAINER_WEIGHT = self.informations.get_container_weight(
            self._container_id)

    def generate_initial_population(self) -> list:
        population = list()
        for _ in range(100):
            chrom = list()
            for _ in range(33):
                chrom.append(random.choice(self._stacks))
            population.append(chrom)
        return population

    def get_fitness_values(self, alternate_value=None) -> list:
        fitness_values = list()
        if alternate_value != None:
            population = alternate_value
        else:
            population = self._population
        for chrom in population:
            chrom_final_score = None
            chrom_sum_weight = 0
            chrom_weight_balancing = self.get_weight_balancing(chrom)
            chrom_width_score = 0
            chrom_length_score = 0
            chrom_area = 0
            chrom_area_score = 0
            chrom_weight_score = 0
            chrom_weight_balancing_score = 0
            for gene in chrom:
                chrom_area += gene.area
            chrom_weight_score = (self.CONTAINER_WEIGHT -
                                  sum(chrom_weight_balancing))
            chrom_weight_balancing[:] = [(chrom_sum_weight / 3) -
                                          weight_section for weight_section in chrom_weight_balancing]
            chrom_area_score = (
                (self.CONTAINER_LENGTH * self.CONTAINER_WIDTH) - chrom_area)
            chrom_length_score = (self.CONTAINER_LENGTH -
                                  self.get_length(chrom)[0])
            chrom_width_score = (sum(self.get_over_usage_width(chrom)[1]))
            chrom_weight_balancing_score = sum(chrom_weight_balancing)
            chrom_final_score = ((chrom_area_score / 10) - chrom_length_score -
                                 chrom_weight_score - chrom_width_score - (chrom_weight_balancing_score / 1000))
            fitness_values.append(chrom_final_score)
        return fitness_values

    def selection(self) -> list:
        offspring_selection = list()
        offspring_selection_fitness_value = list()
        _backup_fitness = copy.deepcopy(self._fitness_value)
        for _ in range(int(0.3 * len(self._population))):
            max_value_idx = _backup_fitness.index(max(_backup_fitness))
            offspring_selection.append(
                copy.deepcopy(self._population[max_value_idx]))
            offspring_selection_fitness_value.append(
                copy.deepcopy(_backup_fitness[max_value_idx]))
            _backup_fitness[max_value_idx] = -9999999
        return offspring_selection

    def crossover(self, offspring_selection) -> list:
        uniform_positions = list()
        offspring_crossover = list()
        for _ in range(random.randint(0, 16)):
            rand_value = random.randint(0, 32)
            if rand_value not in uniform_positions:
                uniform_positions.append(rand_value)
            else:
                while rand_value in uniform_positions:
                    rand_value = random.randint(0, 32)
                uniform_positions.append(rand_value)
        for x in range(len(offspring_selection)):
            male_parent = x
            female_parent = (len(offspring_selection) - 1) - x
            child_one = copy.deepcopy(offspring_selection[male_parent])
            child_two = copy.deepcopy(offspring_selection[female_parent])
            for j in uniform_positions:
                child_one[j], child_two[j] = copy.deepcopy(
                    child_two[j]), copy.deepcopy(child_one[j])
            offspring_crossover.append(child_one)
            offspring_crossover.append(child_two)
        return offspring_crossover

    def mutation(self, offspring_crossover) -> list:
        # adaptive mutation
        fitness_value = self.get_fitness_values(offspring_crossover)
        offspring_mutation = list()
        for _ in range(10):
            rand_chrom = random.choice(offspring_crossover)
            to_mutate_chrom = copy.deepcopy(rand_chrom)
            if rand_chrom not in offspring_mutation:
                offspring_mutation.append(
                    self.perform_mutation(to_mutate_chrom, fitness_value))
            else:
                while rand_chrom in offspring_mutation:
                    rand_chrom = random.choice(offspring_crossover)
                to_mutate_chrom = copy.deepcopy(rand_chrom)
                offspring_mutation.append(
                    self.perform_mutation(to_mutate_chrom, fitness_value))
        return offspring_mutation

    def perform_mutation(self, to_mutate_chrom, fitness_value):
        mutate_positions = list()
        standard_rate = 0.11
        avg_score = sum(fitness_value) / len(fitness_value)
        fitness_by_one_value = self.get_fitness_by_one(to_mutate_chrom)
        if fitness_by_one_value > avg_score:
            standard_rate = 0.03
        elif fitness_by_one_value < avg_score:
            standard_rate = 0.16
        for _ in range(int(standard_rate * len(self._population[0]))):
            mutate_pos = random.randint(0, 32)
            if mutate_pos not in mutate_positions:
                mutate_positions.append(mutate_pos)
            else:
                while mutate_pos in mutate_positions:
                    mutate_pos = random.randint(0, 32)
                mutate_positions.append(mutate_pos)
        for value in mutate_positions:
            temp = copy.deepcopy(self.get_optimal_value)
            to_mutate_chrom[value] = temp
        return copy.deepcopy(to_mutate_chrom)

    def get_optimal_value(self, parent_chrom, position):
        check_length = self.get_length(parent_chrom)[1]
        check_width, widths = self.get_over_usage_width(parent_chrom)
        pos_y_one = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
        pos_y_two = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
        pos_y_three = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
        mutate_position_y = None
        mutate_pattern = {
            "Y1": [0, 1, 2],
            "Y2": [-1, 0, 1],
            "Y3": [-2, -1, 0]
        }
        if check_length and check_width > 0:
            temp = copy.deepcopy(StacksMaker.stack_zero)
            return temp
        elif check_width > 0 and not check_length:
            if position in pos_y_one:
                mutate_position_y = "Y1"
            elif position in pos_y_two:
                mutate_position_y = "Y2"
            else:
                mutate_position_y = "Y3"
            value_one = parent_chrom[mutate_pattern[mutate_position_y]
                [0] + position]
            value_two = parent_chrom[mutate_pattern[mutate_position_y]
                [1] + position]
            value_three = parent_chrom[mutate_pattern[mutate_position_y][2] + position]
            width_arr = [value_one.width, value_two.width, value_three.width]
            sum_width = sum(width_arr)
            max_width = max(width_arr)
            if (sum_width - max_width) < 0.76:
                temp = copy.deepcopy(StacksMaker.stack_zero)
                return temp
            else:
                for x in self._stacks:
                    if x.width <= (sum_width - max_width):
                        temp = x
                        return temp
        else:
            temp = copy.deepcopy(StacksMaker.stack_zero)
            return temp
        return None

    def get_fitness_by_one(self, chrom):
        chrom_final_score = None
        chrom_sum_weight = 0
        chrom_weight_balancing = self.get_weight_balancing(chrom)
        chrom_width_score = 0
        chrom_length_score = 0
        chrom_area = 0
        chrom_area_score = 0
        chrom_weight_score = 0
        chrom_weight_balancing_score = 0
        for gene in chrom:
            chrom_area += gene.area
        chrom_weight_score = (self.CONTAINER_WEIGHT -
                                sum(chrom_weight_balancing))
        chrom_weight_balancing[:] = [(chrom_sum_weight / 3) -
                                        weight_section for weight_section in chrom_weight_balancing]
        chrom_area_score = (
            (self.CONTAINER_LENGTH * self.CONTAINER_WIDTH) - chrom_area)
        chrom_length_score = (self.CONTAINER_LENGTH -
                                self.get_length(chrom)[0])
        chrom_width_score = (sum(self.get_over_usage_width(chrom)[1]))
        chrom_weight_balancing_score = sum(chrom_weight_balancing)
        chrom_final_score = ((chrom_area_score / 10) - chrom_length_score -
                                chrom_weight_score - chrom_width_score - (chrom_weight_balancing_score / 1000))
        return chrom_final_score

    def get_weight_balancing(self, chrom) -> list:
        cnt = 0
        weights = [0, 0, 0]
        sum_weight = 0
        for x in chrom:
            if cnt == 10 or cnt == 21 or cnt == 32:
                weights[int(str(cnt)[1])] += sum_weight
                sum_weight = 0
            for k, v in x.weight_each.items():
                sum_weight += sum(v)
            cnt += 1
        return weights

    def get_over_usage_width(self, chrom):
        cnt = 1
        over_cnt = 0
        widths = list()
        sum_width = 0
        for x in chrom:
            if cnt == 3:
                if sum_width > self.CONTAINER_WIDTH:
                    over_cnt += 1
                widths.append(self.CONTAINER_WIDTH - sum_width)
                sum_width = 0
                cnt = 0
            sum_width += x.width
        return over_cnt, widths

    def get_length(self, chrom):
        over_usage = False
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
        length_list = [sum(x1), sum(x2), sum(x3)]
        if max(length_list) > self.CONTAINER_LENGTH:
            over_usage = True
            over_usage_value = max(length_list)
        return max(length_list), over_usage
    def run(self):
        self._population = self.generate_initial_population()
        for x in range(1000):
            self._fitness_value = self.get_fitness_values()
            print(self._fitness_value)
            if max(self._fitness_value) > 0:
                break
            else :
                print(f'Training @ Generation : {x}')
            selection = self.selection()
            offspring_crossover = self.crossover(copy.deepcopy(selection))
            offspring_mutation = self.mutation(copy.deepcopy(offspring_crossover))
            self._population = selection + offspring_crossover + offspring_mutation

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
    ga = GeneticAlgorithm("20Standard", remaining_parcels, stacks)
    ga.run()

