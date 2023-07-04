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
 - PyQt5 (for GUI only)

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

`ui.py`: main entry to GUI component, must be in the same working directory as `run_benchmark.py`, see more details in 
[GUI Explanations](#gui-explanations).

`runbenchmark.py`: spawns an internal process that runs benchmark for the GUI, must be in the same working directory 
as `ui.py`, see more details in [GUI Explanations](#gui-explanations).

## GUI Explanations
User must specify three parameters for the benchmark to run: _**directory of trace files**_, 
_**directory of Extension files (language files)**_, and _**path to Record class file**_, unless they already exist in
the current working directory and automatically detected by the software;    

The three parameters will then be passed into `run_benchmark.py` as command line options `-t`, `-E` and `-R` respectively,
and benchmark data will be produced by running this program as an internal process;

In our project, the three parameters are named `.data`, `.Extension` and `.Extension\record.py`
(`.Extension\newrecord.py`) respectively. 

We provide traces from PlanetLab in `.data` by default. Users are free to use their own trace files. However, 
the structure and format of the files MUST comply to `.data`;

We provide three failure detector language files (`.Extension\accural.txt`, `.Extension\bertier.txt`, 
`.Extension\chen.txt`) by default. Users are encouraged to add more failure detectors. However, user MUST ensure that 
every `.txt` file in _**directory of Extension files (language files)**_ is a language file; 

We provide two Record class files (`.Extension\record.py`, `.Extension\newrecord.py`) by default. Users are free to 
create their own Record classes. However, the classes MUST implement `AbstractRecord` class in `.Extension\_record.py`
, and it is recommended that the file is named `record.py` under _**directory of Extension files (language files)**_;

We DO NOT provide a way to add metrics in the GUI since it involves the modification of `run_benchmark.py`. We STRONGLY 
DISCOURAGE user to do so, and take no responsibility for any consequences.

## Contacts
Juncheng Dong (NYU Shanghai): [jd4115@nyu.edu](mailto:jd4115@nyu.edu)    
Ruhao Xin (NYU Shanghai): [rx434@nyu.edu](mailto:rx434@nyu.edu)    
Olivier Gilles Marin (NYU Shanghai): [ogm2@nyu.edu](mailto:ogm2@nyu.edu)
