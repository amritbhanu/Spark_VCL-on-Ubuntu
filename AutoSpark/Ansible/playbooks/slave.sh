ansible-playbook -s --extra-vars 'MASTER_YES="false" USER="" SPARK_URL="spark://abc:7077" MASTER_IP=""' sparkplaybook.yml -i slave_inventory
