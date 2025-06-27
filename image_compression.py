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

    [2] Returns a compression_amount for the image compression.
    """

    def user_preferred_image_compression_input():
        # Time complexity : O (1)
        header = "\n\n" + "-" * 70 + "\n\n"
        try:
            compression_amount_input = int(
                input(
                    """
    
Please select the amount of compression you want to apply 
----------------------------------------------------------------

[1] Low Image Compression (Reduces image quality very slightly)

[2] Mid Image Compression (Reduces image quality tolerably)

[3] High Image Compression (Reduces image quality significantly)

[4] Very High Compression (Reduces image quality by a lot)

[5] Custom 


Select from the above options: """
                ).strip()
            )

            while compression_amount_input not in [1, 2, 3, 4,5]:
                print(header)
                print("Please try again with a valid input")
                print(header)
                return user_preferred_image_compression_input()

            return func(compression_amount_input)

        # Checks for value errors, i.e :
        # >>> string input like : a,b,c,word,@,#,',"",etc.
        except ValueError:
            print(header)
            print("Please try again with a valid input")
            print(header)
            return user_preferred_image_compression_input()

        # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
        except KeyboardInterrupt:
            sys.exit()

    return user_preferred_image_compression_input


@validate_input
def get_compression_quality(compression_quality=None):
    """
    This function does the following task:
    --------------------------------------------

    It reads the user's preferred compression quality and respectively
    outputs a quality suitable for the user's compression needs.
    """
    # Time complexity : O(1)
    if compression_quality in [1,2,3,4]:
        quality_config = {
            1: {"quality": 75},
            2: {"quality": 50},
            3: {"quality": 25},
            4: {"quality": 5},
        }
        compression_quality = quality_config[compression_quality]["quality"]
        
    else:
        compression_quality = int(input("""
\n\n
1.Very high quality lies between 75 - 90.
------------------------------------------ 
2.Average quality lies between 40 - 75.
------------------------------------------
3.Decent quality lies between 25 - 40.
------------------------------------------
4.Poor quality lies below 25. 


>> Add your custom compression quality : """))
        


    return compression_quality


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


class ImageCompression:
    """
    This class creates an image object that requires the following parameters
    to function:
    --------------------------------------------------------------------------------
    [1] Image Input File Path
    [2] Image Output Directory Path
    [3] Image Compression Quality
    [4] Image File Name

    The following are the methods that can be performed on an instance of this class:

    [1] get_image_file_type
    [2] compress_image_file
    """

    def __init__(
        self,
        image_input_file_path,
        image_output_dir_path,
        compression_quality,
        image_file_name,
    ):
        self.image_input_file_path = image_input_file_path
        self.image_output_dir_path = image_output_dir_path
        self.image_file_extension = os.path.splitext(self.image_input_file_path)[
            1
        ].lower()
        self.image_file_name = image_file_name
        self.compression_quality = compression_quality

    def get_image_file_type(self):
        """
        This function does the following task:
        ----------------------------------------------

        It reads the input image file and returns the image filetype.
        This is later used to save the compressed image.
        """
        # Time complexity : O(1)
        with Image.open(self.image_input_file_path) as img:
            # Returns the image format ("JPEG","PNG","SVG",etc.)
            image_file_type = str(img.format)
            return image_file_type

    def compress_image_file(self):
        """
        This function does the following task:
        -----------------------------------------------

        [1] Creates an output path for the compressed file.
        [2] Reads the compression quality from the get_compression_quality() function.
        [3] Saves the compressed image file to the output path.
        """
        # Time complexity : O(1)
        output_path = f"{self.image_output_dir_path}/{self.image_file_name}"

        with Image.open(self.image_input_file_path) as img:
            img.save(
                output_path,
                self.get_image_file_type(),
                optimize=True,
                quality=self.compression_quality,
            )
            print("-" * 70)
            print(f"Saved {self.image_file_name} to {output_path}.")
            print("-" * 70)


def main():
    """
    This function does the following tasks :
    --------------------------------------------------

    [1] Reads the compression quality input [format > Integer]
    [2] Gets the image input file path/paths [format > List]
    [3] Reads the output directory path [format > String]

    [4] Uses a for loop to extract the path from the image input file path list.
    [5] Gets the filename from the path.
    [6] Uses the ImageCompression class to create an instance.
    [7] Checks the image file type and performs the image compression.
    """
    # Time complexity : O(n + 1)
    quality = get_compression_quality()
    image_input_file_paths = open_gui_for_individual_file_paths()
    image_output_directory_path = open_gui_for_output_directory_path()
    for path in image_input_file_paths:
        image_file_name = os.path.basename(path)
        image_file = ImageCompression(
            path, image_output_directory_path, quality, image_file_name
        )
        try:
            image_file.compress_image_file()

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
