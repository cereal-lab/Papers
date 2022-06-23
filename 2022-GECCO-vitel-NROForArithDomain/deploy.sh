# runtime: java 1.8 or later, python3, git
git clone --depth 1 --branch arith_domain https://github.com/cereal-lab/ecj.git #to fetch arith_domain tagged version to ecj folder
cd ecj 
make jar # builds ecj with NRO 
# use java commands from data/exp0 or next one 
# NRO rewrites are placed in ec.domain.regression.strategy package AxiomsX classes
cp target/ecj-27.jar ../
cd ..
# post processing
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
deactivate