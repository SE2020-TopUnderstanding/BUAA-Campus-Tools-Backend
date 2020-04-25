nohup python3 -u interface.py -d 1 > ddl.out 2>&1 &
nohup python3 -u interface.py -o 1 > other.out 2>&1 &
nohup python3 -u interface.py -r 1 > queue.out 2>&1 &