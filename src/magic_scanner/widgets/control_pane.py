from ..decorators import reify
from . import _tk as tk


class ControlPane(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self._layout()

        self.pack(expand=1, fill=tk.BOTH)
    
    def _layout(self):
        form_rows = [
            (self._phash_label, self._phash_text),
            (self._ocr_label, self._ocr_text)
        ]
        self.columnconfigure(0, weight=0, pad=5)
        self.columnconfigure(1, weight=1, pad=5)
        self.rowconfigure(len(form_rows), weight=1)

        for row, (label, field) in enumerate(form_rows):
            self.rowconfigure(row, pad=5)
            label.grid(row=row, column=0, sticky=tk.W+tk.E)
            field.grid(row=row, column=1, sticky=tk.W+tk.E)
        
        # add 2 to the row to put the button after the spacer grid area
        self.add_to_library_button.grid(row=len(form_rows)+2, column=0, columnspan=2, sticky=tk.W+tk.E)

    @reify
    def ocr_result(self):
        return tk.StringVar()

    @reify
    def phash_result(self):
        return tk.StringVar()

    @reify
    def _phash_label(self):
        return tk.Label(self, text="P-Hash")
    
    @reify
    def _phash_text(self):
        return tk.Entry(self, state=tk.DISABLED, textvariable=self.phash_result)

    @reify
    def _ocr_label(self):
        return tk.Label(self, text="Title (OCR)")
    
    @reify
    def _ocr_text(self):
        return tk.Entry(self, state=tk.DISABLED, textvariable=self.ocr_result)

    @reify
    def add_to_library_button(self):
        return tk.Button(self, text="Add to Library")
    
