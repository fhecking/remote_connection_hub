import os

def download_profiles(sftp, home_dir, server, user, output_dir, **kwargs):
    """
    Reads .profile and .bash_profile from the remote home directory and writes their contents
    into a local file named user_server.txt.
    """
    print(f"Downloading profiles for {user}@{server} to {output_dir}...")
    profile_files = [f"{home_dir}/.profile", f"{home_dir}/.bash_profile"]
    local_filename = f"{output_dir}/{user}_{server}.txt"
    with open(local_filename, 'w', encoding='utf-8') as local_file:
        for remote_file in profile_files:
            try:
                with sftp.open(remote_file, 'rb') as remote_f:
                    content = remote_f.read().decode('utf-8')
                    local_file.write(f"===== {os.path.basename(remote_file)} =====\n")
                    local_file.write(content)
                    local_file.write("\n\n")
            except FileNotFoundError:
                local_file.write(f"===== {os.path.basename(remote_file)} not found =====\n\n")
    print(f"Profiles saved to {local_filename}")

