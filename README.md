# :: :: :::WELCOME TO VENOM:: :: ::

## Installation 
Installing MongoDB 
```bash 
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod 
``` 
Install VENOM 
```bash 
git clone https://github.com/J0LGER/VENOM.git
```
