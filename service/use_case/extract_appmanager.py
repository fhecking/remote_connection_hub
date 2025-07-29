import os

def extract_appmanager_section(sftp, home_dir, server, user, output_dir, **kwargs):
    """
    Extracts all lines after the AppManager marker from a remote file.
    Returns the extracted lines as a list of strings.
    """
    marker = (
#        "#-------------------------------------\n"
        "# AppManager fuer Interaktion mit Applikationsprozessen\n"
#        "#-------------------------------------\n"
    )

    profile_files = [f"{home_dir}/.profile", f"{home_dir}/.bash_profile"]
    profile_file = None
    for pf in profile_files:
        try:
            sftp.stat(pf)
            profile_file = pf
            break
        except FileNotFoundError:
            continue
    if not profile_file:
        print(f"  No .profile or .bash_profile found for {user}@{server}, skipping.")
        return

    with sftp.open(profile_file, 'rb') as f:
        content = f.read().decode('utf-8')
    idx = content.find(marker)
    if idx == -1:
        lines = []
    # Get all lines after the marker
    after_marker = content[idx + len(marker):]
    lines = after_marker.splitlines(keepends=True)
    save_lines_to_local_file(lines, "output.txt", f"{user}@{server}")



def save_lines_to_local_file(lines, local_file_path, server_header):
    """
    Appends the given lines to a local file, prepending a header if the file is empty.
    """
    file_exists = os.path.exists(local_file_path)
    write_mode = 'a' if file_exists else 'w'
    with open(local_file_path, write_mode, encoding='utf-8') as f:
        if not file_exists or os.stat(local_file_path).st_size == 0:
            f.write(f"# {server_header}\n")
        
        f.write(f"\n\n# {server_header}\n")
        f.writelines(lines)
