import logging

def upload_file(ssh, sftp, home_dir, server, user, **kwargs):
    """
    Upload a file to a specific path on the remote server.

    :param sftp: The SFTP connection object.
    :param kwargs: Additional arguments, including:
        - local_file_path: The path to the local file to be uploaded.
        - remote_file_path: The destination path on the remote server.
    """
    
    local_file_path = kwargs.get("local_file_path")
    remote_file_path = kwargs.get("remote_file_path")

    logging.info(f"Upload file for {user}@{server} to {home_dir} ...")


    if not local_file_path or not remote_file_path:
        raise ValueError("Both 'local_file_path' and 'remote_file_path' must be provided.")

    try:
        logging.info(f"Uploading file from {local_file_path} to {remote_file_path}...")

        # Use the SFTP connection to upload the file
        with sftp.open(remote_file_path, "wb") as remote_file:
            with open(local_file_path, "rb") as local_file:
                remote_file.write(local_file.read())

        logging.info(f"File uploaded successfully to {remote_file_path}.")
    except Exception as e:
        logging.error(f"Failed to upload file: {e}")
        raise