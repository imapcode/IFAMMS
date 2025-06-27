# pylint: disable=line-too-long
"""System Module"""
import sys  # USE CASE: Forcefully exiting the program while in use.
import tkinter as tk  # USE CASE: GUI for users preferred I/O Paths.
from tkinter import filedialog  # USE CASE: GUI for users preferred I/O Paths.
import os  # USE CASE: Read file names.
from PIL import Image  # USE CASE: Performing image conversions for majority formats.
from PIL import UnidentifiedImageError  # USE CASE: Error handling for corrupted files.

root = tk.Tk()
root.withdraw()


def validate_input(func):
    """
    This decorator does the following tasks:
    ----------------------------------------------------

    [1] Validates user input to prevent any errors caused by it
    in between the program.

    [2] Returns an image_height and an image_width for resizing the image.
    """

    def user_preferred_image_dimensions_input():
        # Time complexity : O(1)
        header = "\n\n" + "-" * 70 + "\n\n"
        try:
            image_height = int(
                input(
                    """
    
Please enter the image height :
--------------------------------------------------------

Height (in pixels) : """
                ).strip()
            )
            image_width = int(
                input(
                    """
    
Please enter the image width :
--------------------------------------------------------

Width (in pixels) : """
                ).strip()
            )

            if image_height == 0 or image_width == 0:
                print(header)
                print("Warning : Height or Width can not be 0")
                print(header)
                return user_preferred_image_dimensions_input()

            image_dimensions = (image_height, image_width)
            return func(image_dimensions)

        # Checks for value errors, i.e :
        # >>> string input like : a,b,c,word,@,#,',"",etc.

        except ValueError:
            print(header)
            print("Please try again with a valid input")
            print(header)
            return user_preferred_image_dimensions_input()

        # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
        except KeyboardInterrupt:
            sys.exit()

    return user_preferred_image_dimensions_input


@validate_input
def get_image_dimensions(image_dimensions=None):
    """
    This function does the following task:
    --------------------------------------------
    It reads the user's preferred image width and image height.
    """
    # Time complexity : O(1)
    return image_dimensions


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
    output directory for the resized image/images. [Output Format > String]

    """
    # Time complexity : O(1)
    output_image_directory_path = filedialog.askdirectory(title="Save To")

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


class ImageResize:
    """
    This class creates an image object that requires the following parameters
    to function:
    --------------------------------------------------------------------------------
    [1] Image Input File Path
    [2] Image Output Directory Path
    [3] Output Image Dimensions
    [4] Image File Name

    The following are the methods that can be performed on an instance of this class:

    [1] get_image_file_type
    [2] resize_image_file
    """

    def __init__(
        self,
        image_input_file_path,
        image_output_dir_path,
        img_size,
        image_file_name,
    ):
        self.image_input_file_path = image_input_file_path
        self.image_output_dir_path = image_output_dir_path
        self.image_file_extension = os.path.splitext(self.image_input_file_path)[
            1
        ].lower()
        self.img_size = img_size
        self.image_file_name = image_file_name

    def get_image_file_type(self):
        """
        This function does the following task:
        ----------------------------------------------

        It reads the input image file and returns the image filetype.
        This is later used to save the resized image.
        """
        # Time complexity : O(1)
        with Image.open(self.image_input_file_path) as img:
            image_file_type = str(img.format)
            return image_file_type

    def resize_image_file(self):
        """
        This function does the following task:
        ----------------------------------------------

        [1] Creates an output path for the resized image file.
        [2] Reads the output size for the image from the get_image_dimensions() function.
        [3] Saves the resized image file to the output path.
        """
        # Time complexity : O(1)
        output_path = f"{self.image_output_dir_path}/{self.image_file_name}"
        with Image.open(self.image_input_file_path) as img:
            resized_img = img.resize(self.img_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path, self.get_image_file_type())
            print("-" * 70)
            print(f"Saved {self.image_file_name} to {output_path}.")
            print("-" * 70)


def main():
    """
    This function does the following tasks :
    --------------------------------------------------

    [1] Reads the image dimensions [format > Tuple]
    [2] Gets the image input file path/paths [format > List]
    [3] Reads the output directory path [format > String]

    [4] Uses a for loop to extract the path from the image input file path list.
    [5] Gets the filename from the path.
    [6] Uses the ImageResize class to create an instance.
    [7] Checks the image file type and resizes the image.
    """
    # Time complexity : O(n + 1)
    img_size = get_image_dimensions()
    image_input_file_paths = open_gui_for_individual_file_paths()
    image_output_directory_path = open_gui_for_output_directory_path()
    for path in image_input_file_paths:
        image_file_name = os.path.basename(path)
        image_file = ImageResize(
            path, image_output_directory_path, img_size, image_file_name
        )
        try:
            image_file.resize_image_file()

        # This error is raised in heavy operations(for e.g. width and height of 200000000).
        # This error is raised when memory runs out of space for allocation of this program.
        except MemoryError:
            print(
                "Failed to resize image. Please try again with a valid image height and width"
            )
            return main()

        # This error is raised when file is corrupted.
        # It is also applicable to files with unknown extension (which is not likely since we handle that possibility early in the input file selection gui itself.)
        except UnidentifiedImageError:
            print("-" * 70)
            print(f"\n\n{image_file_name} failed to convert.")
            print("This could be because the file is corrupted.\n\n")
            print("-" * 70)

        # This error is raised when the input image file is modified or deleted while the program is running.
        except FileNotFoundError:
            print("-" * 70)
            print(f"{image_file_name} failed to convert.")
            print("This could be because the file was modified during conversion.")
            print("-" * 70)

        # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
        except KeyboardInterrupt:
            sys.exit()

    return None


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
