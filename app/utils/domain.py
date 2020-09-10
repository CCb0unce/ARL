import tld
import re
import geoip2.database
from app.config import Config
from . import IPy


blackdomain_list = None
blackhexie_list = None

def check_domain_black(domain):
    global blackdomain_list
    global blackhexie_list
    if blackdomain_list is None:
        with open(Config.black_domain_path) as f:
            blackdomain_list = f.readlines()

    for item in blackdomain_list:
        item = item.strip()
        if item and domain.endswith(item):
            return True

    if blackhexie_list is None:
        with open(Config.black_heixie_path) as f:
            blackhexie_list = f.readlines()


    for item in blackhexie_list:
        item = item.strip()
        _, _, subdomain = tld.parse_tld(domain, fix_protocol=True, fail_silently=True)
        if subdomain and  item and  item.strip() in subdomain:
            return True

    return False




def is_valid_domain(domain):
    from app.utils import domain_parsed
    if "." not in domain:
        return False

    if domain_parsed(domain):
        return True

    return False

#判断是否在黑名单IP内，有点不严谨
def in_black_ips(target):
    try:
        for ip in Config.BLACK_IPS:
            if "-" in target:
                target = target.split("-")[0]

            if IPy.IP(target) in IPy.IP(ip):
                return True
    except Exception as e:
        logger.warn("error on check black ip {} {}".format(target, e))



def get_ip_asn(ip):
    item = {}
    try:
        reader = geoip2.database.Reader(Config.asn_data_path)
        response = reader.asn(ip)
        item["number"] = response.autonomous_system_number
        item["organization"] = response.autonomous_system_organization
        reader.close()
    except Exception as e:
        logger.warning("{} {}".format(e, ip))

    return item

def get_ip_address(ip):
    try:
        reader = geoip2.database.Reader(Config.city_data_path)
        response = reader.city(ip)
        item = {
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
            "country_name": response.country.name,
            "country_code": response.country.iso_code,
            "region_name": response.subdivisions.most_specific.name,
            "region_code": response.subdivisions.most_specific.iso_code,
        }
        reader.close()
        return item

    except Exception as e:
        logger.warning("{} {}".format(e,ip))
        return {}



