import re
import numpy
import pandas
import zipfile
import argparse
from tqdm import tqdm
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Python script to be used for extracting random compounds in MOL2 format from the zip archives of this database. Random selection works compound wise, not tranche-wise.')
    parser.add_argument('-i','--input_file', type=str, default='./T38DrugDB.csv', help='Path to the input file containing the smiles String, the tranche-IDs and the ZINC-IDs.')
    parser.add_argument('-N','--random_lines',type=int, default=100, help='Number of random compounds to be extraced from the compressed database.')
    parser.add_argument('-d','--outputDirectory',type=str, default='./tempPDBQT/', help='Output directory that will contain the random subsample of compounds.')

    # set argument variables
    args = parser.parse_args()
    input_file = args.input_file
    random_lines = args.random_lines
    outputDirectory = args.outputDirectory

    # subsample the N random compounds from the list of molecules
    compounds = pandas.read_csv(input_file).sample(random_lines).values
    tranches = numpy.unique(compounds[:,2])
    pdbqt_ligands = []

    # extract the random compounds into memory from zip archives
    progress_bar = tqdm(tranches, position=1, bar_format='{desc}|{bar:60}|{n}/{total} [{elapsed}<{remaining}]')
    for tranche in progress_bar:
        progress_bar.set_description(f'Extracting from {tranche}...')
        pdbqt_ligands.extend(extract_resorted_pdbqt_archives(compounds,tranche))
    
    # writing compounds to files in specified directory
    Path(outputDirectory).mkdir(parents=True, exist_ok=True)
    for pdbqt_ligand in tqdm(pdbqt_ligands, desc=f'Writing Files to {outputDirectory}...', bar_format='{desc}|{bar:60}|{n}/{total} [{elapsed}<{remaining}]'):
        zincID = re.search('ZINC[0-9]+',str(pdbqt_ligand)).group(0)
        with open(f'{outputDirectory}/{zincID}.pdbqt','wb') as outputFile:
            outputFile.write(pdbqt_ligand)

def read_shuffled_sample_compounds(input_file):
    return [compound.strip().split(',') for compound in open(input_file)]


def extract_resorted_pdbqt_archives(compounds,tranche):
    indices = numpy.where(compounds == tranche)[0]
    tranche_zincIDs = numpy.char.add(compounds[indices][:,1].astype(str), '.pdbqt')
    tranche_zip = zipfile.ZipFile(f'./tinyPDBQT_filtered/{tranche}.zip', 'r')
    pdbqt_fileslist = tranche_zip.namelist()
    pdbqt_files = [tranche_zip.read(f'{zincID}') for zincID in sort_sublist_by_original_list(pdbqt_fileslist, tranche_zincIDs)]
    return pdbqt_files


def sort_sublist_by_original_list(full_list, sublist):
    order_dict = {element: index for index, element in enumerate(full_list)}
    return sorted(sublist, key=lambda x: order_dict[x])

if __name__ == "__main__":
    main()
