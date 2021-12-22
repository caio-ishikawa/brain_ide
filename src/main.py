from prompt_toolkit import prompt, PromptSession
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
import keyboard

global idx 
global output_pane_size
idx = 0
output_pane_size = 20

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

def run_debug(n):
    code_input = text_buffer.text
    parsed_code = interpy.parse(code_input)
    global idx
    idx += 1
    (compiler_output, memory) = interpy.compile(parsed_code[0:idx])
    output_buffer.text = str(memory[0:idx]) 

def clear_buffers(n):
    text_buffer.text = ""
    output_buffer.text = ""

def enlarge_output_pane(n):
    global output_pane_size
    output_pane_size += 1
    Application.invalidate()
    print(output_pane_size)

# Exits IDE #
def exit(n):
    get_app().exit();

# Declaring content #
text_buffer = Buffer()
output_buffer = Buffer()
button = Button("Run", handler=run_code)
text_area = BufferControl(buffer=output_buffer)

