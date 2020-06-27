import random
import sys

class Individual:
    """
    Abstract class to define an individual.
    """
    def eval_objective_functions(self):
        """
        Abstract method that must be implemented
        by child classes to calculate the individual's 
        objective values.
        """
        pass

    def get_objectives(self):
        """
        Abstract method that must be implemented to return
        the Individual's objective values list
        """
        pass

class NSGAIIIndividual(Individual):
    """
    Definition of a NSGA-II individual
    """
    def __init__(self, dna):
        """
        Initialization of a NSGA-II individual.
        """
        self.dna = dna
        self.objective_values = []
        self.rank = 0
        self.crowding_distance = 0
        self.domination_count = 0
        self.dominated_individuals = []

class NSGAII:
    """
    Nondominated Sorting Genetic Algorithm implementation
    for multi-objective optimization.
    """
    def __init__(self, obj_func, gene_domain, population_size, mutation_rate, gene_count, max_iterations):
        """
        Set the configuration for the algorithm
        """
        self.objective_functions = obj_func
        self.gene_domain = gene_domain
        self.gene_count = gene_count
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_iterations = max_iterations

    def run(self):
        """
        Performs the optimization process.
        """
        r = []
        p = self.initialize_population(self.gene_domain[0], self.gene_domain[1], self.population_size, self.gene_count)
        q = self.initialize_population(self.gene_domain[0], self.gene_domain[1], self.population_size, self.gene_count)
        current_iteration = 0
        while current_iteration < self.max_iterations:
            r = [*p, *q]
            r = self.evaluate_objectives(r)
            r = self.non_dominated_sorting(r)
            r = self.sort_crowding_distance(r)
            p = r[:self.population_size]
            q = self.generate_offspring(p, self.mutation_rate, self.gene_count, self.gene_domain)
            current_iteration += 1
        r = [*p, *q]
        self.evaluate_objectives(r)
        return r

    def initialize_population(self, min_val, max_val, population_size, total_genes):
        """
        Creates a population of individuals with
        random values.
        """
        individuals = []
        # TODO: refactor these to use list comprehension
        for i in range(population_size):
            individuals.append(NSGAIIIndividual([random.uniform(min_val, max_val) for i in range(total_genes)]))
        return individuals

    def evaluate_objectives(self, solutions):
        """
        Evaluates the objective values for each
        solution in the set.
        """
        for solution in solutions:
            objective_values = []
            for objective_function in self.objective_functions:
                objective_values.append(objective_function[0](solution.dna, *objective_function[1]))
            solution.objective_values = objective_values
        return solutions

    def generate_offspring(self, parents, mutation_rate, gene_count, domain):
        """
        Creates a new population of solutions from a parent population.
        """
        # TODO: refactor these to use list comprehension
        childs = []
        # loop until new population size is equal to parent population size
        for i in range(self.population_size):
            p1 = self.tournament_selection(parents)
            p2 = self.tournament_selection(parents)
            # crossover
            child = self.crossover(p1, p2)
            # mutation
            child = self.mutate(child, mutation_rate, gene_count, domain)
            childs.append(child)
        return childs

    def tournament_selection(self, solutions):
        """
        Randomly picks two solutions and returns
        the best by evaluating rank and crowding
        distance.
        """
        c1 = random.choice(solutions)
        c2 = random.choice(solutions)
        if c1.rank == c2.rank:
            return c1 if c1.crowding_distance > c2.crowding_distance else c2
        else:
            return c1 if c1.rank < c2.rank else c2

    def crossover(self, p1, p2):
        """
        Creates a new solution by mixing half of
        the genes from parent p1 and half of the genes
        from parent p2.
        """
        middle_point = int(len(p1.dna)/2)
        dna = [*p1.dna[:middle_point], *p2.dna[middle_point:]]
        individual = NSGAIIIndividual(dna)
        return individual

    def mutate(self, solution, mutation_rate, gene_count, domain):
        """
        Update the value of a random gene for a given solution.
        """
        rounds = int(mutation_rate*100)
        # TODO: refactor these to use list comprehensions
        for i in range(rounds):
            gene_index = random.choice(range(gene_count))
            solution.dna[gene_index] = random.uniform(domain[0], domain[1])
        return solution

    def sort_crowding_distance(self, solutions):
        """
        Sorts a set of solutions in descending order
        according to the crowding distance of each solution.
        """
        self.reset_crowding_distance(solutions)
        result = []
        # get front count
        last_front = solutions[-1].rank
        objective_count = len(solutions[0].objective_values)
        # loop from 1 to last front value inclusive
        for current_front in range(1, last_front+1):
            # get front according to the current iteration
            current_front_members = [s for s in solutions if s.rank == current_front]
            # loop from 0 to the last objective value exclusive
            for current_objective in range(objective_count):
                current_front_members = sorted(current_front_members, reverse=True, key=lambda s: s.objective_values[current_objective])
                # get min and max value for the current objective values
                s_max_objective = max(current_front_members, key=lambda s: s.objective_values[current_objective])
                s_max_objective.crowding_distance = sys.float_info.max
                s_min_objective = min(current_front_members, key=lambda s: s.objective_values[current_objective])
                s_min_objective.crowding_distance = sys.float_info.max
                # loop through each solution in the front
                for i in range(1, len(current_front_members)-1):
                    # calculate crowding distance
                    current_front_members[i].crowding_distance = current_front_members[i].crowding_distance + self.calculate_crowding_distance(
                        current_front_members[i+1].objective_values[current_objective], 
                        current_front_members[i-1].objective_values[current_objective], 
                        s_min_objective.objective_values[current_objective], 
                        s_max_objective.objective_values[current_objective])
            
            result.extend(sorted(current_front_members, reverse=True, key=lambda s: s.crowding_distance))
        return result

    def reset_crowding_distance(self, solutions):
        """
        Update the crowding distance value for each
        solution in the given set.
        """
        for i in range(len(solutions)):
            solutions[i].crowding_distance = 0

    def calculate_crowding_distance(self, next_objective, prev_objective, min_objective, max_objective):
        return (next_objective - prev_objective) / (max_objective - min_objective) if min_objective != max_objective else 0

    def non_dominated_sorting(self, solutions):
        """
        Evaluate domination criteria for each solution
        and then groups the solutions by fronts.
        """
        # reset domination stats
        self.reset_domination_stats(solutions)
        # evaluate domination criteria for all solutions
        self.evaluate_domination(solutions)
        # group the solutions by fronts
        return self.create_ranked_fronts(solutions)

    def reset_domination_stats(self, solutions):
        """
        Set all domination stats to zero.
        """
        for i in range(len(solutions)):
            solutions[i].rank = 0
            solutions[i].domination_count = 0
            solutions[i].dominated_individuals = []
    
    def evaluate_domination(self, solutions):
        """
        Calculates the domination count, which is a
        number indicating how many solutions dominates
        the current solution, and store the dominated solutions
        in a list.
        """
        i = 0
        while i < len(solutions):
            j = 0
            while j < len(solutions):
                if i != j:
                    if self.is_dominant(solutions[i], solutions[j]):
                        solutions[i].dominated_individuals.append(j)
                        solutions[j].domination_count += 1
                j += 1
            i += 1

    def create_ranked_fronts(self, solutions):
        """
        Process all solutions to group them in fronts based
        in the domination criteria. All solutions having a
        domination count of zero are considered to be part of
        the same front.
        """
        current_rank = 1
        ranked_solutions = []
        while True:
            if len(ranked_solutions) == len(solutions):
                break
            for s in solutions:
                if s.rank == 0 and s.domination_count == 0:
                    for dominated_s_i in s.dominated_individuals:
                        solutions[dominated_s_i].domination_count -= 1
                    s.rank = current_rank
                    ranked_solutions.append(s)
            current_rank += 1
        return ranked_solutions

    def is_dominant(self, s1, s2):
        """
        Returns True if solution s1 dominates solution s2, otherwise 
        it returns False. The criteria for checking dominance is:
        1.- The objective values of s1 are no worse than those of 
            s2 in all objectives.
        2.- The objective values of solution s1 are strictly better 
            than at least one of those of solution s2
        """
        better_objective_values = False
        for s1_obj, s2_obj in zip(s1.objective_values, s2.objective_values):
            if s1_obj <= s2_obj:
                if s1_obj < s2_obj:
                    better_objective_values = True
            else:
                return False
        return better_objective_values
