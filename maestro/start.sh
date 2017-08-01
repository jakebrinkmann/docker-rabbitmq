#!/bin/bash
sleep 5 # Wait for RabbitMQ to startup all the way FIXME: Better way to do this?

python /usr/src/app/maestro/populate_queues.py
