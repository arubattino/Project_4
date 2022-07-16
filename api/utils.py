from ast import Return
import os
import hashlib


def allowed_file(filename):

    '''Function to validate the file extension'''
    
    ALLOWED_EXTENSIONS = {".png",".jpg",".JPG",".JPEG",".jpeg",".gif",".GIF",".PNG"}
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    valid_file = ext in ALLOWED_EXTENSIONS

    return  valid_file


def get_file_hash(file):

    '''Function to return hash + extension as string'''

    hash_file = hashlib.md5(file.read()).hexdigest()
    _, ext = os.path.splitext(file.filename)  
    ext = ext.lower()
    file_new_name = f'{hash_file}{ext}'
    file.seek(0)
   
    return  file_new_name