#from the source directory.

wget https://pypi.python.org/packages/source/a/ansible/ansible-1.9.4.tar.gz
tar -xvf ansible-1.9.4.tar.gz
cd ansible-1.9.4
sudo python setup.py install
cd ..
rm ansible-1.9.4.tar.gz
sudo rm -rf ansible-1.9.4

if [ ! -d "ssh_keys" ]; then
  #ssh-keygen -t rsa
  #mkdir ssh_keys
  #cp ~/.ssh/id_rsa ssh_keys/id_rsa
  #cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub
  # Control will enter here if $DIRECTORY doesn't exist.
fi

sudo python setup.py install
echo $1 > user.txt

export ANSIBLE_HOST_KEY_CHECKING=False

sudo apt-get update -y

cd AutoSpark/scripts
sudo ./setup_machine.sh

cd ../driver

if [ ! -d "node_modules" ]; then
  npm install
  # Control will enter here if $DIRECTORY doesn't exist.
fi

sudo sh -c "echo \"StrictHostKeyChecking no\" >> /etc/ssh/ssh_config"

node autospark-cluster-launcher.js
