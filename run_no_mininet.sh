#/bin/bash


#run this code like ./run_no_mininet.sh <path-to-last-run>
#don't forget to make this file executable, chmod +x run_no_mininet.sh
if [ -z "$1" ]
then
      echo "Error: Please enter last run path"
      exit 2
fi
python3 program.py --pop 50 --iter 50 --no-mininet --toponame abilene --last-result-path $1 --n 1 --new
python3 program.py --pop 50 --iter 50 --no-mininet --toponame abilene --last-result-path $1 --n 2
python3 program.py --pop 50 --iter 50 --no-mininet --toponame abilene --last-result-path $1 --n 3
python3 program.py --pop 50 --iter 50 --no-mininet --toponame abilene --last-result-path $1 --n 4
python3 program.py --pop 50 --iter 50 --no-mininet --toponame abilene --last-result-path $1 --n 5
