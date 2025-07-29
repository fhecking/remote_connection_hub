# Common Controls Python Project

This project provides tools for accessing and managing remote Linux servers using SSH. It supports both password and RSA key authentication, and can be extended to use PuTTY session data on Windows.

---

## Folder Structure

```
common_controls/
├── alias_utils.py
├── exe_utils.py
├── main.py
├── output.txt
├── putty_utils.py
├── README.md
├── server_utils.py
├── server.txt
├── <potential_rsa>
├── ssh_utils.py
└── __pycache__/
```

---

## Main Features

- **Read server connection info** from `server.txt` (supports both password and RSA key authentication).
- **Connect to remote servers** via SSH and extract alias/environment configuration sections from `.profile` or `.bash_profile`.
- **Append extracted sections** to a local `output.txt` file, grouped by server.
- **(Planned)**: Support for extracting server info from PuTTY sessions on Windows.

---

## Usage

### 1. Prepare `server.txt`

Each line should be:
```
server;user;password;keypath
```
- `password` or `keypath` can be empty, but at least one must be provided.
- Lines starting with `#` are ignored.

Example:
```
10.20.30.152;my_user;my_password;
10.20.30.152;my_user;;my_file_rsa
```

### 2. Run the Script

```sh
python3 main.py
```

- By default, uses `server.txt` for server info.

#### To (eventually) use PuTTY sessions:

```sh
python3 main.py putty
```
- **Note:** PuTTY session support is not yet implemented. The script will print a message and exit early if this option is used.

---

## Code Overview

- **main.py**: Entry point. Reads server info and processes each server.
- **server_utils.py**: Reads and parses `server.txt`.
- **ssh_utils.py**: Handles SSH/SFTP connection logic.
- **exe_utils.py**: High-level logic for updating profiles and extracting configuration sections.
  - This should be more seen as an example implementation. In case other functionallity is necessary, custom methods can be added in an extra file or as methods into the `exe_utils.py`. Moreover, the newly created functionallity then has to be added into the  `main.py` as a replacment.
- **putty_utils.py**: (Windows only) Reads PuTTY session data from the registry.

---

## Extending

- To add PuTTY session support, implement the logic in `main.py` where indicated.

---

## Requirements

The scripts have been developed to use on a linux enviornment, mainly WSL (Windows-Subsystem für Linux). It should be possible to also execute it on Windows, but will not be described further:

- Python 3.x
- Execute the `prepare.sh`
  - sets up the virtual environemnt
  - `paramiko` (install with `pip install paramiko`)
- (Optional, Windows only) `winreg` is built-in for PuTTY session support.

---
