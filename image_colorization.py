# pylint: disable=line-too-long
# pylint: disable=C0303
# pylint: disable=C0103
# pylint: disable=R0903
# pylint: disable=E1101

"""System module."""
import sys
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2

root = tk.Tk()
root.withdraw()

class ImageColorization:
    """
    This class creates an image object that requires the following parameters
    to function:
    --------------------------------------------------------------------------------
    [1] Image Input File Path
    [2] Image Output Directory Path
    [3] Image File Name

    The following are the methods that can be performed on an instance of this class:

    [1] convert_bw_to_colorized
    """
    def __init__(self,image_input_file_path,image_output_dir_path,image_file_name):

        self.image_input_file_path = image_input_file_path
        self.image_output_dir_path = image_output_dir_path
        self.image_file_name = image_file_name

    def convert_bw_to_colorized(self):
        # ! Do a complete fact check of the following docstring before pushing.

        """
        This function does the following task:
        -----------------------------------------------

        [1] Reads the input image file
        [2] Changes the size of the image for color precision. 
        [3] Changes the size back to normal after colorization.
        """

        # Time complexity : O(1)
        image = cv2.imread(self.image_input_file_path)
        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)

        colorized = (255 * colorized).astype("uint8")

        output_path = f"{self.image_output_dir_path}/{self.image_file_name}"

        print("-" * 70)
        print(f"Saved {self.image_file_name} to {output_path}.")
        print("-" * 70)
        
        cv2.imwrite(output_path,colorized)

def open_gui_for_individual_file_paths():
    """
    This function does the following tasks:
    -------------------------------------------------

    [1] Opens a File Dialog Box GUI for user to select the image file/files.

    [2] Returns the image file path/paths. [Output Format > List]

    """
    # Time complexity : O(1)
    filetypes = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.tiff",
        "*.tif",
        "*.gif",
        "*.ico",
        "*.webp",
    ]

    filetypes_displayed_in_gui = (("Image Files", filetypes),)
    image_input_file_paths = list(
        filedialog.askopenfilenames(
            title="Select Image File/Files", filetypes=filetypes_displayed_in_gui
        )
    )

    if image_input_file_paths:
        return image_input_file_paths

    print("-" * 70)
    print("\n\nNo files were selected\n\n")
    print("-" * 70)
    sys.exit()

def open_gui_for_output_directory_path():
    """
    This function does the following task:
    --------------------------------------------------

    [1] Opens a File Dialog Box GUI for user to select the
    output directory for the compressed image/images. [Output Format > String]

    """
    # Time complexity : O(1)
    output_image_directory_path =   filedialog.askdirectory(title="Save To")

    # The following code checks if the user selected an output path,
    # if the user selects no output path, then it saves the image to a default path
    # Default Path : Pictures folder for any operating system (Windows,Linux,MacOS)
    if output_image_directory_path:
        return output_image_directory_path

    pictures_folder = os.path.join(os.path.expanduser("~"), "Pictures")
    # The following replaces "\" from the tkinter path, and replaces it with "/" as good practice for path naming conventions.
    pictures_folder = pictures_folder.replace("\\", "/")

    print("-" * 70)
    print("\n\nNo output path selected.")
    print(f'By default, image will be stored at "{pictures_folder}".\n\n')
    print("-" * 70)
    return pictures_folder

prototx_path = './models/colorization_deploy_v2.prototxt'
model_path = './models/colorization_release_v2.caffemodel'
kernel_path = './models/pts_in_hull.npy'

net = cv2.dnn.readNetFromCaffe(prototx_path, model_path)
pts = np.load(kernel_path)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def main():
    """
    This function does the following tasks :
    --------------------------------------------------

    [1] Gets the image input file path/paths [format > List]
    [2] Reads the output directory path [format > String]

    [3] Uses a for loop to extract the path from the image input file path list.
    [4] Gets the filename from the path.
    [5] Uses the ImageColorization class to create an instance.
    [6] Converts the black and white image to colored and saves it.
    
    """
    # Time complexity : O(n + 1)
    image_paths = open_gui_for_individual_file_paths()
    image_output_dir_path = open_gui_for_output_directory_path()

    for path in image_paths:
        image_file_name = os.path.basename(path)
        image_file = ImageColorization(path,image_output_dir_path,image_file_name)
        image_file.convert_bw_to_colorized()

def execute():
    """
    This function executes the entire program.
    """
    # Time complexity : O(1)
    try:
        main()
    # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    except KeyboardInterrupt:
        sys.exit()
