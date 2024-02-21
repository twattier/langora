import os
from flask import Flask, request
from flask_restx import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import Schema, fields


from config.env import Config
from db.datamodel import Knowledge, Topic, Search, Source, SearchSource, SourceText, SourceTextImage
from task.service_task import SEARCH_STATUS
from langora import Langora
from db.dbvector import STORE

svc = Flask(__name__)
api = Api(app=svc, version='1.0', title='Langora API', 
          description="REST API for Langora knowledge base system")

ns_knowledges = api.namespace('knowledges',description='Knowledges resources')
ns_topics = api.namespace('topics',description='Topics resources')
ns_searches = api.namespace('searches',description='Searches resources')
ns_sources = api.namespace('sources',description='Sources resources')
ns_tasks = api.namespace('tasks',description='Submit or manage Tasks')


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

class SearchSourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SearchSource
    rank = ma.auto_field()
    date_created = ma.auto_field()
    source = Nested(SourceShortSchema)

class SearchShortSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Search
    id = ma.auto_field()
    query = ma.auto_field()
    nb_sources = fields.Function(lambda obj: obj.nb_sources())
search_short_schema = SearchShortSchema()
searches_short_schema = SearchShortSchema(many=True)

class SourceSearchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SearchSource
    rank = ma.auto_field()
    date_created = ma.auto_field()
    search = Nested(SearchShortSchema)

class SourceTextImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SourceTextImage
    id = ma.auto_field()
    order = ma.auto_field()
    url = ma.auto_field()
    alt = ma.auto_field()    

class SourceTextSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SourceText
    id = ma.auto_field()
    order = ma.auto_field()
    index = ma.auto_field()
    title = ma.auto_field()
    text = ma.auto_field()
    images = Nested(SourceTextImageSchema, many=True)

class SourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Source
    id = ma.auto_field()
    url = ma.auto_field()
    site = ma.auto_field()
    title = ma.auto_field()
    snippet = ma.auto_field()
    extract = ma.auto_field()
    date_extract = ma.auto_field()
    summary = ma.auto_field()
    date_summary = ma.auto_field()
    source_texts = Nested(SourceTextSchema, many=True)   
    search_sources = Nested(SourceSearchSchema, many=True)   
source_schema = SourceSchema()

class TopicShortSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Topic
    id = ma.auto_field()
    name = ma.auto_field()

class TopicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Topic
    id = ma.auto_field()
    name = ma.auto_field()
    searches =  Nested(SearchShortSchema, many=True)
topic_schema = TopicSchema()
topics_schema = TopicSchema(many=True)

class SearchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Search
    id = ma.auto_field()
    query = ma.auto_field()
    date_created = ma.auto_field()
    topics = Nested(TopicShortSchema, many=True)
    search_sources = Nested(SearchSourceSchema, many=True)    
search_schema = SearchSchema()

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
# Knowledges

@ns_knowledges.route('/', methods=['GET'])
class Knowledge(Resource):
    @ns_knowledges.doc('Get Knowledge base information')
    def get(self):
        global app       
        try:
            sdb = app.create_session()
            data = sdb.select_knowledge()
            return knowledge_schema.dump(data)
        finally:
            sdb.close()

@ns_knowledges.route('/stats', methods=['GET'])
class Stats(Resource):
    @ns_knowledges.doc('Get Knowledge base statistics')
    def get(self):
        global app                  
        return app.stats()
    
@ns_knowledges.route('/similarities', methods=['GET'])
@ns_knowledges.param('query', 'Query for similarity research')
class SourceSimilarities(Resource):
    @ns_knowledges.doc('Similarity research')
    def get(self):
        global app
        try:
            sdb = app.create_session()
            query = request.args.get('query')
            
            data = {}
            data['query'] = query
            sim_sources = app.db.vector.similarity_sources(sdb, query)
            data['sources'] = similarity_sources_schema.dump(sim_sources)
            sim_searches = app.db.vector.similarity_searches(sdb, query)
            data['searches'] = similarity_searches_schema.dump(sim_searches)            
            return data
        finally:
            sdb.close()

       
@ns_knowledges.route('/genai', methods=['GET'])
@ns_knowledges.param('query', 'Query for genAI')
class genAI(Resource):
    @ns_knowledges.doc('genAI')
    def get(self):
        global app
        try:
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
        finally:
            sdb.close()
    
@ns_knowledges.route('/extract', methods=['POST'])
@ns_knowledges.param('summarize', 'Update up to summarization (0/1)')
class UpdateKnowledge(Resource):
    @ns_knowledges.doc('Launch Task to fill empty source extraction')
    def post(self, summarize='0'):
        global app        
        up_to_store = STORE.SRC_SUMMARY if summarize == '1' else STORE.SRC_EXTRACT
        app.update_db_knowledge(up_to_store)  
    
# ---------------------------------------------------------------------------
# Topics
    
@ns_topics.route('/', methods=['GET', 'POST'])
class Topics(Resource):
    @ns_topics.doc('Get topics')
    def get(self):
        global app    
        try:
            sdb = app.create_session()
            data = sdb.select_topics()
            return topics_schema.dump(data)
        finally:
            sdb.close()

    @ns_topics.doc('Add topics')
    def post(self):
        global app   
        data = request.get_json()        
        app.add_topics(data['topics'], up_to_store_id=STORE.SRC_SUMMARY.value)

@ns_topics.route('/suggest', methods=['GET'])
class SuggestTopics(Resource):
    @ns_topics.doc('Suggest Topics')
    def get(self):
        global app
        try:
            sdb = app.create_session()
            return app.model.suggest_topics(sdb)
        finally:
            sdb.close()
    
# ---------------------------------------------------------------------------
# Searches

@ns_searches.route('/', methods=['GET'])
class Searches(Resource):
    @ns_searches.doc('Get searches')
    def get(self):
        global app
        try:
            sdb = app.create_session()
            data = sdb.select_top_searches(max=10)
            return searches_short_schema.dump(data)
        finally:
            sdb.close()

@ns_searches.route('/<search_id>', methods=['GET'])
class Search(Resource):
    @ns_searches.doc('Get searche')
    def get(self, search_id):
        global app
        try:
            sdb = app.create_session()
            data = sdb.select_search_by_id(search_id)
            return search_schema.dump(data)
        finally:
            sdb.close()
    
@ns_searches.route('/similarities', methods=['GET'])
@ns_searches.param('query', 'Query for similarity research')
class SearchesSimilarities(Resource):
    @ns_searches.doc('Similarity research')
    def get(self):
        global app
        try:
            sdb = app.create_session()
            query = request.args.get('query')
            
            data = {}
            data['query'] = query        
            sim_searches = app.db.vector.similarity_searches(sdb, query, nb=10)
            data['searches'] = similarity_searches_schema.dump(sim_searches)            
            return data
        finally:
            sdb.close()

# ---------------------------------------------------------------------------
# Sources
    
@ns_sources.route('/', methods=['GET'])
class Sources(Resource):
    @ns_sources.doc('Get sources')
    def get(self):
        global app
        try:
            sdb = app.create_session()      
            data = sdb.select_top_sources(max=10)
            return sources_short_schema.dump(data)
        finally:
            sdb.close()

@ns_sources.route('/<source_id>', methods=['GET'])
class Source(Resource):
    @ns_sources.doc('Get sources')
    def get(self, source_id):
        global app
        try:
            sdb = app.create_session()      
            data = sdb.select_source_by_id(source_id)
            return source_schema.dump(data)
        finally:
            sdb.close()

@ns_sources.route('/<source_id>/sourcetexts', methods=['POST'])
class SourceTexts(Resource):
    @ns_sources.doc('Update SourceTexts')
    def post(self, source_id):
        global app
        try:
            loader = app.create_loader()
            changes = request.json            
            loader.update_texts(source_id, changes)
        finally:
            loader.sdb.close()

@ns_sources.route('/similarities', methods=['GET'])
@ns_sources.param('query', 'Query for similarity research')
class SearchesSimilarities(Resource):
    @ns_sources.doc('Similarity research')
    def get(self):
        global app
        try:
            sdb = app.create_session()
            query = request.args.get('query')
            
            data = {}
            data['query'] = query        
            sim_sources = app.db.vector.similarity_sources(sdb, query, nb=10)
            data['sources'] = similarity_sources_schema.dump(sim_sources)
            return data
        finally:
            sdb.close()
    
@ns_sources.route('/summaries', methods=['POST'])
class SourcesSummaries(Resource):
    @ns_sources.doc('Launch Task to fill empty source summary')
    def post(self):
        global app
        try:
            loader = app.create_loader()
            loader.update_summarize_sources()
        finally:
            loader.sdb.close()

# ---------------------------------------------------------------------------
# Task
    
@ns_tasks.route('/status/<status_type>', methods=['GET'])
@ns_tasks.param('status_type', 'Status ["all", "pending" / "queued", "started", "finished", "failed"]')
@ns_tasks.response(404, 'Invalid status : Need ["all", "pending" / "queued", "started", "finished", "failed"]')
class StatusTasks(Resource):
    @ns_tasks.doc('List of task per status')
    def get(self, status_type):
        if status_type not in SEARCH_STATUS:
            api.abort(404)
        global app
        try:
            loader = app.create_loader()
            data = loader.list_tasks(status_type)
            return tasks_schema.dump(data)        
        finally:
            loader.sdb.close()
    
if __name__ == '__main__':
    svc.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)