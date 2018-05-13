from django.test import TestCase

from engine.detect_face import FaceDetector
from engine.find_names import FindName
from engine.image_search import ImageSearch
from engine.social_search import SocialSearch


class Test(TestCase):
    def test_engine(self):
        # detector = FaceDetector('test', 'test.jpg')
        # detector.detect()
        #
        # image_search = ImageSearch('test')
        # results = image_search.search()
        #
        # for key, results in results.items():
        #     find_name = FindName(results)
        #     find_name.find()

        res = SocialSearch(name='Jobs Steve').search()
        print(res.person, res.possible_persons)