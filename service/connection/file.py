def read_connection_file(filename):
    """
    Reads server info from a file.
    Each line should be: server;user;password;keypath
    password or keypath can be empty, but at least one must be provided.
    Lines starting with # or empty lines are skipped.
    Returns a list of dicts: {'server': ..., 'user': ..., 'password': ..., 'keypath': ...}
    """
    servers = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(';')
            # Ensure at least 4 fields
            while len(parts) < 4:
                parts.append('')
            server, user, password, keypath = parts[:4]
            servers.append({
                'server': server,
                'user': user,
                'password': password if password else None,
                'keypath': keypath if keypath else None
            })
    return servers