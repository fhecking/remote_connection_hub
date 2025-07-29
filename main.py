## Global Imports
import tkinter as tk
import logging

# ## Relative Imports
from .view import UseCaseExecutionApp
from .config.logging import configure_logging

def main():
    """
    Main entry point for the application.
    """
    configure_logging()
    logging.info("Starting the Connection Manager application.")

    try:
        root = tk.Tk()
        root.update_idletasks()  # Ensure the window is initialized

        # Get the dimensions of the primary screen
        primary_screen_width = root.winfo_screenwidth()
        primary_screen_height = root.winfo_screenheight()

        # # Optionally, set a maximum size if multi-monitor setup causes issues
        max_width = 1600  # Example: Width of the primary monitor
        max_height = 800  # Example: Height of the primary monitor

        # # Use the smaller of the actual screen size or the max size
        screen_width = min(primary_screen_width, max_width)
        screen_height = min(primary_screen_height, max_height)

        # Set the window size to the primary screen dimensions
        root.geometry(f"{screen_width}x{screen_height}+160+140")

        logging.info("Connection Manager GUI initialized successfully.")
        app = UseCaseExecutionApp(root)
        logging.info("Starting Tkinter main event loop.")
        root.mainloop()
        logging.info("Application closed.")
    except Exception as e:
        logging.error(f"An error occurred in the main application: {e}", exc_info=True)

if __name__ == "__main__":
    main()

