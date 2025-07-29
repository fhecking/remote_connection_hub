def clean_profile(sftp, home_dir, server, user, **kwargs):
    profile_files = [f"{home_dir}/.profile", f"{home_dir}/.bash_profile"]
    profile_file = None

    marker = (
        ". $PROJDISC/etc/profile.general"
    )

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

    with sftp.open(profile_file, 'r') as f:
        lines = f.readlines()

    cleaned_lines = []
    found_marker = False
    for line in lines:
        cleaned_lines.append(line)
        if marker in line:
            found_marker = True
            break

    if found_marker:
        with sftp.open(profile_file, 'w') as f:
            f.writelines(cleaned_lines)
        print(f"  Cleaned {profile_file} on {server}: removed lines below marker.")
    else:
        print(f"  Marker not found in {profile_file} on {server}, no changes made.")