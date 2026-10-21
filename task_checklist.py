# ============================================================================
# Import necessary libraries
# ============================================================================
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime
import json
import os
import textwrap  # Added for wrapping long text
from typing import Dict, List

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
    
    # Priority Colors
    PRIORITY_COLORS = {
        "High": "#ef4444",
        "Normal": "#f59e0b",
        "Low": "#10b981"
    }
    
    # Fonts
    FONT_TITLE = ("Segoe UI", 20, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 10, "bold")


# ============================================================================
# Custom Styled Widgets (ModernText has been removed)
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
# File Processing Class
# ============================================================================

class TaskManager:
    """Class for managing task data file operations."""
    
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
    
    def _get_next_task_id(self, data: Dict) -> int:
        """Helper to get the next available task ID."""
        if "tasks" not in data or not data["tasks"]:
            return 1
        return max(task.get("task_id", 0) for task in data["tasks"]) + 1

    def save_task(self, title: str, description: str, due_date: str, priority: str) -> None:
        """Save a new task to the data file."""
        data = self._read_data()
        if "tasks" not in data:
            data["tasks"] = []
        
        task_id = self._get_next_task_id(data)
        new_task = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "completed": False,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Corrected format string
        }
        data["tasks"].append(new_task)
        self._write_data(data)

    def load_tasks(self) -> List[Dict]:
        """Load all tasks from the data file."""
        data = self._read_data()
        return data.get("tasks", [])

    def toggle_task_completion(self, task_id: int) -> None:
        """Toggle the completion status of a task."""
        data = self._read_data()
        if "tasks" in data:
            for task in data["tasks"]:
                if task["task_id"] == task_id:
                    task["completed"] = not task.get("completed", False)
                    task["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if task["completed"] else None
                    self._write_data(data)
                    return
        raise Exception("Task not found.")

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the data file."""
        data = self._read_data()
        if "tasks" in data:
            original_length = len(data["tasks"])
            data["tasks"] = [t for t in data["tasks"] if t["task_id"] != task_id]
            if len(data["tasks"]) < original_length:
                self._write_data(data)
                return
        raise Exception("Task not found.")


# ============================================================================
# GUI Application Class
# ============================================================================

class TaskChecklistApp:
    """Main GUI application for the Task Checklist with modern styling."""
    
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

        self.root.title("✨ Task Checklist")
        self.root.geometry("900x650")
        self.root.configure(bg=ModernTheme.BG_DARK)
        self.root.resizable(True, True)
        
        # Center window on screen (only for standalone mode)
        if self.is_standalone:
            self._center_window()
        
        # Set up the close protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.manager = TaskManager()
        self.index_to_task_id: Dict[int, int] = {}  # Maps listbox indices to task IDs
        self._create_widgets()
        self._refresh_task_display()

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
        header_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK) # This one is correct
        header_frame.pack(fill=tk.X, pady=(0, 20))

        if not self.is_standalone:
            back_btn = ModernButton(header_frame, "← Back", self._go_back, 
                                    ModernTheme.BG_LIGHT, ModernTheme.ACCENT_PRIMARY,
                                    width=100, height=32)
            back_btn.pack(side=tk.LEFT, pady=(0, 10))
        
        # Title with gradient effect simulation
        title_label = tk.Label(header_frame, text="📋 Task Checklist", 
                               font=ModernTheme.FONT_TITLE, bg=ModernTheme.BG_DARK,
                               fg=ModernTheme.ACCENT_PRIMARY)
        title_label.pack(side=tk.LEFT)
        
        # --- Content Area ---
        content_frame = tk.Frame(main_frame, bg=ModernTheme.BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # === LEFT COLUMN - Add Task Form ===
        left_column = tk.Frame(content_frame, bg=ModernTheme.BG_DARK)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Add Task Card
        add_card = tk.Frame(left_column, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        add_card.pack(fill=tk.X, pady=(0, 15))
        
        card_title = tk.Label(add_card, text="➕ Add New Task", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        card_title.pack(anchor=tk.W, pady=(0, 15))

        # Form Fields
        tk.Label(add_card, text="Task Title", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.title_entry = ModernEntry(add_card, placeholder="Enter task title", icon="📝")
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Due Date (YYYY-MM-DD)", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.due_date_entry = ModernEntry(add_card, placeholder="Enter due date", icon="🗓️")
        self.due_date_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Priority", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        self.priority_combo = ModernCombobox(add_card, values=["Low", "Normal", "High"], default="Normal")
        self.priority_combo.pack(fill=tk.X, pady=(0, 10))

        tk.Label(add_card, text="Description", font=ModernTheme.FONT_SMALL, bg=ModernTheme.BG_MEDIUM,
                 fg=ModernTheme.TEXT_SECONDARY).pack(anchor=tk.W, pady=(5, 2))
        
        # Use standard ScrolledText with modern styling ---
        desc_frame = tk.Frame(add_card, bg="#2d3748", relief=tk.FLAT, borderwidth=1)
        desc_frame.pack(fill=tk.X, pady=(0, 15))
        self.description_text = scrolledtext.ScrolledText(
            desc_frame,
            bg="#2d3748",
            fg=ModernTheme.TEXT_PRIMARY,
            insertbackground=ModernTheme.ACCENT_PRIMARY,
            relief=tk.FLAT,
            font=ModernTheme.FONT_BODY,
            wrap=tk.WORD,
            height=5
        )
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add Button
        add_btn = ModernButton(add_card, "✓ Add Task", self._add_task, 
                               ModernTheme.ACCENT_PRIMARY, "#00b8d4", width=280, height=42)
        add_btn.pack(pady=(5, 0))

        # === RIGHT COLUMN - Task List ===
        right_column = tk.Frame(content_frame, bg=ModernTheme.BG_MEDIUM, padx=20, pady=20)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        list_header = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        list_header.pack(fill=tk.X, pady=(0, 15))
        
        list_title = tk.Label(list_header, text="📋 Tasks", font=ModernTheme.FONT_SUBTITLE,
                              bg=ModernTheme.BG_MEDIUM, fg=ModernTheme.TEXT_PRIMARY)
        list_title.pack(side=tk.LEFT)
        
        self.count_label = tk.Label(list_header, text="0 tasks", font=ModernTheme.FONT_SMALL,
                                    bg=ModernTheme.BG_LIGHT, fg=ModernTheme.TEXT_SECONDARY, padx=10, pady=3)
        self.count_label.pack(side=tk.RIGHT)

        # Task List with custom styling
        list_container = tk.Frame(right_column, bg="#2d3748")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container, bg=ModernTheme.BG_LIGHT, troughcolor=ModernTheme.BG_MEDIUM)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                         bg="#2d3748", fg=ModernTheme.TEXT_PRIMARY,
                                         font=ModernTheme.FONT_BODY, relief=tk.FLAT,
                                         selectbackground=ModernTheme.ACCENT_PRIMARY,
                                         selectforeground=ModernTheme.BG_DARK,
                                         highlightthickness=0, borderwidth=0,
                                         activestyle='none')
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.task_listbox.yview)

        # Action Bar
        action_frame = tk.Frame(right_column, bg=ModernTheme.BG_MEDIUM)
        action_frame.pack(fill=tk.X, pady=(15, 0))

        # Toggle Completion Button
        toggle_btn = ModernButton(action_frame, "✓ Toggle", self._toggle_task_completion,
                                  ModernTheme.ACCENT_TERTIARY, "#9333ea", width=100, height=32)
        toggle_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Delete Button
        delete_btn = ModernButton(action_frame, "🗑 Remove", self._delete_task,
                                  ModernTheme.ACCENT_SECONDARY, "#dc2626", width=100, height=32)
        delete_btn.pack(side=tk.RIGHT)

    def _add_task(self):
        """Handles the 'Add Task' button click."""
        title = self.title_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_combo.get()
        # Use standard ScrolledText's get method 
        description = self.description_text.get("1.0", tk.END).strip()

        try:
            if not title:
                messagebox.showerror("Error", "Please enter a task title.")
                return
                
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return
                    
            self.manager.save_task(title, description, due_date, priority)
            messagebox.showinfo("Success", f"Task '{title}' added successfully! 🎉")
            
            # Simplified clearing logic for the ScrolledText
            self.title_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.priority_combo.set("Normal")
            self.description_text.delete("1.0", tk.END)
            
            self._refresh_task_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _toggle_task_completion(self):
        """Handles the 'Toggle Completion' button click."""
        selected_indices = self.task_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a task to toggle.")
            return

        selected_idx = selected_indices[0]
        task_id = self.index_to_task_id.get(selected_idx)
        if task_id is None:
            messagebox.showerror("Error", "Could not determine task ID.")
            return

        try:
            self.manager.toggle_task_completion(task_id)
            messagebox.showinfo("Success", f"Task completion status updated. ✓")
            self._refresh_task_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete_task(self):
        """Handles the 'Remove Task' button click."""
        selected_indices = self.task_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a task to remove.")
            return

        selected_idx = selected_indices[0]
        task_id = self.index_to_task_id.get(selected_idx)
        if task_id is None:
            messagebox.showerror("Error", "Could not determine task ID.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove this task?"):
            try:
                self.manager.delete_task(task_id)
                messagebox.showinfo("Success", f"Task removed. 👋")
                self._refresh_task_display()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    @staticmethod
    def _wrap_lines(text: str, width: int) -> List[str]:
        """Wrap text to a given width, breaking long words when needed."""
        wrapped = textwrap.wrap(
            text or "",
            width=width,
            break_long_words=True,
            break_on_hyphens=False
        )
        return wrapped if wrapped else ["(no description)"]

    def _refresh_task_display(self):
        """Refreshes the task listbox and the count display."""
        self.task_listbox.delete(0, tk.END)
        self.index_to_task_id = {}
        
        # Load tasks
        tasks = self.manager.load_tasks()
        
        # Sort tasks: incomplete first, then by priority, then by due date
        priority_order = {"High": 0, "Normal": 1, "Low": 2}
        def sort_key(t):
            return (
                t.get("completed", False),
                priority_order.get(t.get("priority", "Normal"), 1),
                t.get("due_date", ""),
                t.get("task_id", 0)
            )
        tasks_sorted = sorted(tasks, key=sort_key)
        
        for task in tasks_sorted:
            task_id = task.get("task_id", 0)
            completed = task.get("completed", False)
            
            # Status indicators
            if completed:
                status_icon = "✅"
                status_text = "Completed"
            else:
                status_icon = "⏳"
                status_text = "Pending"
            
            # Priority indicators
            priority = task.get("priority", "Normal")
            if priority == "High":
                priority_icon = "🔴"
            elif priority == "Normal":
                priority_icon = "🟡"
            else:
                priority_icon = "🟢"
            
            # Due date
            due_date = task.get("due_date", "No due date") or "No due date"
            
            # Title and description with wrapping
            title = (task.get("title", "") or "").strip() or "(no title)"
            description = (task.get("description", "") or "").strip() or "(no description)"
            title_lines = self._wrap_lines(title, width=50)
            desc_lines = self._wrap_lines(description, width=70)

            line_prefix = f"#{task_id} │ "
            meta = f"{priority_icon} {priority} │ 📅 {due_date} │ {status_text}"
            
            # First line: task id + title + meta
            first_line = f"{line_prefix}{status_icon} {title_lines[0]} │ {meta}"
            idx = self.task_listbox.size()
            self.task_listbox.insert(tk.END, first_line)
            self.index_to_task_id[idx] = task_id

            # Continuation lines for long titles
            for line in title_lines[1:]:
                idx = self.task_listbox.size()
                self.task_listbox.insert(tk.END, f"{' ' * len(line_prefix)}  {line}")
                self.index_to_task_id[idx] = task_id

            # Description lines
            desc_prefix = " " * len(line_prefix) + "📝 "
            for line in desc_lines:
                idx = self.task_listbox.size()
                self.task_listbox.insert(tk.END, f"{desc_prefix}{line}")
                self.index_to_task_id[idx] = task_id

            # Spacer between tasks
            idx = self.task_listbox.size()
            self.task_listbox.insert(tk.END, "")
            self.index_to_task_id[idx] = task_id

        # Update count label
        count = len(tasks)
        completed_count = sum(1 for t in tasks if t.get("completed", False))
        self.count_label.config(text=f"{count} tasks ({completed_count} completed)")


# ============================================================================
# Execution: Main program entry point
# ============================================================================

def main():
    """Main function to run the application."""
    # When running standalone, create an instance with no master
    root = None # This will trigger the standalone mode in the class
    app = TaskChecklistApp(root)
    app.root.mainloop()

if __name__ == "__main__":
    main()