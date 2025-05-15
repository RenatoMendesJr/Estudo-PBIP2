import os

def check_file_exists(file_path):
    return os.path.isfile(file_path)

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)