"""
Main image processing class

Must be initialized with an image path
"""
import os
import cv2
import pytesseract
import numpy as np
from src.ocr.preprocessor.preprocessor import get_boxes

# for runnning tesseract locally
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


class OCR:
    """
    Runs OCR on table image
    """

    def __init__(self, image_path):
        self._image = cv2.imread(image_path, 0)

    def get_image(self):
        """GETTER"""
        return self._image

    def extract_table(self):
        """
        Run table extraction and return array of shape(rows, columns)
        """
        bitnot, bounding_boxes = get_boxes(self._image)
        row = []
        for i in bounding_boxes:
            for j in i:
                if len(j) == 0:
                    row.append(["", -2])
                else:
                    col = []
                    for k in j:
                        y, x, w, h = (k[0], k[1], k[2], k[3])
                        cropped_img = bitnot[x : x + h, y : y + w]
                        col = _run_tesseract(cropped_img)
                    row.append(col)

        arr = np.array(row)
        return arr.reshape((len(bounding_boxes), len(bounding_boxes[0]), 2)).tolist()


def _run_tesseract(image):
    tesseract_config = """-c tessedit_char_whitelist=
        "01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-/ '"
        --psm 6 --oem 1"""
    out = pytesseract.image_to_data(
        image,
        lang="eng",
        config=tesseract_config,
        output_type=pytesseract.Output.DICT,
    )
    ind = np.where(np.array(out.get("conf")) != "-1")
    text = ""
    conf = 0
    if len(ind[0]) >= 1:
        for i in ind[0]:
            text = " ".join([text, out.get("text")[i]])
            conf += float(out.get("conf")[i])
        conf = conf / len(ind[0])
    if text == "" and conf == 0:
        conf = -2  # this denotes a empty space predition
    return [text, conf]


if __name__ == "__main__":
    ocr = OCR("../../../test_img.png")
    print(ocr.extract_table())
