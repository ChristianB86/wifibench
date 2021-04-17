# wifibench
python tool to test connection speed between two devices

Usage:
Start as server:
./wifibench.py -s

Start as server on specific port:
./wifibench.py -s -p 3050

Start as client:
./wifibench.py -c host
./wifibench.py -c host -p 3050

example:

./wifibench.py -c 192.168.0.2 
./wifibench.py -c sub.example.tld
