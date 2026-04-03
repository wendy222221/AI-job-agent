import json
import time
import uuid
from datetime import datetime

class StructuredLogger:
    def __init__(self, trace_id):
        self.trace_id = trace_id

    def log(self, level, message, **kwargs):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": self.trace_id,
            "level": level,
            "message": message,
            **kwargs
        }
        print(json.dumps(log_obj, ensure_ascii=False))

def get_logger():
    return StructuredLogger(str(uuid.uuid4()))