#from the source directory.
python setup.py install

#this will create 1 instance and we will install the packages and whatever is needed for that.
vcl-opsworks request add --image-id 3630 --node-type master -c 1 --playbook main.yml "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall" "aagrawa8@NCSU"
#it will return a connecting ip address, use that to do ssh.

dir=$(pwd)
val=1
while read line           
do           
     val=$"$line"           
done < $dir/AutoSpark/Ansible/playbooks/master_inventory

#ssh to 1 of the ips
ssh -X aagrawa8@$val

