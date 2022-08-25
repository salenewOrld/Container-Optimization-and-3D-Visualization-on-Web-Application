import random
import copy
from tabnanny import check
import parcels
from StackMaker import *
from DataManager import *
class GeneticAlgorithm:
    def __init__(self, stacks, container_id, remaining_stacks):
        self.stacks = stacks
        self.container_id = container_id
        #self.container_info = parcels.Info.get_container_info(self.container_id)
        self.remaining_stacks = remaining_stacks
    def initial_population_generator(self):
        # creating pop
        population = list()
        for _ in range(100):
            chromosome = list()
            for _ in range(33):
                chromosome.append(random.choice(self.stacks))
            population.append(chromosome)
        #balancing pop
        for index, chrom in enumerate(population):
            for idx, stack in enumerate(chrom):
                if idx == 0:
                    pass
                else :
                    if idx < 19 and (stack.volume < chrom[idx-1].volume):
                        population[index][idx-1], population[index][idx] = population[index][idx], population[index][idx-1]
                    elif stack.volume > chrom[idx-1].volume :
                        population[index][idx-1], population[index][idx] = population[index][idx], population[index][idx-1]
        return population
    def fitness_calculation(self, population, container_id):
        #clear_output(wait=True)
        container_info = parcels.Info.get_container_info(container_id)
        chromosome_scores = list()
        balancing_scores = list()
        sum_area = 0
        for chrom in population:
            weight_balancing = list()
            sum_weight_section = 0
            longest_length = 0
            widest_width = 0
            length = []
            final_score = 0
            width_score = 0
            cnt = 1
            for idx, stack in enumerate(chrom):
                if stack != None:
                    sum_area += stack.area
                if idx == 10 or idx == 21 or idx == 32:
                    weight_balancing.append(sum_weight_section)
                    sum_weight_section = 0
                for key, value in stack.weight_each.items():
                    sum_weight_section += sum(value)
                if cnt == 3:
                    length.append(longest_length)
                    longest_length = 0
                    if widest_width == 0:
                        pass
                    else :
                        width_score += 1 - (abs(container_info[0] - widest_width) / container_info[0])
                    widest_width = 0
                    cnt = 0
                if stack.length > longest_length:
                    longest_length = stack.length
                
                if widest_width < stack.width:
                    widest_width = stack.width
                
                cnt += 1
            sum_area = 1 - ((abs(((container_info[0] * container_info[1]) - sum_area))) / (container_info[0] * container_info[1]))
            weight_balancing_score = 1 - (abs(((weight_balancing[0] - weight_balancing[1]) + (weight_balancing[1] - weight_balancing[2]))) / 1000)
            length_score = 1 - (abs((container_info[1] - sum(length)) / container_info[1]))
            weight_score = 1 - (abs((parcels.Info.get_container_weight(container_id) - sum(weight_balancing)) / parcels.Info.get_container_weight(container_id) ))
            final_score = sum_area + weight_balancing_score + length_score + weight_score + width_score
            # final_score = sum_area + weight_balancing_score + length_score
            chromosome_scores.append(final_score)
        #normalizing score
        # norm_area = np.linalg.norm(area_scores)
        # norm_length = np.linalg.norm(length_scores)
        # norm_balancing = np.linalg.norm(balancing_scores)
        # # normalized_area = list(area_scores / norm_area)
        # normalized_length = (length_scores - min(length_scores)) / (max(length_scores) - min(length_scores))
        # normalized_balancing = (balancing_scores - min(balancing_scores)) / (max(balancing_scores) - min(balancing_scores))
        # for j in range(len(normalized_balancing)):
        #     chromosome_scores.append(area_scores[j] + normalized_length[j] + normalized_balancing[j])
        # norm = np.linalg.norm(chromosome_scores)
        # normalized_scores = chromosome_scores / norm
        # for j in range(len(chromosome_scores)):
        #     chromosome_scores[j] = (chromosome_scores[j] - min(chromosome_scores)) / (max(chromosome_scores) - min(chromosome_scores))
        return chromosome_scores
    def selection(self, population, fitness_scores):
        selected_chromosomes = list()
        cnt = 1
        for _ in fitness_scores:
            if cnt == 30:
                break
            max_score_idx = fitness_scores.index(max(fitness_scores))
            selected_chromosomes.append(copy.deepcopy(population[max_score_idx]))
            fitness_scores[max_score_idx] = -99
            min_score_idx = fitness_scores.index(min(fitness_scores))
            selected_chromosomes.append(copy.deepcopy(population[min_score_idx]))
            fitness_scores[min_score_idx] = 999
            cnt += 1
        return selected_chromosomes
    def crossover(self, offspring_selection):
        offspring_crossover = list()
        uniform_perf_positions = list()
        for _ in range(int(33/5)):
            uniform_perf_positions.append(random.randint(0, 32))
        for x in range(len(offspring_selection)):
            child_one = offspring_selection[x]
            child_two = offspring_selection[x]
            parent_one = x
            parent_two = (len(offspring_selection) - 1) - x
            for j in range(33):
                if j in uniform_perf_positions:
                    child_one[j] = copy.deepcopy(offspring_selection[parent_one][j])
                    child_two[j] = copy.deepcopy(offspring_selection[parent_two][j])
                else :
                    child_one[j] = copy.deepcopy(offspring_selection[parent_two][j])
                    child_two[j] = copy.deepcopy(offspring_selection[parent_one][j])
            offspring_crossover.append(child_one)
            offspring_crossover.append(child_two)
        # for x in range(len(offspring_selection)):
        #     parent_1 = x % 2
        #     parent_2 = x % 3
        #     child = offspring_selection[parent_1][0:17] + offspring_selection[parent_2][17:]
        #     child_2 = offspring_selection[parent_2][0:17] + offspring_selection[parent_1][17:]
        #     offspring_crossover.append(child)
        #     offspring_crossover.append(child_2)
        return offspring_crossover
    def find_sum_length(self, chrom):
        x1, x2, x3 =[chrom[0].length,
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
        all_length = [sum(x1), sum(x2), sum(x3)]
        return max(all_length)
    def find_max_width(self, pos_1, pos_2, pos_3):
        list = [pos_1.width, pos_2.width, pos_3.width]
        return list.index(max(list))
    def find_optimal_stack(self, pos_1, pos_2, pos_3, chrom, container_info, stacks, main_pos):
        # check whether what stack does have potential to be placed in the stack
        # check whether in the section, the width is over or not
        # check whether in the chrom, the length is over or not
        # check whether in the chrom, the area is over or not
        pos_list = [pos_1, pos_2, pos_3]
        sum_area = self.find_sum_area(chrom)
        if sum_area > (container_info[0] * container_info[1]):
            return copy.deepcopy(StacksMaker.stack_zero)
        elif self.find_sum_length(chrom) > container_info[1]:
            return copy.deepcopy(StacksMaker.stack_zero)
        if (pos_1.width + pos_2.width + pos_3.width) > container_info[0]:
            after_del_widest = container_info[0] - main_pos.width
            if after_del_widest < 0.76:
                return copy.deepcopy(StacksMaker.stack_zero)
            else :
                for j in stacks:
                    if j.width <= after_del_widest:
                        return copy.deepcopy(j)


    def mutation(self, offspring_crossover, stacks, width_mutate, container_info):
        ''' Figure out how tf could I be able to put sorta shitty genes whichs stuck in the overwidth usage row
        Method 1: Find the empty row (more than 2 genes in the row are 0) => find a row thats overwidth => pull out the problemed stack
        => put it into the row (the row must be empty or have enough space to store the pulled out stack.'''
        offspring_mutation = list()
        for _ in range(10) :
            pos_1 = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
            pos_2 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
            pos_3 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]
            all_pos = pos_1 + pos_2 + pos_3
            #print(stacks)
            mutating_chrom = random.choice(offspring_crossover)
            if self.check_width(mutating_chrom, container_info) == False:
                mutating_chrom[18], mutating_chrom[19], mutating_chrom[20] = copy.deepcopy(StacksMaker.stack_zero), copy.deepcopy(StacksMaker.stack_zero), copy.deepcopy(StacksMaker.stack_zero)
            for _ in range(3):
                rand_pos = random.choice(pos_1 + pos_2 + pos_3)
                if rand_pos in pos_1:
                    optimal_stack = self.find_optimal_stack(mutating_chrom[rand_pos], mutating_chrom[rand_pos+1], mutating_chrom[rand_pos+2], mutating_chrom, container_info, stacks, mutating_chrom[rand_pos])
                    index = pos_1.index(rand_pos)
                    pos_1.pop(index)
                elif rand_pos in pos_2:
                    optimal_stack = self.find_optimal_stack(mutating_chrom[rand_pos-1], mutating_chrom[rand_pos], mutating_chrom[rand_pos+1], mutating_chrom, container_info, stacks, mutating_chrom[rand_pos])
                    index = pos_2.index(rand_pos)
                    pos_2.pop(index)
                else :
                    optimal_stack = self.find_optimal_stack(mutating_chrom[rand_pos-2], mutating_chrom[rand_pos-1], mutating_chrom[rand_pos], mutating_chrom, container_info, stacks, mutating_chrom[rand_pos])
                    index = pos_3.index(rand_pos)
                    pos_3.pop(index)
                temp = optimal_stack
                mutating_chrom[rand_pos] = temp
            rand_pos_one = random.randint(0, 12)
            rand_pos_two = random.randint(13, 25)
            rand_pos_three = random.randint(26, 32)
            temp_1, temp_2, temp_3 = mutating_chrom[rand_pos_one], mutating_chrom[rand_pos_two], mutating_chrom[rand_pos_three]
            mutating_chrom[rand_pos_one], mutating_chrom[rand_pos_three]  = temp_3, temp_1
            offspring_mutation.append(mutating_chrom)
            # if not self.check_length(mutating_chrom, container_info):
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(StacksMaker.stack_zero)
            # else :
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(random.choice(stacks))
            # if not self.check_width(mutating_chrom, container_info):
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(StacksMaker.stack_zero)
            # else :
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(random.choice(stacks))
            # if self.find_sum_area(mutating_chrom) > (container_info[0] * container_info[1]):
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(StacksMaker.stack_zero)
            # else :
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(random.choice(stacks))
            # if not self.check_length(mutating_chrom, container_info):
            #     mutating_chrom[random.choice(pos_1)] = copy.deepcopy(StacksMaker.stack_zero)
            #     mutating_chrom[random.choice(pos_1) + 1] = copy.deepcopy(StacksMaker.stack_zero)
            #     mutating_chrom[random.choice(pos_1) + 2] = copy.deepcopy(StacksMaker.stack_zero)
            # else :
            #     length_mutate_pos = random.randint(0, len(mutating_chrom) - 1) 
            #     mutating_chrom[length_mutate_pos] = copy.deepcopy(random.choice(stacks))
            # if not self.check_width(mutating_chrom, container_info):
            #     mutating_chrom[random.randint(0, 32)] = copy.deepcopy(StacksMaker.stack_zero)
            # else :
            #     under_value = list()
            #     width_mutate_pos = random.randint(0, len(mutating_chrom) - 1)
            #     mutating_chrom[width_mutate_pos] = copy.deepcopy(random.choice(stacks))
            # # if width_mutate_pos != length_mutate_pos:
            # #     if width_mutate_pos in pos_1:
            # #         sum_width = mutating_chrom[width_mutate].width + mutating_chrom[width_mutate + 1].width + mutating_chrom[width_mutate + 2].width
            # #         largest_stack_width = mutating_chrom[width_mutate]
            # #         index = width_mutate
            # #         for idx, x in enumerate([mutating_chrom[width_mutate], mutating_chrom[width_mutate + 1], mutating_chrom[width_mutate + 2]]):
            # #             if x.width > largest_stack_width.width:
            # #                 temp = x
            # #                 largest_stack_width = temp
            # #                 index = idx + width_mutate
            # #         if (sum_width - largest_stack_width.width) < 0.76:
            # #             mutating_chrom[index] = copy.deepcopy(StacksMaker.stack_zero)
            # #         else:
            # #             for x in stacks:
            # #                 if x.width <= (sum_width - largest_stack_width.width):
            # #                     mutating_chrom[index] = copy.deepcopy(x)
            #offspring_mutation.append(mutating_chrom)

            # cnt = 1
            # width = 0
            # largest_index = 0
            # largest_stack = StacksMaker.stack_zero
            # longest_stack = mutating_chrom[0]
            # longest_stack_est = StacksMaker.stack_zero
            # longest_stack_est_index = 0
            # longest_index = 0
            # length = 0
            # longest_stack_length = mutating_chrom[0].length
            # random_randint = random.randint(0, 1)
            # for idx, j in enumerate(mutating_chrom):
            #     #print(longest_stack.length)
            #         if cnt == 3:
                        
            #             length += longest_stack_length
            #             if width > container_info[0]:
            #                 new_width = width - largest_stack.width
            #                 if new_width < 0.76:
            #                     mutating_chrom[largest_index] = StacksMaker.stack_zero
            #                 else :
            #                     for x in stacks:
            #                         if x.width <= new_width:
            #                             mutating_chrom[largest_index] = x
            #             largest_stack = StacksMaker.stack_zero
            #             width = 0
            #             cnt = 1
            #             longest_stack = StacksMaker.stack_zero
            #         #print(length, self.container_info[1])
            #         if largest_stack.width < j.width:
            #             largest_stack = j
            #             largest_index = idx
            #         if j.length > longest_stack_length:
            #             longest_stack = j
            #             longest_index = idx
            #         if longest_stack_est.length < j.length:
            #             longest_stack_est = j
            #             longest_stack_est_index = idx
            # longest_length = mutating_chrom[0].length
            # longest_stack_index = 0
            # longest_stack_length = mutating_chrom[0].length
            # sum_length = 0
            # cnt_l = 1
            # for idx, value in enumerate(mutating_chrom):
            #         if cnt_l == 3:
            #             #print(f"row {idx} = {longest_length}")
            #             sum_length += longest_length
            #             longest_length = 0
            #             cnt_l = 1
            #         if value.length >= longest_length:
            #             longest_length = value.length
            #         if value.length > longest_stack_length:
            #             longest_stack_index = idx
            #         cnt_l += 1
            #     #print(sum_length, self.container_info[1])
            # if sum_length > container_info[1]:
            #         # mutating_chrom[longest_stack_index] = copy.deepcopy(StacksMaker.stack_zero)
            #         # mutating_chrom[longest_stack_index + 1] = copy.deepcopy(StacksMaker.stack_zero)
            #         if longest_stack_index in pos_1:
            #             mutating_chrom[longest_stack_index] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index + 1] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index + 2] = copy.deepcopy(StacksMaker.stack_zero)
            #         elif longest_stack_index in pos_2:
            #             mutating_chrom[longest_stack_index - 1] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index + 1] = copy.deepcopy(StacksMaker.stack_zero)
            #         elif longest_stack_index in pos_3:
            #             mutating_chrom[longest_stack_index - 2] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index - 1] = copy.deepcopy(StacksMaker.stack_zero)
            #             mutating_chrom[longest_stack_index] = copy.deepcopy(StacksMaker.stack_zero)
                #print(sum_length, self.container_info[1])
                        

            # sections_chrom = [[mutating_chrom[0:2]], [mutating_chrom[3:5]], [mutating_chrom[6:8]], 
            # [mutating_chrom[9:11]], [mutating_chrom[12:14]], [mutating_chrom[15:17]], [mutating_chrom[18:20]],
            # [mutating_chrom[21:23]], [mutating_chrom[24:26]], [mutating_chrom[27:29]], [mutating_chrom[30:32]]]
            # zeros = 0
            # indexes = []
            # for j in sections_chrom:
            #     for idx, x in enumerate(j):
            #         if zeros == 2:
            #             indexes.append(idx)
            #         if idx % 3 == 0:
            #             zeros = 0
            #         if x == StacksMaker.stack_zero:
            #             zeros += 1
            # for _ in range(3):
            #     rand_int = random.randint(0, 32)
            #     # if not self.check_width(mutating_chrom):
            #     #     mutating_chrom[rand_int] = StacksMaker.stack_zero
            #     # elif not self.check_length(mutating_chrom):
            #     #     mutating_chrom[rand_int] = StacksMaker.stack_zero
            #     # else :
            #     mutating_chrom[rand_int] = random.choice(stacks)
            #     rand_pos_one = random.randint(0, 32)
            #     rand_pos_two = random.randint(0, 32)
            #     random_pos_three = random.randint(0, 32)
            #     random_pos_four = random.randint(0, 32)
            #     random_pos_five = random.randint(0, 32)
            #     random_pos_six = random.randint(0, 32)
            #     mutating_chrom[rand_pos_one], mutating_chrom[random_pos_six] = mutating_chrom[random_pos_six], mutating_chrom[rand_pos_one]
            #     mutating_chrom[rand_pos_two], mutating_chrom[random_pos_five] = mutating_chrom[random_pos_five], mutating_chrom[rand_pos_two]
            #     mutating_chrom[random_pos_three], mutating_chrom[random_pos_four] = mutating_chrom[random_pos_four], mutating_chrom[random_pos_three]
            #     # if (rand_pos_one + 1) % 3 == 0 or (rand_pos_one + 2) % 3 == 0 or (rand_pos_one) % 3 == 0:
            #     #     if mutating_chrom[rand_pos_one] != StacksMaker.stack_zero:
            #     #         try :
            #     #             if mutating_chrom[rand_pos_one - 1] != StacksMaker.stack_zero and mutating_chrom[rand_pos_one + 1] != StacksMaker.stack_zero and mutating_chrom[rand_pos_one] != StacksMaker.stack_zero:
            #     #                 rand_pos_none = random.randint(rand_pos_one - 1, rand_pos_one + 1)
            #     #             elif mutating_chrom[rand_pos_one] != StacksMaker.stack_zero and mutating_chrom[rand_pos_one + 1] != StacksMaker.stack_zero and mutating_chrom[rand_pos_one + 2] != StacksMaker.stack_zero:
            #     #                 rand_pos_none = random.randint(rand_pos_one, rand_pos_one + 2)
            #     #             else :
            #     #                 rand_pos_none = random.randint(rand_pos_one - 2, rand_pos_one)
            #     #         except:
            #     #             pass
            #     # if len(indexes) == 0:
            #     #     rand_choice_zero = rand_pos_two
            #     # else :
            #     #     rand_choice_zero = random.choice(indexes)
            #     # mutating_chrom[rand_pos_none], mutating_chrom[rand_choice_zero] = mutating_chrom[rand_choice_zero], mutating_chrom[rand_pos_none]
            # offspring_mutation.append(mutating_chrom)
        # for _ in range(10):
        #     mutating_chrom = random.choice(offspring_crossover)
        #     rows = []
        #     row_sub = []
        #     for idx, value in enumerate(mutating_chrom):
        #         if idx % 3 == 0:
        #             rows.append(row_sub)
        #             row_sub.clear()
        #         row_sub.append(value)
        #     row_cnt = 0
        #     sum_row = 0
        #     zeros = 0
        #     overwidth_rows = []
        #     underwidth_rows = []
        #     overwidth_width = []
        #     underwidth_width = []
        #     for row in rows:
        #         for idx, element in enumerate(row):
        #             if element.name == 0:
        #                 zeros += 1
        #             sum_row += element.width
        #             if idx % 3 == 0:
        #                 if sum_row > self.container_info[0]:
        #                     overwidth_rows.append(row_cnt)
        #                     overwidth_width.append(sum_row)
        #                 if zeros >= 2:
        #                     underwidth_rows.append(row_cnt)
        #                     underwidth_width.append(sum_row)
        #                 zeros = 0
        #                 row_cnt += 1
        #                 sum_row = 0
        #     if len(overwidth_rows) == 0:
        #         break
        #     else :
        #         if len(underwidth_rows) == 0:
        #             for j in range(len(overwidth_rows)):
        #                 min_stack = rows[overwidth_rows[j]][0]
        #                 min_area = 0
        #                 for x in rows[overwidth_rows[j]]:
        #                     if x.area > min_area:
        #                         min_area = x.area
        #                         min_stack = x
        #                 index = rows[overwidth_rows[j]].index(min_stack)
        #                 rows[overwidth_rows[j]][index] = copy.deepcopy(StacksMaker.stack_zero)
        #         else :
        #             for j in range(len(underwidth_rows)):
        #                 under_width = random.randint(0, 2)
        #                 over_width_rand = random.choice(overwidth_rows)
        #                 over_width_rand_pos = random.randint(0, 2)

        #                 rows[underwidth_rows[j]][under_width], rows[over_width_rand][over_width_rand_pos] = rows[over_width_rand][over_width_rand_pos], rows[underwidth_rows[j]][under_width]

        #     new_mutate_chromosome = rows[0] + rows[1] + rows[2] + rows[3] + rows[4] + rows[5] + rows[6] + rows[7] + rows[8] + rows[9] + rows[10]
        #     offspring_mutation.append(new_mutate_chromosome)
        # stacks_width = list()
        # for x in stacks:
        #     stacks_width.append(x.width)
        # for _ in range(10):
        #     mutate_chrom = random.choice(offspring_crossover)
        #     for _ in range(3):
        #         rand_pos = random.randint(0, 32)
        #         if mutate_chrom[rand_pos].width > 1.185:
        #             for x in stacks_width:
        #                 if x < 1.185:
        #                     index = stacks_width.index(x)
        #                     mutate_chrom[rand_pos] = stacks[index]
        #     #     else :
        #     #         for x in stacks_width:
        #     #             if x > 1.185:
        #     #                 index = stacks_width.index(x)
        #     #                 mutate_chrom[rand_pos] = stacks[index]
        #     offspring_mutation.append(mutate_chrom)

        # for _ in range(10):
        #     overwidth_arr = list()
        #     width_val = 0
        #     rand_chrom = random.choice(offspring_crossover)
        #     row = 1
        #     for idx, value in enumerate(rand_chrom):
        #         width_val += value.width
        #         if idx % 3 == 0:
        #             if width_val > self.container_info[0]:
        #                 overwidth_arr.append(row)
        #             width_val = 0
        #             row += 1
        #     for x in range(len(overwidth_arr)):
        #         rand_chrom[overwidth_arr[x]] = StacksMaker.stack_zero
        #     offspring_mutation.append(rand_chrom)

        # mutate_value_one = None
        # mutate_value_two = None
        # mutate_value_three = None
        # for _ in range(10):
        #     mutate_chrom = random.choice(offspring_crossover)
        #     # if self.find_sum_area(mutate_chrom) > (self.container_info[0] * self.container_info[1]):
        #     #     mutate_chrom[random.randint(0, 32)] = StacksMaker.stack_zero
        #     #     mutate_chrom[random.randint(0, 32)] = StacksMaker.stack_zero
        #     #     mutate_chrom[random.randint(0, 32)] = StacksMaker.stack_zero
        #     # else :
        #     width_arr = list()
        #     for idx, value in enumerate(mutate_chrom):
        #         width_arr.append(value.width)
        #         if idx % 3 == 0:
        #             if sum(width_arr) > self.container_info[0]:
        #                 random_stack = random.choice(stacks)
        #                 if sum([random_stack.width, width_arr[1], width_arr[2]]) < self.container_info[0]:
        #                     mutate_chrom[idx-2] = random_stack
        #                 elif sum([width_arr[0], random_stack.width, width_arr[2]]) < self.container_info[0]:
        #                     mutate_chrom[idx-1] = random_stack
        #                 elif sum([width_arr[0], width_arr[1], random_stack.width]) < self.container_info[0]:
        #                     mutate_chrom[idx] = random_stack
        #                 else :
        #                     mutate_chrom[random.randint(idx-3, idx)] = StacksMaker.stack_zero
        #             width_arr.clear()
                            
                # if self.find_section_weight_area(0, mutate_chrom)[0] > (self.find_sum_area(mutate_chrom) / 3):
                #     diff = self.find_section_weight_area(0, mutate_chrom)[0] - self.find_sum_area(mutate_chrom) / 3
                #     if diff > 3.3633:
                #         for j in mutate_chrom:
                #             if j.name == 106 or j.name == 207:
                #                 for x in self.stacks:
                #                     if x.name == 101 or x.name == 102 or x.name == 201 or x.name == 202:
                #                         mutate_chrom[mutate_value_one] = x
            #     mutate_value_one = random.choice(self.stacks)
            #     mutate_value_two = random.choice(self.stacks)
            #     mutate_value_three = random.choice(self.stacks)
            # mutate_pos_one = random.randint(0, 10)
            # mutate_pos_two = random.randint(11, 21)
            # mutate_pos_three = random.randint(22, 32)
            # mutate_chrom[mutate_pos_one] = mutate_value_one
            # mutate_chrom[mutate_pos_two] = mutate_value_two
            # mutate_chrom[mutate_pos_three] = mutate_value_three

            # offspring_mutation.append(mutate_chrom)
        return offspring_mutation
    def find_sum_area(self, chromosome):
        area = 0
        for j in chromosome:
            if j == None:
                pass
            else :
                area += j.area
        return area
    def find_section_weight_area(self, section, chrom):
        area = 0
        weight = 0
        if section == 0:
            min_range = 0
            max_range = 10
        elif section == 1:
            min_range = 11
            max_range = 21
        elif section == 2:
            min_range = 22
            max_range = 32
        for j in chrom[min_range, max_range]:
            area += j.area
            for k, v in j.weight_each.items():
                for l in v:
                    weight += l
        return area, weight
    def check_width(self, chrom, container_info):
        width = 0
        cnt = 1
        cnt_over = 0
        for idx, value in enumerate(chrom):
            if cnt == 3:
                if width > container_info[0]:
                    cnt_over += 1
                width = 0
                cnt == 1
            width += value.width
            cnt += 1
        if cnt_over > 0:
            return False
        elif cnt_over == 0:
            return True
    def check_length(self, chrom, container_info):
        longest_length = chrom[0].length
        sum_length = 0
        cnt = 1
        for idx, value in enumerate(chrom):
            if cnt == 3:
                #print(f"row {idx} = {longest_length}")
                sum_length += longest_length
                longest_length = 0
                cnt = 0
            if value.length >= longest_length:
                longest_length = value.length
            cnt += 1
        #print(sum_length, self.container_info[1])
        if sum_length <= container_info[1]:
            return True
        else :
            return False
    def find_remaining_stacks(self, stacks, chrom):
        for j in chrom:
            if j.name == 0:
                pass
            else :
                stacks[j.name] -= 1
        return stacks
    def execute(self):
        initial_population = self.initial_population_generator()
        population = initial_population
        width_mutate = False
        result = {
            "Data" : {
                "Container" : []
            }
        }
        con_index = 0
        container_cnt = 0
        while sum(list(self.remaining_stacks.values())) > 24:
            score_streak = 0
            container_info = parcels.Info.get_container_info(self.container_id[con_index])
            prev_score = 0
            for j in range(1000):
                #print(f'Runing generation {x+1} ...')
                chromosome_scores = self.fitness_calculation(population, self.container_id[con_index])

                print(prev_score, max(chromosome_scores))
                print(f"Container #{container_cnt}; Generation = {j+1} ;Highest chromosome score = {round(max(chromosome_scores), 2)}")
                print(f"Streak = {score_streak}")
                area = self.find_sum_area(population[chromosome_scores.index(max(chromosome_scores))])
                area_check = True
                if score_streak > 100:
                    if area > container_info[0] * container_info[1]:
                        area_check = False
                    print(f"Area check : {area_check}")
                    print(f"Width check : {self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info)}")
                    print(f'Length check : {self.check_length(population[chromosome_scores.index(max(chromosome_scores))], container_info)}')
                    break
                if round(prev_score, 2) == round(max(chromosome_scores), 2):
                    if area_check and self.check_length(population[chromosome_scores.index(max(chromosome_scores))], container_info) and self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info):
                        score_streak += 1
                sum_length = self.find_sum_length(population[chromosome_scores.index(max(chromosome_scores))])
                length_check = True
                if sum_length > container_info[1]:
                    length_check = False
                print(sum_length)
                print(f"Area check : {area_check}")
                print(f"Width check : {self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info)}")
                print(f'Length check : {length_check}')
                # if j > 1000:
                #     if ((self.find_sum_area(population[chromosome_scores.index(max(chromosome_scores))]) 
                #     > 
                #     ((container_info[0] * container_info[1]) * 0.7)) 
                #     and 
                #     self.find_sum_area(population[chromosome_scores.index(max(chromosome_scores))]) 
                #     <= 
                #     (container_info[0] * container_info[1])) :
                #         print("pass area")
                #         if self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info):
                #             print("pass width")
                #             if self.check_length(population[chromosome_scores.index(max(chromosome_scores))], container_info):
                #                 print("pass length")
                #                 break
                offspring_selection = self.selection(population, copy.deepcopy(chromosome_scores))
                offspring_crossover = self.crossover(offspring_selection)
                offspring_mutation = self.mutation(offspring_crossover, self.stacks, width_mutate, container_info=container_info)
                new_population = offspring_selection + offspring_crossover + offspring_mutation
                population = new_population
                prev_score = max(chromosome_scores)
                #x += 1
            remaining_stacks = self.find_remaining_stacks(self.remaining_stacks, population[chromosome_scores.index(max(chromosome_scores))])
            self.remaining_stacks = remaining_stacks
            #print(sum(list(self.remaining_stacks.values())))
            for k, v in remaining_stacks.items():
                if v < 0:
                    for x in self.stacks:
                        if x.name == k:
                            self.stacks.remove(x)
                            break
            print(self.stacks)
            data = DataManager.to_json(population[chromosome_scores.index(max(chromosome_scores))], self.container_id[con_index])
            result['Data']['Container'].append(data)
            if con_index >= len(self.container_id) - 1:
                con_index = 0
            if len(self.container_id) > 1:
                con_index += 1
            container_cnt += 1
        return result

if __name__ == '__main__':
    sm = StacksMaker()
# def execute(stacks, container_id, remaining_stacks):
#     ga = GeneticAlgorithm(stacks, container_id, remaining_stacks)
#     for j in range(1000):
#                 #print(f'Runing generation {x+1} ...')
#                 chromosome_scores = ga.fitness_calculation(population, ga.container_id[con_index])

#                 print(prev_score, max(chromosome_scores))
#                 print(f"Container #{container_cnt}; Generation = {j+1} ;Highest chromosome score = {round(max(chromosome_scores), 2)}")
#                 print(f"Streak = {score_streak}")
#                 area = self.find_sum_area(population[chromosome_scores.index(max(chromosome_scores))])
#                 area_check = True
#                 if score_streak > 100:
#                     if area > container_info[0] * container_info[1]:
#                         area_check = False
#                     print(f"Area check : {area_check}")
#                     print(f"Width check : {self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info)}")
#                     print(f'Length check : {self.check_length(population[chromosome_scores.index(max(chromosome_scores))], container_info)}')
#                     break
#                 if round(prev_score, 2) == round(max(chromosome_scores), 2):
#                     if area_check and self.check_length(population[chromosome_scores.index(max(chromosome_scores))], container_info) and self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info):
#                         score_streak += 1
#                 sum_length = self.find_sum_length(population[chromosome_scores.index(max(chromosome_scores))])
#                 length_check = True
#                 if sum_length > container_info[1]:
#                     length_check = False
#                 print(sum_length)
#                 print(f"Area check : {area_check}")
#                 print(f"Width check : {self.check_width(population[chromosome_scores.index(max(chromosome_scores))], container_info)}")
#                 print(f'Length check : {length_check}')