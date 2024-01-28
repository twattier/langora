import os
from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import Schema, fields

from config.env import Config
from db.datamodel import Knowledge, Search, Source
from task.service_task import SEARCH_STATUS
from langora import Langora

svc = Flask(__name__)
api = Api(app=svc, version='1.0', title='Langora API', 
          description="REST API for Langora knowledge base system")
ns_task = api.namespace('tasks',description='Submit or manage Tasks')

ma = Marshmallow(svc)

if Config.DEBUG:    
    import rq_dashboard    
    svc.config.from_object(rq_dashboard.default_settings)
    svc.config["RQ_DASHBOARD_REDIS_URL"] = Config.REDIS_URL
    rq_dashboard.web.setup_rq_connection(svc)
    svc.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

app = Langora(is_task_mode=True)
app.init_store_model()

# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------
class KnowledgeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Knowledge
    agent = ma.auto_field()
knowledge_schema = KnowledgeSchema()

class TaskSchema(Schema):
    id = fields.Str()
    cmd = fields.Str()    
    status = fields.Str()
    meta = fields.Dict()
    result = fields.Str()
    enqueued_at = fields.DateTime()
    start_at = fields.DateTime()
    ended_at = fields.DateTime()
    description = fields.Dict()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Datamodel

@api.route('/Knowledge', methods=['GET'])
class Knowledge(Resource):
    @api.doc('Get Knowledge base information')
    def get(self):
        global app        
        try:
            app.db.open_session()
            data = app.db.select_knowledge()
            return knowledge_schema.dump(data)
        finally:
            app.db.close_session()    

# ---------------------------------------------------------------------------
# Task
@ns_task.route('/status/<status_type>', methods=['GET'])
@ns_task.param('status_type', 'Status ["all", "pending" / "queued", "started", "finished", "failed"]')
@ns_task.response(404, 'Invalid status : Need ["all", "pending" / "queued", "started", "finished", "failed"]')
class StatusTasks(Resource):
    @api.doc('List of task per status')
    def get(self, status_type):
        if status_type not in SEARCH_STATUS:
            api.abort(404)
        global app        
        try:
            app.db.open_session()   
            data =  app.loader.list_tasks(status_type)
            return tasks_schema.dump(data)  
        finally:
            app.db.close_session()
    
@ns_task.route('/sources/extract', methods=['GET'])
class SourceExtract(Resource):
    @api.doc('Launch Task to fill empty source extraction')
    def get(self):
        global app
        try:
            app.db.open_session()   
            app.loader.update_extract_sources()                  
        finally:
            app.db.close_session()
    
if __name__ == '__main__':
    svc.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)