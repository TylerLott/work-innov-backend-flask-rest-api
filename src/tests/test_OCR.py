"""
TESTS FOR FLASK REST API

Tests the response from certain api calls that the website will be making

"""
import unittest
from src.ocr.ocr import OCR
from src.tests.correct_test_img_out import TRUE_TABLE


class TestOCR(unittest.TestCase):
    """
    Test the output of OCR
    """

    def test_get_image(self):
        """Ensures the image is loaded correctly if good filepath passed in"""
        ocr = OCR("data/test.png")
        self.assertIsNotNone(ocr.get_image())
        ocr = OCR("noPath.png")
        self.assertIsNone(ocr.get_image())

    def test_extract_table(self):
        """
        Tests the actual output for the test table
        """
        ocr = OCR("data/test.png")
        table = ocr.extract_table()
        self.assertEqual(TRUE_TABLE, table)


if __name__ == "__main__":
    unittest.main()
