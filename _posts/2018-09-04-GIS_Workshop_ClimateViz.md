---
layout: post
title: Data Visualization Workshop Climate Data Visualization
description: Python
image: 
---
<hr />

## Project Description

This module is preparation for the data visualization with Python workshop. No programming background is required. In this installation module, you will follow step-by-step instructions to install python and some of the most popular data processing / visualization libraries we will be suing for this workshop. You will be using Anaconda as a Python management software that is cross platform, thus all the instructions are the same between Windows, OSX and Linux. 

***

# Step 1
### Python Installation

Please follow the steps detailed in the [Data Science Intro](https://tedngai.github.io/itlworkshops/2019/DataSci01/){:target="_blank"}  for instructions to install Anaconda and create virtual environments. There is step-by-step instructions there. 

You will want to create a new virtual environment for this workshop, and you will need the following packages, netCDF4, numpy, matplotlib, and basemap. First create a new virtual environment.

```
conda create -n climateViz python=3.7
```
Once it's done, activtate the envionrment

```
conda activate climateViz
```

Now install the following packages

```
conda install numpy netCDF4 matplotlib basemap
```

***

# Step 2
### Download Climate Data

