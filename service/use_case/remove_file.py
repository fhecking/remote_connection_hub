import logging

def remove_file(connection, remote_file_path):
    """
    Remove a file from the given remote location.

    :param connection: The connection object (e.g., SFTP or SSH connection).
    :param remote_file_path: The path to the file on the remote server.
    """
    try:
        logging.info(f"Attempting to remove file at {remote_file_path}...")

        # Assuming the connection object has an `sftp` attribute for file operations
        connection.sftp.remove(remote_file_path)

        logging.info(f"File successfully removed from {remote_file_path}.")
    except FileNotFoundError:
        logging.error(f"File not found: {remote_file_path}")
        raise FileNotFoundError(f"File not found: {remote_file_path}")
    except Exception as e:
        logging.error(f"Failed to remove file: {e}")
        raise