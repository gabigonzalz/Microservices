import asyncio
from nats.aio.client import Client as NATS

nats_client = NATS()

# Establish a connection to NATS
async def connect_to_nats():
    await nats_client.connect(
    "nats://nats:4222",
    connect_timeout=10,
    flush_timeout=10,
    reconnect_time_wait=2,
)

# Subscribe to a NATS subject
async def subscribe_to_subject(subject, callback):
    if not nats_client.is_connected:
        await connect_to_nats()
    await nats_client.subscribe(subject, cb=callback)

# Close the NATS connection
async def close_nats():
    if nats_client.is_connected:
        await nats_client.close()
