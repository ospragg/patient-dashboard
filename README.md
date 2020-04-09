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
	- mkdir -p downloads/credentials
	- nano downloads/credentials/aws.yaml

- run tests:
	- python3 -m unittest discover -v