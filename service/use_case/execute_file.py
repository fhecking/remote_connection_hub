import logging

def execute_file(ssh, sftp, home_dir, server, user, **kwargs):
    """
    Execute a file on the remote server with a specific command.

    :param connection: The connection object (e.g., SSH connection).
    :param remote_file_path: The path to the file on the remote server.
    :param command: The command to execute the file (e.g., "python", "bash").
    """

    command = kwargs.get("command")
    remote_file_path = kwargs.get("remote_file_path")

    logging.info(f"Upload file for {user}@{server} to {home_dir} ...")

    try:
        
        full_command = f"{command} {remote_file_path}"
        logging.info(f"Executing command on remote server: {full_command}")

        # Assuming the connection object has an `exec_command` method
        stdin, stdout, stderr = ssh.exec_command(full_command)

        # Read the output and error streams
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        if error:
            logging.error(f"Error while executing file: {error}")
            raise Exception(f"Execution failed: {error}")

        logging.info(f"Execution output: {output}")
        return output
    except Exception as e:
        logging.error(f"Failed to execute file: {e}")
        raise