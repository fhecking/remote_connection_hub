from tkinter import messagebox, ttk
from ..components.notebook_manager import NotebookManager

from tkinter import messagebox, ttk
from ..components.notebook_manager import NotebookManager


class TabDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.notebook_manager = None
        self.setup_ui()

    def setup_ui(self):
        """Create the tab display UI."""
        # Use self.parent directly instead of self.parent.root
        frame = ttk.Frame(self.parent)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.notebook_manager = NotebookManager(frame)

    def display_connections(self, tree, callback):
        """Display connections in the notebook."""
        if not tree or "children" not in tree:
            messagebox.showerror("Error", "Invalid tree structure or no connections found.")
            return

        self.notebook_manager.create_tabs(tree["children"], callback)