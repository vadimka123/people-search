from django.test import TestCase

from engine.detect_face import FaceDetector
from engine.find_names import FindName
from engine.image_search import ImageSearch


class Test(TestCase):
    def test_engine(self):
        detector = FaceDetector('test', 'test.jpg')
        detector.detect()

        image_search = ImageSearch('test')
        results = image_search.search()

        find_name = FindName(results)
        name = find_name.find()
