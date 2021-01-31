"""
Wrap tesseract in a ctypes wrapper, instead of using pytesseract

pytesseract doesn't interact with the tesseract dll, instead it saves images to disk,
and invokes a subprocess. This is fine for OCR for still images, but when you are doing OCR
pretty frequently on the results of a webcam feed it can be a huge performance hit.

Instead I'm writing a thin wrapper around the tesseract C API, which is many many times faster

"""
from contextlib import contextmanager
from ctypes import CDLL, c_char_p, c_int, c_void_p

import numpy as np

from .decorators import reify


class Tesseract:
    """Quick ctypes wrapper for tesseract.

    I could have used cffi and this would be a lot cleaner
    but for some reason on windows cffis dlopen wouldn't work unless I called ctypes CDLL.
    probably a path issue or something.
    """
    # used for cleanup, we dont need to initialize a handle just to free it
    _initialized = False

    def __init__(self, language=None, data_path=None, tesseract_library='tesseract'):
        self.language = language
        self.data_path = data_path
        self._tesseract_library = tesseract_library

    @reify
    def _libtesseract(self):
        return CDLL(self._tesseract_library)

    @reify
    def _version(self):
        tess_version = self._libtesseract.TessVersion

        tess_version.restype = c_char_p

        return tess_version
    
    @reify
    def version(self):
        return self._version()
    
    @reify
    def _create(self):
        create = self._libtesseract.TessBaseAPICreate

        create.restype = c_void_p

        return create
    
    @reify
    def _init(self):
        init = self._libtesseract.TessBaseAPIInit3

        init.argtypes = (c_void_p, c_char_p, c_char_p)
        init.restype = None

        return init

    @reify
    def _delete(self):
        delete = self._libtesseract.TessBaseAPIDelete

        delete.argtypes = (c_void_p, )
        delete.restype = None

        return delete

    @reify
    def _handle(self):
        handle = self._create()
        data_path = self.data_path
        language = self.language

        if language is not None:
            language = language.encode('utf-8')

        if data_path is not None:
            data_path = data_path.encode('utf-8')

        self._init(handle, data_path, language)
        self._initialized = True
        return handle

    @reify
    def _set_image(self):
        set_image = self._libtesseract.TessBaseAPISetImage
        set_image.argtypes = (
            c_void_p,
            c_void_p,
            c_int, c_int,
            c_int, c_int
        )
        set_image.restype = None

        return set_image
    
    @reify
    def _set_source_resolution(self):
        set_source_resolution = self._libtesseract.TessBaseAPISetSourceResolution
        set_source_resolution.argtypes = (c_void_p, c_int)
        set_source_resolution.restype = None

        return set_source_resolution
    
    @reify
    def _get_utf8_text(self):
        get_utf8_text = self._libtesseract.TessBaseAPIGetUTF8Text

        get_utf8_text.argtypes = (c_void_p, )
        get_utf8_text.restype = c_char_p

        return get_utf8_text

    def get_text(self):
        return self._get_utf8_text(self._handle).decode('utf-8')

    
    def set_source_resolution(self, ppi):
        self._set_source_resolution(self._handle, ppi)
    
    def set_image(self, image, ppi=72):
        height, width, depth = image.shape

        if not image.data.contiguous:
            # sometimes the backing store of ndarray is not contiguous memory
            # in that case, convert the image into a block of contiguous memory
            image = np.ascontiguousarray(image)

        self._set_image(
            self._handle,
            image.ctypes.data,
            width, height,
            depth, width * depth
        )
        self.set_source_resolution(ppi)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._initialized:
            self._delete(self._handle)
