import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os

# Setup appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def launch_login():
    root = ctk.CTk()
    root.title("LOGIN SYSTEM")
    root.geometry('950x550')
    root.resizable(False, False)
    root.configure(fg_color="#FFFFFF")

    # Get absolute path of this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Background Image
    try:
        bg_img_path = os.path.join(script_dir, "images", "picture.png")
        light_image = Image.open(bg_img_path)
        bg_image = ctk.CTkImage(light_image=light_image, size=(550, 550))
        bg_label = ctk.CTkLabel(root, image=bg_image, text="")
        bg_label.place(x=400, y=0)
        bg_label.lower()
        # Keep reference to prevent garbage collection
        root.bg_image = bg_image
    except FileNotFoundError:
        print("Background image not found:", bg_img_path)

    # Login Frame
    frame = ctk.CTkFrame(root, width=400, height=550, corner_radius=0, fg_color="#FFFFFF")
    frame.place(x=0, y=0)

    # Logo
    try:
        logo_img_path = os.path.join(script_dir, "images", "logo.png")
        logo_image = Image.open(logo_img_path)
        logo_img = ctk.CTkImage(light_image=logo_image, size=(200, 200))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="")
        logo_label.place(x=75, y=0)
        # Keep reference to prevent garbage collection
        frame.logo_img = logo_img
    except FileNotFoundError:
        print("Logo image not found:", logo_img_path)

    # Heading
    heading = ctk.CTkLabel(frame, text="LOG IN", text_color="#452C8E", font=("Helvetica", 24, "bold"))
    heading.place(x=130, y=165)

    # Subheading
    subheading = ctk.CTkLabel(
        frame,
        text="Welcome to the System – Where Managing People Begins",
        text_color="#D72D51",
        font=("Segoe UI Semibold", 14, "bold"),
        wraplength=280,
        justify="center"
    )
    subheading.place(x=60, y=195)

    # Username Field
    user = ctk.CTkEntry(frame, width=250, placeholder_text="Username", font=("Segoe UI", 12),
                        border_width=0, corner_radius=0, fg_color="white", text_color="black")
    user.place(x=50, y=260)
    ctk.CTkFrame(frame, width=250, height=2, fg_color="black").place(x=50, y=290)

    # Password Field
    password = ctk.CTkEntry(frame, width=250, placeholder_text="Password", font=("Segoe UI", 12),
                            show="*", border_width=0, corner_radius=0, fg_color="white", text_color="black")
    password.place(x=50, y=310)
    ctk.CTkFrame(frame, width=250, height=2, fg_color="black").place(x=50, y=340)

    # Login Button Action
    def login_action():
        username = user.get()
        pwd = password.get()

        if username == '' or pwd == '':
            messagebox.showerror('Error', 'All fields are required')
        elif username == 'admin' and pwd == 'admin123':
            root.destroy()  # Close login window
            import ems
            ems.launch_ems()  # Launch EMS window
        else:
            messagebox.showerror('Error', 'Invalid credentials')

    # Login Button
    login_btn = ctk.CTkButton(
        frame, text="Sign In", width=250, command=login_action,
        font=("Segoe UI", 14, "bold"), fg_color="#1A5276",
        hover_color="#154360", cursor="hand2", corner_radius=8
    )
    login_btn.place(x=50, y=370)

    # Remember Me Checkbox
    remember = ctk.CTkCheckBox(
        frame, text="Remember me",
        font=("Segoe UI", 13),
        checkbox_width=18,
        checkbox_height=18,
        border_width=1
    )
    remember.place(x=50, y=420)

    # Forgot Password Functionality
    def forgot_password():
        messagebox.showinfo("Forgot Password", "Please contact your administrator for password reset.")

    # Forgot Password Link
    forgot_link = ctk.CTkLabel(
        frame, text="Forgot password?",
        font=("Segoe UI", 13, "underline"),
        text_color="gray",
        cursor="hand2"
    )
    forgot_link.place(x=50, y=450)
    forgot_link.bind("<Button-1>", lambda e: forgot_password())

    root.mainloop()

if __name__ == "__main__":
    launch_login()
