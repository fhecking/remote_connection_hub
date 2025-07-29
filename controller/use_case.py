from enum import Enum
import logging

from ..service.connection.ssh_connector import connect_ssh_and_exec_use_case
## Relative Imports
from ..service.use_case.upload_file import upload_file
from ..service.use_case.execute_file import execute_file
from ..service.use_case.remove_file import remove_file


class UseCase(Enum):
    upload_file = "upload_file"
    execute_file = "execute_file"
    remove_file = "remove_file"

USE_CASE_MAPPING = {
    UseCase.upload_file.value: upload_file,
    UseCase.execute_file.value: execute_file,
    UseCase.remove_file.value: remove_file
}

def execute_use_case(use_case_name, connection, **kwargs):
    logging.info(f"Executing use_case: {use_case_name}")

    if use_case_name not in USE_CASE_MAPPING:
        raise ValueError(f"Unknown use case: {use_case_name}")
    action = USE_CASE_MAPPING[use_case_name]
    #action(connection, **kwargs)

    user = connection.get("user");
    server = connection.get("server");
    password = connection.get("password")
    if not user or not server:
        raise ValueError("Connection must include 'user' and 'server' keys.")
    
    connect_ssh_and_exec_use_case(server, user , action, password, **kwargs)
