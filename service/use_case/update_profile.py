from common_controls.use_case.update_profile_utils.alias_utils import get_existing_aliases, get_missing_aliases, ALIAS_DEFS


def update_profile(sftp, home_dir, server, user, output_dir, **kwargs):
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

    with sftp.open(profile_file, 'r') as f:
        lines = f.readlines()


    try:
        # print(f"  Adding aliases to {profile_file} on {server}: {', '.join([a.split()[1].split('=')[0] for a in to_add])}")
        with sftp.open(profile_file, 'a') as f:
            for line in ALIAS_DEFS:
                f.write(line + '\n')
        print(f"  Appended ALIAS_DEFS to {profile_file} on {server}.")
    except Exception as e:
        print(f"  Failed to append ALIAS_DEFS to {profile_file} on {server}: {e}")




