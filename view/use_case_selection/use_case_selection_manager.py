import tkinter as tk
from tkinter import ttk
from ...controller.use_case import  UseCase
from ..utils.use_case_execution import confirm_selection

class UseCaseSelectionManager:
    def __init__(self, parent, confirm_callback, back_callback):
        self.parent = parent
        self.confirm_callback = confirm_callback
        self.back_callback = back_callback

        # Variables
        self.connections = []
        self.use_case_var = tk.StringVar()

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Set up the use case execution UI."""
        # Connections display
        self.connections_label = ttk.Label(self.parent, text="Selected Connections:")
        self.connections_label.pack(pady=5)

        self.connections_listbox = tk.Listbox(self.parent, height=10)
        self.connections_listbox.pack(fill="x", padx=10, pady=5)

        # Use case selection
        self.use_case_label = ttk.Label(self.parent, text="Select Use Case:")
        self.use_case_label.pack(pady=5)

        self.use_case_dropdown = ttk.Combobox(
            self.parent,
            textvariable=self.use_case_var,
            state="readonly",
            values=[UseCase.value for UseCase in UseCase],
        )
        self.use_case_dropdown.pack(pady=5)

        # Confirm button
        self.execute_button = ttk.Button(
            self.parent, text="Confirm", command=lambda: confirm_selection(self.connections, self.confirm_callback , self.use_case_var.get())
        )
        self.execute_button.pack(pady=10)

        # Back button
        self.back_button = ttk.Button(
            self.parent, text="Back", command=self.back_callback
        )
        self.back_button.pack(pady=5)

    def set_connections(self, connections):
        """Set the connections to display."""
        self.connections = connections
        self.connections_listbox.delete(0, tk.END)
        for conn in connections:
            self.connections_listbox.insert(tk.END, f"{conn['server']} ({conn['user']})")

