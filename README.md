# HIT137 Assignment 3 - Image Editor

## Group Members
- Harsh Rastogi
- Kazi Rubaiyat Islam
- Rashedul Islam Jisan
- Robiul Islam

---

## Project Description
This project is a desktop image editor developed using Python, Tkinter for the GUI, and Pillow (PIL) for image processing. The application allows users to:

1. Load images from their local device.
2. Crop images using mouse interaction.
3. Resize images using a slider.
4. Apply additional image processing features like grayscale conversion, brightness adjustment, and rotation.
5. Save the edited images.

The project demonstrates our understanding of Object-Oriented Programming (OOP) principles, GUI development, and image processing.

---

## Team Contributions

### Team Member 1 : Harsh Rastogi
#### Responsibilities:
- Created the base structure of the application.
- Set up the main window using Tkinter.
- Added the canvas for displaying images.
- Implemented the "Load Image" button and its functionality.
- Added a label to display the names of the contributors.
- Set up the GitHub repository and added all team members as collaborators.

#### Code Overview:
- The `ImageEditor` class is the main class that initializes the application window.
- The `load_image` method allows users to select and load an image from their local device.
- The `resize_to_fit` method ensures the loaded image fits within the canvas while maintaining its aspect ratio.

---

### Team Member 2 : Robiul Islam
#### Responsibilities :
- Implemented the image loading functionality.
- Added the ability to display the loaded image on the canvas.
- Set up mouse event handlers for cropping functionality.

#### Code Overview :
- The `load_image` method uses `filedialog` to allow users to select an image file.
- The `resize_to_fit` method resizes the image to fit the canvas without distortion.
- Mouse events (`<ButtonPress-1>`, `<B1-Motion>`, `<ButtonRelease-1>`) are bound to the canvas to enable cropping.

---

### Team Member 3: Rashedul Islam Jisan
#### Responsibilities :
- Implemented the image cropping functionality.
- Added real-time visual feedback for the cropping area.
- Created a new window to display the cropped image.

#### Code Overview :
- The `on_mouse_press`, `on_mouse_drag`, and `on_mouse_release` methods handle mouse interactions for cropping.
- The `open_crop_window` method opens a new window to display the cropped image.
- The cropped image is displayed alongside the original image for comparison.

---

### Team Member 4 : Kazi Rubaiyat Islam
#### Responsibilities:
- Implemented image resizing using a slider.
- Added image processing features like grayscale conversion, brightness adjustment, and rotation.
- Implemented undo/redo functionality for edits.
- Added the ability to save the edited image.

#### Code Overview :
- The `crop_resize_image` method allows users to resize the cropped image using a slider.
- The `crop_to_grayscale`, `crop_adjust_brightness`, and `crop_rotate_image` methods provide additional image processing features.
- The `undo_crop_edit` and `redo_crop_edit` methods allow users to undo or redo their edits.
- The `save_cropped_image` method saves the edited image to the user's local device.

---

## Repository Structure
