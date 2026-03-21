
* Starts **RabbitMQ (assumed already running)**
* Runs a **Producer API (FastAPI)**
* Runs a **Worker Consumer**
* Runs a **Client**
* Prints **explicit step-by-step logs**
* Shows **inputs and outputs clearly**
* Demonstrates **message flow visibility**

---

# 📁 Recommended Project Structure

```
api-gateway/
│
├── venv/
├── producer.py
├── worker.py
├── client.py
├── api-gateway.sh
└── README.md
```

---

# 🟢 1. Improved Producer (FastAPI)

This version:

* Creates connection safely
* Logs every step
* Shows message metadata
* Uses proper channel handling

---

# 🟢 2. Improved Worker (Consumer)

This version:

* Prints clear lifecycle logs
* Shows message receipt
* Simulates processing time
* Acknowledges properly
* Handles graceful shutdown

---

# 🟢 3. Dedicated Client Script

Instead of curl, this gives structured logs.

---

# 🟢 4. Gateway Script

This script:

* Starts services in correct order
* Waits properly
* Shows progress
* Prints clear stage headers
* Runs cleanly

---

# 🟢 5. How To Run

```bash
chmod +x api-gateway.sh
./api-gateway.sh
```

---

# 🟢 6. Expected Output Flow

### Terminal 1 (Worker)

```
Worker Starting...
Waiting for messages...

--------------------------------------------------
Message Received
Message Body: Hello RabbitMQ from Client!
Message ID: 3f2c...
Processing message...
Processing complete
Message acknowledged
--------------------------------------------------
```

---

### Terminal 2 (Script)

```
CLIENT STARTING
Sending Request to Producer API...
RESPONSE FROM PRODUCER:
{
  "status": "queued",
  "message_id": "3f2c...",
  "data_sent": "Hello RabbitMQ from Client!"
}
```

---

### Producer Logs

```
STEP 1: Received API request
Input Data: Hello RabbitMQ from Client!

STEP 2: Publishing message
Message ID: 3f2c...

STEP 3: Message successfully queued
```

---

# 🟢 7. What This Demonstrates

✔ REST → Message Queue
✔ Producer decoupling
✔ Worker asynchronous processing
✔ Message persistence
✔ Proper ACK handling
✔ Clear message lifecycle
✔ Real-world architecture pattern

---

# 🟢 8. Architecture Being Demonstrated

```
Client
   │
   ▼
FastAPI Producer
   │
   ▼
RabbitMQ Exchange
   │
   ▼
task_queue
   │
   ▼
Worker Consumer
```

---

# API-GATEWAY complete execution log

```
$:~/api-gateway$ ./api-gateway.sh
==================================================
🚀 RABBITMQ API-GATEWAY
==================================================
API-GATEWAY: 🔧 Checking Python dependencies...
API-GATEWAY: ✅ Dependencies verified
API-GATEWAY: 🧹 Cleaning previous processes...
API-GATEWAY: 🗑 Removing old queue (if exists)...
[sudo] password for admin:
Deleting queue 'task_queue' on vhost '/' ...
Error:
Queue not found
==================================================
🔵 STEP 1: Starting FastAPI Producer
==================================================
INFO:     Started server process [120723]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
==================================================
🔵 STEP 2: Starting Worker Consumer
==================================================
WORKER: 🟢 Worker Starting...
WORKER: 🟢 Waiting for messages...
==================================================
🔵 STEP 3: Sending Client Request
==================================================

CLIENT: 🚀 CLIENT STARTING
CLIENT: 📤 Sending Request to Producer API:
CLIENT:    URL: http://localhost:8000/job
CLIENT:    Payload: {'data': 'Hello RabbitMQ from Client!'}
PRODUCER: 🔵 Received API request
PRODUCER: 📥 Input Data: Hello RabbitMQ from Client!
PRODUCER: 🔵 Publishing message to RabbitMQ
PRODUCER: 📤 Message ID: 9f0eefe5-cd5b-4e41-8c4c-3bedca06e608
--------------------------------------------------
PRODUCER: 🟢 Message successfully queued
WORKER: 🔵 Message Received
WORKER: 📩 Message Body: Hello RabbitMQ from Client!
WORKER: 🆔 Message ID: 9f0eefe5-cd5b-4e41-8c4c-3bedca06e608
WORKER: 🔵 Processing message...
INFO:     127.0.0.1:48608 - "POST /job HTTP/1.1" 200 OK

CLIENT: 🟢 RESPONSE FROM PRODUCER:
{'status': 'queued', 'message_id': '9f0eefe5-cd5b-4e41-8c4c-3bedca06e608', 'data_sent': 'Hello RabbitMQ from Client!'}

CLIENT: ✅ Client Finished
WORKER: 🟢 Processing complete
WORKER: 🟢 Message acknowledged
--------------------------------------------------
==================================================
🟢 API-GATEWAY COMPLETE
==================================================
API-GATEWAY: Stopping services...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [120723]
API-GATEWAY: 🗑 cleanup queue ...
Deleting queue 'task_queue' on vhost '/' ...
Queue was successfully deleted with 0 ready messages
API-GATEWAY: 🎉 All processes terminated cleanly.
```
