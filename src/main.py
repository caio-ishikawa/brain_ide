from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import Application
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import NumberedMargin
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.bindings.page_navigation import scroll_page_up, scroll_page_down
import interpy
import time

global output_height
output_height = 20
# Gets code from text buffer, parses it with interpy, sets the start time of the function, compiles with interpy, sets end time of the function and joins the output of the code with the elapsed time (end time - start time) #
def run_code(n):
    code_input = text_buffer.text
    parsed_code = interpy.parse(code_input)
    compile_start_time = time.time()
    (compiler_output, memory) = interpy.compile(parsed_code)
    compile_end_time = time.time()
    elapsed_time = str(compile_end_time - compile_start_time)
    output = compiler_output + "\n\n" + "Elapsed time: " + elapsed_time
    output_buffer.text = output

## not working
def increase_output_height(n):
    global output_height 
    output_height += 1
    return output_height

def focus_down(n):
    w = n.app.layout.current_window
    n.app.layout.focus(w)

# Exits IDE #
def exit(n):
    get_app().exit();



# Declaring content #
text_buffer = Buffer()
output_buffer = Buffer()
button = Button("Run", handler=run_code)
text_area = BufferControl(buffer=output_buffer)

# Initializing content in window #
root_container = HSplit([
    Window(content=BufferControl(text_buffer), wrap_lines=True, style="bg:#2F3248", left_margins=[NumberedMargin()]),
    Window(height=1, char="-"),
    Window(content=text_area, height=output_height,  style="bg:#2F3248")
])

# KEYBINDS #
key_binds = KeyBindings()
key_binds.add("c-r")(run_code)
key_binds.add("c-q")(exit)
key_binds.add("c-j")(focus_down)

# LAYOUT #
layout = Layout(root_container)
# APP INIT #
application = Application(layout=layout, key_bindings=key_binds, full_screen=True, mouse_support=True)
application.run()
