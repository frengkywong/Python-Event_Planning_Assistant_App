# ============================================================================
# Import necessary libraries
# ============================================================================
import tkinter as tk
from tkinter import messagebox

# Import the three GUI classes from your other files
from guest_list_manager import GuestListManagerApp
from task_checklist import TaskChecklistApp
from countdown_timer import CountdownTimerApp


# ============================================================================
# Main Application Class
# ============================================================================

class EventPlanningApp:
    """Main GUI application for Event Planning Assistant."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✨ Event Planning Assistant")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a2e") # Use the same dark background
        self.root.resizable(True, True)
        
        # Center window on screen
        self._center_window()
        
        self._setup_main_menu()

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = 900
        height = 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _setup_main_menu(self):
        """Setup the main menu interface."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # --- Main Container ---
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Header Section ---
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill=tk.X, pady=(0, 40))
        
        # Title
        title_label = tk.Label(header_frame, text="🎉 Event Planning Assistant", 
                               font=("Segoe UI", 24, "bold"), bg="#1a1a2e",
                               fg="#00d9ff")
        title_label.pack(pady=70,fill=tk.X)
        
        # --- Menu Options ---
        menu_frame = tk.Frame(main_frame, bg="#1a1a2e")
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu buttons
        button_style = {
            "font": ("Segoe UI", 14, "bold"),
            "width": 30,
            "height": 2,
            "bg": "#16213e",
            "fg": "#ffffff",
            "relief": tk.RAISED,
            "cursor": "hand2"
        }
        
        # Button 1: Guest List Manager
        # The GuestListManagerGUI class needs a 'back_callback' function.
        # We provide 'self._setup_main_menu' as that function.
        btn1 = tk.Button(
            menu_frame,
            text="👥 Guest List Manager",
            # --- SIMPLIFIED CALL ---
            command=self._show_guest_list_manager, 
            **button_style
        )
        btn1.pack(pady=10)
        
        # Button 2: Task Checklist
        btn2 = tk.Button(
            menu_frame,
            text="📋 Task Checklist",
            command=self._show_task_checklist,
            **button_style
        )
        btn2.pack(pady=10)
        
        # Button 3: Countdown Timer
        btn3 = tk.Button(
            menu_frame,
            text="⏰ Countdown Timer",
            command=self._show_countdown_timer,
            **button_style
        )
        btn3.pack(pady=10)
        
        # Button 4: Exit
        btn4 = tk.Button(
            menu_frame,
            text="🚪 Exit",
            command=self.root.quit,
            **button_style
        )
        btn4.pack(pady=10)

    def _show_guest_list_manager(self):
        """Show Guest List Manager interface."""
        # Clear the main window first
        for widget in self.root.winfo_children():
            widget.destroy()
        # Then show the Guest List Manager
        GuestListManagerApp(self.root, self._setup_main_menu)

    def _show_task_checklist(self):
        """Show Task Checklist interface."""
        # Clear the main window first
        for widget in self.root.winfo_children():
            widget.destroy()
        # Then show the Task Checklist
        TaskChecklistApp(self.root, self._setup_main_menu)

    def _show_countdown_timer(self):
        """Show Countdown Timer interface."""
        # Clear the main window first
        for widget in self.root.winfo_children():
            widget.destroy()
        CountdownTimerApp(self.root, self._setup_main_menu)


# ============================================================================
# Execution: Main program entry point
# ============================================================================

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = EventPlanningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()