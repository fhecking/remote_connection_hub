from tkinter import ttk, messagebox
from ...controller.use_case import UseCase

class ExecuteFile:
    def __init__(self, parent, connections, execute_callback, back_callback):
        self.parent = parent
        self.connections = connections
        self.execute_callback = execute_callback,
        self.back_callback = back_callback

        self.remote_path_var = None
        self.remote_exec_cmd = None

        self.setup_ui()



    def setup_ui(self):
        """Set up the execute file view UI."""
        remote_path_label = ttk.Label(self.parent, text="Remote Path:")
        remote_path_label.pack(pady=5)

        self.remote_path_var = ttk.Entry(self.parent, width=50)
        self.remote_path_var.pack(pady=5)

        remote_exec_label = ttk.Label(self.parent, text="Execution Command:")
        remote_exec_label.pack(pady=5)

        self.remote_exec_cmd = ttk.Entry(self.parent, width=50)
        self.remote_exec_cmd.pack(pady=5)

        # Execute button
        execute_button = ttk.Button(
            self.parent, text="Execute Command", command=self.execute_command
        )
        execute_button.pack(pady=10)

        # Back button
        self.back_button = ttk.Button(
            self.parent, text="Back", command=lambda: self.back_callback(self.connections)
        )
        self.back_button.pack(pady=5)


    def execute_command(self):
        """Execute the command on the remote server."""
        remote_path = self.remote_path_var.get()
        remote_command = self.remote_exec_cmd.get()

        if not remote_path or not remote_command:
            messagebox.showwarning("Warning", "Please specify a remote path and command.")
            return

        try:
            # Pass connections, remote_path, and remote_command as keyword arguments
            self.execute_callback(
                self.connections,
                UseCase.upload_file.value,
                remote_path=remote_path,
                remote_command=remote_command
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command: {e}")
