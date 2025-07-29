## Global Imports
from typing import Union, Dict, List
from enum import Enum
import logging

## Relative Imports
from ..service.connection.file import read_connection_file
from ..service.connection.m_remote_ng import read_mremoteng_connections_as_tree, Node

class ConnectionType(Enum):
    MREMOTE_NG = "mRemoteNG"
    FILE = "file"
    PUTTY = "putty"

def load_connections(source: str, config_path: str) -> Union[Node, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    """
    Load connections based on the source type.

    Args:
        source (str): The source type (e.g., "mRemoteNG", "file", "putty").
        config_path (str): The path to the configuration file.

    Returns:
        Union[Node, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
        A tree structure for mRemoteNG or a list of connections for other sources.

    Raises:
        ValueError: If the source type is unknown.
        NotImplementedError: If the source type is not yet implemented.
    """
    logging.info(f"Loading {source} connections from {config_path}")

    if source == ConnectionType.MREMOTE_NG.value:
        return read_mremoteng_connections_as_tree(config_path)
    elif source == ConnectionType.FILE.value:
        return read_connection_file(config_path)
    elif source == ConnectionType.PUTTY.value:
        # Placeholder for future implementation
        raise NotImplementedError("PuTTY session loading is not implemented yet.")
    else:
        raise ValueError(f"Unknown connection source: {source}")