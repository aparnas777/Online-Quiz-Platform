import streamlit as st

class Pageloader:
    def __init__(self):
        pass

    def load_component(self, component_file):
        with open(component_file, 'r') as file:
            code = file.read()
        exec(code, globals())
