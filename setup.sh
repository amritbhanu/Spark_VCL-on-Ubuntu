#from the source directory.

sudo apt-get upgrade -y
sudo apt-get install python-pip -y
sudo apt-get install python-dev -y
sudo apt-get install libgmp3-dev -y
pip install pycrypto

cp AutoSpark/Spark_Jobs/lda.zip ~
cd ../
mv spark/spark_latest/conf/spark-env.sh.template spark/spark_latest/conf/spark-env.sh
touch spark/spark_latest/conf/slaves
unzip lda.zip
rm lda.zip
cd Spark_VCL-on-Ubuntu
wget https://pypi.python.org/packages/source/a/ansible/ansible-1.9.4.tar.gz
tar -xvf ansible-1.9.4.tar.gz
cd ansible-1.9.4
sudo python setup.py install
cd ..
rm ansible-1.9.4.tar.gz
sudo rm -rf ansible-1.9.4

#if [ ! -d "ssh_keys" ]; then
  #ssh-keygen -t rsa
  #mkdir ssh_keys
  #cp ~/.ssh/id_rsa ssh_keys/id_rsa
  #cp ~/.ssh/id_rsa.pub ssh_keys/id_rsa.pub
  # Control will enter here if $DIRECTORY doesn't exist.
#fi

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
sudo sh -c "echo \" UserKnownHostsFile /dev/null\" >> /etc/ssh/ssh_config"

node autospark-cluster-launcher.js
