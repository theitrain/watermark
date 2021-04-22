# watermark
Python script to add a watermark or logo to images

### Requirements
Pillow:
```
pip install pillow
```

[Pillow Docs](https://python-pillow.github.io/)

### Usage
This script allows you to add a watermark or logo to images in a specified folder. The script takes three arguments:

1. The folder with the images you want to watermark
2. The path of the logo to add
3. The float value for the alpha value on the logo
4. The position you want to place the logo (optional)

The final value for the alpha float will depend on the current value for each pixel, will be proportional.
Must introduce a number between 0 and 1 

> will default to 0.5

These are the valid positions:

- topleft
- topright
- bottomleft
- bottomright
- center (if no position is specified, this will be the default)

Any other position will result in an error.

---

To use watermark.py without specifying a position:

```
python watermark.py  './images' 'logo.png'
```

To use watermark.py and specify an aplha value
```
python watermark.py  './images' 'logo.png' 0.4
```

To use watermark.py and specify a position:
```
python watermark.py  './images' 'logo.png' bottomright
```

To use watermark.py and specify an aplha value and a position:
```
python watermark.py  './images' 'logo.png' 0.4 bottomright
```
---
### Adapting
If you want to save your watermarked images as new files instead of saving over the existing files, simply add a prefix to any image.save() lines:

```
image.save(path + '/fancy_new_prefix_' + filename)
```

### Ideas for future improvements
- allow custom positioning
- adjust watermarks to be semi-transparent
