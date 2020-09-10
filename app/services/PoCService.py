import time
import json
from app import  utils
from app.config import Config
from .baseThread import BaseThread
logger = utils.get_logger()


class PoC(BaseThread):
    def __init__(self, sites, concurrency=3):
        super().__init__(sites, concurrency = concurrency)
        self.poc_map = {}

    def work(self, site):
        url = site + "pma/"
        conn = utils.http_req(url)
        if conn.status_code == 200 and  'href=\'db_structure.php?server=1' in conn.text:
            logger.info("found {}".format(url))
            self.poc_map[url] = conn.status_code


    def run(self):
        t1 = time.time()
        logger.info("start WebAnalyze {}".format(len(self.targets)))
        self._run()
        elapse = time.time() - t1
        logger.info("end WebAnalyze elapse {}".format(elapse))
        return self.poc_map

def poc(sites, concurrency = 3,):
    s = PoC(sites, concurrency = concurrency)
    return s.run()





