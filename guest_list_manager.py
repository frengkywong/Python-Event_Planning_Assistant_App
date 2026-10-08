# ============================================================================
# Import necessary libraries
# ============================================================================
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from typing import Set, Dict

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
        
        style = ttk.Style()
        style.configure("Modern.TCombobox",
                        fieldbackground="#2d3748",
                        background="#2d3748",
                        foreground=ModernTheme.TEXT_PRIMARY)
        
        self.combo = ttk.Combobox(container, textvariable=self.var, values=values,
                                   state="readonly", font=ModernTheme.FONT_BODY)
        self.combo.pack(fill=tk.X, padx=8, pady=8)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        self.var.set(value)

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


class GuestListManager(EventComponent):
    """Guest List Manager class for managing event guests."""
    
    def __init__(self, event_name: str):
        super().__init__(event_name)
        self.guests: Set[str] = set()
        self.guest_details: Dict[str, Dict] = {}
    
    def add_guest(self, name: str, email: str = "", phone: str = "", rsvp: str = "Pending") -> bool:
        name = name.strip().title()
        if not name:
            raise ValueError("Guest name cannot be empty")
        if name in self.guests:
            return False
        self.guests.add(name)
        self.guest_details[name] = {
            "email": email.strip(), "phone": phone.strip(), "rsvp": rsvp.strip(),
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return True
    
    def remove_guest(self, name: str) -> bool:
        name = name.strip().title()
        if name in self.guests:
            self.guests.remove(name)
            del self.guest_details[name]
            return True
        return False
    
    def update_rsvp(self, name: str, rsvp_status: str) -> bool:
        name = name.strip().title()
        if name in self.guest_details:
            self.guest_details[name]["rsvp"] = rsvp_status.strip()
            return True
        return False
    
    def get_rsvp_summary(self) -> Dict[str, int]:
        summary = {"Confirmed": 0, "Declined": 0, "Pending": 0}
        for guest_name in self.guest_details:
            rsvp = self.guest_details[guest_name].get("rsvp", "Pending")
            if rsvp in summary:
                summary[rsvp] += 1
            else:
                summary["Pending"] += 1
        return summary

# ============================================================================
# Data Management Class
# ============================================================================

class GuestListDataManager:
    """Class for managing guest list data file operations."""
    
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
        except (FileNotFoundError, json.JSONDecodeError):
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
    
    def save_guest_list(self, guest_list: GuestListManager) -> None:
        data = self._read_data()
        if "guest_lists" not in data:
            data["guest_lists"] = {}
        
        data["guest_lists"][guest_list.event_name] = {
            "guests": list(guest_list.guests),
            "guest_details": guest_list.guest_details,
            "created_date": guest_list.created_date
        }
        self._write_data(data)
    
    def load_guest_list(self, event_name: str):
        data = self._read_data()
        if "guest_lists" not in data or event_name not in data["guest_lists"]:
            return None
        
        guest_data = data["guest_lists"][event_name]
        guest_list = GuestListManager(event_name)
        guest_list.guests = set(guest_data.get("guests", []))
        guest_list.guest_details = guest_data.get("guest_details", {})
        return guest_list

# ============================================================================
# GUI Application Class
# ============================================================================

class GuestListManagerApp:
    """Main GUI application for the Guest List Manager module."""
    
    def __init__(self, master: tk.Tk, back_callback):
        """Initialize the Guest List Manager GUI."""
        # Use the master window directly ---
        self.root = master
        self.back_callback = back_callback
        
        self.root.title("✨ Guest List Manager")
        self.root.geometry("900x650")
        self.root.configure(bg=ModernTheme.BG_DARK)
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing) # Handle window closing
        
        self.back_callback = back_callback

        # Set up the close protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Create a data manager for THIS GUI.
        self.data_manager = GuestListDataManager()
        
        # Load the guest list from the file at startup.
        self.manager = self.data_manager.load_guest_list("My Event") or GuestListManager("My Event")
        self._create_widgets()
        self._refresh_guest_list()

    def _on_closing(self):
        """Handle the window close event."""
        # Call the back callback to return to the main menu
        if self.back_callback:
            self.back_callback()
        # Then destroy the Toplevel window
        self.root.destroy()

    def _create_widgets(self):
        """Create all the widgets for the application."""
        # Clear existing widgets (important if this GUI is ever recreated)
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- Main Container ---
        main_frame = tk.Frame(self.root, bg=ModernTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Header Section ---
        header_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Add a "Back" button in the header
        header_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        back_btn = ModernButton(header_frame, "← Back", self._go_back, 
                                ModernTheme.BG_LIGHT, ModernTheme.ACCENT_PRIMARY,
                                width=100, height=32)
        back_btn.pack(side=tk.LEFT, pady=(0, 10))
       
        # Title
        title_label = tk.Label(header_frame, text="🎉 Guest List Manager", 
                               font=ModernTheme.FONT_TITLE, bg=ModernTheme.BG_DARK,
                               fg=ModernTheme.ACCENT_PRIMARY)
        title_label.pack(side=tk.LEFT)
        
        # Event name badge
        event_badge = tk.Label(header_frame, text=f"📅 {self.manager.event_name}",
                               font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_LIGHT,
                               fg=ModernTheme.TEXT_SECONDARY, padx=15, pady=5)
        event_badge.pack(side=tk.RIGHT)

        # --- Content Area (Two Columns) ---
        content_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # === LEFT COLUMN - Add Guest Form ===
        left_column = tk.Frame(content_frame, bg=ModernTheme.BG_DARK)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # Add Guest Card
        add_card = tk.Frame(left_column, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        add_card.pack(fill=tk.X, pady=(0, 15))
        
        card_title = tk.Label(add_card, text="➕ Add New Guest", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        card_title.pack(anchor=tk.W, pady=(0, 15))

        # Form Fields
        tk.Label(add_card, text="Name", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.name_entry = ModernEntry(add_card, placeholder="Enter guest name", icon="👤")
        self.name_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Email", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.email_entry = ModernEntry(add_card, placeholder="Enter email address", icon="📧")
        self.email_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Phone", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.phone_entry = ModernEntry(add_card, placeholder="Enter phone number", icon="📱")
        self.phone_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="RSVP Status", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.rsvp_combo = ModernCombobox(add_card, values=["Pending", "Confirmed", "Declined"], default="Pending")
        self.rsvp_combo.pack(fill=tk.X, pady=(0, 15))

        # Add Button
        add_btn = ModernButton(add_card, "✓ Add Guest", self._add_guest, 
                               ModernTheme.ACCENT_PRIMARY, "#00b8d4", width=280, height=42)
        add_btn.pack(pady=(5, 0))

        # === RSVP Summary Card ===
        summary_card = tk.Frame(left_column, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        summary_card.pack(fill=tk.X)
        
        summary_title = tk.Label(summary_card, text="📊 RSVP Summary", font=ModernTheme.FONT_SUBTITLE,
                                 bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        summary_title.pack(anchor=tk.W, pady=(0, 15))

        # Summary Stats Container
        self.stats_frame = tk.Frame(summary_card, bg=ModernTheme.BG_MEDIUM)
        self.stats_frame.pack(fill=tk.X)
        
        self._create_stat_boxes()

        # === RIGHT COLUMN - Guest List ===
        right_column = tk.Frame(content_frame, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        list_header = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        list_header.pack(fill=tk.X, pady=(0, 15))
        
        list_title = tk.Label(list_header, text="👥 Guest List", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        list_title.pack(side=tk.LEFT)
        
        self.count_label = tk.Label(list_header, text="0 guests", font=ModernTheme.FONT_SMALL,
                                    bg=ModernTheme.BG_LIGHT, fg=ModernTheme.TEXT_SECONDARY, padx=10, pady=3)
        self.count_label.pack(side=tk.RIGHT)

        # Guest List with custom styling
        list_container = tk.Frame(right_column, bg="#2d3748")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container, bg=ModernTheme.BG_LIGHT, troughcolor=ModernTheme.BG_MEDIUM)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.guest_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                         bg="#2d3748", fg=ModernTheme.TEXT_PRIMARY,
                                         font=ModernTheme.FONT_BODY, relief=tk.FLAT,
                                         selectbackground=ModernTheme.ACCENT_PRIMARY,
                                         selectforeground=ModernTheme.BG_DARK,
                                         highlightthickness=0, borderwidth=0,
                                         activestyle='none')
        self.guest_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.guest_listbox.yview)

        # Action Bar
        action_frame = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        action_frame.pack(fill=tk.X, pady=(15, 0))

        # Update RSVP Section
        update_section = tk.Frame(action_frame, bg=ModernTheme.BG_MEDIUM)
        update_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(update_section, text="Update RSVP:", font=ModernTheme.FONT_SMALL,
                 bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_SECONDARY).pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_rsvp_combo = ModernCombobox(update_section, values=["Confirmed", "Declined", "Pending"], default="")
        self.update_rsvp_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        update_btn = ModernButton(update_section, "Update", self._update_rsvp,
                                  ModernTheme.ACCENT_TERTIARY, "#9333ea", width=80, height=32)
        update_btn.pack(side=tk.LEFT)

        # Delete Button
        delete_btn = ModernButton(action_frame, "🗑 Remove", self._remove_guest,
                                  ModernTheme.ACCENT_SECONDARY, "#dc2626", width=100, height=32)
        delete_btn.pack(side=tk.RIGHT)

    def _go_back(self):
        """Go back to the main menu."""
        # Call the function that was passed from the main app
        if self.back_callback:
            self.back_callback()

    def _create_stat_boxes(self):
        """Create the RSVP summary stat boxes."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        summary = self.manager.get_rsvp_summary()
        total = len(self.manager.guests)
        
        stats = [
            ("Total", total, ModernTheme.ACCENT_PRIMARY),
            ("Confirmed", summary["Confirmed"], ModernTheme.SUCCESS),
            ("Pending", summary["Pending"], ModernTheme.WARNING),
            ("Declined", summary["Declined"], ModernTheme.ERROR),
        ]
        
        for label, count, color in stats:
            stat_box = tk.Frame(self.stats_frame, bg=ModernTheme.BG_LIGHT, padx=12, pady=8)
            stat_box.pack(side=tk.LEFT, padx=(0, 10), pady=5)
            
            count_label = tk.Label(stat_box, text=str(count), font=("Segoe UI", 18, "bold"),
                                   bg=ModernTheme.BG_LIGHT, fg=color)
            count_label.pack()
            
            text_label = tk.Label(stat_box, text=label, font=ModernTheme.FONT_SMALL,
                                  bg=ModernTheme.BG_LIGHT, fg=ModernTheme.TEXT_SECONDARY)
            text_label.pack()

    # --- User-Defined Functions for GUI Actions ---

    def _add_guest(self):
        """Handles the 'Add Guest' button click."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        rsvp = self.rsvp_combo.get()

        try:
            if self.manager.add_guest(name, email, phone, rsvp):
                # Save the data to the file immediately after a successful change.
                self.data_manager.save_guest_list(self.manager)
                
                messagebox.showinfo("Success", f"Guest '{name}' added successfully! 🎉")
                self.name_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.phone_entry.delete(0, tk.END)
                self.rsvp_combo.set("Pending")
                self._refresh_guest_list()
            else:
                messagebox.showerror("Error", f"Guest '{name}' already exists.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _remove_guest(self):
        """Handles the 'Remove Guest' button click."""
        selected_indices = self.guest_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a guest to remove.")
            return

        selected_item = self.guest_listbox.get(selected_indices)
        # Fixed: Extract guest name correctly from the listbox item
        guest_name = selected_item.split(" │ ")[0].strip()

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {guest_name}?"):
            if self.manager.remove_guest(guest_name):
                # Save the data to the file immediately after a successful change.
                self.data_manager.save_guest_list(self.manager)
                
                messagebox.showinfo("Success", f"Guest '{guest_name}' removed. 👋")
                self._refresh_guest_list()
            else:
                messagebox.showerror("Error", f"Could not find guest '{guest_name}'.")

    def _update_rsvp(self):
        """Handles the 'Update RSVP' button click."""
        selected_indices = self.guest_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a guest to update.")
            return
        
        new_status = self.update_rsvp_combo.get()
        if not new_status:
            messagebox.showwarning("No Status", "Please select a new RSVP status.")
            return

        selected_item = self.guest_listbox.get(selected_indices)
        # Fixed: Extract guest name correctly from the listbox item
        guest_name = selected_item.split(" │ ")[0].strip()

        if self.manager.update_rsvp(guest_name, new_status):
            # Save the data to the file immediately after a successful change.
            self.data_manager.save_guest_list(self.manager)
            
            messagebox.showinfo("Success", f"RSVP for '{guest_name}' updated to '{new_status}'. ✓")
            self._refresh_guest_list()
        else:
            messagebox.showerror("Error", f"Could not find guest '{guest_name}'.")

    def _refresh_guest_list(self):
        """Refreshes the guest listbox and summary display."""
        self.guest_listbox.delete(0, tk.END)
        
        # Status indicators
        status_icons = {"Confirmed": "✅", "Declined": "❌", "Pending": "⏳"}
        
        for guest_name in sorted(list(self.manager.guests)):
            details = self.manager.guest_details[guest_name]
            rsvp = details.get('rsvp', 'Pending')
            icon = status_icons.get(rsvp, "⏳")
            display_text = f"{guest_name} │ {icon} {rsvp}"
            self.guest_listbox.insert(tk.END, display_text)

        # Update count label
        count = len(self.manager.guests)
        self.count_label.config(text=f"{count} guest{'s' if count != 1 else ''}")
        
        # Refresh summary stats
        self._create_stat_boxes()


# ============================================================================
# IMPORTANT: DO NOT RUN THIS FILE DIRECTLY
# ============================================================================
# This file is a module and should only be imported and run by main.py.
# Running it directly will cause a blank window to appear and disappear.
# The main application entry point is handled in main.py.
# ============================================================================

def main():
#     """Main function to run the application."""
    root = tk.Tk()
    app = GuestListManagerApp(root, lambda: None)
    root.mainloop()

if __name__ == "__main__":
    main()