# Data for SAMPL6 Part II paper
[![DOI](https://zenodo.org/badge/223044465.svg)](https://zenodo.org/badge/latestdoi/223044465)

- **data**: The latest archived version of the data can be found on
  Zenodo by following the DOI on the badge. If you want to refer to
  the data over all versions use DOI
  [10.5281/zenodo.3549988](https://doi.org/10.5281/zenodo.3549988).
- **paper**: (add full citation when available)

  Shujie Fan, Bogdan I. Iorga, Oliver Beckstein. _Prediction of octanol-water
  partition coefficients for the SAMPL6-logP molecules using molecular dynamics
  simulations with OPLS-AA, AMBER and CHARMM force fields_. J Computer-Aided
  Molecular Design (2019).

## Background

The [SAMPL6 (Part II) logP
Challenge](https://github.com/MobleyLab/SAMPL6/blob/master/logP_challenge_instructions.md)
consists of predicting the octanol-water partition coefficients (log
P) of 11 small molecules that resemble fragments of small molecule
protein kinase inhibitors. Our aim is to evaluate how well current
models can capture the transfer free energy of small molecules between
different solvent environments through blind predictions.

This repository contains all data discussed in our paper _Prediction
of octanol-water partition coefficients for the SAMPL6-logP molecules
using molecular dynamics simulations with OPLS-AA, AMBER and CHARMM
force fields_ in the SAMPL6 Special Issue of the Journal of
Computer-Aided Molecular Design. 

## Input files

Topology input files for Gromacs 2018 are provided in the `02_top` directory
and its subdirectories for the different compounds and force fields. 

Simulations were set up and managed with
[mdpow](https://github.com/Becksteinlab/MDPOW) (0.7.0 development
version, equivalent to commit
20152ad9723fa5ad9d039362233da07b5fa7811a).

## SAMPL6 submission

- Directory `03_prep_submission` contains scripts to generate the
  submission files from Google Sheets (which we used for aggregating
  data). They are not strictly necessary as supporting information but
  might be of interest for anyone who wants to do something similar
  (although this was more of an experiment than a workflow we would
  generally recommend).
- Directory `04_submission` contains the data for our SAMPL6
  submissions as CSV files.
  
  | number 	| ID    	| force field          	| octanol 	|
  |--------	|-------	|----------------------	|---------	|
  | 1      	| sqosi 	| AMBER/GAFF           	| dry     	|
  | 2      	| 6nmtt 	| AMBER/GAFF           	| wet     	|
  | 3      	| eufcy 	| OPLSAA/LigParGen     	| dry     	|
  | 4      	| mwuua 	| OPLSAA/LigParGen     	| wet     	|
  | 5      	| cp8kv 	| OPLSAA/transferrable 	| dry     	|
  | 6      	| 623c0 	| OPLSAA/transferrable 	| wet     	|
  | 7      	| 3oqhx 	| CHARMM/CGENFF        	| dry     	|
- Directory `06_data` contains the same data but organized by force
  field and molecule.

## Improved protocol

The paper discusses improvements to our protocol. The data for these
calculations can be found in directory `07_alchemlyb_results`.

