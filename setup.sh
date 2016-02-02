#from the source directory.
python setup.py install
echo $1 > user.txt

if [ ! -d "ssh_keys" ]; then
  ssh-keygen -t rsa
  mkdir ssh_keys
  cp ~/.ssh/id_rsa ssh_keys/id_rsa
  cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub
  # Control will enter here if $DIRECTORY doesn't exist.
fi
cp ~/.ssh/* ssh_keys/

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
