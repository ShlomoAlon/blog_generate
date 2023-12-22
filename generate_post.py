from icecream import ic
from parse_page import Reader

if __name__ == '__main__':
    reader = Reader()
    reader.add_python_file('functions.py', 'defined_functions')
    reader.read_code('parse_page.py')
    reader.change_section("readme")
    reader.write_section("start")
    for section in reader.get_current_section().sections:
        print(section)
    print(reader.get_current_section().markdown())
    print(reader.get_current_section().markdown_table_of_contents())
    reader.write_section_to_file()
    # print(reader.current_section)
    # print(reader.get_section("defined_functions").markdown())
