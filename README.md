# Red-Tailed-Boa-Broadcast

**PROVISIONAL SOFTWARE DISCLAIMER**: This software is preliminary and is subject to revision.

Create a workflow for tracking order status using rabbitmq

```
                    +--------+
                    | broker |
                    |        |
+--------+   +---+  | +---+  |  +--------+
|database<---+api+---->out<-----+ leader +---\
+--------+   +-+-+  | +---+  |  +--------+   |
               |    | +---+  |          +----v--+
               \------>in <-------------+ agent |
                    | +---+  |          +-------+
                    +--------+

```

This application is built using the following utilities:

* Database: **PostgreSQL** to keep information about work-unit status
* API: **Python-Flask** http REST service to interact with database, tracking the status
* Broker: **RabbitMQ** communication broker between components
* Leader: **YARN** processor which gathers and prepares work-units to do
* Agent: **Python** application(s) which produce the work-unit final output (random error/success)

## Configuration

Env Var | Host/Port/Value | Description
--- | --- | ---
`RTB_BROADCAST_MAX_QUEUE` | 50 | Always keep `N` in the jobtracker
`RTB_DB_HOST` | postgres:5432 | Database location
`RTB_API_HOST` | rtb-boa:8080 | API
`RTB_BROKER_HOST` | rabbit:5672  | Broker
`RTB_BROKER_BOX` | outbox | Name of the queue to pub/sub to

We use the default postgres username with no password. Since the data table is hard-coded inside the init-db process, it is also hard-coded inside the API. 

## Usage

Start the multi-container application in the background (detached):
```bash

docker-compose up -d [--build]

```

The API is now accessible: `http GET ":8080/"`

### Initialization

When building the image, a backlog of 100 work-units were created, all of which 
need to be completed, and the current status of each are kept in the database.

The goal is to keep the rabbitmq broker queued with work to do 
(configured by `RTB_BROADCAST_MAX_QUEUE` environment variable), while also tracking 
the status of the units until they are completed. 

To see the next units which would be first in line: `http GET ":8080/next"`

### Processing Flow

To get the wheels turning, we will issue a single "go" to the API: `http GET ":8080/go/"`

1. This sends work from the API to the broker, where the leader is listening
1. The leader will store the "out" units in the job tracker, and acknowledge receipt
1. The leader sends a status "queued" back to the broker, including the current queue utilization and status ("queued" will prevent the API from re-sending the unit to the broker)
1. The agents will take work from their job tracker, and publish error or success to the broker
1. The API is listening on the broker, updating scene status as directed (queued/processing/error/success)
1. The API is calculating a "fair use" (TBD), to ensure the utilization is always at the max queued state, until all work is done

**TODO**: [ ] Need to figure out the routing keys used here

# Quick Links

* [RabbitMQ Tutorial - Python](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
* [postgres - Docker Hub](https://hub.docker.com/_/postgres/)
* [rabbitmq - Docker Hub](https://hub.docker.com/_/rabbitmq/)
* [python - Docker Hub](https://hub.docker.com/_/python/)

