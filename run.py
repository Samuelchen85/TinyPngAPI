################################################################
# Python script for compressing images (png/jpg) in a directory
# The compression will make change in place or you can specify a
# a destination dir to store all the compressed images
#
# Usage: python run.py src_dir [dest_dir]
# 
# I wrote this script for my Android project, feel free to use or
# modify this script, but I am NOT responsible for any damages/loss
# caused by using/modifying this script. 
#
# Author: Samuel Chen (ustccmchen@gmail.com)
# Date 06-01-2016
#
#################################################################

# System modules
import sys
import logging
import os

# Tinypng module
import tinify

# Constants
HELP_MSG = "Usage: python run.py src_dir (image source dir) dest_dir (optional)\n       python run.py web_url dest_file_name(optional)"

def check_file_format(file_name):
    file_name = file_name.lower()
    if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg'):
        return True
    else:
        return False

def init_tinify():
    try:
        # Constants, get your own API key from https://tinypng.com/developers/subscription
        tinify.key = os.environ['TINYPNG_API_KEY']
        tinify.validate
    except Exception as e:
        logging.error(e.message)
        pass

def compress_local_file(src_file, dest_file):
    try:
        source = tinify.from_file(src_file)
        source.to_file(dest_file)
    except Exception as e:
        logging.exception(e.message)

def compress_web_image(src_url, dest_file):
    try:
        source = tinify.from_url(src_url)
        source.to_file(dest_file)
    except Exception as e:
        logging.exception(e.message)

def main():
    logging.getLogger().setLevel(logging.INFO)
    init_tinify()
    if len(sys.argv)>3 or len(sys.argv)<2:
        print HELP_MSG
        exit(1)
    else:
        counter = 1
        src_dir = sys.argv[1]
        if src_dir.startswith('http'):
            dest_file = 'web_img.png'
            if len(sys.argv) == 3:
                dest_file = sys.argv[2]
            compress_web_image(src_dir, dest_file)
        else:
            dest_dir = sys.argv[2] if len(sys.argv)==3 else src_dir
            for file in os.listdir(src_dir):
                if check_file_format(file):
                    logging.info('[%d] Compressing file: %s', counter, file)
                    src_file = src_dir + os.sep + file
                    dest_file = src_dir + os.sep + file
                    if dest_dir:
                        dest_file = dest_dir + os.sep + file
                    compress_local_file(src_file, dest_file)
    try:
        quota_left_monthly = tinify.compression_count
        logging.info('\nYou can still compress %s images this month', quota_left_monthly)
    except Exception as e:
        logging.error(e.message)

if __name__ == '__main__':
    main()

