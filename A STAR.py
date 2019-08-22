import heapq


def matrix():
    a = list()
    print('Введите матрицу 10х10')
    print('Условные знаки:\n* - клетка\nX - стартовая клетка\nY - конечная клетка\n# - преграда\nO - путь')
    while len(a) != 10:
        inp = input()
        if len(inp) == 10:
            a.append(list(inp))
        else:
            print('Недопустимое кол-во знаков. Строка не засчиталась')
    return a


def meta_data(a):
    """
    В введеднной матрице находит метаданные
    :param a: Исходная матрица
    :return:
    x_cord - координаты начальной точки
    y_cord  - координаты конечной точки
    walls - координаты преград
    """
    wall, x_cord, y_cord = list(), tuple(), tuple()
    for num1, el1 in enumerate(a):
        for num2, el2 in enumerate(el1):
            if el2.upper() == 'X':
                x_cord = tuple((num2, num1))
            elif el2.upper() == 'Y':
                y_cord = tuple((num2, num1))
            elif el2 == '*':
                wall.append(tuple((num2, num1)))

    return x_cord, y_cord, wall


class Queue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Tree:
    def __init__(self, width, height):
        self.weights = {}
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, coord):
        (x, y) = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, coord):
        return coord not in self.walls

    def neighbors(self, coord):
        (x, y) = coord
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0:
            results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, to_node):
        return self.weights.get(to_node, 1)


def heuristic_man(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def heuristic_euclid(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def star_search(graph, start_cord, goal, heuristic):
    frontier = Queue()
    frontier.put(start_cord, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start_cord] = None
    cost_so_far[start_cord] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_coord in graph.neighbors(current):  # берем следующую координату
            new_cost = cost_so_far[current] + graph.cost(next_coord)  # стоимоть следующей клетки
            if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                cost_so_far[next_coord] = new_cost
                priority = new_cost + heuristic(goal, next_coord)
                frontier.put(next_coord, priority)
                came_from[next_coord] = current

    return came_from


def draw_tile(graph, coord, style, width):
    r = "."
    if 'number' in style and id in style['number']:
        r = "%d" % style['number'][id]
    if 'path' in style and coord in style['path']:
        if 'start' in style and coord == style['start']:
            r = "X"
        elif 'stop' in style and coord == style['stop']:
            r = "Y"
        else:
            r = "O"
    if coord in graph.walls:
        r = "#" * width
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()


def final_path(came_from, start_coord, end):
    current = end
    fin_path = list()
    while current != start_coord:
        fin_path.append(current)
        current = came_from[current]
    fin_path.append(start_coord)
    fin_path.reverse()
    return fin_path


if __name__ == "__main__":
    example = matrix()
    start, stop, walls = meta_data(example)

    tree = Tree(len(example), len(example[0]))
    tree.walls = walls

    #
    tmp_path_euclid = star_search(tree, start, stop, heuristic_euclid)
    path_euclid = final_path(tmp_path_euclid, start, stop)

    tmp_path_man = star_search(tree, start, stop, heuristic_man)
    path_man = final_path(tmp_path_man, start, stop)
    print('Кратчайший путь с эвристикой "Манхэттенское расстонияе": {}\n'
          'Кратчайший путь с эвристикой "Евклидово расстояние": {}\n'.format(len(path_man), len(path_euclid)))
    if len(path_man) <= len(path_euclid):
        print('Манхэттенское:\n')
        draw_grid(tree, path=path_man, start=start, stop=stop)
    else:
        print('Евклидово:\n')
        draw_grid(tree, path=path_euclid, start=start, stop=stop)
