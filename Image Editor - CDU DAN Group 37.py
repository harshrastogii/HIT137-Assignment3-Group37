# ==================================================
# Team Member 1: Base Structure
# ==================================================
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor - CDU CAS/DAN Group 37")

        # Image variables
        self.original_image = None  # Stores the original image loaded by the user
        self.display_image = None   # Stores the resized image displayed on the canvas
        self.image_path = None      # Stores the file path of the loaded image
        self.cropped_image = None   # Stores the cropped image (as a PhotoImage object)
        self.cropped_image_data = None  # Stores the cropped image (as a PIL image object)

        # Canvas for image display
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Text above the load image button
        self.contributors_text = tk.Label(self, text="Created by : Harsh Rastogi, Kazi Rubaiyat Islam, Rashedul Islam Jisan and Robiul Islam", font=("Sans", 12))
        self.contributors_text.pack()

        # Load Image Button
        self.load_button = tk.Button(self, text="Load Image", command=self.load_image)
        self.load_button.pack()

        # For cropping functionality
        self.crop_rectangle = None  # Stores the rectangle drawn for cropping
        self.crop_start_x = self.crop_start_y = 0  # Stores the starting coordinates of the crop rectangle

        # Bind keyboard shortcuts
        self.bind("<Control-o>", self.load_image_shortcut)

# ==================================================
# Team Member 2: Image Loading Functionality
# ==================================================
    def load_image(self):
        """
        Loads an image from the user's local device and displays it on the canvas.
        - Uses filedialog to open a file selection window.
        - Resizes the image to fit the canvas while maintaining aspect ratio.
        - Displays the image on the canvas and sets up mouse events for cropping.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return
        try:
            self.original_image = Image.open(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return
        self.image_path = file_path

        # Rescale the image to fit within the canvas while maintaining aspect ratio
        self.display_image = self.resize_to_fit(self.original_image, self.canvas.winfo_width(), self.canvas.winfo_height())

        # Display the scaled image on the canvas
        self.canvas.image = self.display_image  # Keep a reference to avoid garbage collection
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        # Reset cropping rectangle
        self.canvas.delete(self.crop_rectangle)
        self.crop_rectangle = None

        # Set up mouse event for cropping
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def resize_to_fit(self, image, max_width, max_height):
        """
        Resizes an image to fit within the given dimensions while maintaining its aspect ratio.
        - image: The PIL image object to resize.
        - max_width: The maximum width for the resized image.
        - max_height: The maximum height for the resized image.
        - Returns: A PhotoImage object for display on the canvas.
        """
        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        return ImageTk.PhotoImage(image.resize((new_width, new_height), Image.LANCZOS))

# ==================================================
# Team Member 3: Image Cropping Functionality
# ==================================================
    def on_mouse_press(self, event):
        """
        Handles the mouse press event for cropping.
        - Records the starting coordinates of the crop rectangle.
        - Creates a new rectangle on the canvas.
        """
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)
        self.crop_rectangle = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_start_x, self.crop_start_y, outline="red")

    def on_mouse_drag(self, event):
        """
        Handles the mouse drag event for cropping.
        - Updates the coordinates of the crop rectangle as the user drags the mouse.
        """
        self.canvas.coords(self.crop_rectangle, self.crop_start_x, self.crop_start_y, event.x, event.y)

    def on_mouse_release(self, event):
        """
        Handles the mouse release event for cropping.
        - Calculates the cropping coordinates and crops the image.
        - Opens a new window to display the cropped image.
        """
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_width, img_height = self.original_image.size
        scale_x = img_width / canvas_width
        scale_y = img_height / canvas_height

        # Ensure valid cropping coordinates
        x1 = max(0, min(self.crop_start_x, event.x))
        y1 = max(0, min(self.crop_start_y, event.y))
        x2 = max(0, max(self.crop_start_x, event.x))
        y2 = max(0, max(self.crop_start_y, event.y))

        crop_box = (
            int(x1 * scale_x),
            int(y1 * scale_y),
            int(x2 * scale_x),
            int(y2 * scale_y)
        )

        self.cropped_image_data = self.original_image.crop(crop_box)
        self.cropped_image = ImageTk.PhotoImage(self.cropped_image_data)

        self.open_crop_window()

    def open_crop_window(self):
        """
        Opens a new window to display the cropped image and provide editing options.
        - Includes sliders for resizing and brightness adjustment.
        - Includes buttons for grayscale conversion, rotation, and saving.
        """
        crop_window = tk.Toplevel(self)
        crop_window.title("Cropped Image")

        # Canvas for cropped image
        crop_canvas = tk.Canvas(crop_window, width=400, height=300)
        crop_canvas.pack(fill="both", expand=True)

        # Display cropped image
        crop_canvas.image = self.cropped_image  # Keep a reference to avoid garbage collection
        crop_canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_image)

        # Undo/Redo stacks for cropped image
        undo_stack = []
        redo_stack = []
        original_cropped_image = self.cropped_image_data.copy()

# ==================================================
# Team Member 4: Image Processing & Enhancements
# ==================================================
        def apply_edit(edit_func):
            """
            Applies an edit to the cropped image and updates the display.
            - edit_func: A function that performs the edit and returns the modified image.
            """
            nonlocal undo_stack, redo_stack
            undo_stack.append(self.cropped_image_data.copy())
            redo_stack.clear()  # Clear redo stack after a new edit
            self.cropped_image_data = edit_func()  # Apply the edit and update the cropped image
            update_crop_display()

        def undo_crop_edit():
            """
            Undoes the last edit applied to the cropped image.
            """
            if undo_stack:
                redo_stack.append(self.cropped_image_data.copy())
                self.cropped_image_data = undo_stack.pop()
                update_crop_display()

        def redo_crop_edit():
            """
            Redoes the last undone edit applied to the cropped image.
            """
            if redo_stack:
                undo_stack.append(self.cropped_image_data.copy())
                self.cropped_image_data = redo_stack.pop()
                update_crop_display()

        def update_crop_display():
            """
            Updates the display of the cropped image in the crop window.
            """
            self.cropped_image = ImageTk.PhotoImage(self.cropped_image_data)
            crop_canvas.delete("all")
            crop_canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_image)
            crop_canvas.image = self.cropped_image  # Keep a reference to avoid garbage collection

        def crop_to_grayscale():
            """
            Converts the cropped image to grayscale.
            """
            apply_edit(lambda: self.cropped_image_data.convert("L"))

        def crop_adjust_brightness(value):
            """
            Adjusts the brightness of the cropped image.
            - value: The brightness factor (0.1 to 2.0).
            """
            factor = float(value)
            apply_edit(lambda: ImageEnhance.Brightness(original_cropped_image).enhance(factor))

        def crop_rotate_image():
            """
            Rotates the cropped image by 90 degrees.
            """
            apply_edit(lambda: self.cropped_image_data.rotate(90, expand=True))

        def crop_resize_image(value):
            """
            Resizes the cropped image based on the slider value.
            - value: The resize factor (0.1 to 2.0).
            """
            factor = float(value)
            apply_edit(lambda: original_cropped_image.resize(
                (int(original_cropped_image.width * factor),
                 int(original_cropped_image.height * factor)),
                Image.LANCZOS))

        def save_cropped_image():
            """
            Saves the cropped image to the user's local device.
            """
            if not self.cropped_image_data:
                messagebox.showerror("Error", "No cropped image to save.")
                return
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
                                                     parent=crop_window)
            if save_path:
                try:
                    self.cropped_image_data.save(save_path, quality=95)
                    messagebox.showinfo("Success", "Image saved successfully by G37 Image Editor ", parent=crop_window)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")

        # Buttons for editing cropped image
        tk.Button(crop_window, text="Grayscale", command=crop_to_grayscale).pack()
        tk.Button(crop_window, text="Rotate", command=crop_rotate_image).pack()
        tk.Button(crop_window, text="Save", command=save_cropped_image).pack()
        tk.Button(crop_window, text="Undo", command=undo_crop_edit).pack()
        tk.Button(crop_window, text="Redo", command=redo_crop_edit).pack()

        # Resize slider for cropped image
        resize_slider = tk.Scale(crop_window, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                 label="Resize Image", command=crop_resize_image)
        resize_slider.set(1)  # Default resize image factor
        resize_slider.pack()

        # Brightness slider for cropped image
        brightness_slider = tk.Scale(crop_window, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                      label="Brightness", command=crop_adjust_brightness)
        brightness_slider.set(1)  # Default brightness
        brightness_slider.pack()


# Bind the close event to custom function for confirmation
        crop_window.protocol("WM_DELETE_WINDOW", self.on_close_crop_window(crop_window))

    def on_close_crop_window(self, crop_window):
        def confirm_close():
            if self.custom_messagebox(crop_window):
                crop_window.destroy()
        return confirm_close

    def custom_messagebox(self, parent_window):
        # Custom message box with 'Save' and 'Don't Save' buttons
        msg_box = tk.Toplevel(parent_window)
        msg_box.title("Save Changes")
        msg_box.geometry("300x150")

        message = tk.Label(msg_box, text="Please make sure your image has been saved with all the edited changes.", wraplength=250)
        message.pack(pady=20)

        # Custom 'Save' and 'Don't Save' buttons
        def on_save():
            msg_box.destroy()
            return True  # Allows window to close

        def on_dont_save():
            msg_box.destroy()
            return False  # Prevents window from closing

        save_button = tk.Button(msg_box, text="Saved", command=on_save)
        save_button.pack(side="left", padx=20, pady=10)

        dont_save_button = tk.Button(msg_box, text="No Need", command=on_dont_save)
        dont_save_button.pack(side="right", padx=20, pady=10)

        msg_box.transient(parent_window)  # Makes the message box stay on top of the parent window
        msg_box.grab_set()  # Ensures the user interacts only with this dialog

        parent_window.wait_window(msg_box)  # Wait for the message box to close
        return True  # Default return value; change after user interaction
    
    def load_image_shortcut(self, event):
        """
        Handles the keyboard shortcut (Ctrl+O) for loading an image.
        """
        self.load_image()
