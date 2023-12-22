from __future__ import annotations

from function_marker import function_marker
from functions import *


class MarkDownSection:
    sections: List[Union[str, MarkDownSection]]
    header_level: int = 0
    table_of_contents: bool = False
    name: str

    def __init__(self, name: str, header_level: int = 0, table_of_contents: bool = False):
        self.sections = []
        self.header_level = header_level
        self.table_of_contents = table_of_contents
        self.name = name
        if table_of_contents and header_level == 0:
            self.header_level = 3

    def set_table_of_contents(self, table_of_contents: bool):
        if table_of_contents:
            self.table_of_contents = True
            if self.header_level == 0:
                self.header_level = 3

    def set_header_level(self, header_level: int):
        if header_level != 0:
            self.header_level = header_level

    def add_section(self, section: Union[str, MarkDownSection]):
        self.sections.append(section)

    def markdown(self) -> str:
        result = ''
        if self.table_of_contents:
            assert self.header_level != 0, 'if table of contents is true the header level must be set'
            result += "<a id='" + self.name.replace(' ', '-') + "'></a>\n"

        if self.header_level != 0:
            result += '#' * self.header_level + ' ' + self.name + '\n'
        result += ''.join(
            [section.markdown() if isinstance(section, MarkDownSection) else section for section in self.sections])
        return result

    def markdown_table_of_contents(self) -> str:
        result = ''
        temp_list = [section.markdown_table_of_contents() for section in self.sections if \
                     isinstance(section, MarkDownSection) and section.table_of_contents]
        if self.table_of_contents:
            result += f"- [{self.name}](#{self.name.replace(' ', '-')})\n"
            result += '\n    '
            result += '\n    '.join(temp_list)
        else:
            result += '\n'.join(temp_list)
        return result


class Reader:
    current_section: str
    sections: dict[str, MarkDownSection]

    def __init__(self):
        self.current_section = "default"
        self.sections = {self.current_section: MarkDownSection("default")}

    def add_python_file(self, file_name: str, section_name: str):
        s = "```python\n"
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                s += line
        s += "```\n"
        self.get_section(section_name).add_section(s)

    def change_section(self, section_name: str):
        if section_name not in self.sections:
            self.sections[section_name] = MarkDownSection(section_name)
        self.current_section = section_name

    def get_section(self, section_name: str) -> MarkDownSection:
        """
        if section_name is empty we return the current section, otherwise we return the section with the given name
        if it doesn't exist, we create it
        """
        if section_name == '':
            return self.get_current_section()
        elif section_name in self.sections:
            return self.sections[section_name]
        else:
            section = MarkDownSection(section_name)
            self.sections[section_name] = section
            return section

    def write_section_to_file(self, section_name: str = '', file_name: str = '', table_of_contents: bool = True):

        if section_name == '':
            section_name = self.current_section
        if file_name == '':
            file_name = section_name + '.md'
        if section_name not in self.sections:
            raise Exception("section not found")
        with open(file_name, 'w') as f:
            if table_of_contents:
                f.write("# Table of Contents\n")
                f.write(self.sections[section_name].markdown_table_of_contents())
                f.write("\n\n")
            f.write(self.sections[section_name].markdown())

    def get_current_section(self) -> MarkDownSection:
        return self.sections[self.current_section]

    markdown_string("parse_line")
    """
    We still need to parse the line before we run it. Sometimes there won't be any parentheses on the flags and 
    we need to add them. Sometimes there will be some free whitespace and we need to strip it. The following 
    function does that.
    """
    code_section("parse_line")

    def parse_line(self, line: str) -> str:
        if ")" in line:
            return line.strip()
        else:
            return line.strip() + "()"

    end_code("parse_line")

    set_current_section("reading_code")

    def write_section(self, section_name: str, target_section_name: str = ''):

        if target_section_name == '':
            self.get_current_section().add_section(self.get_section(section_name))
        else:
            self.get_section(target_section_name).add_section(self.get_section(section_name))

    def read_code(self, source_file: str):
        function_names = ["write_section", "markdown_string", "code_section", "end_code"]
        code_section
        with (open(source_file, 'r') as f):
            lines = f.readlines()
            for line_number, line in enumerate(lines):
                end_code
                function_marker

                def exec_write_section(section_name: str, target_section_name: str = ''):
                    self.write_section(section_name, target_section_name)
                    # if target_section_name == '':
                    #     self.get_current_section().add_section(self.get_section(section_name))
                    # else:
                    #     self.get_section(target_section_name).add_section(self.get_section(section_name))

                function_marker

                def exec_markdown_string(tag: str = '', keep_indent: bool = False, header_level: int = 0,
                                         table_of_contents: bool = False):
                    section = self.get_section(tag)
                    if tag == '':
                        assert header_level == 0 and table_of_contents is False, \
                            'if the tag is empty the header level must be 0 and table of contents must be false'
                    section.set_header_level(header_level)
                    section.set_table_of_contents(table_of_contents)


                    s = ''
                    indent = line.index('markdown_string')
                    assert 'markdown_string' in line, 'this line should have markdown_string in it'
                    assert '"""' in lines[line_number + 1], 'markdown_string must be followed by a """'
                    for new_line in lines[line_number + 2:]:
                        if '"""' in new_line:
                            section.add_section(s)
                            return
                        if keep_indent or new_line == '\n':
                            s += new_line
                        else:
                            s += new_line[indent:]
                    assert False, 'markdown_string must be followed by a """'

                function_marker

                def exec_set_current_section(section_name: str, header_level: int = 0, table_of_contents: bool = False):
                    self.change_section(section_name)
                    self.get_current_section().set_header_level(header_level)
                    self.get_current_section().set_table_of_contents(table_of_contents)

                function_marker

                def exec_code_section(section_name: str = '', keep_indent: bool = False, skip_comments: bool = False,
                                      skip_blog_stuff=True):
                    should_end = [False]

                    function_marker

                    def end_code(inner_section_name: str = ''):
                        if inner_section_name == section_name:
                            should_end[0] = True

                    indent = line.index('code_section')
                    assert 'code_section' in line, 'this line should have code_section in it'
                    section = self.get_section(section_name)
                    s = ''
                    s += "```python\n"
                    for new_line in lines[line_number + 1:]:
                        if new_line.strip().startswith('end_code'):
                            parsed_line = self.parse_line(new_line)
                            exec(parsed_line)
                            # exec(self.parse_line(new_line))
                            if should_end[0]:
                                s += "```\n"
                                section.add_section(s)
                                return
                        should_continue = False
                        for function_name in function_names:
                            if new_line.strip().startswith(function_name):
                                should_continue = True
                        if should_continue and skip_blog_stuff:
                            continue
                        if skip_comments and new_line.strip().startswith('#'):
                            continue

                        if keep_indent or new_line == '\n':
                            s += new_line
                        else:
                            s += new_line[indent:]
                    assert False, 'code_section must be followed by an end_code_section with matching section name'

                markdown_string
                """
                We now strip the indent from the line and check if it starts with one of our functions. If it does we
                add exec_ to the beginning and then execute it.
                
                """
                code_section
                stripped_line = line.strip()
                for function_name in ["write_section", "markdown_string", "code_section", "set_current_section"]:
                    if stripped_line.startswith(function_name):
                        exec('exec_' + self.parse_line(line))
                end_code
                markdown_string
                """
                exec is a built in python function that executes a string as python code. This is mind blindingly powerful
                I wouldn't recommend using it in production code but for this use case it is perfect.
                
                What this means for us is that we don't need to write a parser for our flags. We can just let python
                itself do the parsing for us. This is a huge win because parsing is surprisingly hard.
                
                Because exec works on the current scope we define the functions inside the loop. This means
                that these functions have access to all current variables.
                
                Here's a code dump of the functions we defined. Don't worry about understanding them right now. We will
                go through them in detail later.
                """


# def strip_indent(line: str, num_indents: int):
#     return line[num_indents*4:]


#
# def read_function_as_main(func):
#     source = inspect.getsource(func)
#     lines = source.split('\n')[1:]
#     for i in lines:
#         print(strip_indent(i, 1))
#     # source = source.replace('if __name__ == \'__main__\':', 'def main():')
#     # source += '\n\nmain()'
#     # exec(source)


if __name__ == '__main__':
    pass
    set_current_section("start", header_level=1, table_of_contents=True)
    code_section("recursive_1", skip_comments=True)
    code_section("recursive_2", skip_blog_stuff=False)
    # This starts a code block tagged with the name "babies first code block".
    # If you did not use a tag, it would add it to the current section.
    # I didn't do that here since I want to print the code block after the following markdown string
    code_section("babies first code block", skip_blog_stuff=False)
    # this indicates that the following string should be rendered as markdown
    markdown_string
    """
    in this blog post we are going to walk through the process of creating a markdown generator of python heavy code
    using python. The goal is to allow you to annotate your python code with markers and have it automatically
    generate markdown in the specified way. I was trying to write a different blog post and I realized that I couldn't
    find the tool I wanted to generate my blog post from within python code. So I decided to write it myself. 
    
    I then realized that this tool was far more interesting than the blog post I was trying to write. So here we are.
    Writing a blog post about how to write a blog post generator from within said blog post generator. (Very meta :))
    """
    end_code("babies first code block")
    markdown_string
    """

    for example the above statement looked like this in my python code.
    """
    # this writes the previous code block to the current section
    write_section("babies first code block")
    markdown_string
    """
    And this entire section looked like this:
    """
    end_code("recursive_2")
    end_code("recursive_1")
    write_section("recursive_2")

    markdown_string
    """
    The first challenge is how do we create flags that we can use to indicate that a section of code
    should be rendered as markdown. 
    The first idea that comes to mind is to use comment flags for example # markdown_start and # markdown_end
    and # code_start and # code_end.
    This would work but it would be a bit ugly and you wouldn't be able to easily pass arguments
    to the flags easily. 
    Then it hit me, if I created dummy functions that took the arguments I wanted to pass it would be possible
    to use actual python code as flags and get all of python's auto complete functionality.
    We do this in the following fashion. Note: this is in another file.
    """
    write_section('defined_functions')
    markdown_string("Warning", table_of_contents=True)
    """
    These functions do not do anything. They are just dummy functions that the user can use as flags. Since we don't
    want these flags to affect the code we are writing. These flags only become active when we are generating the
    markdown (which for the sake of your sanity should be done in a different file).
    
    The next challenge is actually reading the code.
    """
    write_section("Warning")
    write_section("reading_code")
