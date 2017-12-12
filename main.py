#!/usr/bin/python3

import sys
from parse import parse_arg
import json
from models import Node

def normalize_to_list(data):
    '''Iterate over the JSON file (data)
       to transform each value to a list.'''
    for key, value in data.items():
        if type(value) is not list:
            data[key] = list(value)

def create_nodes(data):
    '''Iterate over the JSON file (data)
       to return a list of Node objects'''
    node_list = []
    for key, value in data.items():
        node = Node(key, value)
        if node not in node_list:
            node_list.append(node)
    
    for key, value in data.items():
        for item in value:
            if not any(x.name == item for x in node_list):
                node_list.append(Node(item))
    
    return node_list

def get_independant_nodes(node_list):
    '''Create a list of node that have no dependencies,
       meaning that they can be processed.'''
    list_inde = []
    for node in node_list:
        if not node.dependencies:
            list_inde.append(node.name)
    return list_inde

def remove_empty_keys(node_list):
    '''Delete all processed nodes from
       the list. Return 0 if no nodes were
       removed (circular dependencies found), 
       else return 1.'''

    flag = 0
    to_remove = []

    for node in node_list:
        if not node.dependencies:
            to_remove.append(node)
            flag = 1

    if to_remove:
        for letter in to_remove:
            node_list.remove(letter)            
            for node in node_list:
                node.clear_dependency(letter)

    return flag
    

def main(argv):
    # Parsing
    fd = parse_arg(argv)
    try:
        data = json.load(fd)
    except ValueError:
        print("Error : your JSON file is corrupted.")
        sys.exit()

    normalize_to_list(data)
    node_list = create_nodes(data)

    result = []

    # Loop while we have nodes to process    
    while node_list:
        result.extend(get_independant_nodes(node_list))
        flag = remove_empty_keys(node_list)
        if not flag:
            print("Error : circular dependencies in file.")
            sys.exit()

    print (result)

if __name__ == "__main__":
    main(sys.argv[1:])