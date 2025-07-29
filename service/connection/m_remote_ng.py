from enum import Enum
import logging
import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Union
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

PATH_M_REMOTE_NG_CONFIGS = "/mnt/c/Users/florian.hecking/AppData/Roaming/mRemoteNG/confCons.xml"

# Define types for better clarity
Connection = Dict[str, Optional[str]]
Node = Dict[str, Union[str, List[Connection], List["Node"]]]  # Recursive type for tree structure

class EncryptionMode(Enum):
    CBC = "CBC"
    GCM = "GCM"

class PasswordEncoding(Enum):
    M_R3_M = "mR3m"

def read_mremoteng_connections_as_groups(connections_file: Optional[str] = None) -> List[Dict[str, Union[str, List[Connection]]]]:
    """
    Reads server info from mRemoteNG's Connections.xml file and retains grouping information.
    Returns a list of dicts: {'group': ..., 'connections': [{'server': ..., 'user': ..., 'password': ..., 'keypath': ...}]}
    """
    if not connections_file or not os.path.exists(connections_file):
        raise FileNotFoundError(f"Connections.xml not found at {connections_file}")

    groups: List[Dict[str, Union[str, List[Connection]]]] = []
    tree = ET.parse(connections_file)
    root = tree.getroot()

    def parse_group(node: ET.Element) -> Dict[str, Union[str, List[Connection]]]:
        """Recursively parse groups and connections."""
        group_name = node.attrib.get("Name", "Ungrouped")
        group: Dict[str, Union[str, List[Connection]]] = {"group": group_name, "connections": []}

        for child in node:
            if child.attrib.get("Type") == "Connection":
                server = child.attrib.get("Hostname", "")
                user = child.attrib.get("Username", "")
                password = child.attrib.get("Password", "")  # Encrypted by default
                keypath = child.attrib.get("KeyFile", "")

                # Add connection to the group
                group["connections"].append({
                    "server": server,
                    "user": user,
                    "password": password if password else None,
                    "keypath": keypath if keypath else None
                })
            elif child.attrib.get("Type") == "Container":
                # Recursively parse sub-groups
                subgroup = parse_group(child)
                groups.append(subgroup)

        return group

    # Parse the root node for groups and connections
    for node in root.findall(".//Node"):
        if node.attrib.get("Type") == "Container":
            group = parse_group(node)
            groups.append(group)

    return groups


def read_mremoteng_connections_as_tree(connections_file: Optional[str] = None) -> Node:
    """
    Reads server info from mRemoteNG's Connections.xml file and organizes it into a tree structure.
    Nodes without connections are treated as headers, and subgroups are nested hierarchically.
    Returns a tree structure as nested dictionaries.
    """
    if not connections_file or not os.path.exists(connections_file):
        raise FileNotFoundError(f"Connections.xml not found at {connections_file}")

    tree = ET.parse(connections_file)
    root = tree.getroot()

    def parse_node(node: ET.Element) -> Node:
        """Recursively parse nodes into a tree structure."""
        node_name: str = node.attrib.get("Name", "Unnamed")
        node_type: str = node.attrib.get("Type", "")

        # Initialize the current node
        current_node: Node = {
            "name": node_name,
            "type": node_type,
            "connections": [],
            "children": []
        }

        # Process child nodes
        for child in node:
            if child.attrib.get("Type") == "Connection":
                # Add connection details
                server: str = child.attrib.get("Hostname", "")
                user: str = child.attrib.get("Username", "")
                password: str = child.attrib.get("Password", "")  # Encrypted by default
                keypath: str = child.attrib.get("KeyFile", "")

                decrypted_password: bytes = base64.b64decode(password) if password else b""


                current_node["connections"].append({
                    "server": server,
                    "user": user,
                    "password": decrypt(EncryptionMode.GCM.value, decrypted_password, PasswordEncoding.M_R3_M.value.encode()) if password else None,
                    "keypath": keypath if keypath else None
                })
            elif child.attrib.get("Type") == "Container":
                # Recursively parse subgroups
                child_node: Node = parse_node(child)
                current_node["children"].append(child_node)

        return current_node

    return parse_node(root)

def decrypt(mode: str, data: bytes, password: bytes) -> str:
    if mode == EncryptionMode.CBC.value:
        return cbc_decrypt(data, password)
    if mode == EncryptionMode.GCM.value:
        return gcm_decrypt(data, password)
    raise ValueError(f"Unknown mode {mode}")


def gcm_decrypt(data: bytes, password: bytes) -> str:
    salt: bytes = data[:16]
    nonce: bytes = data[16:32]
    ciphertext: bytes = data[32:-16]
    tag: bytes = data[-16:]
    # TODO: get these values from the config file
    key: bytes = hashlib.pbkdf2_hmac("sha1", password, salt, 1000, dklen=32)  # default values
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    cipher.update(salt)
    try:
        plaintext: str = cipher.decrypt_and_verify(ciphertext, tag).decode()
    except ValueError:
        logging.error("MAC tag not valid, this means the master password is wrong or the crypto values aren't default")
        raise
    return plaintext


def cbc_decrypt(data: bytes, password: bytes) -> str:
    iv: bytes = data[:16]
    ciphertext: bytes = data[16:]
    key: bytes = hashlib.md5(password).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()