# #!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import argparse
import glob
import logging
import os
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

J2_TEMPLATE_KEY = "zlRsBVKqG0Q8jbh9rceXfF9NhUyX1gkouTKaCuUvSv8="

def gen_key(key_name):
    key = Fernet.generate_key()
    with open(f"{key_name}.key", "wb") as filekey:
        filekey.write(key)
    print(f"{key_name}: {str(key)}")
    

def encrypt_file(dir, file_name, output_dir):
    fernet = Fernet(J2_TEMPLATE_KEY)

    if dir:
        file_path = os.path.join(dir, file_name)
    else:
        file_path = file_name
        file_name = file_path.replace("\\","/").split("/")[-1]

    with open(file_path, "rb") as file:
        original = file.read()
        
    encrypted = fernet.encrypt(original)

    output_file_path = os.path.join(output_dir, f"{file_name}.encrypted")
    with open(output_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def encrypt_files(dir, output_dir):
    print("")
    for file_path in glob.glob(dir, recursive=True):
        print(f"encrypting {file_path}")
        encrypt_file(None, file_path, output_dir)


def read_encrypted_file(encrypted_file_path):
    fernet = Fernet(J2_TEMPLATE_KEY)
    
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    
    return fernet.decrypt(encrypted).decode("utf-8")


def encrypt_str(str_to_encrypt):
    fernet = Fernet(J2_TEMPLATE_KEY)
    return fernet.encrypt(str_to_encrypt)


if __name__ == "__main__":
    # --action gen_key --key_name value
    # --action encrypt_file --key_name value --dir value --file_name value
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--key_name')
    parser.add_argument('--dir')
    parser.add_argument('--file_name')
    parser.add_argument('--file_path')

    args = parser.parse_args()
    OUTPUT_DIR = "./temp/tf/templates"

    if args.action == "gen_key":
        gen_key(args.key_name)
    elif args.action == "encrypt_file":
        encrypt_file(args.dir, args.file_name, OUTPUT_DIR)
    elif args.action == "encrypt_files":
        encrypt_files(args.dir, OUTPUT_DIR)
    elif args.action == "read_encrypted_file":
        contents = read_encrypted_file(args.file_path)
        print(contents)
