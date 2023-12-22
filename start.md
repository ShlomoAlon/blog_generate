in this blog post we are going to walk through the process of creating a blog post generator of python heavy code
using python. The goal is to allow you to annotate your python code with markers and have it automatically
generate a blog post in markdown.



for example the above statement looked like this in my python code.
```python
# this indicates that the following string should be rendered as markdown
markdown_string
"""
in this blog post we are going to walk through the process of creating a blog post generator of python heavy code
using python. The goal is to allow you to annotate your python code with markers and have it automatically
generate a blog post in markdown.
"""
```
And this entire section looked like this:
```python
# this starts a code block tagged with the name recursive
# you could of course not use a tag and it would add it to the current section
# I didn't do that here since I want to print the code block after the following markdown string
code_section("babies first code block", skip_blog_stuff=False)
# this indicates that the following string should be rendered as markdown
markdown_string
"""
in this blog post we are going to walk through the process of creating a blog post generator of python heavy code
using python. The goal is to allow you to annotate your python code with markers and have it automatically
generate a blog post in markdown.
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
```
The first challenge is how do we create flags that we can use to indicate that a section of code should be rendered
as markdown. The first idea that comes to mind is to use commentt flags for example # markdown_start and # markdown_end
and # code_start and # code_end. This would work but it would be a bit ugly and you wouldn't be able to pass arguments
to the flags easily. Then I realized that as long as I created dummy functions that took the arguments I wanted to pass
it would be possible to use actual python code as flags. We do this in the following fashion (sadly I had to actually
use regualar markdown for this section since you can't use the flags until you have defined them):
```python
with open(source_file, 'r') as f:
    lines = f.readlines()
    for line_number, line in enumerate(lines):
```
We now strip the indent from the line and check if it starts with one of our functions. If it does we
add exec_ to the beginning and then execute it.

```python
stripped_line = line.strip()
for function_name in ["write_section", "markdown_string", "code_section", "set_current_section"]:
    if stripped_line.startswith(function_name):
        exec('exec_' + self.parse_line(line))
```
exec is a built in python function that executes a string as python code. This is mind blindingly powerful
I wouldn't recommend using it in production code but for this use case it is perfect.

What this means for us is that we don't need to write a parser for our flags. We can just let python
itself do the parsing for us. This is a huge win because parsing is surprisingly hard.

Because exec works on the current scope we define the functions inside the loop. This means
that these functions have access to all current variables.

Here's a code dump of the functions we defined. Don't worry about understanding them right now. We will
go through them in detail later.
```python
from __future__ import annotations
from typing import *


def write_section(section_name: str, target_section_name: str = ''):
    pass


def markdown_string(tag: str = '', keep_indent: bool = False):
    pass


def set_current_section(section_name: str):
    pass


def code_section(section_name: str = '', keep_indent: bool = False, skip_comments: bool = False,skip_blog_stuff=True):
    pass


def end_code(inner_section_name: str = ''):
    pass


```
