class Strategy:
    def __init__(self):
        pass

    def read_distance_matrix(self, file_name):

        distance_matrix = []
        origin, destination = None, None
        with open('tests/' + file_name + '.txt', 'r') as file:
            lines = file.readlines()
            n = int(lines[0])
            for i in range(n):
                row = list(map(lambda x: int(x), lines[i + 1].split(',')))
                distance_matrix.append(row)

            if len(lines) > n + 1:
                origin, destination = int(lines[n + 1]) - 1, int(lines[n + 2]) - 1

        return distance_matrix, origin, destination

    def get_shortest_path(self, min_route, distance_matrix, origin, destination):
        first = second = None
        for i, el in enumerate(min_route):
            if el == origin or el == destination:
                if first is None:
                    idx_first, first = i, el
                else:
                    idx_second, second = i, el
                    break

        if first is None or second is None:
            raise Exception('First or second is None')

        first_path = min_route[idx_first:idx_second + 1]
        second_path = min_route[idx_second:] + min_route[1:idx_first + 1]
        first_path_distance = self.get_real_distance(first_path, distance_matrix)
        second_path_distance = self.get_real_distance(second_path, distance_matrix)
        if first_path_distance < second_path_distance:
            return first_path_distance, first_path
        return second_path_distance, second_path

    def solve(self, file_name, origin=None, destination=None):
        raise NotImplementedError('Solve method needs to be implemented')

    def check_route(self, min_distance, min_route, distance_matrix):
        real_distance = self.get_real_distance(min_route, distance_matrix)
        if min_distance != real_distance:
            print(min_distance, real_distance)
            raise Exception('min_distance != real_distance')

    def get_real_distance(self, min_route, distance_matrix):
        real_distance = 0
        for i in range(len(min_route) - 1):
            real_distance += distance_matrix[min_route[i]][min_route[i + 1]]
        real_distance += distance_matrix[min_route[-1]][min_route[0]]
        return real_distance
