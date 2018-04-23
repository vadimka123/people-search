import certifi
import io
import os
import pycurl
import time
import threading

from bs4 import BeautifulSoup
from django.conf import settings
from queue import Queue
from os import walk


SEARCH_URL = 'https://www.google.com/searchbyimage?&image_url='


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

    def process(self, image):
        # TODO: upload image and search by them
        image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Steve_Jobs_Headshot_2010-CROP.jpg/267px-Steve_Jobs_Headshot_2010-CROP.jpg'

        returned_code = io.BytesIO()
        full_url = SEARCH_URL + image_url
        conn = pycurl.Curl()
        conn.setopt(conn.CAINFO, certifi.where())
        conn.setopt(conn.URL, str(full_url))
        conn.setopt(conn.FOLLOWLOCATION, 1)
        useragent = """
            Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11
        """
        conn.setopt(conn.USERAGENT, useragent)
        conn.setopt(conn.WRITEFUNCTION, returned_code.write)
        conn.perform()
        conn.close()
        code = returned_code.getvalue().decode('UTF-8')

        soup = BeautifulSoup(code, 'html.parser')

        results = {
            'links': [],
            'titles': [],
            'best_guess': ''
        }

        for div, title in zip(soup.findAll('div', attrs={'class': 'rc'}), soup.findAll('h3', attrs={'class': 'r'})):
            results['links'].append(div.find('a')['href'])
            results['titles'].append(title.get_text())

        for best_guess in soup.findAll('a', attrs={'class': 'fKDtNb'}):
            results['best_guess'] = best_guess.get_text()

        print(results)


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

        threads = []
        search_queue = Queue()

        q_size_limit = 30

        try:
            for x in range(0, len(images)):
                worker = ImageSearchWorker(search_queue,)
                worker.daemon = True
                threads.append(worker)
                worker.start()

            for image in self.images_to_search:
                while search_queue.qsize() >= q_size_limit:
                    time.sleep(1)
                search_queue.put(('{}/{}'.format(self.image_folder, image),))

            search_queue.join()
        except Exception as e:
            print(e)
        finally:
            for thread in threads:
                thread.stop()
            search_queue.queue.clear()
