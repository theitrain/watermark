# Watermark
Python script to add a watermark or logo to images recursively in a specified directory and its subdirectories.

### Requirements
Pillow:
```
pip install pillow
```

[Pillow Docs](https://python-pillow.github.io/)

### Usage
This script allows you to add a watermark or logo to images in a specified folder and its subdirectories. The script takes several arguments:

1. The folder with the images you want to watermark
2. The path of the logo to add
3. The position you want to place the logo (optional)
4. The directory where you want to save the watermarked images (optional; if not provided, the watermarked images will overwrite the original images)
5. Padding (in pixels) around the watermark logo (optional; default is 0)

These are the valid positions:

- topleft
- topright
- bottomleft
- bottomright
- center (if no position is specified, this will be the default)

Any other position will result in an error.

To use watermark.py, specify a position, a destination directory, and scale the watermark to 30% of the image width:

```
python watermark.py './images' 'logo.png' --pos bottomright --new_dir './watermarked_images' --scale 30
```


To use watermark.py, specify a position and a destination directory:

```
python watermark.py './images' 'logo.png' --pos bottomright --new_dir './watermarked_images'
```

To add padding around the watermark:

```
python watermark.py './images' 'logo.png' --pos topleft --padding 20
```

### Adapting
If you want to save your watermarked images to a different directory instead of saving over the existing files, use the `--new_dir` option as shown in the usage examples. The script will maintain the original folder hierarchy in the specified new directory.

### Ideas for future improvements
- Allow custom positioning via exact pixel coordinates.
- Adjust watermarks to be semi-transparent.