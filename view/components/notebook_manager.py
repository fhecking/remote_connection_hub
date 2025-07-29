from tkinter import ttk
from .connection_listbox import ConnectionListbox

class NotebookManager:
    def __init__(self, parent_frame):
        self.notebook = ttk.Notebook(parent_frame)
        self.notebook.pack(fill="both", expand=True)

    def create_tabs(self, nodes, callback):
        """Create tabs for the given nodes."""
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)

        for node in nodes:
            if not node["children"] and not node["connections"]:
                continue

            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text=node["name"])

            if node["connections"]:
                listbox = ConnectionListbox(tab_frame)
                listbox.populate(node["connections"], callback)

            if node["children"]:
                nested_notebook = NotebookManager(tab_frame)
                nested_notebook.create_tabs(node["children"], callback)