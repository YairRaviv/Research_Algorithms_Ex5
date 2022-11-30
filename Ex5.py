from typing import Callable, Any
import networkx as nx


# ----------------------------------------------------------- Question 1 - Bounded Sets Iterator -------------------------------------

class bounded_subsets:
    """
    The solution:
    The Iterator keeps two main variables for the solution:
    1. vars - represents the size of the
    current subset that need to create.
    2. indexes - list of indexes which represents the current indexes (in lst) of the current subset.
    The Iterator iterates from vars = 0 to vars = n (lst size) and return the valid subsets
    with size 0 , then size 1 , etc.

    For each call to __next__ - The iterator if the current subset is valid ,
    if yes - its update the indexes list to represent the next subset and return the current result.
    else - its update the indexes and return to the start of the loop and check again.

    - The only difference between Q1.1 to Q1.2 is the sort of the input list in __init__.
    - The solution is efficient because it checks every possible subset only one time ,
      it doesn't perform any double-loop iteration nor recursion.
      its simply iterate over the "list" of all possible subsets once.

    Tests:
    >>> s = bounded_subsets([3,2,1], 0)
    >>> s.__next__()
    []

   >>> s = bounded_subsets([3,2,1], 6)
   >>> s.__next__()
   []
   >>> s.__next__()
   [1]
   >>> s.__next__()
   [2]
   >>> s.__next__()
   [3]
   >>> s.__next__()
   [1, 2]
   >>> s.__next__()
   [1, 3]
   >>> s.__next__()
   [2, 3]
   >>> s.__next__()
   [1, 2, 3]


    >>> s = bounded_subsets([], 1)
    >>> s.__next__()
    []

    >>> s = bounded_subsets([5,4,3,2,1], 6)
    >>> s.__next__()
    []
    >>> s.__next__()
    [1]
    >>> s.__next__()
    [2]
    >>> s.__next__()
    [3]
    >>> s.__next__()
    [4]
    >>> s.__next__()
    [5]
    >>> s.__next__()
    [1, 2]
    >>> s.__next__()
    [1, 3]
    >>> s.__next__()
    [1, 4]
    >>> s.__next__()
    [1, 5]
    >>> s.__next__()
    [2, 3]
    >>> s.__next__()
    [2, 4]
    >>> s.__next__()
    [1, 2, 3]


    """
    def __init__(self, lst, c):
        self.lst = sorted(lst)
        # self.lst = lst
        self.n = len(lst)
        self.c = c
        self.vars = 0
        self.indexes = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.vars == 0:
            self.vars += 1
            self.indexes.append(0)
            return []
        while True:
            try:
                res = [self.lst[i] for i in self.indexes]
            except:
                self.__update_indexes()
                continue
            if self.vars > self.n:
                raise StopIteration
            if self.vars == self.n:
                if sum(res) > self.c:
                    raise StopIteration
                else:
                    # now vars would be n+1 which cause StopIteration at the next iteration
                    self.vars += 1
                    return res
            if not (sum(res) > self.c):
                break
            else:
                self.__update_indexes()
        self.__update_indexes()
        return res

    def __update_indexes(self):
        if not (self.indexes[self.vars - 1] > (self.n - 1)):
            self.indexes[self.vars - 1] += 1
        else:
            # base case - end of the subsets with size 1.
            if self.vars == 1:
                self.indexes[0] = 0
                self.indexes.append(1)
                self.vars += 1
                return
            last = self.vars - 1
            append = True
            # checks :
            # 1.what is the last index in indexes that require update.
            # 2.Append means this was the last subset of the current size ,
            # so we need to increase vars by 1 and update the indexes.
            while last > 0:
                if self.indexes[last] == (self.indexes[last - 1] + 1):
                    last -= 1
                    continue
                else:
                    append = False
                    last -= 1
                    break
            if append:
                for i in range(self.vars):
                    self.indexes[i] = i
                self.indexes.append(self.vars)
                self.vars += 1
                return

            self.indexes[last] += 1
            tmp = self.indexes[last] + 1
            for i in range(last + 1, self.vars):
                self.indexes[i] = tmp
                tmp += 1
            return





# ----------------------------------------------------------- Question 1 - Strategy BFS/DFS  -------------------------------------



def shortest_path(algorithm: Callable, output: str, inp: Any):
    """
    algorithm = bfs or dfs
    output = 'length' or path
    inp = tuple or list:
        tuple = tuple of two ints represents src and dst and the graph
        list = list of two strings represents the integers of src and dst and the graph


    >>> g = nx.Graph()
    >>> g.add_nodes_from(range(1, 11))
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(4, 5)
    >>> g.add_edge(5, 6)
    >>> g.add_edge(6, 7)
    >>> g.add_edge(7, 8)
    >>> g.add_edge(8, 9)
    >>> g.add_edge(9, 10)
    >>> g.add_edge(1, 5)
    >>> g.add_edge(1, 2)

    "Test BFS for path - list input"
    >>> shortest_path(bfs,'path' , [1,4,g])
    [1, 5, 4]


    >>> g.add_edge(1, 4)
    >>> shortest_path(bfs,'path' , [1,4,g])
    [1, 4]

    >>> shortest_path(bfs,'path' , [1,10,g])
    [1, 5, 6, 7, 8, 9, 10]


    "Test DFS for path - list input"

    >>> g.remove_edge(1,4)
    >>> shortest_path(dfs,'path' , [1,4,g])
    [1, 5, 4]

    >>> g.add_edge(1, 4)
    >>> shortest_path(dfs,'path' , [1,4,g])
    [1, 4]

    >>> shortest_path(dfs,'path' , [1,10,g])
    [1, 5, 6, 7, 8, 9, 10]





    "Test BFS for length - tuple input"
    >>> g.remove_edge(1,4)
    >>> shortest_path(bfs,'length' , (1,4,g))
    3


    >>> g.add_edge(1, 4)
    >>> shortest_path(bfs,'length' , (1,4,g))
    2

    >>> shortest_path(bfs,'length' , (1,10,g))
    7


    "Test DFS for length - tuple input"

    >>> g.remove_edge(1,4)
    >>> shortest_path(dfs,'length' , (1,4,g))
    3

    >>> g.add_edge(1, 4)
    >>> shortest_path(dfs,'length' , (1,4,g))
    2

    >>> shortest_path(dfs,'length' , (1,10,g))
    7




    """

    # tuple = tuple of two ints represents src and dst and the graph
    # list = list of two strings represents the integers of src and dst and the graph
    try:
        if type(inp) is tuple:
            src = inp[0]
            dst = inp[1]
        elif type(inp) is list:
            src = int(inp[0])
            dst = int(inp[1])
        else:
            raise "Invalid Input"
        G = inp[2]
    except:
        raise "Invalid Input"

    try:
        if output == "length":
            return len(algorithm(src, dst , G.neighbors))
        elif output == "path":
            return algorithm(src, dst , G.neighbors)
        else:
            raise "Invalid Input"
    except:
        raise "Invalid Input"






def bfs(start:Any,end:Any,neghibor_function):
    # initalize help lists
    visited = []
    queue = []
    parents = {}

    visited.append(start)
    queue.append(start)
    # while the queue is not empty
    while queue:
        tmp = queue.pop(0)
        # iterate over tmp's neghibors
        for neghibor in neghibor_function(tmp):
            if neghibor == end:
                parents[neghibor] = tmp
                break
            if neghibor not in visited:
                parents[neghibor] = tmp
                visited.append(neghibor)
                queue.append(neghibor)
        #if we found path to "end" during the loop
        if end in parents.keys():
            break
    # if there is no way between start to end
    if end not in parents.keys():
        return []
    # restore the path between start t end
    tmp = end
    path = [end]
    while parents[tmp] != start:
        path.append(parents[tmp])
        tmp = parents[tmp]
    path.append(start)
    return path[::-1]


def bfs(start:Any,end:Any,neghibor_function):
    # initalize help lists
    visited = []
    queue = []
    parents = {}

    visited.append(start)
    queue.append(start)
    # while the queue is not empty
    while queue:
        tmp = queue.pop(0)
        # iterate over tmp's neghibors
        for neghibor in neghibor_function(tmp):
            if neghibor == end:
                parents[neghibor] = tmp
                break
            if neghibor not in visited:
                parents[neghibor] = tmp
                visited.append(neghibor)
                queue.append(neghibor)
        #if we found path to "end" during the loop
        if end in parents.keys():
            break
    # if there is no way between start to end
    if end not in parents.keys():
        return []
    # restore the path between start t end
    tmp = end
    path = [end]
    while parents[tmp] != start:
        path.append(parents[tmp])
        tmp = parents[tmp]
    path.append(start)
    return path[::-1]




def dfs(start:Any,end:Any,neghibor_function):
    # initalize help lists
    visited = []
    stack = []
    parents = {}

    visited.append(start)
    stack.append(start)
    # while the queue is not empty
    while stack:
        tmp = stack.pop()
        # iterate over tmp's neghibors
        for neghibor in neghibor_function(tmp):
            if neghibor == end:
                parents[neghibor] = tmp
                break
            if neghibor not in visited:
                parents[neghibor] = tmp
                visited.append(neghibor)
                stack.append(neghibor)
        #if we found path to "end" during the loop
        if end in parents.keys():
            break
    # if there is no way between start to end
    if end not in parents.keys():
        return []
    # restore the path between start t end
    tmp = end
    path = [end]
    while parents[tmp] != start:
        path.append(parents[tmp])
        tmp = parents[tmp]
    path.append(start)
    return path[::-1]








# ----------------------------------------------------------- Question 3 - Link for the solution -------------------------------------
# https://www.codingame.com/ide/puzzle/super-computer

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS)
    print("{} failures, {} tests".format(failures, tests))
