import subprocess
import yaml
def run_kubectl_command(verb, object, namespace,kubeconfig_file="",extra_flags=""):
    if kubeconfig_file != "":
        kubeconfig_flag = f"--kubeconfig={kubeconfig_file}"
    else:
        kubeconfig_flag = ""
    command = f"kubectl {verb} {object} -n {namespace} {extra_flags} {kubeconfig_flag}"
    command_list = command.split()
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        exit(1)

def run_kubectl_exec(pod_name, namespace,exec_command,kubeconfig_file=""):
    if kubeconfig_file != "":
        kubeconfig_flag = f"--kubeconfig={kubeconfig_file}"
    else:
        kubeconfig_flag = ""

    command = f"kubectl {kubeconfig_flag} -n {namespace} exec {pod_name} -- {exec_command}"
    print(command)
    command_list = command.split()
    print(command_list)
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True
            )
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        exit(1)

def generate_kube_config(sa_token,ca_cert,api_server,user_name,config_output_file="config.yaml"):
    config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster":{
                    "server" : str(api_server),
                    "certificate-authority-data": str(ca_cert)
                },
                "name": str(api_server),
            }
        ],
        "contexts":[
            {
                "context": {
                    "cluster": str(api_server),
                    "user": str(api_server),
                },
                "name": str(api_server),
            }
        ],
        "current-context": str(api_server),
        "users": [
            {
                "name": str(user_name),
                "user": {
                    "token": sa_token
                }
            }
        ]
    }
    config_text = yaml.dump(config, default_flow_style=False)
    open(config_output_file,"w").write(config_text)

    print(f"kubeconfig created for {api_server} in {config_output_file}")
    return config_output_file
