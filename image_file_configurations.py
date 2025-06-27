"""System module."""


#!TODO: Use a json file for the following data for smaller file size and faster parsing.

configurations = {
    1: {
        "conversion_title": "JPEG to PNG",
        "filetype": "*.jpg;*.jpeg",
        "conversion_extension": ".png",
        "conversion_type": "PNG",
    },
    2: {
        "conversion_title": "PNG to JPEG",
        "filetype": "*.png",
        "conversion_extension": ".jpg",
        "conversion_type": "JPEG",
    },
    3: {
        "conversion_title": "BMP to GIF",
        "filetype": "*.bmp",
        "conversion_extension": ".gif",
        "conversion_type": "GIF",
    },
    4: {
        "conversion_title": "TIFF to JPEG",
        "filetype": "*.tiff;*.tif",
        "conversion_extension": ".jpg",
        "conversion_type": "JPEG",
    },
    5: {
        "conversion_title": "GIF to PNG",
        "filetype": "*.gif",
        "conversion_extension": ".png",
        "conversion_type": "PNG",
    },
    # 6: {
    #     "conversion_title": "PSD to PNG",
    #     "filetype": "*.psd",
    #     "conversion_extension": ".png",
    #     "conversion_type": "PNG",
    # },
    # 7: {
    #     "conversion_title": "PSD to JPEG",
    #     "filetype": "*.psd",
    #     "conversion_extension": ".jpg",
    #     "conversion_type": "JPEG",
    # },
    # 8: {
    #     "conversion_title": "SVG to PNG",
    #     "filetype": "*.svg",
    #     "conversion_extension": ".png",
    #     "conversion_type": "PNG",
    # },
    # 9: {
    #     "conversion_title": "SVG to JPEG",
    #     "filetype": "*.svg",
    #     "conversion_extension": ".jpg",
    #     "conversion_type": "JPEG",
    # },
    # 10: {
    #     "conversion_title": "RAW to PNG",
    #     "filetype": "*.raw;*.arw;*.dng;*.nef;*.cr2",
    #     "conversion_extension": ".png",
    #     "conversion_type": "PNG",
    # },
    # 11: {
    #     "conversion_title": "RAW to JPEG",
    #     "filetype": "*.raw;*.arw;*.dng",
    #     "conversion_extension": ".jpg",
    #     "conversion_type": "JPEG",
    # },
    6: {
        "conversion_title": "ICO to PNG",
        "filetype": "*.ico",
        "conversion_extension": ".png",
        "conversion_type": "PNG",
    },
    7: {
        "conversion_title": "ICO to JPEG",
        "filetype": "*.ico",
        "conversion_extension": ".jpg",
        "conversion_type": "JPEG",
    },
    8: {
        "conversion_title": "WebP to PNG",
        "filetype": "*.webp",
        "conversion_extension": ".png",
        "conversion_type": "PNG",
    },
    9: {
        "conversion_title": "WebP to JPEG",
        "filetype": "*.webp",
        "conversion_extension": ".jpg",
        "conversion_type": "JPEG",
    },
    10: {
        "conversion_title": "PNG to ICO",
        "filetype": "*.png",
        "conversion_extension": ".ico",
        "conversion_type": "ICO",
    },
    11: {
        "conversion_title": "JPEG to ICO",
        "filetype": "*.jpg;*.jpeg",
        "conversion_extension": ".ico",
        "conversion_type": "ICO",
    },
    12: {
        "conversion_title": "PNG to WebP",
        "filetype": "*.png",
        "conversion_extension": ".webp",
        "conversion_type": "WebP",
    },
    13: {
        "conversion_title": "JPEG to WebP",
        "filetype": "*.jpg;*.jpeg",
        "conversion_extension": ".webp",
        "conversion_type": "WebP",
    },
}
