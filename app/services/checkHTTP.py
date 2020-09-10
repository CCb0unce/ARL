import threading
import collections
from app import  utils


import  requests.exceptions
logger = utils.get_logger()

class CheckHTTP(object):
    def __init__(self, urls, concurrency=10):
        self.concurrency = concurrency
        self.semaphore = threading.Semaphore(concurrency)
        self.urls = urls
        self.timeout = (5, 3)
        self.checkout_map = {}

    def check(self, url):
        conn = utils.http_req(url, method = "head", timeout = self.timeout)
        if conn.status_code == 400:
            return None

        if (conn.status_code >= 501) and (conn.status_code < 600):
            return None

        if conn.status_code == 403:
            conn2 = utils.http_req(url)
            check = b'</title><style type="text/css">body{margin:5% auto 0 auto;padding:0 18px}'
            if check in conn2.content:
                return None

        item = {
            "status": conn.status_code,
            "content-type": conn.headers.get("Content-Type", "")
        }

        return item

    def work(self, url):
        try:
            out = self.check(url)
            if out is not  None:
                self.checkout_map[url] = out

        except requests.exceptions.RequestException as e:
            pass

        except Exception as e:
            logger.warning("error on url {}".format(url))
            logger.warning(e)

        self.semaphore.release()

    def run(self):
        deque = collections.deque(maxlen=self.concurrency)

        for url in self.urls:
            url = url.strip()
            if not url:
                continue

            if "://" not in url:
                url = "http://" + url
            self.semaphore.acquire()
            t1 = threading.Thread(target=self.work, args=(url,))
            t1.start()

            deque.append(t1)

        for t in list(deque):
            t.join()

        return self.checkout_map


def check_http(urls):
    c = CheckHTTP(urls)
    return  c.run()