from app import utils
import threading
import collections
from app.modules import  DomainInfo
logger = utils.get_logger()

class ResolverDomain():
    def __init__(self, domains, concurrency = 6):
        self.domains = domains
        self.resolver_map = {}
        self.semaphore = threading.Semaphore(concurrency)
        self.concurrency = concurrency


    def run(self):
        self.resolver()
        return self.resolver_map

    def work(self, domain):
        try:
            self.resolver_map[domain] = utils.get_ip(domain)
        except Exception as e:
            logger.exception(e)

        self.semaphore.release()


    '''
    {
        "api.baike.baidu.com":[
            "180.97.93.62",
            "180.97.93.61"
        ],
        "apollo.baidu.com":[
            "123.125.115.15"
        ],
        "www.baidu.com":[
            "180.101.49.12",
            "180.101.49.11"
        ]
    }
    '''
    def resolver(self):
        deque = collections.deque(maxlen=self.concurrency)
        for domain in self.domains:
            curr_domain = domain
            if isinstance(domain, dict):
                curr_domain =curr_domain.get("domain")

            elif isinstance(domain, DomainInfo):
                curr_domain = domain.domain

            if not  curr_domain:
                continue

            if curr_domain in self.resolver_map:
                continue

            self.semaphore.acquire()

            t1 = threading.Thread(target=self.work, args=(curr_domain,))
            t1.start()

            deque.append(t1)

        for t in list(deque):
            t.join()


def resolver_domain(domains, concurrency = 6):
    r = ResolverDomain(domains, concurrency)
    return  r.run()