import redis
from rq import Queue, get_current_job
from rq.job import Job

from config.env import Config
from utils.functions import args_to_string, utc_to_tz, string_to_args

class Task():
    def __init__(self, job:Job) -> None:
        self.id = job.get_id()
        self.cmd = job.description        
        self.status = job.get_status()        
        self.meta = job.get_meta()
        #self.result = str(job.result)
        self.enqueued_at = utc_to_tz(job.enqueued_at)
        self.start_at = utc_to_tz(job.started_at)
        self.ended_at = utc_to_tz(job.ended_at)
        
        self.name = None
        self.item_id = None
        self.item_label = None

SEARCH_STATUS = ["all", "pending", "queued", "started", "finished", "failed"]

class ServiceTask():
    def __init__(self) -> None:
        self.conn = redis.from_url(Config.REDIS_URL)
        self.queue_tasks = {}  

    def init_queues(self, queue_names:list[str]):
        for queue_name in queue_names:
            self.queue_tasks[queue_name] = Queue(f'{Config.REDIS_QUEUE}-{queue_name}', connection=self.conn)              

    def launch_task(self, queue_name, cmd:str, *args, **kwargs)->Task:
        # if self._is_queue_or_running(queue_name, cmd, args):
        #     return None #avoid launch twice
        return Task(self.queue_tasks[queue_name].enqueue(f'{cmd}', *args, **kwargs))
    
    def _is_queue_or_running(self, queue_name, cmd:str, args):        
        task_cmd = "task.%s(%s)" % (cmd, args_to_string(args))        
        tasks = self.list_tasks_status(queue_name, "pending")
        return any(t.cmd == task_cmd for t in tasks)

    def list_tasks_status(self, status:str)->list[Task]:        
        list = []
        for queue_name in self.queue_tasks.keys():
            list.extend(self.list_queue_tasks_status(queue_name, status))
        list.sort(key=lambda t: (t.status, t.enqueued_at), reverse = True)
        return list

    def list_queue_tasks_status(self, queue_name, status:str)->list[Task]:
        job_ids = []        
        if status in ["all", "pending", "queued"]:
            job_ids.extend(self.queue_tasks[queue_name].get_job_ids())
        if status in ["all", "pending", "started"]:        
            job_ids.extend(self.queue_tasks[queue_name].started_job_registry.get_job_ids())        
        if status in ["all", "finished"]:
            job_ids.extend(self.queue_tasks[queue_name].finished_job_registry.get_job_ids())
        if status in ["all", "failed"]:        
            job_ids.extend(self.queue_tasks[queue_name].failed_job_registry.get_job_ids())        

        return self.get_tasks(job_ids)
    
    def get_tasks(self, job_ids:str)->Task:        
        jobs = Job.fetch_many(job_ids, self.conn)
        list = []
        for job in jobs:                        
            list.append(Task(job))
        list.sort(key=lambda t: t.enqueued_at)        
        return list
    
    def get_task(self, job_id:str)->Task:
        try:
            job = Job.fetch(job_id, self.conn)
        except:
            return None
        return Task(job)
    
from abc import ABC
class QueueTask(ABC):
    def __init__(self, tasks:ServiceTask) -> None:
        self.tasks = tasks  

    def _parse_cmd(self, cmd:str)->(str, []):
        idxf = cmd.rfind('.')
        idxp = cmd.find('(')        
        func = cmd[idxf+1:idxp]
        params = cmd[idxp+1:-1]        
        return func, string_to_args(params)

    # def send_progress(self, msg:str, pct:float,
    #                    prt=False, msg_type:str=None):
    #     if prt:
    #         print(msg)
    #     job = get_current_job()
    #     if job:
    #         job.meta['msg'] = msg
    #         job.meta['pct'] = pct
    #         job.save_meta()
    #         if msg_type:
    #             self.send_message(TaskMsg(job.id, msg_type, msg))

    # def send_message(self, msg:TaskMsg)->None:
    #     pass
    #     #self.conn.publish(Config.REDIS_CHANNEL, msg.get_message()) #Manage Notification