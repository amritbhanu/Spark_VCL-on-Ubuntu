#from the source directory.
python setup.py install
echo $1 > user.txt

cd VCL

ssh-keygen -t rsa
mkdir ssh_keys
cp ~/.ssh/id_rsa ssh_keys/id_rsa
cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub

sudo apt-get update -y
sudo apt-get install git

cd VCL/AutoSpark/scripts
sudo ./setup_machine.sh

cd ../driver
npm install

sudo echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

node autospark-cluster-launcher.js'
