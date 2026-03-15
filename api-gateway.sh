#!/usr/bin/env bash

set -e

echo "=================================================="
echo "🚀 RABBITMQ API Gateway"
echo "=================================================="

cd ~/github/api-gateway

source venv/bin/activate

echo "API-GATEWAY: 🔧 Checking Python dependencies..."

pip install --quiet pika fastapi uvicorn requests

echo "API-GATEWAY: ✅ Dependencies verified"

# --------------------------------------------------
# Clean old processes
# --------------------------------------------------

echo "API-GATEWAY: 🧹 Cleaning previous processes..."

pkill -f "uvicorn producer" || true
pkill -f "worker.py" || true

# --------------------------------------------------
# Reset queue
# --------------------------------------------------

echo "API-GATEWAY: 🗑 Removing old queue (if exists)..."
sudo rabbitmqctl delete_queue task_queue || true

sleep 2

# --------------------------------------------------
# Start Producer
# --------------------------------------------------

echo "=================================================="
echo "🔵 STEP 1: Starting FastAPI Producer"
echo "=================================================="

uvicorn producer:app --host 0.0.0.0 --port 8000 &
PRODUCER_PID=$!

sleep 4

# --------------------------------------------------
# Start Worker
# --------------------------------------------------

echo "=================================================="
echo "🔵 STEP 2: Starting Worker Consumer"
echo "=================================================="

python3 worker.py &
WORKER_PID=$!

sleep 4

# --------------------------------------------------
# Run Client
# --------------------------------------------------

echo "=================================================="
echo "🔵 STEP 3: Sending Client Request"
echo "=================================================="

python3 client.py

sleep 5

echo "=================================================="
echo "🟢 DEMO COMPLETE"
echo "=================================================="

echo "API-GATEWAY: Stopping services..."
kill $PRODUCER_PID || true
kill $WORKER_PID || true
sleep 5

echo "API-GATEWAY: 🗑 cleanup queue ..."
sudo rabbitmqctl delete_queue task_queue || true
sleep 2

deactivate

echo "API-GATEWAY: 🎉 All processes terminated cleanly."


