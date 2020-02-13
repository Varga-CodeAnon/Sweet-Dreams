"""Collect informations from the SSH protocol"""

from modules.cherrytree import *

def main_ssh(file_ctd):
    """Execute the information gathering"""
    begin_node(file_ctd,"ssh")
    print("[*] SSH enum in progress...")
    end_node(file_ctd)
    print("[*] SSH enum done!")
    # node_file = cherry_node_head(port,serv,versions[i])  # TODO: à implémenter
    # # import 80.py ou exec 80.py
    # cherry_node_tail(node_file)
    # insert_node(node_file,filename)