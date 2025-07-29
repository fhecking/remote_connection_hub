from tkinter import ttk, messagebox

from ...controller.use_case import UseCase
from ..components.source_selector import SourceSelector


class UploadFile:
    def __init__(self, parent, connections, execute_callback, back_callback):
        """
        Initialize the UploadFileView.

        :param parent: The parent widget where the view will be placed.
        :param connections: The list of selected connections.
        :param execute_callback: A callback to execute the upload_file use case.
        """
        self.parent = parent
        self.connections = connections
        self.execute_callback = execute_callback
        self.back_callback = back_callback

        # Variables
        self.local_file_path = None
        self.remote_file_path = None

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Set up the upload file view UI."""

        # SourceSelector for file selection
        self.source_selector = SourceSelector(self.parent, self.on_file_selected)

        # Remote path entry
        remote_path_label = ttk.Label(self.parent, text="Remote Path:")
        remote_path_label.pack(pady=5)

        self.remote_path_var = ttk.Entry(self.parent, width=50)
        self.remote_path_var.pack(pady=5)

        # Execute button
        execute_button = ttk.Button(
            self.parent, text="Upload File", command=self.execute_upload_file
        )
        execute_button.pack(pady=10)

        # Back button
        self.back_button = ttk.Button(
            self.parent, text="Back", command=lambda: self.back_callback(self.connections)
        )
        self.back_button.pack(pady=5)

    def on_file_selected(self):
        """Handle file selection from the SourceSelector."""
        self.local_file_path = self.source_selector.get_config_path()

    def execute_upload_file(self):
        """Execute the upload_file use case."""
        self.remote_file_path = self.remote_path_var.get()

        if not self.local_file_path or not self.remote_file_path:
            messagebox.showwarning("Warning", "Please select a file and specify a remote path.")
            return

        try:
        # Pass local_file_path and remote_file_path as keyword arguments
            self.execute_callback(
                self.connections,
                UseCase.upload_file.value,
                local_file_path=self.local_file_path,
                remote_file_path=self.remote_file_path,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")