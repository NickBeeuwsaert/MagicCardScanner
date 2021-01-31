# Magic: The Gathering Card Scanner

A project to scan my _Magic: The Gathering_ cards

Written in PySide2 because PySide6 doesnt have the multimedia frameworks and I couldnt get OpenCV and GTK to run in the same environment on Windows.

## Setup

Currently, only Windows is supported because PySide2 and opencv cause the application to crash on linux, and my webcam doesn't have very good linux support.

### 3D Printing

To make scanning cards easier, you can 3D print a holder for your camera

There is a base and mount in the `cad/` directory. The mount is made for a StreamCam but the base should be reusable for different cameras, with just an adapter needing to be designed.

The CAD files are designed for a Ender 3 Pro, so some tweaking might be needed to get the adapter to fit correctly

### Installation

1. Create a virtual environment for python

   Windows:

   ```powershell
   py -3 -m venv venv
   venv\Scripts\activate
   ```

2. Install [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Downloads.html)
3. Install the application
   ```powershell
   pip install .
   ```

# Running

The application should be pretty simple to run,

```powershell
magic_scanner --config config.toml
```
