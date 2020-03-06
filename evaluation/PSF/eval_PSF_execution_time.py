def get_file_names_in_a_directory(dir):
    import os
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return sorted(files)


