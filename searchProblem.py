from queue import PriorityQueue
import threading, queue
from abc import ABC, abstractmethod
from node import *



class SearchProblem(ABC):

    @abstractmethod
    def getStartState(self):
        util.raiseNotDefined()

    @abstractmethod
    def isGoalState(self, state):
        util.raiseNotDefined()

    @abstractmethod
    def getSuccessors(self, state):
        util.raiseNotDefined()


    def depthFirstSearch(graph, start, goal):
        visited = []
        path = []
        q = []
        q.append((start,path))
        while not len(q)==0:
            current_node, path = q.pop()
            if current_node == goal:
                return path + [current_node]
            visited = visited + [current_node]
            child_nodes = graph[current_node]
            for node in child_nodes:
                if node not in visited:
                    if node == goal:
                        return path + [node]
                    q.append((node, path + [node]))
        return path


    def breadthFirstSearch(graph, start, goal):
        visited = []
        path = []
        q = queue.Queue()
        q.put((start,path))
        while not q.empty():
            current_node, path = q.get()
            if current_node == goal:
                return path + [current_node]
            visited = visited + [current_node]
            child_nodes = graph[current_node]
            for node in child_nodes:
                if node not in visited:
                    if node == goal:
                        return path + [node]
                    q.put((node, path + [node]))
        return path


    def add_to_open(open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f >= node.f):
                return False
        return True

    def astar(map, start, end):
        open = []
        closed = []
        start_node = Node(start, None)
        goal_node =  Node(end, None)
        open.append(start_node)
        while len(open) > 0:
            open.sort()
            current_node = open.pop(0)
            closed.append(current_node)
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            (x, y) = current_node.position
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for next in neighbors:
                if next not in map:
                    continue
                neighbor = Node(next, current_node)
                if (neighbor in closed):
                    continue
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                if (SearchProblem.add_to_open(open, neighbor) == True):
                    open.append(neighbor)
        return None

    def greedy(map, start, end):
        open = []
        closed = []
        start_node = Node(start, None)
        goal_node =  Node(end, None)
        open.append(start_node)
        while len(open) > 0:
            open.sort()
            current_node = open.pop(0)
            closed.append(current_node)
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            (x, y) = current_node.position
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for next in neighbors:
                if next not in map:
                    continue
                neighbor = Node(next, current_node)
                if (neighbor in closed):
                    continue
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.h
                if (SearchProblem.add_to_open(open, neighbor) == True):
                    open.append(neighbor)
        return None









