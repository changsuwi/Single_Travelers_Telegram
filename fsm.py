import os, sys, inspect

cmd_folder = os.path.realpath(
    os.path.dirname(
        os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
from transitions import *
from transitions.extensions import GraphMachine
from IPython.display import Image, display, display_png

class Matter(object):
    def is_valid(self):
        return True
    
    def is_not_valid(self):
        return False
    
    def is_also_valid(self):
        return True
    
    # graph object is created by the machine
    def show_graph(self, **kwargs):
        self.get_graph(**kwargs).draw('state.png', prog='dot')
        display(Image('state.png'))


transitions = [
    { 'trigger': 'search', 'source': 'start', 'dest': 'search_scene' },
    { 'trigger': '@GoGoTest_bot', 'source': 'start', 'dest': 'inline mode' },
    { 'trigger': 'no input', 'source': 'inline mode', 'dest': 'inline_result_by_venue' },
    { 'trigger': 'input text', 'source': 'inline_result_by_venue', 'dest': 'inline_result_by_location' },
    { 'trigger': 'input text', 'source': 'inline mode', 'dest': 'inline_result_by_location' },
    { 'trigger': 'input text', 'source': 'inline_result_by_location', 'dest': 'inline_result_by_location' },
    { 'trigger': 'delete text', 'source': 'inline_result_by_location', 'dest': 'inline_result_by_venue' },
    { 'trigger': 'delete @GoGotest', 'source': 'inline_result_by_venue', 'dest': 'inline mode' },
    { 'trigger': 'search', 'source': 'show_scene', 'dest': 'search_scene' },
    { 'trigger': 'start', 'source': 'show_scene', 'dest': 'start' },
    { 'trigger': 'start', 'source': 'inline mode', 'dest': 'start' },
    { 'trigger': 'start', 'source': 'search_scene', 'dest': 'start' },
    { 'trigger': 'by_coordinate', 'source': 'search_scene', 'dest': 'show_scene'},
    { 'trigger': 'by_location', 'source': 'search_scene', 'dest': 'show_scene'},
    { 'trigger': 'watch_more', 'source': 'show_scene', 'dest': 'show_scene'},
    { 'trigger': 'help', 'source': 'start', 'dest': 'help' }

]
states=['start', 'search_scene', 'show_scene', 'help', 'inline_result_by_location', 'inline_result_by_venue']

model = Matter()
machine = GraphMachine(model=model, 
                       states=states, 
                       transitions=transitions,
                       initial='start',
                       show_auto_transitions=False, # default value is False
                       title="FSM",
                       show_conditions=True)
model.show_graph()