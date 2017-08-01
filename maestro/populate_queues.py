import os

import pika

from dbconnect import db_instance


def push_work(work, host='localhost', port=5672, routing_key='task.todo'):
    cfg = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(cfg)
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs',
                             type='topic')

    for unitid, unitname in work:
        message = str(dict(i=unitid, n=unitname))
        channel.basic_publish(exchange='topic_logs',
                              routing_key=routing_key,
                              body=message)
        print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()


def main(max_queue=50, rabbit_host='localhost', rabbit_port=5672):
    """ the main 'Producer' code to publish messages """
    work = db_instance.get_work(n_records=max_queue)
    push_work(work, rabbit_host, rabbit_port)


if __name__ == '__main__':
    MAESTRO_MAX_QUEUE = int(os.environ.get('MAESTRO_MAX_QUEUE', "50"))
    MAESTRO_RMQHOST = os.environ.get('MAESTRO_RMQHOST', 'localhost')
    MAESTRO_RMQPORT = int(os.environ.get('MAESTRO_RMQPORT', '5672'))
    main(MAESTRO_MAX_QUEUE, MAESTRO_RMQHOST, MAESTRO_RMQPORT)
