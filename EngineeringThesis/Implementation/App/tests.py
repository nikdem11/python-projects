import unittest
from app import App


class TestApp(unittest.TestCase):

    def test_validate_video_valid(self):
        app = App()
        self.assertEqual(app.validate_video("../Datasets/tests_data/test.mp4"), True)

    def test_validate_video_invalid(self):
        app = App()
        self.assertEqual(app.validate_video("../Datasets/tests_data/test_bad.mp4"), False)

    def test_validate_existing_folder(self):
        app = App()
        self.assertEqual(app.validate_folder("App"), True)

    def test_validate_nonexisting_folder(self):
        app = App()
        self.assertEqual(app.validate_folder("ApppA"), False)


if __name__ == '__main__':
    unittest.main()
