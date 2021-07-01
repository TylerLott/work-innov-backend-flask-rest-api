"""
TESTS FOR FLASK REST API

Tests the response from certain api calls that the website will be making

"""
import unittest
from src.api.api import app


class TestApi(unittest.TestCase):
    """Tester class for Rest api"""

    def test_example(self):
        """
        Ensures that the example image is returned with code 200
        """
        client = app.test_client(self)
        response = client.get("/api/example_image")
        self.assertEqual(response.status_code, 200)
        response.close()

        response1 = client.post("/api/example_image")
        response2 = client.put("/api/example_image")
        response3 = client.delete("/api/example_image")
        self.assertEqual(response1.status_code, 405)
        self.assertEqual(response2.status_code, 405)
        self.assertEqual(response3.status_code, 405)

    def test_image_upload(self):
        """
        Ensures that post image returns with 200
        """
        client = app.test_client(self)
        with open("data/test.png", "rb") as img_file:
            data = {"name": "this is a name", "age": 12}
            data = {"file": (img_file, "test.png")}
            response = client.post(
                "/api/image_upload", data=data, content_type="multipart/form-data"
            )
            self.assertEqual(response.status_code, 200)

        response2 = client.get("/api/image_upload")
        self.assertEqual(response2.status_code, 405)


if __name__ == "__main__":
    unittest.main()
