import os
from flask import Flask, request
from flask_restx import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import Schema, fields


from config.env import Config
from db.datamodel import Knowledge, Topic, Search, Source
from task.service_task import SEARCH_STATUS
from langora import Langora
from db.dbvector import STORE

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

# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------
class KnowledgeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Knowledge
    agent = ma.auto_field()
knowledge_schema = KnowledgeSchema()

class SearchShortSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Search
    id = ma.auto_field()
    query = ma.auto_field()
    nb_sources = fields.Function(lambda obj: obj.nb_sources())
search_short_schema = SearchShortSchema()
searches_short_schema = SearchShortSchema(many=True)

class TopicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Topic
    id = ma.auto_field()
    name = ma.auto_field()
    searches =  Nested(SearchShortSchema, many=True)
topic_schema = TopicSchema()
topics_schema = TopicSchema(many=True)

class SourceShortSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Source
    id = ma.auto_field()
    url = ma.auto_field()
    site = ma.auto_field()
    title = ma.auto_field()
    snippet = ma.auto_field()
source_short_schema = SourceShortSchema()
sources_short_schema = SourceShortSchema(many=True)

class TaskSchema(Schema):
    id = fields.Str()
    cmd = fields.Str()    
    status = fields.Str()
    meta = fields.Dict()
    result = fields.Str()
    enqueued_at = fields.DateTime()
    start_at = fields.DateTime()
    ended_at = fields.DateTime()    
    name = fields.Str()
    item_id = fields.Str()
    item_label = fields.Str()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class SimilaritySearchSchema(Schema):
    score_query = fields.Float()
    search = Nested(SearchShortSchema)
similarity_search_schema = SimilaritySearchSchema()
similarity_searches_schema = SimilaritySearchSchema(many=True)

class SimilaritySourceSchema(Schema):
    score_total = fields.Function(lambda obj: obj.score_total())
    score_src = fields.Function(lambda obj: obj.score_src())
    score_title = fields.Function(lambda obj: obj.score_title())
    score_summary = fields.Function(lambda obj: obj.score_summary())    
    doc_score = fields.Float()
    doc_type = fields.Str()
    doc_chunk = fields.Int()
    doc_text = fields.Str()
    source = Nested(SourceShortSchema)
similarity_source_schema = SimilaritySourceSchema()
similarity_sources_schema = SimilaritySourceSchema(many=True)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Datamodel

@api.route('/knowledge', methods=['GET'])
class Knowledge(Resource):
    @api.doc('Get Knowledge base information')
    def get(self):
        global app       
        sdb = app.create_session()
        data = sdb.select_knowledge()
        return knowledge_schema.dump(data)

@api.route('/knowledge/stats', methods=['GET'])
class Stats(Resource):
    @api.doc('Get Knowledge base statistics')
    def get(self):
        global app                  
        return app.stats()

@api.route('/topics', methods=['GET', 'POST'])
class Topics(Resource):
    @api.doc('Get topics')
    def get(self):
        global app    
        sdb = app.create_session()
        data = sdb.select_topics()
        return topics_schema.dump(data)

    @api.doc('Add topics')
    def post(self):
        global app   
        data = request.get_json()        
        app.add_topics(data['topics'], up_to_store_id=STORE.SRC_SUMMARY.value)


@api.route('/searches', methods=['GET'])
class Searches(Resource):
    @api.doc('Get searches')
    def get(self):
        global app
        sdb = app.create_session()
        data = sdb.select_top_searches(max=5)
        return searches_short_schema.dump(data)

@api.route('/sources', methods=['GET'])
class Sources(Resource):
    @api.doc('Get sources')
    def get(self):
        global app
        sdb = app.create_session()      
        data = sdb.select_top_sources(max=5)
        return sources_short_schema.dump(data)

@api.route('/similarities', methods=['GET'])
@api.param('query', 'Query for similarity research')
class SourceSimilarities(Resource):
    @api.doc('Similarity research')
    def get(self):
        global app
        sdb = app.create_session()
        query = request.args.get('query')
        
        data = {}
        data['query'] = query
        sim_sources = app.db.vector.similarity_sources(sdb, query)
        data['sources'] = similarity_sources_schema.dump(sim_sources)
        sim_searches = app.db.vector.similarity_searches(sdb, query)
        data['searches'] = similarity_searches_schema.dump(sim_searches)            
        return data
        
@api.route('/genai', methods=['GET'])
@api.param('query', 'Query for genAI')
class genAI(Resource):
    @api.doc('genAI')
    def get(self):
        global app
        sdb = app.create_session()
        query = request.args.get('query')        
        response, sim_docs, sim_sources, sim_searches = app.genAI(sdb, query)
        data = {}
        data['query'] = query
        data['response'] = response
        data['docs'] = similarity_sources_schema.dump(sim_docs)
        data['similarities'] = {'query': query, 
                                'sources': similarity_sources_schema.dump(sim_sources),
                                'searches': similarity_searches_schema.dump(sim_searches)
                                } 
        return data
        

@api.route('/topics/suggest', methods=['GET'])
class SuggestTopics(Resource):
    @api.doc('Suggest Topics')
    def get(self):
        global app
        sdb = app.create_session()
        return app.model.suggest_topics(sdb)

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
        loader = app.create_loader()
        data = loader.list_tasks(status_type)
        return tasks_schema.dump(data)  
    
@ns_task.route('/knowledge/update', methods=['GET'])
@ns_task.param('summarize', 'Update up to summarization (0/1)')
class UpdateKnowledge(Resource):
    @api.doc('Launch Task to fill empty source extraction')
    def get(self, summarize='0'):
        global app        
        up_to_store = STORE.SRC_SUMMARY if summarize == '1' else STORE.SRC_EXTRACT
        app.update_db_knowledge(up_to_store)   

@ns_task.route('/sources/extract', methods=['GET'])
class SourceExtract(Resource):
    @api.doc('Launch Task to fill empty source extraction')
    def get(self):
        global app
        loader = app.create_loader()
        loader.update_extract_sources()                  
    
if __name__ == '__main__':
    svc.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)