import logging
from tkinter import ttk, messagebox
from ...controller.connection_loader import load_connections
from ..components.source_selector import SourceSelector
from .tab_display import TabDisplay
from ..components.selection_display import SelectionDisplay
from ..utils.use_case_execution import confirm_selection


class ConnectionSelectionManager:
    def __init__(self, parent, confirm_callback):
        self.parent = parent
        self.confirm_callback = confirm_callback

        # Variables
        self.selected_connections = []

        # Components
        self.source_selector = None
        self.tab_display = None
        self.selection_display = None

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Set up the connection selection UI."""
        # Source selection
        self.source_selector = SourceSelector(self.parent, self.load_connections)

        # Connections display (TabDisplay)
        self.connections_frame = ttk.Frame(self.parent)
        self.connections_frame.pack(fill="both", expand=True, pady=5)
        self.tab_display = TabDisplay(self.connections_frame)


        # Selection display
        self.selection_display = SelectionDisplay(self.parent)

        # Confirm button
        self.confirm_button = ttk.Button(
            self.parent, text="Confirm Selection", command=lambda: confirm_selection(self.selected_connections, self.confirm_callback)
        )
        self.confirm_button.pack(pady=10)



    def load_connections(self):
        """Load connections and display them in tabs."""
        # Delegate to SourceSelector to get the selected source and config path
        source = self.source_selector.get_selected_source()
        config_path = self.source_selector.get_config_path()

        if not config_path:
            messagebox.showwarning("Warning", "Please select a valid config path.")
            return

        try:
            # Load connections using the selected source and config path
            tree = load_connections(source, config_path)

            # Transfer the data to TabDisplay to display the connections
            self.tab_display.display_connections(tree, self.add_connection_to_selection)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load connections: {e}")

    def add_connection_to_selection(self, connection):
        """Add a connection to the selected connections list."""
        if connection not in self.selected_connections:
            self.selected_connections.append(connection)
            self.selection_display.display_connections(self.selected_connections)

    def delete_connection_from_selection(self, connection):
        """Remove a connection from the selected connections list."""
        if connection in self.selected_connections:
            self.selected_connections.remove(connection)
            self.selection_display.display_connections(self.selected_connections)

    # def confirm_selection(self):
    #     """Confirm the selected connections and move to the next frame."""
    #     if not self.selected_connections:
    #         messagebox.showwarning("Warning", "Please select at least one connection.")
    #         return
        
    #     connections_str = ", ".join([conn["server"] for conn in self.selected_connections])

    #     logging.info(f"Confirmed selected connections: {connections_str}")

    #     self.confirm_callback(self.selected_connections)