import requests
import time

API_URL = "http://localhost:8000/job"

print("\nCLIENT: 🚀 CLIENT STARTING")
time.sleep(1)

payload = {
    "data": "Hello RabbitMQ from Client!"
}

print("CLIENT: 📤 Sending Request to Producer API:")
print(f"CLIENT:    URL: {API_URL}")
print(f"CLIENT:    Payload: {payload}")

response = requests.post(API_URL, json=payload)

print("\nCLIENT: 🟢 RESPONSE FROM PRODUCER:")
print(response.json())

print("\nCLIENT: ✅ Client Finished")
