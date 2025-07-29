from tkinter import ttk, filedialog
from ...controller.connection_loader import ConnectionType


class SourceSelector:
    def __init__(self, parent, load_callback):
        self.parent = parent
        self.load_callback = load_callback

        # Variables
        self.source_var = None
        self.path_var = None

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Create the source selection UI."""
        # Source selection
        source_label = ttk.Label(self.parent, text="Select Source:")
        source_label.pack(pady=5)

        self.source_var = ttk.Combobox(
            self.parent, values=[connType.value for connType in ConnectionType], state="readonly"
        )
        self.source_var.pack(pady=5)

        # Path selection
        path_label = ttk.Label(self.parent, text="Path to File:")
        path_label.pack(pady=5)

        self.path_var = ttk.Entry(self.parent, width=50)
        self.path_var.pack(pady=5)

        browse_button = ttk.Button(
            self.parent, text="Browse", command=self.browse_path
        )
        browse_button.pack(pady=5)

        load_button = ttk.Button(
            self.parent, text="Load File", command=self.load_callback
        )
        load_button.pack(pady=5)

    def browse_path(self):
        """Open a file dialog to select the config path."""
        selected_path = filedialog.askopenfilename(title="Select File")
        if selected_path:
            self.path_var.delete(0, "end")
            self.path_var.insert(0, selected_path)

    def get_selected_source(self):
        """Return the selected source."""
        return self.source_var.get()

    def get_config_path(self):
        """Return the entered configuration path."""
        return self.path_var.get()