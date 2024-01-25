# from rq.job import Job

# class RTask():
#     def __init__(self, job:Job) -> None:
#         self.id = job.get_id()
#         self.cmd = job.description
#         self.desc:TaskDescription = Task.parse_cmd(self.cmd)
#         self.status = job.get_status()        
#         self.meta = job.get_meta()
#         #self.result = str(job.result)
#         self.enqueued_at = utc_to_tz(job.enqueued_at)
#         self.start_at = utc_to_tz(job.started_at)
#         self.ended_at = utc_to_tz(job.ended_at)