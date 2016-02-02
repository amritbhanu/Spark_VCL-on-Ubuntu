var prompt= require('prompt');
var exec = require('child_process').exec;
var sys = require('sys')

// Getting the file directory
BASE_DIR = __dirname

// Starting a new prompt
prompt.start()

// Command Executors
function puts(error, stdout, stderr) { sys.puts(stdout) }

function command_executor(cmd) {

	console.log('Executing :' + cmd);
	var proc = exec(cmd, puts);
	proc.stdout.on('data', function(data) {
	console.log(data);
	});
}

console.log('#########################################');
console.log('##     Welcome to AutoSpark Job Submit   ##');
console.log('#########################################');
console.log('\n')
console.log('Enter provider: vcl');
console.log('\n')

prompt.get(['provider','spark_master_ip', 'spark_context_url','spark_job_file_path', 'job_name_at_destination', 'data_file_name'], function (err, result) {

    provider = result.provider
    spark_master_ip = result.spark_master_ip
    spark_context_url = result.spark_context_url
    spark_job_file_path = result.spark_job_file_path
    job_name_at_destination = result.job_name_at_destination
    data_file_name = result.data_file_name

    // Executing the spark job
    if (provider === 'vcl') {

        console.log("Copying the program to the remote spark master...")
        cmd = "scp -i " + spark_job_file_path + " ubuntu@" + spark_master_ip + ":/home/ubuntu/" + job_name_at_destination
        command_executor(cmd)

        console.log("Running spark job on master...")
        cmd = "ssh -l ubuntu " + spark_master_ip + " 'sudo /spark/spark_latest/bin/pyspark /home/ubuntu/"+ job_name_at_destination + " " + spark_context_url + " " + data_file_name + "'"
        command_executor(cmd)

    }

    // Prompt ends here
    });
