from tkinter import ttk, Listbox

class ConnectionListbox:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.listbox.yview)

    def populate(self, connections, callback):
        """Populate the Listbox with connections."""
        for conn in connections:
            self.listbox.insert("end", f"{conn['server']} ({conn['user']})")

        # Bind selection event to callback
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.on_select(event, connections, callback))

    def on_select(self, event, connections, callback):
        """Handle selection and call the callback."""
        selected_indices = self.listbox.curselection()

        for idx in selected_indices:
            callback(connections[idx])