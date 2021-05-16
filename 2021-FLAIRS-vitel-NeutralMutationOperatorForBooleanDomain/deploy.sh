#!/bin/bash
#clone our version of ecj
git clone https://github.com/cereal-lab/ecj.git nro
cd nro
#this branch contains ready to use nro for boolean domain experiments
git checkout bool_domain #commit when 
#build nro 
cd ecj
make nro 
#use next on Ubuntu to install venv - or consider https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
#apt-get install python3-venv
#create virtual environment for python automation script
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
#specify instead of 2 number of runs for one experiment
#check analyze.py for information of evolutionary process configuration and output or see README
python3 analyze.py 2
deactivate