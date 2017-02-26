#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This module is partially copied from the following url.
Thanks @matthiaseisen

https://gist.github.com/matthiaseisen/3278cedcd53afe62c3f3
'''

import graphviz as gv
import functools


digraph = functools.partial(gv.Digraph, format='pdf')

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph
