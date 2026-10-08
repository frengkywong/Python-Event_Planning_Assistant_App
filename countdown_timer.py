# ============================================================================
# Import necessary libraries
# ============================================================================
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from typing import Dict, List

# ============================================================================
# Backend Logic
# ============================================================================

class EventComponent:
    """A base class for event-related components."""
    def __init__(self, event_name: str):
        self.event_name = event_name
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_info(self) -> Dict:
        return {"event_name": self.event_name, "created_date": self.created_date}


class CountdownTimer(EventComponent):
    """Countdown Timer class for displaying days remaining until an event."""
    
    def __init__(self, event_name: str, event_date: str):
        super().__init__(event_name)
        self.event_date = event_date
        self._validate_date()
    
    def _validate_date(self) -> None:
        """Validate the event date format."""
        try:
            datetime.strptime(self.event_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got {self.event_date}")
    
    def calculate_days_remaining(self) -> int:
        """Calculate the number of days remaining until the event."""
        try:
            event_datetime = datetime.strptime(self.event_date, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            event_date_only = event_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            delta = event_date_only - today
            return delta.days
        except Exception as e:
            raise Exception(f"Error calculating days remaining: {str(e)}")
    
    def get_status_message(self) -> str:
        """Get a formatted status message based on days remaining."""
        days = self.calculate_days_remaining()
        
        if days < 0:
            return f"Event '{self.event_name}' has passed {abs(days)} days ago."
        elif days == 0:
            return f"Event '{self.event_name}' is TODAY!"
        elif days == 1:
            return f"Event '{self.event_name}' is TOMORROW!"
        else:
            return f"Event '{self.event_name}' is in {days} days."
    
    def get_info(self) -> Dict:
        """Override base class method to include countdown-specific info."""
        base_info = super().get_info()
        base_info.update({
            "event_date": self.event_date,
            "days_remaining": self.calculate_days_remaining(),
            "status_message": self.get_status_message()
        })
        return base_info


# ============================================================================
# Modern Theme Configuration
# ============================================================================

class ModernTheme:
    """Modern color scheme and styling constants."""
    
    # Color Palette
    BG_DARK = "#1a1a2e"
    BG_MEDIUM = "#16213e"
    BG_LIGHT = "#0f3460"
    
    ACCENT_PRIMARY = "#00d9ff"      # Cyan/Teal
    ACCENT_SECONDARY = "#ff6b6b"    # Coral Red
    ACCENT_TERTIARY = "#a855f7"     # Purple
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_MUTED = "#6b7280"
    
    SUCCESS = "#10b981"             # Green
    WARNING = "#f59e0b"             # Orange
    ERROR = "#ef4444"               # Red
    
    # RSVP Colors
    RSVP_COLORS = {
        "Confirmed": "#10b981",
        "Declined": "#ef4444",
        "Pending": "#f59e0b"
    }
    
    # Fonts
    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 10, "bold")


# ============================================================================
# Custom Styled Widgets
# ============================================================================

class ModernButton(tk.Canvas):
    """A modern styled button with hover effects."""
    
    def __init__(self, parent, text, command, bg_color, hover_color, width=120, height=36, **kwargs):
        super().__init__(parent, width=width, height=height, bg=ModernTheme.BG_MEDIUM, 
                         highlightthickness=0, **kwargs)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        self.width = width
        self.height = height
        
        self._draw_button(bg_color)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _draw_button(self, color):
        self.delete("all")
        # Rounded rectangle
        radius = 8
        self.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill=color, outline=color)
        self.create_arc(self.width-radius*2, 0, self.width, radius*2, start=0, extent=90, fill=color, outline=color)
        self.create_arc(0, self.height-radius*2, radius*2, self.height, start=180, extent=90, fill=color, outline=color)
        self.create_arc(self.width-radius*2, self.height-radius*2, self.width, self.height, start=270, extent=90, fill=color, outline=color)
        self.create_rectangle(radius, 0, self.width-radius, self.height, fill=color, outline=color)
        self.create_rectangle(0, radius, self.width, self.height-radius, fill=color, outline=color)
        # Text
        self.create_text(self.width//2, self.height//2, text=self.text, fill="white", font=ModernTheme.FONT_BUTTON)
    
    def _on_enter(self, event):
        self._draw_button(self.hover_color)
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        self._draw_button(self.bg_color)
    
    def _on_click(self, event):
        if self.command:
            self.command()


class ModernEntry(tk.Frame):
    """A modern styled entry field with icon support."""
    
    def __init__(self, parent, placeholder="", icon="", **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_LIGHT)
        
        self.placeholder = placeholder
        self.placeholder_active = True
        
        # Container frame with border effect
        self.container = tk.Frame(self, bg=ModernTheme.BG_LIGHT, padx=2, pady=2)
        self.container.pack(fill=tk.X, expand=True)
        
        inner_frame = tk.Frame(self.container, bg="#2d3748")
        inner_frame.pack(fill=tk.X, expand=True, padx=1, pady=1)
        
        if icon:
            icon_label = tk.Label(inner_frame, text=icon, bg="#2d3748", fg=ModernTheme.TEXT_SECONDARY,
                                  font=("Segoe UI", 12))
            icon_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.entry = tk.Entry(inner_frame, bg="#2d3748", fg=ModernTheme.TEXT_SECONDARY,
                              insertbackground=ModernTheme.ACCENT_PRIMARY, relief=tk.FLAT,
                              font=ModernTheme.FONT_BODY, **kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        
        self.entry.insert(0, placeholder)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=ModernTheme.TEXT_PRIMARY)
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=ModernTheme.TEXT_SECONDARY)
            self.placeholder_active = True
    
    def get(self):
        if self.placeholder_active:
            return ""
        return self.entry.get()
    
    def delete(self, first, last):
        self.entry.delete(first, last)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=ModernTheme.TEXT_SECONDARY)
        self.placeholder_active = True


class ModernCombobox(tk.Frame):
    """A modern styled combobox."""
    
    def __init__(self, parent, values, default="", **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_LIGHT)
        
        self.var = tk.StringVar(value=default)
        
        container = tk.Frame(self, bg="#2d3748", padx=1, pady=1)
        container.pack(fill=tk.X, expand=True)
        
        style = tk.Style()
        style.configure("Modern.TCombobox",
                        fieldbackground="#2d3748",
                        background="#2d3748",
                        foreground=ModernTheme.TEXT_PRIMARY)
        
        self.combo = tk.Combobox(container, textvariable=self.var, values=values,
                                   state="readonly", font=ModernTheme.FONT_BODY)
        self.combo.pack(fill=tk.X, padx=8, pady=8)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)


# ============================================================================
# File Processing Class
# ============================================================================

class CountdownTimerManager:
    """Class for managing countdown timer data file operations."""
    
    def __init__(self, filename: str = "event_data.json"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.filename):
            self._write_data({})
    
    def _read_data(self) -> Dict:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Data file is corrupted. Creating new file.")
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
            return {}
    
    def _write_data(self, data: Dict) -> None:
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error writing file: {str(e)}")
    
    def save_timer(self, timer: CountdownTimer) -> None:
        data = self._read_data()
        if "timers" not in data:
            data["timers"] = []
        
        timer_data = {
            "event_name": timer.event_name,
            "event_date": timer.event_date,
            "created_date": timer.created_date
        }
        
        # Check if timer already exists (update instead of duplicate)
        timers_list = data["timers"]
        for i, existing_timer in enumerate(timers_list):
            if existing_timer["event_name"] == timer.event_name:
                timers_list[i] = timer_data
                self._write_data(data)
                return
        
        # Add new timer
        timers_list.append(timer_data)
        self._write_data(data)
    
    def load_timers(self) -> List[Dict]:
        data = self._read_data()
        return data.get("timers", [])
    
    def delete_timer(self, event_name: str) -> bool:
        data = self._read_data()
        if "timers" not in data:
            return False
        
        original_length = len(data["timers"])
        data["timers"] = [t for t in data["timers"] if t["event_name"] != event_name]
        
        if len(data["timers"]) < original_length:
            self._write_data(data)
            return True
        return False


# ============================================================================
# GUI Application Class
# ============================================================================

class CountdownTimerApp:
    """Main GUI application for the Countdown Timer with modern styling."""
    
    def __init__(self, master=None, back_callback=None):
        # Check if running as standalone or imported ===
        if master is None:
            # Running as a standalone script, create the main window
            self.root = tk.Tk()
            self.is_standalone = True
        else:
            # Imported by main.py, create a child window
            self.root = master
            self.is_standalone = False

        self.back_callback = back_callback

        self.root.title("✨ Countdown Timer")
        self.root.geometry("900x650")
        self.root.configure(bg=ModernTheme.BG_DARK)
        self.root.resizable(True, True)
        
        # Center window on screen (only for standalone mode)
        if self.is_standalone:
            self._center_window()
        
        # Set up the close protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.manager = CountdownTimerManager()
        self._create_widgets()
        self._refresh_timer_display()

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = 900
        height = 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _on_closing(self):
        """Handle the window close event."""
        if self.is_standalone:
            # If running standalone, just quit the app
            self.root.quit()
        else:
            # If imported, call the back callback to return to the main menu
            if self.back_callback:
                self.back_callback()

    def _go_back(self):
        """Go back to the main menu."""
        # Call the function that was passed from the main app
        if self.back_callback:
            self.back_callback()

    def _create_widgets(self):
        """Create all the widgets for the application."""
        
        # --- Main Container ---
        main_frame = tk.Frame(self.root, bg=ModernTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Header Section ---
        header_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Add a "Back" button in the header
        header_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK) # This one is correct
        header_frame.pack(fill=tk.X, pady=(0, 20))

        if not self.is_standalone:
            back_btn = ModernButton(header_frame, "← Back", self._go_back, 
                                    ModernTheme.BG_LIGHT, ModernTheme.ACCENT_PRIMARY,
                                    width=100, height=32)
            back_btn.pack(side=tk.LEFT, pady=(0, 10))
        
        # Title with gradient effect simulation
        title_label = tk.Label(header_frame, text="⏰ Countdown Timer", 
                               font=ModernTheme.FONT_TITLE, bg=ModernTheme.BG_DARK,
                               fg=ModernTheme.ACCENT_PRIMARY)
        title_label.pack(side=tk.LEFT)
        
        # --- Content Area ---
        content_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # === LEFT COLUMN - Add Event Form ===
        left_column = tk.Frame(content_frame, bg=ModernTheme.BG_DARK)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Add Event Card
        add_card = tk.Frame(left_column, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        add_card.pack(fill=tk.X, pady=(0, 15))
        
        card_title = tk.Label(add_card, text="➕ Add New Event", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        card_title.pack(anchor=tk.W, pady=(0, 15))

        # Form Fields
        tk.Label(add_card, text="Event Name", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.name_entry = ModernEntry(add_card, placeholder="Enter event name", icon="📅")
        self.name_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Event Date (YYYY-MM-DD)", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.date_entry = ModernEntry(add_card, placeholder="Enter event date", icon="🗓️")
        self.date_entry.pack(fill=tk.X, pady=(0, 15))

        # Add Button
        add_btn = ModernButton(add_card, "✓ Add Event", self._add_timer, 
                               ModernTheme.ACCENT_PRIMARY, "#00b8d4", width=280, height=42)
        add_btn.pack(pady=(5, 0))

        # === RIGHT COLUMN - Event List ===
        right_column = tk.Frame(content_frame, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        list_header = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        list_header.pack(fill=tk.X, pady=(0, 15))
        
        list_title = tk.Label(list_header, text="📅 Event Countdowns", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        list_title.pack(side=tk.LEFT)
        
        self.count_label = tk.Label(list_header, text="0 events", font=ModernTheme.FONT_SMALL,
                                    bg=ModernTheme.BG_LIGHT, fg=ModernTheme.TEXT_SECONDARY, padx=10, pady=3)
        self.count_label.pack(side=tk.RIGHT)

        # Event List with custom styling
        list_container = tk.Frame(right_column, bg="#2d3748")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container, bg=ModernTheme.BG_LIGHT, troughcolor=ModernTheme.BG_MEDIUM)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.event_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                         bg="#2d3748", fg=ModernTheme.TEXT_PRIMARY,
                                         font=ModernTheme.FONT_BODY, relief=tk.FLAT,
                                         selectbackground=ModernTheme.ACCENT_PRIMARY,
                                         selectforeground=ModernTheme.BG_DARK,
                                         highlightthickness=0, borderwidth=0,
                                         activestyle='none')
        self.event_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.event_listbox.yview)

        # Action Bar
        action_frame = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        action_frame.pack(fill=tk.X, pady=(15, 0))

        # Delete Button
        delete_btn = ModernButton(action_frame, "🗑 Remove", self._remove_timer,
                                  ModernTheme.ACCENT_SECONDARY, "#dc2626", width=100, height=32)
        delete_btn.pack(side=tk.RIGHT)

    def _add_timer(self):
        """Handles the 'Add Event' button click."""
        name = self.name_entry.get()
        date = self.date_entry.get()

        try:
            if not name:
                messagebox.showerror("Error", "Please enter an event name.")
                return
                
            if not date:
                messagebox.showerror("Error", "Please enter an event date.")
                return
                
            timer = CountdownTimer(name, date)
            self.manager.save_timer(timer)
            messagebox.showinfo("Success", f"Event '{name}' added successfully! 🎉")
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self._refresh_timer_display()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _remove_timer(self):
        """Handles the 'Remove Event' button click."""
        selected_indices = self.event_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select an event to remove.")
            return

        selected_item = self.event_listbox.get(selected_indices)
        # Extract event name from the listbox item
        event_name = selected_item.split(" │ ")[0].strip()

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {event_name}?"):
            if self.manager.delete_timer(event_name):
                messagebox.showinfo("Success", f"Event '{event_name}' removed. 👋")
                self._refresh_timer_display()
            else:
                messagebox.showerror("Error", f"Could not find event '{event_name}'.")

    def _refresh_timer_display(self):
        """Refreshes the event listbox and the count display."""
        self.event_listbox.delete(0, tk.END)
        
        # Status indicators
        timers_data = self.manager.load_timers()
        
        for timer_data in timers_data:
            try:
                timer = CountdownTimer(timer_data["event_name"], timer_data["event_date"])
                days = timer.calculate_days_remaining()
                status = timer.get_status_message()
                
                # Color coding for urgency
                if days < 0:
                    icon = "❌"  # Past event
                elif days == 0:
                    icon = "🎉"  # Today
                elif days <= 7:
                    icon = "⚠️"  # Soon
                else:
                    icon = "📅"  # Future
                
                display_text = f"{timer.event_name} │ {icon} {status}"
                self.event_listbox.insert(tk.END, display_text)
            except Exception as e:
                error_text = f"Error loading timer: {str(e)}"
                self.event_listbox.insert(tk.END, error_text)

        # Update count label
        count = len(timers_data)
        self.count_label.config(text=f"{count} event{'s' if count != 1 else ''}")


# ============================================================================
# Execution: Main program entry point
# ============================================================================

def main():
    """Main function to run the application."""
    # When running standalone, create an instance with no master
    root = None # This will trigger the standalone mode in the class
    app = CountdownTimerApp(root)
    app.root.mainloop()

if __name__ == "__main__":
    main()