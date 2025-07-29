import winreg

def get_putty_sessions():
    """
    Retrieves PuTTY sessions from the Windows registry.
    Returns a list of dictionaries, each containing session name, host, user, and keyfile.
    """
    
    sessions = []
    # Attempt to read PuTTY sessions from the Windows registry
    # PuTTY stores session information in the registry under HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions
    # Each session is a subkey under this key, with values for HostName, UserName, and PublicKeyFile
    base_key = r"Software\SimonTatham\PuTTY\Sessions"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                session_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, session_name) as session_key:
                    try:
                        host, _ = winreg.QueryValueEx(session_key, "HostName")
                    except FileNotFoundError:
                        host = ""
                    try:
                        user, _ = winreg.QueryValueEx(session_key, "UserName")
                    except FileNotFoundError:
                        user = ""
                    try:
                        keyfile, _ = winreg.QueryValueEx(session_key, "PublicKeyFile")
                    except FileNotFoundError:
                        keyfile = ""
                    sessions.append({
                        "session": session_name,
                        "host": host,
                        "user": user,
                        "keyfile": keyfile
                    })
    except Exception as e:
        print(f"Error reading PuTTY sessions: {e}")
    return sessions
