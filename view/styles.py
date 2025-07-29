from tkinter import ttk

def apply_styles():
    """Apply custom styles to the application."""
    style = ttk.Style()
    style.configure("Custom.TNotebook", padding=5)
    style.configure("Custom.TFrame", background="white")
    style.configure("Custom.TLabel", font=("Arial", 10))