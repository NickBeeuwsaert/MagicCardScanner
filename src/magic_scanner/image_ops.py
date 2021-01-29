import cv2
import numpy as np
import pytesseract

phasher = cv2.img_hash.PHash_create()

# Rough estimate of 65mm for width and 90mm for height
MTG_CARD_ASPECT_RATIO = 65.0 / 90.0

def getAngle(point):
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
    ], key=lambda p: getAngle(center - p))

    # if the image isn't close enough in aspect ratio to our reference ratio
    # then stop processing
    if abs((width / height) - MTG_CARD_ASPECT_RATIO) > 0.05:
        return

    # transform = cv2.getAffineTransform(
    #     np.float32(box)[1:],
    #     np.array([
    #         # [1000, 0],
    #         [0, 0],
    #         [0, 1000],
    #         [1000, 1000],
    #     ], dtype=np.float32)
    # )

    # transformed_image = cv2.warpAffine(
    #     grayscale,
    #     transform,
    #     (1000, 1000)
    # )

    transform = cv2.getPerspectiveTransform(
        np.float32(box),
        np.array([
            [1000, 0],
            [0, 0],
            [0, 1000],
            [1000, 1000],
        ], dtype=np.float32)
    )

    transformed_image = cv2.warpPerspective(
        grayscale,
        transform,
        (1000, 1000)
    )
    cv2.imshow("transform", transformed_image)

    return transformed_image

def read_title(image):
    """Expect an image of a MTG card, upright, cropped and stretch to fit 1000x1000"""
    title_image = image[
        25*2:55*2,
        40*2:350*2,
        ...
    ]

    title = pytesseract.image_to_string(
        title_image
    ).strip()

    return title

def get_image_hash(image):
    return phasher.compute(image)
