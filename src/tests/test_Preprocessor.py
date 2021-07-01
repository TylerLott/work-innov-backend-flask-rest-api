"""
Tests for the image preprocessor methods used before text extraction
"""
import unittest
import numpy as np
import cv2
from src.ocr.preprocessor.preprocessor import (
    _get_inverted,
    _get_vertical_lines,
    _get_horizontal_lines,
    _combine_lines,
    _overlay_lines,
    _get_bounding_boxes,
    _sort_bounding_boxes,
    _get_final_boxes,
)
from src.tests.correct_test_img_out import (
    BOUNDING_BOXES,
    SORTED_BOUNDING_BOXES,
    FINAL_BOUNDING_BOXES,
)


class TestPreprocessor(unittest.TestCase):
    """
    Test each step of the preprocessing
    """

    def test_get_inverted(self):
        """Compare known inverted img to functional output"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        self.assertIsNotNone(inv)
        np.testing.assert_equal(np.any(np.not_equal(img, inv)), True)

    def test_get_vertical_lines(self):
        """Compare known vertical lines to functional output"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        vert = _get_vertical_lines(img, inv)
        valid_vert = cv2.imread("data/vertical.png", 0)
        self.assertIsNotNone(vert)
        np.testing.assert_equal(np.all(np.equal(vert, valid_vert)), True)

    def test_get_horizontal_lines(self):
        """Compare known horizontal lines to functional output"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        valid_hor = cv2.imread("data/horizontal.png", 0)
        self.assertIsNotNone(hor)
        np.testing.assert_equal(np.all(np.equal(hor, valid_hor)), True)

    def test_combine_lines(self):
        """Tests adding vertical and horizontal lines into a single image"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        vert = _get_vertical_lines(img, inv)
        com = _combine_lines(vert, hor)
        valid_com = cv2.imread("data/combined.png", 0)
        self.assertIsNotNone(com)
        np.testing.assert_equal(np.all(np.equal(com, valid_com)), True)

    def test_overlay_lines(self):
        """Tests when the combine lines are overlayed with the original with bitwise not"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        vert = _get_vertical_lines(img, inv)
        com = _combine_lines(vert, hor)
        overlay = _overlay_lines(img, com)
        valid_over = cv2.imread("data/bitnot.png", 0)
        self.assertIsNotNone(overlay)
        np.testing.assert_equal(np.all(np.equal(overlay, valid_over)), True)

    def test_get_bounding_boxes(self):
        """Compares known values to function values"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        vert = _get_vertical_lines(img, inv)
        com = _combine_lines(vert, hor)
        bounding_boxes = _get_bounding_boxes(com)
        self.assertIsNotNone(bounding_boxes)
        np.testing.assert_equal(
            np.all(np.allclose(bounding_boxes, BOUNDING_BOXES, rtol=1)),
            True,  # within 1 pixel
        )

    def test_sort_bounding_boxes(self):
        """Tests sorting the bounding boxes into correct rows and columns"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        vert = _get_vertical_lines(img, inv)
        com = _combine_lines(vert, hor)
        bounding_boxes = _get_bounding_boxes(com)
        sort = _sort_bounding_boxes(bounding_boxes)
        self.assertIsNotNone(sort)
        np.testing.assert_equal(
            np.all(np.allclose(sort, SORTED_BOUNDING_BOXES, rtol=1)),
            True,  # within 1 pixel
        )

    def test_get_final_boxes(self):
        """Tests method for handling ragged tables"""
        img = cv2.imread("data/test.png", 0)
        inv = _get_inverted(img)
        hor = _get_horizontal_lines(img, inv)
        vert = _get_vertical_lines(img, inv)
        com = _combine_lines(vert, hor)
        bounding_boxes = _get_bounding_boxes(com)
        sort = _sort_bounding_boxes(bounding_boxes)
        final = _get_final_boxes(sort)
        self.assertIsNotNone(final)
        np.testing.assert_equal(
            np.all(np.allclose(final, FINAL_BOUNDING_BOXES, rtol=1)),
            True,  # within 1 pixel
        )
