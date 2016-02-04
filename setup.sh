#from the source directory.
python setup.py install
echo $1 > user.txt

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
