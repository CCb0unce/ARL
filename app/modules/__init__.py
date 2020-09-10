from .ipInfo import PortInfo, IPInfo
from .baseInfo import BaseInfo
from .domainInfo import DomainInfo
from .pageInfo import PageInfo
from app.config import Config


class ScanPortType:
    TEST = Config.TOP_10
    TOP100 = Config.TOP_100
    TOP1000 = Config.TOP_1000
    ALL = "0-65535"


class DomainDictType:
    TEST = Config.DOMAIN_DICT_TEST
    BIG = Config.DOMAIN_DICT_2W


class CollectSource:
    DOMAIN_BRUTE = "domain_brute"
    BAIDU = "baidu"
    RISKIQ = "riskIQ"
    ALTDNS = "altdns"
    ARL = "arl"
    SITESPIDER = "site_spider"
    SEARCHENGINE = "search_engine"


class TaskStatus:
    WAITING = "waiting"
    DONE = "done"
    ERROR = "error"
    STOP = "stop"


Sessions = {
    Config.API_KEY: {
        "type": "api",
        "token": Config.API_KEY
    }
}
