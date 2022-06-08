# A Benchmarking Platform for Failure Detectors  
The project features a benchmarking platform that allows users to specify FD algorithms, 
gives an objective evaluation of the performance of different failure detectors, and visualizes
the results in various ways. Since PlanetLab data is used for the benchmark algorithm, 
no distributed environment is required for running the code. Now, the program
can only be run from Python command, and it will be turned into a CLI tool in a future release.

## Requirements
Software (see details in `requirements.txt`):    
 - Python 3.8 (recommended, other versions not tested)
 - matplotlib
 - numpy
 - pandas
 - psutil

Hardware:    
 - Windows 10 or 11 (recommended, other systems are not tested)
 - Core i5 or better
 - 2 GB RAM or larger

## Installation
1. Clone the Git repo. `git clone https://github.com/BenchamrkingPlatformforFailuredetector/Benchmark_Platform_for_Failure_Detector [path]`
2. Install requirements. `pip install -r requirements.txt`

## Components
`data` (directory): PlanetLab time series data, see details in `data/README-trace-files-explanation.txt`.

`Extension` (directory): folder to place the language files and record class .py files to specify customized FD algorithms.

`accural.py`: implements Accural FD.

`benchmark.py`: calculates benchmark scores and unifies output formats.

`bertier_estimate.py`: implements Bertier's FD.

`chen_estimate.py`: implements Chen's FD.

`main.py`: entry file that parses command line arguments and executes corresponding code.

`run.py`: runs the benchmark algorithm and obtains actual performance data.

`visualization.py`: implements functions to visualize the performances of FD algorithms.

## Contacts
Juncheng Dong (NYU Shanghai): [jd4115@nyu.edu](mailto:jd4115@nyu.edu)    
Ruhao Xin (NYU Shanghai): [rx434@nyu.edu](mailto:rx434@nyu.edu)    
Olivier Gilles Marin (NYU Shanghai): [ogm2@nyu.edu](mailto:ogm2@nyu.edu)
