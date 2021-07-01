"""
Methods for preprocessing the image before OCR can be done

The main purpose of this module is to extract the bounding boxes of the table so the
OCR class can use them to perform OCR on the images
"""
import numpy as np
import cv2


def get_boxes(image):
    """
    Uses the private helper functions to construct the bounding boxes for the image table

    Returns:
        [
            Bitnot image (should have lines excluded mostly, will help with OCR)
            Array of all final bounding boxes [x, y, width, height]
        ]
    """
    invert = _get_inverted(image)
    combined_lines = _combine_lines(
        _get_vertical_lines(image, invert), _get_horizontal_lines(image, invert)
    )
    boxes = _get_bounding_boxes(combined_lines)
    boxes = _sort_bounding_boxes(boxes)
    return (_overlay_lines(image, combined_lines), _get_final_boxes(boxes))


def _get_inverted(image):
    _, inverted_image = cv2.threshold(
        image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    return 255 - inverted_image


def _get_vertical_lines(image, inverted_image):
    kernel_len = np.array(image).shape[1] // 25
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    vertical_lines = cv2.erode(inverted_image, ver_kernel, iterations=3)
    return cv2.dilate(vertical_lines, ver_kernel, iterations=3)


def _get_horizontal_lines(image, inverted_image):
    kernel_len = np.array(image).shape[1] // 25
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    horizontal_lines = cv2.erode(inverted_image, hor_kernel, iterations=3)
    return cv2.dilate(horizontal_lines, hor_kernel, iterations=3)


def _combine_lines(vertical_lines, horizontal_lines):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    combined_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    combined_lines = cv2.erode(~combined_lines, kernel, iterations=2)
    _, combined_lines = cv2.threshold(
        combined_lines, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    return combined_lines


def _overlay_lines(image, combined_lines):
    bitxor = cv2.bitwise_xor(image, combined_lines)
    return cv2.bitwise_not(bitxor)


def _sort_contours(contours, method="ttb"):
    reverse = False
    i = 0
    if method in ("rtl", "btt"):
        reverse = True
    if method in ("ttb", "ltr"):
        i = 1
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    contours, _ = zip(
        *sorted(zip(contours, bounding_boxes), key=lambda b: b[1][i], reverse=reverse)
    )
    return contours


def _get_bounding_boxes(combined_lines):
    contours, _ = cv2.findContours(
        combined_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = _sort_contours(contours)
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 1000 and h < 500:
            boxes.append([x, y, w, h])
    return boxes


def _sort_bounding_boxes(boxes):
    rows, col = [], []
    mean_height = np.mean([box[3] for box in boxes])
    for i in boxes:
        if boxes.index(i) == 0:
            col.append(i)
            prev = i
        else:
            if i[1] <= prev[1] + mean_height / 2:
                col.append(i)
                prev = i
                if boxes.index(i) == len(boxes) - 1:
                    rows.append(col)
            else:
                rows.append(col)
                col = []
                prev = i
                col.append(i)
    return rows


def _get_center(rows):
    center = [
        int(rows[0][j][0] + rows[0][j][2] / 2) for j in range(len(rows[0])) if rows[0]
    ]
    center = np.array(center)
    center.sort()
    return center


def _get_shape_cnt(rows):
    col_cnt = 0
    for i in rows:
        temp_col_cnt = len(i)
        if temp_col_cnt > col_cnt:
            col_cnt = temp_col_cnt  # for ragged tables
    return col_cnt


def _get_final_boxes(rows):
    """This handles for ragged tables that may be input"""
    final_boxes = []
    center = _get_center(rows)
    col_cnt = _get_shape_cnt(rows)
    for i in rows:
        lis = []
        for _ in range(col_cnt):
            lis.append([])
        for j in i:
            diff = abs(center - (j[0] + j[2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(j)
        final_boxes.append(lis)
    return final_boxes
