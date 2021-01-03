from flask import Blueprint, jsonify
from flask_restx import Api, Resource, reqparse
import pymysql
import re
import time
from . import conn, reconnect, last_connection

# from flask_restx import reqparse
# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args()

blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/docs')

# Bring in the rest of our API code here
@api.route('/')
class Home(Resource):
    def get(self):
        return {'data': 'Welcome to the home page', 'error': None}

@api.route('/countries/', '/countries/<string:word>')
class GetCountries(Resource):
    def get(self, word = ''):
        parser = reqparse.RequestParser()
        parser.add_argument('all')
        args = parser.parse_args()
        return {'data': "Error encountered. Try again later.", 'error': str(e)}, 500

@api.route('/country/<string:country>')
class FilterCountry(Resource):
    def get(self, country):
        parser = reqparse.RequestParser()
        parser.add_argument('cursor', 0, type='int')
        parser.add_argument('limit', 20, type='int')
        args = parser.parse_args()

        return jsonify(args)

    def get_by_country(self, country, id=0, limit=20):
        rows = {}
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = f"SELECT * FROM v_companies WHERE id > {id} AND country = '{country}' LIMIT {limit}"
                cursor.execute(query)
                rows = cursor.fetchall()
        except Exception:
            reconnect()
        return rows

    def safe_count_rows(self, **kwargs):
        res = {'args': kwargs}
        ask = safe_where_args(**kwargs)

        # only treat values as text (not working with NULL)
        where = ' AND '.join([f"{ask_i[0]} {ask_i[1]} '{str(ask_i[2])}'" for ask_i in ask])
        if ask:
            with conn.cursor() as cursor:
                query = f"SELECT COUNT(*) FROM v_companies WHERE {where};"
                cursor.execute(query)
                result = cursor.fetchone()
                res['n_rows'] = result[0]
        return res, 200

def safe_where_args(**kwargs):
    ask = []
    if 'id' in kwargs:
        ask.append('id', '>', f"{kwargs.get('id')}")
    for kw in ('site', 'country', 'category'):
        if kw in kwargs:
            ask.append((kw, '=', f"{kwargs.get(kw)}"))
    return ask

def return_forbidden(path):
    content = {
        'error': '403 - Forbidden',
        'data': {
            'path': path,
        }
    }
    return content, 403