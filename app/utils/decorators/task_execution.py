import time
import datetime
from app.utils.kafka_producer import send_to_stream


def send_to_output_stream(method):
    def out_stream(*args, **kw):
        try:
            ts = time.time()
            dt = datetime.datetime.now().timestamp()
            result = method(*args, **kw)
            te = time.time()
            send_to_stream("RUN_TASK_EXECUTE", {
                'event_time': dt,
                'execution_data': result,
                'execute_time': ts-te,
            })
            return result
        except Exception as e:
            send_to_stream(
                "ERROR_TASK_EXECUTE", {'stack_trace': e})
    return out_stream
