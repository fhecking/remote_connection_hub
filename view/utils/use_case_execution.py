import logging
from tkinter import messagebox

def confirm_selection(selected_connections, confirm_callback, use_case=None):
    """Confirm the selected connections and move to the next frame."""
    if not selected_connections:
        messagebox.showwarning("Warning", "Please select at least one connection.")
        return
        
    connections_str = ", ".join([conn["server"] for conn in selected_connections])

    logging.info(f"Confirmed selected connections: {connections_str}")

    if use_case:
        logging.info(f"Use case selected: {use_case}")
        confirm_callback(selected_connections, use_case)
    else:
        logging.info("No use case selected, proceeding with confirmation.")
        confirm_callback(selected_connections)

