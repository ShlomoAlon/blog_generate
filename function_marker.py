def function_marker():
    pass


if __name__ == '__main__':
    new_file = """from __future__ import annotations
from typing import *\n\n\n"""
    with open('parse_page.py', 'r') as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines):
            if line.strip().startswith('function_marker'):
                current_line = line_number + 1
                while True:
                    new_file += lines[current_line].strip().replace("exec_", "")
                    if lines[current_line].strip().endswith(':'):
                        break
                    current_line += 1
                new_file += '\n    pass\n\n\n'
    with open("functions.py", "w") as f:
        f.write(new_file)