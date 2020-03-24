from strategies.strategy import Strategy


class DPStrategy(Strategy):
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.name = 'DP'

    def solve(self, file_name, origin=None, destination=None):
        distance_matrix, origin, destination = self.read_distance_matrix(file_name)
        n = len(distance_matrix)
        if n > 20:
            return None, None
        dp = [[None for _ in range(n)] for _ in range(1 << n)]
        prev = [[None for _ in range(n)] for _ in range(1 << n)]
        dp[1][0] = 0
        for msk in range(1 << n):
            for i in range(n):
                if (msk & (1 << i)) != 0:
                    continue
                for j in range(n):
                    if dp[msk][j] is not None and i != j:
                        if dp[msk | (1 << i)][i] is None:
                            dp[msk | (1 << i)][i] = dp[msk][j] + distance_matrix[j][i]
                            prev[msk | (1 << i)][i] = j
                        elif dp[msk | (1 << i)][i] > dp[msk][j] + distance_matrix[j][i]:
                            prev[msk | (1 << i)][i] = j
                            dp[msk | (1 << i)][i] = dp[msk][j] + distance_matrix[j][i]
        min_distance, min_route = self.extract_solution(n, dp, prev, distance_matrix)

        return min_distance, min_route

    def extract_solution(self, n, dp, prev, distance_matrix):
        min_distance = None
        last_idx = None
        for i in range(1, n):
            if dp[(1 << n) - 1][i] is not None:
                if min_distance is None:
                    min_distance = dp[(1 << n) - 1][i] + distance_matrix[i][0]
                    last_idx = i
                elif min_distance > dp[(1 << n) - 1][i] + distance_matrix[i][0]:
                    min_distance = dp[(1 << n) - 1][i] + distance_matrix[i][0]
                    last_idx = i

        min_route = []
        msk = (1 << n) - 1
        while prev[msk][last_idx] is not None:
            min_route.append(last_idx)
            last_idx, msk = prev[msk][last_idx], msk ^ (1 << last_idx)

        min_route.append(last_idx)

        min_route = list(reversed(min_route))
        min_route.append(0)

        self.check_route(min_distance, min_route, distance_matrix)

        return min_distance, min_route
