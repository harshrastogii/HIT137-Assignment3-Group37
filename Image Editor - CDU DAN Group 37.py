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

