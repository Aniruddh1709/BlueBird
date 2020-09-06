import sys
import os

from sqslistener import SQSListener

sys.path.append('/<project_name>')

from app import app


class Listener(SQSListener):
    def handle_message(self, body, event_type):
        pass

    @classmethod
    def start(cls):
        listener = Listener(
            access_key_id=app.config['AWS_S3_ACCESS_KEY_ID'],
            secret_access_key=app.config['AWS_S3_SECRET_ACCESS_KEY'],
            region_name=app.config['AWS_REGION'],
            #add SQS_URL and replace the key in settings
            queue=app.config['SQS_URL']
        )

        env = os.environ['ENV'].lower() if 'ENV' in os.environ else 'development'
        if env == 'development':
            exit(0)

        listener.listen()
        exit(1)


if __name__ == '__main__':
    Listener.start()
