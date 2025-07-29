import paramiko
import logging
from typing import Callable, Optional, Tuple


def connect_ssh(
    server: str,
    user: str,
    password: Optional[str] = None,
    key_path: Optional[str] = None
) -> Tuple[paramiko.SSHClient, paramiko.SFTPClient, str]:
    """
    Establish an SSH connection and return the SSH client, SFTP client, and home directory.

    :param server: Server address
    :param user: Username
    :param password: Password for authentication (optional)
    :param key_path: Path to the SSH private key file (optional)
    :return: Tuple containing the SSH client, SFTP client, and home directory path
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if key_path:
        # Use RSA private key authentication
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        ssh.connect(server, username=user, pkey=private_key, timeout=10)
    elif password:
        # Use username/password authentication
        ssh.connect(server, username=user, password=password, timeout=10)
    else:
        raise ValueError("Either password or key_path must be provided for authentication.")

    sftp = ssh.open_sftp()
    home_dir = sftp.normalize('.')
    return ssh, sftp, home_dir


def connect_ssh_and_exec_use_case(
    server: str,
    user: str,
    use_case: Callable[[paramiko.SFTPClient, str, str, str], None],
    password: Optional[str] = None,
    keypath: Optional[str] = None,
    **kwargs
) -> None:
    """
    Wrapper to handle SSH connection and execute a specific action.

    :param server: Server address
    :param user: Username
    :param use_case: Callable function for the specific use case
    :param password: Password for authentication (optional)
    :param keypath: Path to the SSH private key file (optional)
    :param kwargs: Additional arguments for the action
    """
    logging.info(f"Connecting to {user}@{server}...")
    try:
        ssh, sftp, home_dir = connect_ssh(server, user, password, keypath)
        if use_case:
            use_case(ssh, sftp, home_dir, server, user, **kwargs)
        sftp.close()
        ssh.close()
        logging.info(f"Action {use_case.__name__} executed successfully on {server}.")
    except Exception as e:
        logging.error(f"Failed to connect or execute {use_case.__name__} on {server}: {e}")