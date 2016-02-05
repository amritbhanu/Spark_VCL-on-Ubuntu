#from the source directory.
wget https://pypi.python.org/packages/source/a/ansible/ansible-1.9.4.tar.gz
tar -xvf ansible-1.9.4.tar.gz
cd ansible-1.9.4
python setup.py install

sudo python setup.py install
echo $1 > user.txt

export ANSIBLE_HOST_KEY_CHECKING=False

sudo apt-get update -y
sudo apt-get install git

cd AutoSpark/scripts
sudo ./setup_machine.sh

cd ../driver

if [ ! -d "node_modules" ]; then
  npm install
  # Control will enter here if $DIRECTORY doesn't exist.
fi



sudo sh -c "echo \"StrictHostKeyChecking no\" >> /etc/ssh/ssh_config"

node autospark-cluster-launcher.js
