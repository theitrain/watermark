import os
import argparse
import piexif
from PIL import Image, ImageOps, UnidentifiedImageError

def add_watermark(directory, logo_path, position, new_directory, padding, scale):
    """
    Add a watermark to images in the specified directory.

    Args:
    - directory (str): The directory containing images to be watermarked.
    - logo_path (str): Path to the watermark logo.
    - position (str): Position of the watermark on the image.
    - new_directory (str): Directory to save watermarked images.
    - padding (int): Padding around the logo in pixels.
    - scale (float): Scale of the logo relative to the shorter side of the image (percentage).
    """
    EXTS = ('.jpg', '.jpeg', '.png')

    # EXIF tags to preserve (using piexif tag keys)
    TAGS_TO_KEEP = {
        "ExposureTime": 33434,
        "ISOSpeedRatings": 34855,
        "DateTimeOriginal": 36867,
        "ShutterSpeedValue": 37377,
        "FocalLength": 37386,
        "FocalLengthIn35mmFilm": 41989,
        "LensMake": 42035,
        "LensModel": 42036,
    }

    try:
        original_logo = Image.open(logo_path)
        original_logo = ImageOps.exif_transpose(original_logo)
    except UnidentifiedImageError:
        print(f"Failed to read logo from {logo_path}. Ensure it's a valid image format.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Check if the logo has an alpha channel
    if original_logo.mode == 'RGBA':
        logo_mask_original = original_logo.split()[3]
    else:
        logo_mask_original = None
    
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(EXTS) and filename != os.path.basename(logo_path):
                full_path = os.path.join(dirpath, filename)
                try:
                    image = Image.open(full_path)
                    image = ImageOps.exif_transpose(image)
                except UnidentifiedImageError:
                    print(f"Skipped {filename}. Unsupported image format.")
                    continue
                except Exception as e:
                    print(f"An error occurred while processing {filename}: {e}")
                    continue
                exif_data_raw = image.info.get("exif")
                if not exif_data_raw:
                    print(f"No EXIF data found for {filename}. Skipping.")
                    continue
                    
                exif_data = piexif.load(exif_data_raw)

                filtered_exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
                for ifd in exif_data:
                    if not isinstance(exif_data[ifd], dict):  # Skip if there's no EXIF data in the current IFD
                        continue
                    for tag, value in exif_data[ifd].items():
                        for name, tag_id in TAGS_TO_KEEP.items():
                            if tag == tag_id:
                                filtered_exif[ifd][tag] = value

                imageWidth, imageHeight = image.size
                shorter_side = min(imageWidth, imageHeight)
                new_logo_width = int(shorter_side * scale / 100)
                logo_aspect_ratio = original_logo.width / original_logo.height
                new_logo_height = int(new_logo_width / logo_aspect_ratio)

                # Resize the logo and its mask
                logo = original_logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
                if logo_mask_original:
                    logo_mask = logo_mask_original.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
                    if logo_mask.mode not in ('L', '1'):
                        logo_mask = logo_mask.convert('L')
                else:
                    logo_mask = None

                # Determine watermark position
                if position == 'topleft':
                    paste_x, paste_y = padding, padding
                elif position == 'topright':
                    paste_x, paste_y = imageWidth - new_logo_width - padding, padding
                elif position == 'bottomleft':
                    paste_x, paste_y = padding, imageHeight - new_logo_height - padding
                elif position == 'bottomright':
                    paste_x, paste_y = imageWidth - new_logo_width - padding, imageHeight - new_logo_height - padding
                elif position == 'bottomcenter':
                    paste_x, paste_y = (imageWidth - new_logo_width) // 2, imageHeight - new_logo_height - padding
                elif position == 'center':
                    paste_x, paste_y = (imageWidth - new_logo_width) // 2,  (imageHeight - new_logo_height) // 2
                else:
                    print(f"Invalid position: {position}. Skipping {filename}.")
                    continue

                try:
                    image.paste(logo, (paste_x, paste_y), logo_mask)
                except Exception as e:
                    print(f"Failed to paste logo on {filename}: {e}")
                    continue

                # Determine the relative path
                relative_path = os.path.relpath(dirpath, directory)
                save_directory = new_directory if new_directory else directory
                final_save_directory = os.path.join(save_directory, relative_path)

                if not os.path.exists(final_save_directory):
                    os.makedirs(final_save_directory)

                new_image_path = os.path.join(final_save_directory, filename)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                exif_bytes = piexif.dump(filtered_exif)
                image.save(new_image_path, exif=exif_bytes)
                print(f"Added watermark to {new_image_path}")

    original_logo.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to add watermarks to images. Given a directory, this will traverse through all its images and apply the specified watermark. The resulting watermarked images can be saved in the same directory or a new specified directory, maintaining the original directory structure.")

    parser.add_argument('dir', 
                        help="Directory containing the images you want to watermark. The script will search recursively within this directory.",
                        metavar='SourceDirectory')

    parser.add_argument('logo', 
                        help="Path to the logo image that will be used as the watermark.",
                        metavar='WatermarkLogoPath')

    parser.add_argument('--pos', 
                        choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'], 
                        default='center',
                        help="Specifies the position of the watermark on the image. Default is 'center'.")

    parser.add_argument('--new_dir',
                        default=None, 
                        help="An optional directory where the watermarked images will be saved. If not provided, watermarked images will overwrite originals in the source directory. The original directory structure will be maintained.",
                        metavar='DestinationDirectory')

    parser.add_argument('--padding', 
                        type=int, 
                        default=0,
                        help="Specifies the padding (in pixels) around the watermark, useful when watermark is positioned at the corners. Default is 0, meaning no padding.")
    parser.add_argument('--scale',
                        type=float, 
                        default=20,
                        help="Resize the watermark based on a percentage of the image's width. E.g., for 10% of the image's width, provide 10.")


    args = parser.parse_args()

    add_watermark(args.dir, args.logo, args.pos, args.new_dir, args.padding, args.scale)
