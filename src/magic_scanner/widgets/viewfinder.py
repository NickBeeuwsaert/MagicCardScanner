from PIL import Image, ImageTk

from ..decorators import reify
from . import _tk as tk


class Viewfinder(tk.Frame):
    image = None

    def __init__(self, master):
        super().__init__(master, style='Viewfinder.TFrame')

        # Not sure if this is the correct way to vertically center the video feed
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        self.label.grid(row=1, column=1)

    @reify
    def label(self):
        return tk.Label(self)
    
    
    def set_frame(self, frame):
        if self.image is None:
            self.image = ImageTk.PhotoImage(
                Image.fromarray(frame)
            )
            self.label["image"] = self.image
        else:
            self.image.paste(
                Image.fromarray(frame)
            )
