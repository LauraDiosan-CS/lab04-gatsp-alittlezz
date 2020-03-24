from service import Service


class ConsoleUI:
    def __init__(self):
        self.running = False
        self.input_commands = {
            '1': {'function': self.run_all_tests, 'description': 'Run all tests with the selected algorithm and '
                                                                 'compare them to DP and OrTools solutions'},
            '2': {'function': self.run_one_test, 'description': 'Run a certain test with the selected algorithm'},
            'x': {'function': self.terminate, 'description': 'Exit'}
        }
        self.service = Service()

    def run(self):
        self.running = True
        while self.running:
            self.print_menu()
            self.print_delimiter()
            self.handle_input()
            self.print_delimiter()

    def terminate(self):
        self.running = False

    def run_one_test(self, file_name=None, algorithm_used=None):
        if file_name is None:
            file_name = input('Name of the file containing the test: ')
        if algorithm_used is None:
            print('Choose an algorithm:')
            print('1) DP')
            print('2) Normal GA')
            algorithm_used = input('Algorithm: ')

        params = {}
        params['popSize'] = int(input("Population size = "))
        params['noGen'] = int(input("Number of generations = "))

        result = self.service.run_one_test(file_name, algorithm_used, params)
        print('Minimum distance for strategy is', result['strategy_solution'])
        print('Minimum route for strategy is', result['strategy_route'])
        print(result['compare_to_solution'])
        print(result['compare_to_dp_solution'])

    def run_all_tests(self):
        test_names = self.service.get_test_names()
        for test_name in test_names :
            self.run_one_test(test_name)
            self.print_delimiter()

    def print_menu(self):
        for key, value in self.input_commands.items():
            print(key + '. ' + value['description'])

    def print_delimiter(self):
        print('_' * 90)

    def handle_input(self):
        command = input('Command: ')
        try:
            self.input_commands[command]['function']()
        except KeyError:
            print('Command not available')
        except Exception as e:
            print(e)



