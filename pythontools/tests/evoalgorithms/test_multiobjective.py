from pythontools.evoalgorithms.multiobjective import NSGAII

class TestMultiObjective:
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

    def test_run_nsga_ii(self):
        odds = [17.00, 11.00, 7.00, 41.00, 8.50, 6.50, 19.00, 19.00, 8.00, 101.00, 71.00, 9.50, 61.00, 11.00, 56.00, 26.00]
        max_budget = 10000
        objective_functions = [(self.max_loss, [odds]), (self.loss_probability, [odds]), (self.max_budget_delta, [max_budget])]
        gene_domain = [100, 650]
        population_size = 20
        mutation_rate = 0.01
        total_genes = 16
        max_iterations = 1000

        nsgaii_algorithm = NSGAII(objective_functions, gene_domain, population_size, mutation_rate, total_genes, max_iterations)
        nsgaii_algorithm.run()