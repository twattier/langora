from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import Schema, fields

from config.env import Config
from db.datamodel import Knowledge, Search, Source
from langora import Langora

svc = Flask(__name__)
api = Api(app=svc, version='1.0', title='Langora API', 
          description="REST API for Langora knowledge base system")

ma = Marshmallow(svc)

app = Langora()
app.init_services()

# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------
class KnowledgeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Knowledge
    agent = ma.auto_field()
    topics = ma.auto_field()
knowledge_schema = KnowledgeSchema()

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@api.route('/Knowledge', methods=['GET'])
class Knowledge(Resource):
    @api.doc('Get Knowledge base information')
    def get(self):
        global app
        return app.get_knowledge(knowledge_schema)
    
if __name__ == '__main__':
    svc.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)