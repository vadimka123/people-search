import heapq
import spacy
import requests
import operator
import threading
import time

from bs4 import BeautifulSoup
from queue import Queue


class FindNamesWorker(threading.Thread):
    def __init__(self, queue):
        super(FindNamesWorker, self).__init__()
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

    def process(self, nlp, url, results):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.title:
            title = str(soup.title.string)
            for token in nlp(title):
                if token.ent_type_ == 'PERSON':
                    results.append(str(token).lower())


class FindName(object):
    def __init__(self, urls):
        self.urls = urls

    def find(self):
        threads = []
        search_queue = Queue()

        q_size_limit = 30

        results = []

        nlp = spacy.load('en')

        try:
            for x in range(0, len(self.urls)):
                worker = FindNamesWorker(search_queue, )
                worker.daemon = True
                threads.append(worker)
                worker.start()

            for url in self.urls:
                while search_queue.qsize() >= q_size_limit:
                    time.sleep(1)
                search_queue.put((nlp, url, results))

            search_queue.join()
        except Exception as e:
            print(e)
        finally:
            for thread in threads:
                thread.stop()
            search_queue.queue.clear()

        results_hash = dict()

        for result in results:
            results_hash.setdefault(result, 0)
            results_hash[result] += 1

        r = heapq.nlargest(2, results_hash.items(), key=operator.itemgetter(1))
        name = ''
        for part in r:
            name += ' ' + part[0]

        return name.title()
