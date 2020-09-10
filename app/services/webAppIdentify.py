import time
import json
from app import  utils
from app.config import Config
from .baseThread import BaseThread
logger = utils.get_logger()



web_app_rules = json.loads("\n".join(utils.load_file(Config.web_app_rule)))

class WebAppIdentify:
    def __init__(self, site_info):
        self.site_info = site_info
        self.result = {
            "name": "Java",
            "confidence": "80",
            "version": "",
            "icon": "default.png",
            "website": "https://www.riskivy.com",
            "categories": []
        }

    def run(self):
        return self.identify()

    def identify(self):
        for cms in web_app_rules:
            rule = web_app_rules[cms]
            rule_headers = rule.get("headers", [])
            rule_title_list = rule.get("title", [])
            if not rule_title_list and not rule_headers:
                continue

            for rule_header in rule_headers:
                if not rule_header:
                    continue
                if rule_header in self.site_info["headers"]:
                    self.result["name"] = cms
                    return self.result

            for rule_title in rule_title_list:
                if not rule_title:
                    continue

                if rule_title in self.site_info["title"]:
                    self.result["name"] = cms
                    return self.result



def web_app_identify(site_info):
    s = WebAppIdentify(site_info)
    return s.run()





