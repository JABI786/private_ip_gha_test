#!/usr/bin/env python3
import sys
#import difflib

def print_full_file_contents(file_path):
    with open("../" + file_path, 'r') as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines, start=0):
            print(f"{line_number}    {line}")

if __name__ == "__main__":
    #pr_changed_file_paths = sys.argv[1:-1]  # Last argument is the diff data as a string
    pr_changed_file_paths = sys.argv[1:]
    for file_path in pr_changed_file_paths:
        print(file_path)
        if file_path.endswith(".sls"):
          print_full_file_contents(file_path)
