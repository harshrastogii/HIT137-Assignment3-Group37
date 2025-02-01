from tkinter import Tk, filedialog, Button, Label
from PIL import Image, ImageTk

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:  # Ensure a file was selected
        try:
            image = Image.open(file_path)
            image.thumbnail((500, 500))  # Resize the image to fit
            photo = ImageTk.PhotoImage(image)

            # Update the label with the image
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to the image object
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text="Failed to load image.")
    else:
        print("No file selected.")

# Set up the main application window
root = Tk()
root.title("Image Editor")

# Set up the label for displaying images
image_label = Label(root)
image_label.pack()

# Set up the button to load images
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack()

root.mainloop()