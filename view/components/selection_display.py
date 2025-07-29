from tkinter import ttk, Listbox, END, messagebox


class SelectionDisplay:
    def __init__(self, parent):
        self.parent = parent

        # Variables
        self.connections = []  # List of all displayed connections

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Set up the selection display UI."""
        # Label for the connections list
        label = ttk.Label(self.parent, text="Selected Connections:")
        label.pack(anchor="w", padx=10, pady=5)

        # Listbox to display selected connections
        self.listbox = Listbox(self.parent, selectmode="extended", height=10)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # Delete button
        delete_button = ttk.Button(
            self.parent, text="Delete Selected", command=self.delete_selected_connections
        )
        delete_button.pack(pady=5)

    def display_connections(self, connections):
        """
        Display the given connections in the Listbox.

        :param connections: A list of connection dictionaries to display.
        """
        self.connections = connections
        self.listbox.delete(0, END)  # Clear the Listbox

        for conn in connections:
            # Add each connection to the Listbox
            self.listbox.insert(END, f"{conn['server']} ({conn['user']})")

    def delete_selected_connections(self):
        """Delete the selected connections from the Listbox."""
        selected_indices = list(self.listbox.curselection())
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one connection to delete.")
            return

        # Remove the selected connections from the internal list
        selected_indices.reverse()  # Reverse to avoid index shifting when deleting
        for idx in selected_indices:
            del self.connections[idx]

        # Update the Listbox
        self.display_connections(self.connections)

        # Notify the parent manager (optional, if needed)
        return self.connections