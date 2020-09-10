from .conn import conn_db


def get_task_ids(domain):
    query = {"target": domain}
    task_ids = []
    for item in conn_db('task').find(query):
        task_ids.append(str(item["_id"]))


    return task_ids


def get_domain_by_id(task_id):
    query = {"task_id": task_id}
    domains = []
    for item in conn_db('domain').find(query):
        domains.append(item["domain"])

    return domains


def arl_domain(domain):
    domains = []
    for task_id in get_task_ids(domain):
        for item in get_domain_by_id(task_id):
            if item.endswith("." + domain):
                domains.append(item)

    return list(set(domains))