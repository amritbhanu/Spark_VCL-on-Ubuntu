import logging
import requests
import time
import os
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils
from ansible.inventory.group import Group
from ansible.inventory.host import Host

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class VCLOpsworks(object):
    def __init__(self, config, image_id, start, length, count, node_type, playbook):
        self.config = config
        self.image_id = image_id
        self.length = length
        self.start = start
        self.count = count
        self.node_type = node_type
        self.hosts = {}
        self.MIN_SLEEP = 10
        self.playbook = playbook

    def run(self):
        for response in self.config.api.add_request(image_id=self.image_id,
                                                    start=self.start,
                                                    length=self.length,
                                                    count=self.count):
            if response["status"] == "success":
                log.info("request success")
                request_id = response["requestid"]
                log.info("request id {}".format(request_id))
                self.__wait_for_request_ready(request_id)
                server_ip, connect_port, user = self.__connect(request_id)
                self.hosts[server_ip] = {
                    "ansible_ssh_host": server_ip,
                    "ansible_ssh_user": user,
                    "ansible_ssh_port": connect_port
                }
        log.info("hosts {}".format(self.hosts))
        self.create_servers_file(self.hosts, self.node_type)
	#self.create_shell_script(self.hosts)
        if self.playbook:
            val=self.configure_hosts(self.hosts, self.playbook)


    def __wait_for_request_ready(self, request_id):
        log.info("checking request {} status".format(request_id))
        response = self.config.api.get_request_status(request_id)
        status = response['status']
        wait_time = max(int(response['time']) * 30, self.MIN_SLEEP) if status != 'ready' else None
        while status == "loading":
            log.info("sleeping for {} seconds".format(wait_time))
            time.sleep(wait_time)
            log.info("checking request {} status".format(request_id))
            response = self.config.api.get_request_status(request_id)
            status = response['status']
            wait_time = max(int(response['time']) * 30, self.MIN_SLEEP) if status != 'ready' else None

    def __connect(self, request_id):
        log.info("connecting to {}".format(request_id))
        remote_ip = requests.get('http://httpbin.org/ip').json()['origin']
        response = self.config.api.get_request_connect_data(request_id=request_id,
                                                 remote_ip=remote_ip)
        log.debug("response {}".format(response))
        status = response['status']
        server_ip = response['serverIP']
        connect_port = int(response['connectport'])
        user = response['user']
        return server_ip, connect_port, user

    def configure_hosts(self, reservation_obj, playbook):
        inven = Inventory(host_list=reservation_obj.keys())
        for host in inven.get_hosts():
            for key, value in reservation_obj[host.name].items():
                host.set_variable(key, value)

        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        pb = PlayBook(inventory=inven,
                      playbook=playbook,
                      stats=stats,
                      callbacks=playbook_cb,
                      runner_callbacks=runner_cb)
        pb.run()

    def create_servers_file(self, cluster_info, node_type):

	if (node_type=='master'):
		python_file_path = os.path.dirname(os.getcwd())

		master_file_path = os.path.join(python_file_path +
				                    "/VCL/AutoSpark/Ansible/playbooks/master_file")

		master_file = open(master_file_path, "w")
		master_file.truncate()
		master_file.write(cluster_info.keys()[0] +"\n")
		master_file.close()
	elif (node_type=='slave'):
		slave_file_path = os.path.join(python_file_path +
				                   "/VCL/AutoSpark/Ansible/playbooks/slave_file")

		slave_file = open(slave_file_path, "w")
		slave_file.truncate()

		# Writing the slave inventory file
		for slave in range(0,len(cluster_info.keys())):
			slave_file.write(cluster_info.keys()[slave] +"\n")

		slave_file.close()
	

    def create_inventory_file(self, cluster_info):

	python_file_path = os.path.dirname(os.getcwd())

	master_file_path = os.path.join(python_file_path +
		                            "/VCL/AutoSpark/Ansible/playbooks/master_inventory")

	master_file = open(master_file_path, "w")
	master_file.truncate()

	# Writing the master inventory file
	master_file.write("[sparknodes]\n")
	master_file.write(cluster_info.keys()[0] +"\n")
        slave_file_path = os.path.join(python_file_path +
		                           "/VCL/AutoSpark/Ansible/playbooks/slave_inventory")

	slave_file = open(slave_file_path, "w")
	slave_file.truncate()

	# Writing the slave inventory file
	slave_file.write("[sparknodes]\n")
	if len(cluster_info)>1:
		for slave in range(1,len(cluster_info.keys())):
		    slave_file.write(cluster_info.keys()[slave] +"\n")

	master_file.close()
	slave_file.close()

    def create_shell_script(self, cluster_info):

	    master = cluster_info.keys()[0]
	    python_file_path = os.path.dirname(os.getcwd())

	    # Master shell script
	    shell_script_master_path = os.path.join(python_file_path +
		                                    "/VCL/AutoSpark/Ansible/playbooks/master.sh")

	    script_file_master = open(shell_script_master_path, "w")
	    script_file_master.truncate()
	    script_file_master.write("ansible-playbook -s --extra-vars ")
	    script_file_master.write("\'MASTER_YES=\"true\" USER=\"ubuntu\" ")
	    script_file_master.write("SPARK_URL=\"\" MASTER_IP=\"")
	    script_file_master.write(master)
	    script_file_master.write("\"\' sparkplaybook.yml -i master_inventory\n")

	    # Slave shell script
	    shell_script_slave_path = os.path.join(python_file_path +
		                                   "/VCL/AutoSpark/Ansible/playbooks/slave.sh")
	    if len(cluster_info)>1:
		    script_file_slave = open(shell_script_slave_path, "w")
		    script_file_slave.truncate()
		    script_file_slave.write("ansible-playbook -s --extra-vars ")
		    script_file_slave.write("\'MASTER_YES=\"false\" USER=\"ubuntu\" ")
		    script_file_slave.write("SPARK_URL=\"spark://")
		    script_file_slave.write(master + ":7077\" ")
		    script_file_slave.write("MASTER_IP=\"\"")
		    script_file_slave.write("\' sparkplaybook.yml -i slave_inventory\n")
