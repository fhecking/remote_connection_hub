import os

def download_app_manager_ini(sftp, home_dir, server, user, output_dir, **kwargs):
    """
    Reads the AppManager.ini file from the remote home directory and writes its contents
    into a local file named user_server_AppManager.ini.
    """

    print(f"Downloading AppManager.ini for {user}@{server}...")
    stdin, stdout, stderr = sftp.ssh.exec_command('source ~/.profile; echo "$APPMAN_HOME/inconso_admin"')
    appman_inconso_admin = stdout.read().decode().strip()
    if not appman_inconso_admin:
        raise Exception("Could not determine $APPMAN_HOME on remote server.")

    remote_file = f"{appman_inconso_admin}/appManager.ini"
    print(f"Downloading {remote_file} from {server} for user {user}...")
    local_filename = f"{output_dir}/{user}_{server}_AppManager.ini"
    
    try:
        with sftp.open(remote_file, 'rb') as remote_f:
            content = remote_f.read().decode('utf-8')
            with open(local_filename, 'w', encoding='utf-8') as local_file:
                local_file.write(content)
        print(f"AppManager.ini saved to {local_filename}")
    except FileNotFoundError:
        print(f"AppManager.ini not found on {server} for user {user}")

