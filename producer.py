import pika
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI()

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "task_queue"

class JobRequest(BaseModel):
    data: str


def get_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel


@app.post("/job")
def send_job(job: JobRequest):

    logging.info("PRODUCER: 🔵 Received API request")
    logging.info(f"PRODUCER: 📥 Input Data: {job.data}")

    connection, channel = get_channel()

    message_id = str(uuid.uuid4())

    logging.info("PRODUCER: 🔵 Publishing message to RabbitMQ")
    logging.info(f"PRODUCER: 📤 Message ID: {message_id}")

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=job.data,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
            message_id=message_id,
        ),
    )

    connection.close()

    logging.info("PRODUCER: 🟢 Message successfully queued")

    return {
        "status": "queued",
        "message_id": message_id,
        "data_sent": job.data,
    }
