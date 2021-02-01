# Magic: The Gathering Card Scanner

A project to scan my _Magic: The Gathering_ cards

## Setup

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

   Windows:
   ```powershell
   pip install .
   ```

# Running

The application should be pretty simple to run.

First make sure you have a config file setup, a reference one for windows is provided in `config_windows.toml`

```powershell
magic_scanner --config config_windows.toml
```
