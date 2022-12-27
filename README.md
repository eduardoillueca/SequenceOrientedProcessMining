# Sequence-Oriented Sensitive Analysis for PM2.5 exposure and risk assessment using Interactive Process Mining 

This is the repository with the source code for the manuscript Sequence-Oriented Sensitive Analysis for PM2.5 exposure and risk assessment using Interactive Process Mining. Please note that this is a research repository and the code should be improved in future iterations in order to obtain a whole application. Next, it is described the content of the principal directories.

## config

This directory contains all the configuration files needed to run the model. These include the geojson with the I/O ratios, as well as the statistics needed to generate the synthetic population.

## data

This directory is subdivided in three:

### aq_data

This is the gridded air quality data, obtained from an air quality model. In our case, it is generated from the reference air quality stations using bilinear interpolation

### population_data

This is the data generated by the script *generator.py*, and it includes the citizens informations: id, work, location and epidemiological data

### sequence_data

These are the activities performed by the citizens with the corresponding exposure and risk. It is the input for the *Interactive Process Mining* and it is generated by the *sequences.py* script. The v6 labels are the dataset used to compute the KPIs presented in the paper, but note that each execution of *sequences.py* will generate different datasets - with equivalent KPIs

## scripts

There are four scripts

**generator.py**: it takes as input the configuration files and generate the population for the study

**sequences.py**: it takes as input the gridded air quality data and the population data. Then, it generates a csv with the sequence activities per citizens

**KPI.py**: it takes as input the sequence activities and compute the KPIs, plotting them in a gauge diagram

**anova.py**: it takes as input the sequence activities and compute the ANOVA analysis, with the corresponding plots.

Note that the scenarios selection is done through *Interactive Process Mining*. The PMApp tool for this study is a software developed in a previous project, which is not open access, and should be requested to the authors.
