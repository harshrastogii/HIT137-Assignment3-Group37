import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")

        # Image variables
        self.original_image = None
        self.display_image = None
        self.image_path = None
        self.cropped_image = None
        self.cropped_image_data = None
        self.undo_stack = []
        self.redo_stack = []

        # Canvas for image display
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load Image Button
        self.load_button = tk.Button(self, text="Load Image", command=self.load_image)
        self.load_button.pack()

        # For cropping functionality
        self.rect = None
        self.start_x = self.start_y = 0

        # For displaying cropped image
        self.cropped_image_label = tk.Label(self, text="Cropped Image:")
        self.cropped_image_label.pack()

        # Slider for resizing cropped image
        self.resize_slider = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL, label="Resize Factor")
        self.resize_slider.set(1)  # Default resize factor
        self.resize_slider.pack()
        self.resize_slider.bind("<Motion>", self.resize_image)

        # Save Button
        self.save_button = tk.Button(self, text="Save Image", command=self.save_image)
        self.save_button.pack()

        # Undo/Redo Buttons
        self.undo_button = tk.Button(self, text="Undo", command=self.undo_action)
        self.undo_button.pack()
        self.redo_button = tk.Button(self, text="Redo", command=self.redo_action)
        self.redo_button.pack()

        # Rotate Button
        self.rotate_button = tk.Button(self, text="Rotate Image", command=self.rotate_image)
        self.rotate_button.pack()

        # Bind keyboard shortcuts (Ctrl+S for save)
        self.bind("<Control-s>", self.save_image_shortcut)

    def load_image(self):
        """Loads an image and displays it on the canvas."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return
        self.image_path = file_path
        self.original_image = Image.open(file_path)
        
        # Rescale the image to fit within the canvas while maintaining aspect ratio
        self.display_image = self.resize_to_fit(self.original_image, self.canvas.winfo_width(), self.canvas.winfo_height())
        
        # Display the scaled image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

        # Reset cropping rectangle
        self.canvas.delete(self.rect)
        self.rect = None

        # Set up mouse event for cropping
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def resize_to_fit(self, image, max_width, max_height):
        """Resize the image to fit within the given dimensions, maintaining aspect ratio."""
        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        return ImageTk.PhotoImage(image.resize((new_width, new_height), Image.LANCZOS))

    def on_mouse_press(self, event):
        """Captures the initial position of the mouse."""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        """Updates the rectangle while dragging the mouse."""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        """Crops the image and displays the result."""
        # Scale crop box to original image resolution
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_width, img_height = self.original_image.size
        scale_x = img_width / canvas_width
        scale_y = img_height / canvas_height

        # Scale the crop coordinates back to original resolution
        crop_box = (
            int(self.start_x * scale_x),
            int(self.start_y * scale_y),
            int(event.x * scale_x),
            int(event.y * scale_y)
        )

        self.cropped_image_data = self.original_image.crop(crop_box)
        self.cropped_image = ImageTk.PhotoImage(self.cropped_image_data)

        # Display full image in the background and cropped image on top without overlap
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)  # Show the full image again
        self.canvas.create_image(self.start_x, self.start_y, anchor=tk.NW, image=self.cropped_image)
        
        # Display cropped image label
        self.cropped_image_label.config(text="Cropped Image: [Click to resize and save]")

        # Save the action for undo
        self.undo_stack.append(('crop', crop_box))
        self.redo_stack.clear()  # Clear redo stack on new action

    def resize_image(self, event=None):
        """Resizes the cropped image based on the slider value."""
        if self.cropped_image:
            resize_factor = self.resize_slider.get()
            cropped_image = self.cropped_image_data
            width, height = cropped_image.size
            new_size = (int(width * resize_factor), int(height * resize_factor))
            resized_image = cropped_image.resize(new_size, Image.LANCZOS)
            self.cropped_image = ImageTk.PhotoImage(resized_image)

            # Re-display both full and resized cropped images
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)  # Show full image
            self.canvas.create_image(self.start_x, self.start_y, anchor=tk.NW, image=self.cropped_image)

            # Save the action for undo
            self.undo_stack.append(('resize', resize_factor))
            self.redo_stack.clear()  # Clear redo stack on new action

    def save_image(self, event=None):
        """Save the cropped or original image."""
        if self.cropped_image_data:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                # Save cropped image in its original resolution with high quality
                self.cropped_image_data.save(save_path, quality=95)  # Use a high-quality setting
                messagebox.showinfo("Success", "Image saved successfully.")
        else:
            messagebox.showerror("Error", "No cropped image to save.")

    def save_image_shortcut(self, event=None):
        """Save the image using Ctrl+S keyboard shortcut."""
        self.save_image()

    def undo_action(self):
        """Undo the last action."""
        if not self.undo_stack:
            return  # No actions to undo
        last_action, data = self.undo_stack.pop()
        if last_action == 'crop':
            # Undo crop
            self.canvas.delete(self.rect)
            self.rect = None
            self.cropped_image_data = None
            self.cropped_image = None
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)  # Reload original image
        elif last_action == 'resize':
            # Undo resize by resetting to original size
            self.cropped_image = ImageTk.PhotoImage(self.cropped_image_data)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_image)
        self.redo_stack.append((last_action, data))

    def redo_action(self):
        """Redo the last undone action."""
        if not self.redo_stack:
            return  # No actions to redo
        last_action, data = self.redo_stack.pop()
        if last_action == 'crop':
            # Redo crop
            self.start_x, self.start_y, self.end_x, self.end_y = data
            self.on_mouse_release(None)
        elif last_action == 'resize':
            # Redo resize
            self.resize_slider.set(data)
            self.resize_image()

    def rotate_image(self):
        """Rotate the image."""
        if self.cropped_image_data:
            rotated_image = self.cropped_image_data.rotate(90, expand=True)
            self.cropped_image_data = rotated_image
            self.cropped_image = ImageTk.PhotoImage(rotated_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_image)

            # Save the action for undo
            self.undo_stack.append(('rotate', None))
            self.redo_stack.clear()  # Clear redo stack on new action

if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()