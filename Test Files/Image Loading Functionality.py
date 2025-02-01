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
