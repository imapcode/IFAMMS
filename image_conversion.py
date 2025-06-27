# pylint: disable=line-too-long
# pylint: disable=C0303
"""System module."""
import sys  # USE CASE: Forcefully exiting the program while in use.
import tkinter as tk  # USE CASE: GUI for users preferred I/O Paths.
from tkinter import filedialog  # USE CASE: GUI for users preferred I/O Paths.
import os  # USE CASE: Read file names.
from PIL import Image  # USE CASE: Performing image conversions for majority formats.
from PIL import UnidentifiedImageError  # USE CASE: Error handling for corrupted files.

# Moderation : Discontinuing the following libraries and all related functions due to closed maintanance.
#---------------------------------------------------------------------------------------------
# from psd_tools import PSDImage  # USE CASE: Performing image conversions for PSD files.
# import cairosvg  # USE CASE: Performing image conversions for SVG files.
# import rawpy  # USE CASE: Performing image conversions for RAW files
#---------------------------------------------------------------------------------------------
import image_file_configurations  # USE CASE: Contains all configurations for image_conversions.


root = tk.Tk()
root.withdraw()


def validate_input(func):
    """
    This decorater does the following tasks :
    ------------------------------------------------------------

    [1] Validates user input to prevent any errors caused by it
    in between the program.

    [2] Displays the possible image conversion by reading
    "Conversion Titles" from image_file_configurations.py.

    [3] Returns a conversion index to access
    an image files configuration. [Outupt Format > Integer]

    """

    def user_preffered_image_conversion_input():
        # Prints the possible image conversions read from image_file_configuration.py
        # Time Complexity : O(n)
        print("\n")
        for count, title in enumerate(
            image_file_configurations.configurations.values()
        ):
            print(f"[{count + 1}] {title['conversion_title']}")

        try:
            header = "\n\n" + "-" * 70 + "\n\n"

            conversion_idx_input = int(
                input("\n\nSelect from the above options : ").strip()
            )

            if conversion_idx_input in image_file_configurations.configurations:
                return func(conversion_idx_input)

            if conversion_idx_input not in image_file_configurations.configurations:
                print(header)
                print("Please try again with a valid input")
                print(header)
                return user_preffered_image_conversion_input()

            return None

        # Checks for value errors, i.e :
        # >>> string input like : a,b,c,word,@,#,',"",etc.

        except ValueError:
            print(header)
            print("Please try again with a valid input")
            print(header)
            return user_preffered_image_conversion_input()

        # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
        except KeyboardInterrupt:
            sys.exit()

    return user_preffered_image_conversion_input


@validate_input
def read_file_configuration(configuration_idx=None):
    """
    This function does the following task:
    ---------------------------------------------

    [1] Reads coniguration_idx from user_input and returns the respective
    image file configuration. [Output Format > Dictionary]

    """
    # Time complexity : O(1)
    configuration = image_file_configurations.configurations[configuration_idx]
    return configuration


def open_gui_for_input_file_path(image_file_configuration):
    """
    This function does the following tasks:
    -----------------------------------------------

    [1] Reads the expected input file type from the image configuration
    returned from the function "read_file_configuration()".

    [2] Opens a File Dialog Box GUI for user to select the image file/files.

    [3] Returns the image file path/paths. [Output Format > List]

    """
    # Time complexity : O(1)
    input_file_extension = image_file_configuration["filetype"]
    filetypes_displayed_in_gui = (
        (f"Image Files ({input_file_extension})", input_file_extension),
    )

    image_input_file_paths = list(
        filedialog.askopenfilenames(
            title="Select Image File/Files", filetypes=filetypes_displayed_in_gui
        )
    )
    # The following checks if user has selected any file. If user selects no file, the program exits itself.
    if image_input_file_paths:
        return image_input_file_paths

    print("-" * 70)
    print("\n\nNo Image File Selected\n\n")
    print("-" * 70)
    sys.exit()


def open_gui_for_output_directory_path():
    """
    This function does the following task:
    --------------------------------------------------

    [1] Opens a File Dialog Box GUI for user to select the
    output directory for the converted image/images. [Output Format > String]

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


class ImageConversion:
    """
    This class creates an image object that requires the following parameters
    to function:
    ----------------------------------------------------------------------------
    [1] Image Input File Path
    [2] Image Output Directory Path
    [3] Image File Name
    [4] Image File Configuration


    The following are the methods that can be performed on an instance of
    this class:
    ----------------------------------------------------------------------------

    [1] normal_image_conversion
    [2] psd_image_conversion
    [2] svg_image_conversion
    [2] raw_image_conversion

    NOTE : The methods above are applicable to their respective instances only,
    i.e, normal image files like .jpg, .png, .gif, etc. can't use the method psd_conversion
    and vice versa.

    """

    def __init__(
        self,
        image_input_file_path,
        image_output_directory_path,
        image_file_name,
        image_configuration,
    ):
        """
        This is a constructor method that requires the following attributes:
        -------------------------------------------------------------------------

        [1] Image Input File Path [format > String]
        [2] Image Output Directory Path [format > String]
        [3] Image File Name [format > String]
        [4] Image Configuration [format > Dictionary]

        Using these attributes required by the constructor methods, the following
        attributes are declared:
        --------------------------------------------------------------------------

        [1] Output Path For Saving [format > String]
        [2] Output Path For Saving SVG Conversions [format > String]
        [3] Output Path For Saving RAW Conversion [format > String]


        Please Note :
        ---------------
        It is easy to confuse the "Output Path For Saving" with the
        required attribute "Image Output Directory Path",
        however both are different, the "Output Path For Saving" is the output
        path for the converted image file whereas, the "Image Output Directory Path"
        is of the directory, the converted image/images will be saved in.

        """
        self.image_input_file_path = image_input_file_path
        self.image_output_directory_path = image_output_directory_path
        self.image_file_name = image_file_name
        self.image_configuration = image_configuration
        self.output_path_for_saving = rf"{self.image_output_directory_path}/{os.path.splitext(self.image_file_name)[0]}{self.image_configuration['conversion_extension']}"
        self.output_path_for_saving_svg_conversions = rf"{self.image_output_directory_path}/{os.path.splitext(self.image_file_name)[0]}.png"
        self.output_path_for_saving_raw_conversions = rf"{self.image_output_directory_path}/{os.path.splitext(self.image_file_name)[0]}{self.image_configuration['conversion_extension']}"

    def normal_image_conversion(self):
        """
        This method converts images to formats that are supported by
        Pillow :
        -----------------------------------------------------------------
        [1] JPEG to PNG
        [2] PNG to JPEG
        [3] BMP to GIF
        [4] TIFF to JPEG
        [5] GIF to PNG
        [6] ICO to PNG
        [7] ICO to JPEG
        [8] WebP to PNG
        [9] WebP to JPEG
        [10] PNG to ICO
        [11] JPEG to ICO
        [12] PNG to WebP
        [13] JPEG to WebP


        Please Note:
        -------------
        There are certain formats remaining that can be converted via pillow,
        but haven't been converted using it due to availability of better
        and more suitable alternate libraries.
        """
        # Time complexity : O(1)
        with Image.open(self.image_input_file_path) as img:
            # Checks the image for alpha channel
            if "P" in img.mode:
                img = img.convert("RGB")
            elif "A" in img.mode:
                # Merges the alpha image with a white background.
                # This is done, so any transparent parts are filled with white color before conversion
                try:
                    background = Image.new("RGB", img.size, "white")
                    background.paste(img, mask=img)
                    img = background

                # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
                except KeyboardInterrupt:
                    print("Sorry there was an error")
                    sys.exit()                


            img.save(self.output_path_for_saving)
            print("-" * 70)
            print(f"Saved {self.image_file_name} to {self.output_path_for_saving}")
            print("-" * 70)

    # def psd_image_conversion(self):
    #     """
    #     This method converts PSD Images to PNG or JPEG file formats.
    #     """
    #     # Time complexity : O(1)
    #     try:
    #         psd_img = PSDImage.open(self.image_input_file_path)
    #         psd_img.composite().save(
    #             self.output_path_for_saving, self.image_configuration["conversion_type"]
    #         )
    #         print("-" * 70)
    #         print(f"Saved {self.image_file_name} to {self.output_path_for_saving}")
    #         print("-" * 70)

    #     # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    #     except KeyboardInterrupt:
    #         print("Sorry there was an error")
    #         sys.exit()

    # def svg_image_conversion(self):
    #     """
    #     This method converts SVG Images to PNG or JPEG file formats.
    #     """
    #     # Time complexity : O(1)
    #     cairosvg.svg2png(
    #         url=self.image_input_file_path,
    #         write_to=self.output_path_for_saving_svg_conversions,
    #     )

    #     if self.image_configuration["conversion_type"] == "JPEG":
    #         self.image_input_file_path = self.output_path_for_saving_svg_conversions
    #         self.normal_image_conversion()
    #         os.remove(self.output_path_for_saving_svg_conversions)

    #     else:
    #         print("-" * 70)
    #         print(
    #             f"Saved {self.image_file_name} to {self.output_path_for_saving_svg_conversions}"
    #         )
    #         print("-" * 70)

    # def raw_image_conversion(self):
    #     """
    #     This method converts RAW Images to PNG or JPEG file formats.
    #     """
    #     # Time complexity : O(1)
    #     try:
    #         with rawpy.imread(self.image_input_file_path) as raw_img:
    #             try:
    #                 rgb = raw_img.postprocess()
    #                 raw_img = Image.fromarray(rgb)
    #                 raw_img.save(self.output_path_for_saving_raw_conversions)
    #                 print("-" * 70)
    #                 print(
    #                     f"Saved {self.image_file_name} to {self.output_path_for_saving_raw_conversions}"
    #                 )
    #                 print("-" * 70)

    #             # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    #             except KeyboardInterrupt:
    #                 print("Sorry there was an error")
    #                 sys.exit()

    #     # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    #     except KeyboardInterrupt:
    #         print("Sorry there was an error")
    #         sys.exit()


def main():
    """
    This function performs the following tasks:
    ------------------------------------------------------

    [1] Reads the image file configuration [format > Dictionary]
    [2] Gets the image input file path/paths [format > List]
    [3] Reads the output directory path [format > String]

    [4] Uses a for loop to extract the path from the image input file path list.
    [5] Gets the filename from the path.
    [6] Uses the ImageConversion class to create an instance.
    [7] Checks the image file type to perform the respective conversion.

    """

    # Time complexity : O(n)
    # The following are the parameters required by the image_file class.
    image_file_configuration = read_file_configuration()
    image_input_file_paths = open_gui_for_input_file_path(image_file_configuration)
    image_output_directory_path = open_gui_for_output_directory_path()

    for path in image_input_file_paths:
        image_file_name = os.path.basename(
            path
        )  # Gets the filename from the original image path
        image_file = ImageConversion(
            path,
            image_output_directory_path,
            image_file_name,
            image_file_configuration,
        )

        # The following conditional logic is to check the original image's filetype and checks if file is corrupted
        try:
            if image_file_configuration["filetype"] == "*.psd":
                image_file.psd_image_conversion()
            elif image_file_configuration["filetype"] == "*.svg":
                image_file.svg_image_conversion()
            elif image_file_configuration["filetype"] == "*.raw;*.arw;*.dng":
                image_file.raw_image_conversion()
            else:
                image_file.normal_image_conversion()

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
