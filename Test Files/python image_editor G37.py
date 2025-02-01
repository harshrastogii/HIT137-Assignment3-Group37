import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance


class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor - CDU CAS/DAN Group 37")

        # Image variables
        self.original_image = None
        self.display_image = None
        self.image_path = None
        self.cropped_image = None
        self.cropped_image_data = None

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
        self.rect = None
        self.start_x = self.start_y = 0

        # Bind keyboard shortcuts
        self.bind("<Control-o>", self.load_image_shortcut)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return
        self.image_path = file_path
        self.original_image = Image.open(file_path)

        # Rescale the image to fit within the canvas while maintaining aspect ratio
        self.display_image = self.resize_to_fit(self.original_image, self.canvas.winfo_width(), self.canvas.winfo_height())

        # Display the scaled image on the canvas
        self.canvas.image = self.display_image  # Keep a reference to avoid garbage collection
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        # Reset cropping rectangle
        self.canvas.delete(self.rect)
        self.rect = None

        # Set up mouse event for cropping
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def resize_to_fit(self, image, max_width, max_height):
        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        return ImageTk.PhotoImage(image.resize((new_width, new_height), Image.LANCZOS))

    def on_mouse_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_width, img_height = self.original_image.size
        scale_x = img_width / canvas_width
        scale_y = img_height / canvas_height

        # Ensure valid cropping coordinates
        x1 = max(0, min(self.start_x, event.x))
        y1 = max(0, min(self.start_y, event.y))
        x2 = max(0, max(self.start_x, event.x))
        y2 = max(0, max(self.start_y, event.y))

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

        def apply_edit(edit_func):
            nonlocal undo_stack, redo_stack  # Allow access to these variables
            undo_stack.append(self.cropped_image_data.copy())
            redo_stack.clear()  # Clear redo stack after a new edit
            self.cropped_image_data = edit_func()  # Apply the edit and update the cropped image
            update_crop_display()

        def undo_crop_edit():
            if undo_stack:
                redo_stack.append(self.cropped_image_data.copy())
                self.cropped_image_data = undo_stack.pop()
                update_crop_display()

        def redo_crop_edit():
            if redo_stack:
                undo_stack.append(self.cropped_image_data.copy())
                self.cropped_image_data = redo_stack.pop()
                update_crop_display()

        def update_crop_display():
            self.cropped_image = ImageTk.PhotoImage(self.cropped_image_data)
            crop_canvas.delete("all")
            crop_canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_image)
            crop_canvas.image = self.cropped_image  # Keep a reference to avoid garbage collection

        def crop_to_grayscale():
            apply_edit(lambda: self.cropped_image_data.convert("L"))

        def crop_adjust_brightness(value):
            factor = float(value)
            apply_edit(lambda: ImageEnhance.Brightness(original_cropped_image).enhance(factor))

        def crop_rotate_image():
            apply_edit(lambda: self.cropped_image_data.rotate(90, expand=True))

        def crop_resize_image(value):
            factor = float(value)
            apply_edit(lambda: original_cropped_image.resize(
                (int(original_cropped_image.width * factor),
                 int(original_cropped_image.height * factor)),
                Image.LANCZOS))

        def save_cropped_image():
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
                                                     parent=crop_window)
            if save_path:
                self.cropped_image_data.save(save_path, quality=95)
                messagebox.showinfo("Success", "Image saved successfully.", parent=crop_window)

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
        self.load_image()


if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()