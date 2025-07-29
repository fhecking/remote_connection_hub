import os

from common_controls.ssh_utils import connect_ssh


def upload_appmanager_zip_if_not_exists(sftp, projdisc, server, user, local_zip_path):
    """
    Uploads the AppManager-1.4.1.zip file to the remote server at $PROJDISC if it does not already exist.
    """
    remote_file_path = f"{projdisc}/AppManager-1.4.1.zip"
    remote_dir = projdisc
    filename = "AppManager-1.4.1.zip"
    try:
        if filename in sftp.listdir(remote_dir):
            print(f"{remote_file_path} already exists on {server}, skipping upload.")
        else:
            sftp.put(local_zip_path, remote_file_path)
            print(f"Uploaded {local_zip_path} to {remote_file_path} on {server}.")
    except Exception as e:
        print(f"Error checking/uploading file: {e}")

def connect_and_upload_zip(server, user, password=None, key_path=None, local_zip_path=None):
    print(f"Connecting to {user}@{server}...")
    if local_zip_path is None:
        # Set default path relative to the script location
        local_zip_path = os.path.join(os.path.dirname(__file__), "assets", "AppManager-1.4.1.zip")
    try:
        ssh, sftp, home_dir = connect_ssh(server, user, password, key_path)
        # Get $PROJDISC value from remote
        stdin, stdout, stderr = ssh.exec_command('source ~/.profile; echo $PROJDISC')
        projdisc = stdout.read().decode().strip()
        if not projdisc:
            raise Exception("Could not determine $PROJDISC on remote server.")
        upload_appmanager_zip_if_not_exists(sftp, projdisc, server, user, local_zip_path)
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"  Failed to connect or upload {local_zip_path} to {server}: {e}")