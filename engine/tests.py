from django.test import TestCase

from engine.detect_face import FaceDetector
from engine.image_search import ImageSearch


class Test(TestCase):
    def test_face(self):
        detector = FaceDetector('test', 'test.jpg')
        detector.detect()
        image_search = ImageSearch('test')
        image_search.search()
