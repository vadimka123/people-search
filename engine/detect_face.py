import face_recognition
import shutil
import os
import uuid

from django.conf import settings
from PIL import Image


class FaceDetector(object):
    def __init__(self, image_folder, image_name):
        self.image_folder = image_folder
        self.image_name = image_name

    def detect(self):
        image = face_recognition.load_image_file('{}/media/{}/{}'.format(settings.BASE_DIR, self.image_folder,
                                                                         self.image_name))

        face_locations = face_recognition.face_locations(image)

        directory = '{}/media/{}/faces'.format(settings.BASE_DIR, self.image_folder)
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            if not os.path.exists(directory):
                os.makedirs(directory)
            pil_image.save('{}/{}.jpg'.format(directory, str(uuid.uuid4())[:8]))
