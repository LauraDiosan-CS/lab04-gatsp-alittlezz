"""Simple travelling salesman problem between cities."""

from __future__ import print_function

from console_ui import ConsoleUI
import math

def encode_data(file_name, new_file_name):
    coords = []
    with open('tests/' + file_name, 'r') as file:
        for line in file.readlines():
            _, lat, lon = line.split(' ')
            lat = float(lat)
            lon = float(lon)
            coords.append([lat, lon])
    distance_matrix = []

    def euclidean(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(round(euclidean(coords[i], coords[j])))
        distance_matrix.append(row)

    with open('tests/' + new_file_name, "w") as file:
        file.write(str(len(distance_matrix)) + '\n')
        for row in distance_matrix:
            file.write(','.join(map(lambda x: str(x), row)) + '\n')

    print("Finished encoding", file_name, '....')

from timeit import default_timer as timer

if __name__ == '__main__':
   ui = ConsoleUI()
   ui.run()