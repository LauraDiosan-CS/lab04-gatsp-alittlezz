from strategies.dp_strategy import DPStrategy
from strategies.first_ga_strategy import NormalGA


class Service:
    def __init__(self):
        self.__dp_strategy = DPStrategy()
        self.__test_names = ['easy_01_4', 'easy_02_4', 'medium_00_8', 'medium_01_131', 'medium_02_237', 'medium_03_379', 'hard_01_662']

    def run_one_test(self, file_name, algorithm_used, params):
        strategy = self.get_strategy(algorithm_used)
        strategy_sol, strategy_route = strategy.solve(file_name, params)
        if strategy_sol is None:
            return {'strategy_solution': 'No solution',
                    'strategy_route': 'No route',
                    'compare_to_solution': 'Nothing to compare',
                    'compare_to_dp_solution': 'Nothing to compare'}

        self.writeSolutionToFile(file_name, strategy_sol, strategy_route)

        result = {'strategy_solution': strategy_sol,
                  'strategy_route': strategy_route}

        expected_sol = int(open('tests/' + file_name + '_solution.txt', 'r').readlines()[0])
        result['compare_to_solution'] = self.get_compare_state(strategy_sol, expected_sol, strategy.name, 'Expected solution')

        dp_sol, _ = self.__dp_strategy.solve(file_name)
        result['compare_to_dp_solution'] = self.get_compare_state(strategy_sol, dp_sol, strategy.name, self.__dp_strategy.name)

        return result

    def get_strategy(self, algorithm_used):
        if algorithm_used == '1':
            return DPStrategy()
        elif algorithm_used == '2':
            return NormalGA()
        raise Exception('There is no strategy')

    def writeSolutionToFile(self, file_name, min_distance, min_route):
        with open('tests/' + file_name + '_computed.txt', 'w') as file:
            file.write(str(len(min_route)) + '\n')
            file.write(','.join(map(lambda x: str(x + 1), min_route)) + '\n')
            file.write(str(min_distance) + '\n')


    def get_test_names(self):
        return self.__test_names

    def get_compare_state(self, strategy_sol, expected_sol, name_1, name_2):
        if expected_sol is None:
            return name_2 + ' strategy could not find an answer in time'
        elif strategy_sol > expected_sol:
            percentage = int((strategy_sol / expected_sol - 1) * 10000) / 100
            return name_1 + ' is ' + str(percentage) + '% worse than the ' + name_2 + '(' + str(expected_sol) + ')'
        else:
            percentage = int((expected_sol / strategy_sol - 1) * 10000) / 100
            return name_1 + ' is ' + str(percentage) + '% better than the ' + name_2 + '(' + str(expected_sol) + ')'
