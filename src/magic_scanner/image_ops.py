import cv2
import numpy as np

phasher = cv2.img_hash.PHash_create()

# Rough estimate of 65mm for width and 90mm for height
MTG_CARD_ASPECT_RATIO = 65.0 / 90.0

def union(a, b):
    """Take two bounding boxes and union them together"""
    x0, y0, w0, h0 = a
    w0 += x0
    h0 += y0
    x1, y1, w1, h1 = b
    w1 += x1
    h1 += y1

    x = min(x0, x1)
    y = min(y0, y1)
    w = max(w0, w1)
    h = max(h0, h1)

    return (
        x, y,
        w - x, h - y
    )

def contours_bounding_box(contours):
    """get the bounding boxes of several contours"""
    if not contours:
        return None
    
    boxes = [
        cv2.boundingRect(contour)
        for contour in contours
    ]

    box, *boxes = boxes

    for b in boxes:
        box = union(box, b)
    return box
        

def get_angle(point):
    x, y = point
    return np.arctan2(y, x)

def extract_card(buffer):

    buffer = cv2.rotate(buffer, cv2.ROTATE_90_COUNTERCLOCKWISE)
    grayscale = cv2.cvtColor(buffer, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    _, threshold = cv2.threshold(
        blurred,
        100,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(
        255 - threshold.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cardContours = sorted([
        contour
        for contour in contours
        if len(
            cv2.approxPolyDP(
                contour,
                0.04 * cv2.arcLength(contour, True),
                True
            )
        ) == 4
    ], key=cv2.contourArea, reverse=True)

    # No card was found, bail
    if not cardContours:
        return

    largestCard, *_ = cardContours
    rectangle = cv2.minAreaRect(largestCard)
    center, size, angle = rectangle
    width, height = size

    box = sorted([
        point
        for point in cv2.boxPoints(rectangle)
    ], key=lambda p: get_angle(center - p))

    # if the image isn't close enough in aspect ratio to our reference ratio
    # then stop processing
    if abs((width / height) - MTG_CARD_ASPECT_RATIO) > 0.05:
        return

    # Perspective warping probably isn't necessary here
    # since we are just transforming a box with no perspective on it at all
    # but this code is a bit more readable than doing an affine transform imo
    # and in the future I'd like to do some magic with hough lines and kmeans
    # to get the cards perspective and warp from that.
    
    # I can't just get the cards perspective from the contour, since
    # approxPolyDP will cut of edge of the card, due to the rounded corners

    transform = cv2.getPerspectiveTransform(
        np.float32(box),
        np.array([
            [1000, 0],
            [0, 0],
            [0, 1000],
            [1000, 1000],
        ], dtype=np.float32)
    )

    return cv2.warpPerspective(
        buffer,
        transform,
        (1000, 1000)
    )

def get_title(card):
    """
        This method could be a bit more flexible.

        It basically takes a rough cut out of wher we think the title should be on a MTG card,
        crops that out, finds the contours for the text, gets the bounding boxes and then
        unions them all to get a rough estimate of where the text rectangle is.

        tesseract has a method to do just this, but then I'd have to wrap some leptonica types
        in addition to the tesseract types.

        But if I WERE to wrap the leptonica types, I could just get the first recognized line of text
        and assume that is the card title, and avoid cropping a ton
    """
    x = 85
    y = 60
    width = 600
    height = 35
    title_image = card[
        y : y + height,
        x : x + width
    ]
    canny = cv2.Canny(
        title_image, 100, 150
    )

    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cbox = contours_bounding_box(contours)
    if cbox is None:
        return None
    x, y, width, height = cbox
    final = title_image[
        y : y + height,
        x : x + width
    ]
    return final

def get_image_hash(image):
    return phasher.compute(image)
