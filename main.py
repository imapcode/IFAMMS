# pylint: disable=line-too-long
# pylint: disable=C0413
"""System Module."""
import sys

# This is to add the image_file_configurations.py file to the path temporarily.
sys.path.append("./image_operations/")

from image_operations import (
    image_conversion,
    image_compression,
    image_resizing,
    image_manager
)

import image_colorization


print(
    """


██╗    ███████╗     █████╗     ███╗   ███╗    ███╗   ███╗    ███████╗
██║    ██╔════╝    ██╔══██╗    ████╗ ████║    ████╗ ████║    ██╔════╝
██║    █████╗      ███████║    ██╔████╔██║    ██╔████╔██║    ███████╗
██║    ██╔══╝      ██╔══██║    ██║╚██╔╝██║    ██║╚██╔╝██║    ╚════██║
██║    ██║         ██║  ██║    ██║ ╚═╝ ██║    ██║ ╚═╝ ██║    ███████║
╚═╝    ╚═╝         ╚═╝  ╚═╝    ╚═╝     ╚═╝    ╚═╝     ╚═╝    ╚══════╝
                                                                     

-----------------------------------------------------------------------"""
)


def user_preferred_application_input():
    """
    This function does the following tasks:
    ---------------------------------------------------

    [1] Asks the user for their preferred application.
    [2] Verifies user input to avoid any errors
    [3] Returns the user input [Output > Integer]
    """
    # Time complexity : O(1)
    try:
        print(
            """

            
Please select one of the following options:
-----------------------------------------------------


[1] Image Conversion

[2] Image Compression

[3] Image Resizing

[4] Image Colorization

[5] Image Management

        """
        )

        preferred_application_input = int(
            input("Please select one of the above options : ")
        )

        # Checks if the user's input is in [1,2,3]
        while preferred_application_input not in [1, 2, 3, 4, 5]:
            print("-" * 70)
            print("\n\nPlease try again with a valid input.\n\n")
            print("-" * 70)
            # Recalls the function for correct input
            return user_preferred_application_input()

        # Returns user's input
        return preferred_application_input

    # Checks for value errors, i.e :
    # >>> string input like : a,b,c,word,@,#,',"",etc.

    except ValueError:
        print("-" * 70)
        print("\n\nPlease try again with a valid input.\n\n")
        print("-" * 70)
        # Recalls the function for correct input.
        return user_preferred_application_input()

    # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    except KeyboardInterrupt:
        sys.exit()


def main():
    """
    This function does the following tasks:
    ---------------------------------------------

    [1] Reads the user input.
    [2] Executes the user preferred program.

    """
    # Time complexity : O(1)
    user_preferred_input = user_preferred_application_input()
    try:
        # Checks for user input and runs the respective program.
        if user_preferred_input == 1:
            image_conversion.execute()
        elif user_preferred_input == 2:
            image_compression.execute()
        elif user_preferred_input == 3:
            image_resizing.execute()
        elif user_preferred_input == 4:
            image_colorization.execute()
        elif user_preferred_input == 5:
            image_manager.execute()

    # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    except KeyboardInterrupt:
        sys.exit()


def get_continuation_input():
    """
    This function does the following task:
    ------------------------------------------------

    [1] Prompts the user with an input asking if they want to
    continue or exit the program.
    [2] If user wants to continue then the main() function is executed again.
    [3] If user wants to exit, then the program quits using sys.exit().

    """
    # Time complexity : O(1)
    continuation_input = str(
        input(
            '\n\nPress "C" if you\'d like to continue and "Q" if you\'d like to exit :'
        )
        .strip()
        .lower()
    )

    try:
        if continuation_input == "c":
            print("\n\n")
            main()
            return get_continuation_input()

        if continuation_input == "q":
            sys.exit()

        else:
            print("-" * 70)
            print("\n\nPlease try again with a valid input.\n\n")
            print("-" * 70)
            return get_continuation_input()

    # Checks for value errors, i.e :
    # >>> integer input like : 1,2,3,1234,etc.
    except ValueError:
        print("-" * 70)
        print("\n\nPlease try again with a valid input.\n\n")
        print("-" * 70)
        return get_continuation_input()


def execute():
    """
    This function executes the entire program.
    """
    # Time complexity : O(1)
    main()
    try:
        get_continuation_input()

    # Exits the program when forcefully interupted, usually when pressed : Ctrl + C, Ctrl + D, Ctrl + Z.
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    execute()
