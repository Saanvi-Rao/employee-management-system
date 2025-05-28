import customtkinter as ctk
from PIL import Image
import os

from add_employee import open_add_employee_window
from update_employee import open_update_employee_window
from view_employee import open_view_employee_window
from delete_employee import open_delete_employee_window
from database import initialize_database

# Initialize the database (and create tables if they don't exist)
initialize_database()

# Set CustomTkinter appearance mode and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class EMSWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("EMPLOYEE MANAGEMENT SYSTEM")
        self.geometry('950x550')
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")
        self.setup_ui()

    def _handle_delete_employee_click(self):
       
        # Hide the current EMS window
        self.withdraw()

       
        open_delete_employee_window(self, on_close_callback=self._show_ems_window_after_delete)

    def _show_ems_window_after_delete(self):
        """
        Callback function executed when the delete employee window closes.
        Reveals the main EMS window again.
        """
        # Show the main EMS window
        self.deiconify()
     

    def setup_ui(self):
        """
        Sets up all the UI elements for the main EMS window, including images and buttons.
        """
        # Get the directory of the current file to construct image paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(base_dir, "images")  # Assuming images are in 'images' folder

        # --- Background Image ---
        try:
            bg_image_path = os.path.join(images_dir, "final1.png")
            bg_image_pil = Image.open(bg_image_path)
            # Create a CTkImage object with the loaded PIL image
            bg_image = ctk.CTkImage(light_image=bg_image_pil, size=(950, 550))
            # Create a label to display the background image
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print(f"Background image (final1.png) not found in {images_dir}. Check the path.")
        except Exception as e:
            print(f"Error loading background image: {e}")

        # --- Logo Image ---
        try:
            logo_img_path = os.path.join(images_dir, "logo.png")
            logo_img_pil = Image.open(logo_img_path)
            logo_img = ctk.CTkImage(light_image=logo_img_pil, size=(250, 250))
            logo_label = ctk.CTkLabel(self, image=logo_img, text="")
            logo_label.place(x=70, y=0)
        except FileNotFoundError:
            print(f"Logo image (logo.png) not found in {images_dir}. Check the path.")
        except Exception as e:
            print(f"Error loading logo image: {e}")

        # --- Additional Decorative Image ---
        try:
            extra_img_path = os.path.join(images_dir, "wokr.png")
            extra_img_pil = Image.open(extra_img_path)
            extra_img = ctk.CTkImage(light_image=extra_img_pil, size=(370, 350))
            extra_label = ctk.CTkLabel(self, image=extra_img, text="")
            extra_label.place(x=10, y=200)
        except FileNotFoundError:
            print(f"Extra image (wokr.png) not found in {images_dir}. Check the path.")
        except Exception as e:
            print(f"Error loading extra image: {e}")

        # --- Button Frame ---
        # A frame to hold the action buttons
        button_frame = ctk.CTkFrame(self, width=200, height=300, fg_color="#FFFFFF")
        button_frame.place(x=605, y=245)

        # Define common style properties for buttons
        button_style = {
            "width": 150,
            "height": 10,
            "corner_radius": 8,
            "font": ("Segoe UI", 14, "bold"),
            "text_color": "white"
        }

        # Data for creating multiple buttons dynamically
        buttons_data = [
            ("Add Employee", "#1A873A", "#27ae60", lambda: open_add_employee_window(self)),
            ("Update Employee", "#3942BA", "#2980b9", lambda: open_update_employee_window(self)),
            # IMPORTANT CHANGE: Use the new handler for Delete Employee button
            ("Delete Employee", "#990018", "#c0392b", self._handle_delete_employee_click),
            ("View Employees", "#7D3C98", "#9b59b6", lambda: open_view_employee_window(self))
        ]

        # Create and pack buttons based on the data
        for text, color, hover_color, command in buttons_data:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                fg_color=color,
                hover_color=hover_color,
                command=command,
                **button_style
            )
            btn.pack(pady=10) # Add padding between buttons

def launch_ems():
    """
    Initializes and runs the main EMS application.
    """
    app = EMSWindow()
    app.mainloop()

if __name__ == "__main__":
    launch_ems()