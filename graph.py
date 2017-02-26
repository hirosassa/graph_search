#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gv
import pickle

class Node:
    def __init__(self, name):
        self.name = name

class Graph:
    '''
    This class represents directed graph
    '''
    def __init__(self):
        self.node_set = set()
        self.forward_edge_set = dict()
        self.backward_edge_set = dict()

    def insert_node(self, node):
        self.node_set.add(node)
       
    def insert_edge(self, from_node, to_node):
        if not from_node in self.node_set:
            self.insert_node(from_node)
        if not to_node in self.node_set:
            self.insert_node(to_node)

        if(from_node in self.forward_edge_set):
            self.forward_edge_set[from_node].add(to_node)
        else:
            self.forward_edge_set[from_node] = {to_node}
        if (to_node in self.backward_edge_set):
            self.backward_edge_set[to_node].add(from_node)
        else:
            self.backward_edge_set[to_node] = {from_node}

    def dump_graph(self):
        '''
        This method outputs the graph.
        '''
        with open('graph.pickle', 'wb') as f:
            pickle.dump([self.node_set, self.forward_edge_set, self.backward_edge_set], f)

    def load_graph(self):
        '''
        This method loads the graph dumpped by dump_graph method.
        '''
        with open('graph.pickle', 'rb') as f:
            graph_data = pickle.load(f)
        self.node_set = graph_data[0]
        self.forward_edge_set = graph_data[1]
        self.backward_edge_set = graph_data[2]
            
    def construct_graph(self, filenames):
        '''
        This method constructs graph from an input list of file paths.
        '''
        for filename in filenames:
            node_list = [node.strip() for node in open(filename, 'r')]
            # The first line of the file represents current node
            current_node = node_list[0]
            self.node_set.add(current_node)
            
            # The rest lines represents prior node
            prior_nodes = node_list[1:]
            for prior_node in prior_nodes:
                prior_node.strip()
                self.insert_edge(prior_node, current_node)        

    def _dfs(self, edge_set, start_node):
        '''
        This method search the set of reachable nodes from start_node
        by depth-first search.
        It is note that the reachable node set contains start_node.
        '''
        stack = [start_node]
        visited = []
        while stack:
            current_node = stack.pop()
            if current_node not in visited:
                visited.append(current_node)
                priors = edge_set.get(current_node)
                if priors == None:
                    continue
                stack = list(priors) + stack
        return visited

    def succ_nodes(self, node):
        '''
        This method returns the set of successor nodes of the input node.
        '''
        return self._dfs(self.forward_edge_set, node)
    
    def pred_nodes(self, node):
        '''
        This method returns the set of predecessor nodes of the input node.
        '''
        return self._dfs(self.backward_edge_set, node)

    def visualize(self, filepath):
        '''
        This method visualize the graph by graphviz format.
        '''
        nodes = list(self.node_set)

        # trasform the directed edge set of the graph in the set of (src, dst) tuples
        tmp = [(src, list(dsts)) for src, dsts in self.forward_edge_set.items()]
        edges = []
        for src, dsts in tmp:
            for dst in dsts:
                edges.append((src, dst))

        # render the graph
        graph = gv.add_edges(
            gv.add_nodes(gv.digraph(), nodes), edges
        ).render(filepath)

if __name__ == '__main__':
    # construct a new graph
    g = Graph()
    ls = ['sample/1.txt', 'sample/2.txt', 'sample/3.txt', 'sample/4.txt', 'sample/5.txt', 'sample/6.txt']
    g.construct_graph(ls)
    print(g.node_set)
    print(g.forward_edge_set)

    # predecessor and successor search
    print(g.pred_nodes('3'))
    print(g.succ_nodes('3'))

    # visualize
    g.visualize('sample/graph')

    # dump
    g.dump_graph()

    # load the graph
    h = Graph()
    h.load_graph()
    print(h.node_set)
    print(h.forward_edge_set) 
