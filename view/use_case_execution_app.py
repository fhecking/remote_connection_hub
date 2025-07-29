import logging
from tkinter import ttk

from remote_connection_hub.view.use_case_execution.execute_file import ExecuteFile
from .connection_selection.connection_selection_manager import ConnectionSelectionManager
from .use_case_selection.use_case_selection_manager import UseCaseSelectionManager
from .use_case_execution.upload_file import UploadFile
from ..controller.use_case import UseCase, execute_use_case

class UseCaseExecutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Use Case Execution App")

        # Initialize frames
        self.connection_selection_frame = ttk.Frame(self.root)
        self.use_case_execution_frame = ttk.Frame(self.root)
        self.upload_file_frame = ttk.Frame(self.root)
        self.execute_file_frame = ttk.Frame(self.root)

        # Initialize managers
        self.connection_selection_manager = ConnectionSelectionManager(
            self.connection_selection_frame, self.move_to_use_case_execution
        )
        self.use_case_execution_manager = UseCaseSelectionManager(
            self.use_case_execution_frame, self.move_to_use_case_view, self.move_to_connection_selection
        )

        # Views to determine based on use case selection
        self.upload_file_view = None
        self.execute_file_view = None

        # Start with the connection selection frame
        self.connection_selection_frame.pack(fill="both", expand=True)

    def move_to_use_case_execution(self, selected_connections):
        """Switch to the use case execution frame."""
        logging.info("Moving to Use Case Execution with selected connections.")
        self.connection_selection_frame.pack_forget()
        self.upload_file_frame.pack_forget()
        self.execute_file_frame.pack_forget()


        self.use_case_execution_manager.set_connections(selected_connections)
        self.use_case_execution_frame.pack(fill="both", expand=True)

    def move_to_connection_selection(self):
        """Switch back to the connection selection frame."""
        logging.info("Moving back to Connection Selection.")
        self.use_case_execution_frame.pack_forget()
        self.connection_selection_frame.pack(fill="both", expand=True)
        self.move_to_upload_file_view([])  # Reset upload file view

    def move_to_upload_file_view(self, selected_connections):
        """Switch to the upload_file view."""
        logging.info("Moving to Upload File View.")
        self.connection_selection_frame.pack_forget()
        self.use_case_execution_frame.pack_forget()

        # Initialize the upload_file view if not already done
        if not self.upload_file_view:
            self.upload_file_view = UploadFile(
                self.upload_file_frame, selected_connections, self.execute_use_case
            )
        self.upload_file_frame.pack(fill="both", expand=True)

    def move_to_use_case_view(self, connections, use_case):
        logging.info(f"Moving to {use_case}.")
        self.connection_selection_frame.pack_forget()
        self.use_case_execution_frame.pack_forget()

        if use_case == UseCase.upload_file.value:
            if not self.upload_file_view:
                self.upload_file_view = UploadFile(
                    self.upload_file_frame, connections, self.execute_use_case, self.move_to_use_case_execution
                )
            self.upload_file_frame.pack(fill="both", expand=True)
        elif use_case == UseCase.execute_file.value:
            # Initialize the ExecuteFile view here if needed
            self.execute_file_view = ExecuteFile(
                self.execute_file_frame, connections, self.execute_use_case, self.move_to_use_case_execution
            )

            self.execute_file_frame.pack(fill="both", expand=True)


    def execute_use_case(self, connections, use_case, **kwargs):
        """Execute the use case."""

        try:
            for connection in connections:
                logging.info(f"Executing use case {use_case} on connection {connection['server']} ({connection['user']})")
                execute_use_case(
                    use_case, #UseCase.upload_file.value,
                    connection,
                    **kwargs
                )
        except Exception as e:
            logging.error(f"Failed to upload file: {e}")