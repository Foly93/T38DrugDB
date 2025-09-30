# T38DrugDB - ZINC20 Filtered Compound Database

_The Database is available from Github and Zenodo. Zenodo contains the full database while github only contains the executables and README._

## Overview
T38DrugDB provides:
- **34,345,597 compounds** in PDBQT and MOL2 formats
- **Filtered dataset** based on LogP, molecular weight, and medicinal chemistry guidelines
- **Random subsampling tools** for flexible dataset creation

## Usage
This directory contains a subset of the ZINC20 database filtered for physicochemical and structural properties observed in medicinal compounds. The purpose of this database is to aid drug discovery, especially concerning virtual screening via autodock-GPU. However, any other chemoinformatics tool for drug discovery that relies on MOL2 or PDBQT files may benefit from this subset.\
The main component are the ```PDBQT_filtered``` and ```MOL2_filtered``` subdirectories that contain >34,000,000 compounds in PDBQT/MOL2 format deposited in several ```.zip``` archives. The two subdirectories can be downloaded from Zenodo. They required further compression into ```.tar.gz``` to comply with Zenodo's upload size limit and need to be decompressed to yield the aforementioned ```.zip``` archives for intended usage with the supplied python scripts.\
The intended use of this database is to cover an extensive part of medicinally relevant chemical space for drug discovery projects. For this purpose, the full database can be used or it can be randomly subsampled via ```fetch_N_random_PDBQTs.py``` and ```fetch_N_random_MOL2s.py``` (make sure all required Python modules are installed). \
The ```.zip``` format was chosen to keep the database portable; however, this causes performance bottlenecks when trying to access the compounds. Using ```fetch_N_random_PDBQTs.py``` to subsample around 100,000 compounds may take 10 minutes, depending on the hardware. Therefore, ```tinyDB``` was created, which contains a tiny subset with around 200,000 compounds and fewer ```.zip``` archives while also containing ```fetch_N_random_*.py``` with identical functionality. Any testing should be conducted in this subdirectory for faster results. The file ```example.sh``` extracts 100 random PDBQT and MOL2 compounds into ```tempPDBQT/``` and ```tempMOL2/``` within seconds and is the quickest way to showcase the database's functionality.

## Quickstart
Test functionality with a Python script:
```bash
# Download only tinyDB/
cd tinyDB
python fetch_N_random_PDBQTs.py -i tinyT38DrugDB.csv -N 100 -d ./tempPDBQT/
```
Or use the provided example script to extract 100 random compounds into `tempPDBQT/` and `tempMOL2/` within seconds.
```bash
./example.sh
```
Use the Jupyter notebook for more detailed exploration:
```bash
jupyter notebook fetch_N_random_PDBQTs.ipynb
```
Compounds can also be extracted manually via their ZINC ID and corresponding tranche:
```bash
# For PDBQT format,
unzip -p PDBQT_filtered/HFABMN.zip ZINC000006949878.pdbqt > test.pdbqt
# For MOL2 format 
unzip -p MOL2_filtered/FFADMN.zip ZINC000620995125.mol2 > test.mol2
```

## Directory Structure
```
T38DrugDB/
├── README.md                 # THIS file
├── T38drugDB.csv             # Compound Table (34M+ rows, 3 cols)
├── fetch_N_random_PDBQTs.py  # PDBQT sampling script
├── fetch_N_random_MOL2s.py   # MOL2 sampling script
├── PDBQT_filtered/           # Main database (PDBQT format 35 GB; *.tar.gz: 16 GB)
│   └── [trancheID].zip       # Compressed compound batches
├── MOL2_filtered/            # Main database (MOL2 format 75 GB; *.tar.gz: 31 GB)
│   └── [trancheID].zip       # Compressed compound batches
└── tinyDB/                          # TEST SUBSET (1.2 GB)
    ├── example.sh                   # Quick test script
    ├── fetch_N_random_PDBQTs.py     # see above
    ├── fetch_N_random_MOL2s.py      # see above
    ├── fetch_N_random_PDBQTs.ipynb  # interactive subsampling
    ├── tinyPDBQT_filtered/          # see above PDBQT_filtered/
    │   └── [trancheID].zip          # see above
    └── tinyMOL2_filtered/           # see above MOL2_filtered/
        └── [trancheID].zip          # see above
```

## Brief File Descriptions
* **T38drugDB.csv**
  - only available at Zenodo
  - list of all SMILES and ZINCIDs contained in T38DrugDB.zip 
  - auxiliary file for subsampling compounds from the database
  - 34,345,597 lines
* **fetch_N_random_PDBQTs.py and fetch_N_random_MOL2s.py**
  - Python executable to subsample the database randomly
  - the file ```T38drugDB.csv``` is used for subsampling
  - files are extracted from the zip files in ```PDBQT_filtered``` or ```MOL2_filtered```
  - files are extracted into a directory specified as a command line argument to the python script (see ```python fetch_N_random_PDBQTs.py --help```)
  - It can take up to 10 minutes for a subsample ranging in the hundreds of thousands compounds
* **PDBQT_filtered/ and MOL2_filtered/**
  - only available at Zenodo
  - uploaded as .tar.gz and need to be extracted before usage
  - subdirectories with 35 GB and 75 GB of data
  - contains downloaded compounds from the ZINC20 database 
  - filtered via the ZINC20 webpage and according to the Handbook of Medicinal Chemistry
  - further info on filtering see **Filter Criteria Applied to ZINC20 Database**
  - compounds are stored in zip archives individually
* **tinyDB/**
  - lightweight database for testing and quick downloading
  - contains only 1.2 GB instead of 110 GB of Data
* **example.sh**
  - Quick demonstration script
  - executes the two Python scripts to extract 100 random compounds in both formats
  - also requires installing the required Python modules
* **tinyDB/fetch_N_random_PDBQTs.ipynb**
  - jupyter notebook for interactive testing
  - this file subsamples the PDBQT database randomly
  - the file ```tinyT38drugDB.csv``` is used for subsampling
  - files are extracted from the zip files in ```tinyPDBQT_filtered```
  - output directory specified as an argument in the ```parser.parse_args()``` function

## Optimization Tips
1. Download only ```tinyDB/``` first for development and testing
2. Download and extract ```PDBQT_filtered.tar.gz``` and ```MOL2_filtered.tar.gz``` after you verified ```tinyDB/``` works with your approach/workflow
3. Consider writing custom parallel processing scripts for extensive extractions

## Filter Criteria Applied to ZINC20 Database:
| property                | range (including) |
|-------------------------|-------------------|
| LogP                    | 1 to 3            |
| Mass                    | 250 to 450 Da     |
| NOCount                 | 2 to 9            |
| NHOHCount               | 0 to 3            |
| TPSA                    | 19 to 70 A^2      |
| NumRotatableBonds       | 1 to 8            |
| NumAromaticCarbocycles  | 0 to 2            |
| NumAromaticHeterocycles | 0 to 1            |
| NumAromaticRings        | 1 to 3            |
| FractionCSP3            | 0.2 to 0.6        |

## Citation
If you use T38DrugDB in your research, please cite:
```
[Add appropriate citation information here once available]
```

## License
This work is licensed under a Creative Commons Attribution 4.0 International License. See creativecommons.org/licenses/by/4.0/ for further information.

## Contact
For questions, issues, or contributions:
- luis.vollmers@tum.de
- zacharias@tum.de
- %%%publication DOI once available
