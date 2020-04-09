# patient-dashboard

## setup

- set up ec2
	- sudo yum update
	- sudo yum install htop
	- sudo yum install git-core
	- sudo yum install python3
	- git clone https://github.com/ospragg/patient-dashboard.git
	- cd patient-dashboard
	- git remote set-url origin https://ospragg@github.com/ospragg/patient-dashboard.git
	- pip3 install -r requirements.txt --user
	- mkdir -p data/credentials
	- nano data/credentials/patient-tracker-a176de3bd573.json
	- nano data/credentials/server.crt
	- nano data/credentials/server.key
	- forward port sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080
		- iptables -t nat -L --line-numbers
        	- list port forwarding with line numbers
        - iptables -t nat -D PREROUTING 1
        	- delete by line number
        - iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

- run tests:
	- python3 -m unittest discover -v