import cv2

from ..decorators import reify
from ..image_ops import extract_card, get_image_hash, get_title
from . import _tk as tk
from .control_pane import ControlPane
from .viewfinder import Viewfinder


class MainWindow(tk.PanedWindow):
    def __init__(self, master, capture, tesseract):
        super().__init__(master, orient=tk.HORIZONTAL)

        self.capture = capture
        self.tesseract = tesseract

        self.add(self.viewfinder)
        self.add(self.control_pane)

        self.pack(fill=tk.BOTH, expand=1)

        self.after(0, self._update)
    
    def _process_frame(self, frame):
        card = extract_card(frame)
        if card is None:
            return

        title_image = get_title(card)
        if title_image is None:
            return

        self.tesseract.set_image(title_image)
        self.control_pane.ocr_result.set(self.tesseract.get_text())

        phash = get_image_hash(card)
        self.control_pane.phash_result.set(''.join(format(b, '02x') for b in phash.flat))


    def _update(self):
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        _, frame = self.capture.read()

        self.viewfinder.set_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self._process_frame(frame)


        self.after(int(1000 / fps), self._update)

    @reify
    def viewfinder(self):
        return Viewfinder(self)

    @reify
    def control_pane(self):
        return ControlPane(self)
