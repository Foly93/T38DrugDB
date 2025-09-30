#!/bin/bash

python fetch_N_random_PDBQTs.py --help 
python fetch_N_random_PDBQTs.py -i tinyT38DrugDB.csv -N 100 -d ./tempPDBQT/

python fetch_N_random_MOL2s.py --help 
python fetch_N_random_MOL2s.py -i tinyT38DrugDB.csv -N 100 -d ./tempMOL2/
