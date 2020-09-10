import re
from flask_restplus import Resource, Api, reqparse, fields
from app import modules
from bson.objectid import ObjectId

from app.utils import conn_db as conn
base_query_fields = {
    'page': fields.Integer(description="当前页数", example=1),
    'size': fields.Integer(description="页面大小", example=10),
    'order': fields.String(description="排序字段", example='_id'),
}

class ARLResource(Resource):
    def get_parser(self, model, location='json'):
        parser = reqparse.RequestParser(bundle_errors=True)
        for name in model:
            curr_field = model[name]

            parser.add_argument(name,
                                required=curr_field.required,
                                type=curr_field.format,
                                help=curr_field.description,
                                location=location)
        return parser

    def parse_args(self, model, location='json'):
        parser = self.get_parser(model, location)
        args = parser.parse_args()
        return args

    def build_db_query(self, args):
        query_args = {}
        for key in args:
            if key in base_query_fields:
                continue

            if key == '_id':
                if args[key]:
                    query_args[key] = ObjectId(args[key])

                continue

            if args[key] is None:
                continue

            if isinstance(args[key], str):
                query_args[key] = {
                    "$regex": re.escape(args[key]),
                    '$options': "i"
                }
            else:
                query_args[key] = args[key]


        return query_args


    def build_return_items(self, data):
        items = []

        for item in data:
            if "_id" in item:
                item["_id"] = str(item["_id"])
            items.append(item)

        return items

    def build_data(self, args= None , collection = None):

        default_field = self.get_default_field(args)
        page = default_field.get("page", 1)
        size = default_field.get("size", 10)
        orderby_list = default_field.get('order', [("_id", -1)])
        query = self.build_db_query(args)
        result = conn(collection).find(query).sort(orderby_list).skip(size*(page-1)).limit(size)
        count = conn(collection).count(query)
        items = self.build_return_items(result)

        if '_id' in query:
            query['_id'] = str(query['_id'])

        data = {
            "page": page,
            "size": size,
            "total": count,
            "items": items,
            "query": query,
            "code": 200
        }
        return data

    '''
    取默认字段的值，并且删除
    '''
    def get_default_field(self, args):
        default_field_map = {
            "page": 1,
            "size": 10,
            "order": "-_id"
        }

        ret = default_field_map.copy()

        for x in default_field_map:
            if x in args and args[x]:
                ret[x] =  args.pop(x)
                if x == "size":
                    if ret[x]<=0:
                        ret[x] = 10
                    if ret[x]>= 10000:
                        ret[x] = 10000

                if x == "page":
                    if ret[x]<=0:
                        ret[x] = 1

        orderby_list = []
        orderby_field = ret.get("order", "-_id")
        for field in orderby_field.split(","):
            field = field.strip()
            if field.startswith("-"):
                orderby_list.append((field.split("-")[1], -1))
            elif field.startswith("+"):
                orderby_list.append((field.split("+")[1], 1))
            else:
                orderby_list.append((field, 1))

        ret['order'] = orderby_list
        return ret


def get_arl_parser(model, location = 'args'):
    r = ARLResource()
    return r.get_parser(model, location)

from .task import ns as task_ns
from .domain import ns as domain_ns
from .site import ns as site_ns
from .ip import ns as ip_ns
from .url import ns as url_ns
from .user import ns as user_ns
from .image import ns as image_ns
from .cert import ns as cert_ns
from .service import ns as service_ns
from .fileleak import ns as filleak_ns
from .export import ns as export_ns
