import cloudinary
import os
import time
import threading

from cloudinary.api import delete_resources
from cloudinary.uploader import upload
from django.conf import settings
from queue import Queue
from os import walk

from engine.incandescent import Client


class ImageSearchWorker(threading.Thread):
    def __init__(self, queue):
        super(ImageSearchWorker, self).__init__()
        self._stop = threading.Event()
        self.queue = queue

    def run(self):
        try:
            while not self._stop.isSet():
                try:
                    self.process(*self.queue.get())
                except Exception as e:
                    print(e)
                finally:
                    self.queue.task_done()
        except Exception as e:
            print(e)

    def stop(self):
        self._stop.set()

    def process(self, image, results):
        result = upload(image)

        if result.get('url'):
            search = Client()
            search.add_image_urls([result.get('url')])
            search.make_request_data()
            search.make_request()
            search_results = search.get_results()

            results[result.get('url')] = search_results

            delete_resources(public_ids=[result.get('public_id')])


class ImageSearch(object):
    def __init__(self, image_folder):
        self.image_folder = '{}/media/{}/faces'.format(settings.BASE_DIR, image_folder)

    @property
    def images_to_search(self):
        if not self.image_folder or not os.path.exists(self.image_folder):
            return []
        images_to_search = []
        for (dirpath, dirnames, filenames) in walk(self.image_folder):
            images_to_search.extend(filenames)
            break
        return images_to_search

    def search(self):
        images = self.images_to_search

        cloudinary.config(
            cloud_name="vadimka",
            api_key="996446192869348",
            api_secret="paxsYQvJej8MDg3DTihxWmWaR-4"
        )

        threads = []
        search_queue = Queue()

        q_size_limit = 30

        results = {}

        try:
            for x in range(0, len(images)):
                worker = ImageSearchWorker(search_queue,)
                worker.daemon = True
                threads.append(worker)
                worker.start()

            for image in self.images_to_search:
                while search_queue.qsize() >= q_size_limit:
                    time.sleep(1)
                search_queue.put(('{}/{}'.format(self.image_folder, image), results))

            search_queue.join()
        except Exception as e:
            print(e)
        finally:
            for thread in threads:
                thread.stop()
            search_queue.queue.clear()

        return results
