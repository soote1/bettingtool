import json
from multiprocessing import get_logger

from pythontools.actionmanager.actions import BaseAction
from pythontools.evoalgorithms.multiobjective import NSGAII

class DeserializeJsonAction(BaseAction):
    """
    An action to convert a json string
    to a python dictionary.
    """
    def __init__(self, config):
        """
        Initialize action.
        """
        super().__init__(config)
        self.logger = get_logger()

    def run(self, data):
        """
        Convert json string to python dictionary.
        """
        self.logger.info(f"converting json string to python dictionary")
        data_dict = json.loads(data)
        data_dict["next_action"] = self.config["next_action"]
        return data_dict

class DuplicateFilter(BaseAction):
    """
    An action to filter duplicate odds
    """
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        return data

class IncompleteScoresFilter(BaseAction):
    """
    An action to filter games with incomplete scores
    """
    TARGET_SCORES = "target_scores"
    def __init__(self, config):
        super().__init__(config)
        self.logger = get_logger()
        self.load_config()

    def load_config(self):
        self.logger.info(f"loading config for {self.__class__.__name__}")
        self.target_scores_set = set(self.config[self.TARGET_SCORES])

    def run(self, data):
        """
        """
        self.logger.info("running incomplete scores filter action")
        filtered_odds = [float(odd[2]) for odd in data["odds"] if odd[0].strip() in self.target_scores_set]
        data["filtered_odds"] = filtered_odds
        if len(filtered_odds) != len(self.target_scores_set):
            self.logger.info("incomplete scores found... interrupt the process")
            self.logger.info(f"filtered odds: {filtered_odds}")
            data["next_action"] = ""
        else:
            data["next_action"] = self.config["next_action"]
        return data

class SearchOptimalWagerSetAction(BaseAction):
    """
    An action to search the optimal bet strategy.
    """
    MAX_BUDGET = "max_budget"
    GENE_DOMAIN = "gene_domain"
    POPULATION_SIZE = "population_size"
    MUTATION_RATE = "mutation_rate"
    GENE_COUNT = "gene_count"
    MAX_ITERATIONS = "max_iterations"
    OPTIMAL_WAGERS = "optimal_wagers"
    def __init__(self, config):
        """
        Initialize search action.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.load_config()
    
    def load_config(self):
        self.max_budget = self.config[self.MAX_BUDGET]
        self.gene_domain = self.config[self.GENE_DOMAIN]
        self.population_size = self.config[self.POPULATION_SIZE]
        self.mutation_rate = self.config[self.MUTATION_RATE]
        self.gene_count = self.config[self.GENE_COUNT]
        self.max_iterations = self.config[self.MAX_ITERATIONS]

    def run(self, data):
        """
        Runs an instance of a NSGA-II algorithm to search
        the optimal set of wagers with the minimal risk.
        """
        self.logger.info(f"preparing data for nsga algorithm")
        odds = data["filtered_odds"]
        self.logger.info(f"running nsga algorithm against {odds}")
        objective_functions = [
            (self.max_loss, [odds]), 
            (self.loss_probability, [odds]), 
            (self.max_budget_delta, [self.max_budget])]

        nsgaii_algorithm = NSGAII(
            objective_functions, 
            self.gene_domain, 
            self.population_size, 
            self.mutation_rate, 
            self.gene_count, 
            self.max_iterations)

        optimal_wagers = nsgaii_algorithm.run()
        for optimal_wager in optimal_wagers:
            self.logger.info(f"odds: {odds}")
            self.logger.info(f"wagers: {optimal_wager.dna}")
            self.logger.info(f"objective values: {optimal_wager.objective_values}")
        data[self.OPTIMAL_WAGERS] = optimal_wagers
        data["next_action"] = self.config["next_action"]
        return data

    def max_loss(self, wagers, odds):
        """
        Gets the maximum loss in all the losing games.
        """
        required_budget = 0
        for wager in wagers:
            required_budget = required_budget + wager

        max_loss = 0
        for i in range(len(wagers)):
            profit = wagers[i]*odds[i]
            loss = required_budget - profit
            max_loss = loss if loss > max_loss else max_loss
        return max_loss/required_budget

    def loss_probability(self, wagers, odds):
        """
        Counts how many loss scenarios exist.
        """
        required_budget = 0
        for wager in wagers:
            required_budget = required_budget + wager

        losing_games = 0
        for i in range(len(wagers)):
            profit = wagers[i]*odds[i]
            loss = required_budget - profit
            losing_games = losing_games + 1 if loss > 0 else losing_games
        return losing_games/len(odds)

    def max_budget_delta(self, wagers, max_budget):
        """
        Calculates the diference between the maximum allowed budget
        and the money required to play the game.
        """
        required_budget = 0
        for wager in wagers:
            required_budget = required_budget + wager
        return required_budget/max_budget