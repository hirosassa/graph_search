#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import graph

class TestGraph(unittest.TestCase):
    '''
    Unit test for graph.py
    '''
    def setUp(self):
        '''
        This method sets up the test graph data
        '''
        test_graph_data = {'1': [], '2': ['1'], '3': ['1', '4'], '4': [],
                           '5': ['2', '3'], '6': ['3']}
        self.g = graph.Graph()
        self.g.construct_from_edgeset(test_graph_data)
        
    def test_pred_nodes(self):
        preds = set(self.g.pred_nodes('5'))
        expected = set(['1', '4', '2', '3', '5'])
        self.assertEqual(preds, expected)

    def test_succ_nodes(self):
        succs = set(self.g.succ_nodes('1'))
        expected = set(['1', '2', '3', '5', '6'])
        self.assertEqual(succs, expected)


if __name__ == '__main__':
    unittest.main()
