from common_controls.ssh_utils import connect_ssh

def connect_and_install_appmanager(server, user, password=None, key_path=None):
    print(f"Connecting to {user}@{server} for AppManager installation...")
    try:
        ssh, sftp, home_dir = connect_ssh(server, user, password, key_path)
        commands = [
            "cd $PROJDISC",
            "wget http://ifbmvn1:8082/artifactory/libs-release-local/com/inconso/bend/server/AppManager/1.4.1/AppManager-1.4.1.zip",
            "unzip -o ./AppManager-1.4.1.zip",
            "cd ./AppManager",
            "mkmf",
            "make inst"
        ]
        # Join commands with '&&' to ensure sequential execution and stop on error
        full_command = " && ".join(commands)
        stdin, stdout, stderr = ssh.exec_command(full_command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print("Errors:", err)
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"  Failed to connect or install AppManager on {server}: {e}")

        #proj && wget http://ifbmvn1:8082/artifactory/libs-release-local/com/inconso/bend/server/AppManager/1.4.1/AppManager-1.4.1.zip && unzip -o ./AppManager-1.4.1.zip && cd ./AppManager && mkmf && make inst

        ##proj && unzip -o ./AppManager-1.4.1.zip && cd ./AppManager && mkmf && make inst && cd $APPMAN_HOME && tree