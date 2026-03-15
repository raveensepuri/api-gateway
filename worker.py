import pika
import time
import logging

logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format="%(message)s")

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "task_queue"

logging.info("WORKER: 🟢 Worker Starting...")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST)
)

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

channel.basic_qos(prefetch_count=1)

logging.info("WORKER: 🟢 Waiting for messages...")


def callback(ch, method, properties, body):

    logging.info("--------------------------------------------------")
    logging.info("WORKER: 🔵 Message Received")
    logging.info(f"WORKER: 📩 Message Body: {body.decode()}")
    logging.info(f"WORKER: 🆔 Message ID: {properties.message_id}")

    logging.info("WORKER: 🔵 Processing message...")
    time.sleep(3)  # simulate workload

    logging.info("WORKER: 🟢 Processing complete")

    ch.basic_ack(delivery_tag=method.delivery_tag)

    logging.info("WORKER: 🟢 Message acknowledged")
    logging.info("--------------------------------------------------")


channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
)

channel.start_consuming()
