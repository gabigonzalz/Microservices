from nats.aio.client import Client as NATS

nats_client = NATS()

# Establish the connection to NATS
async def connect_to_nats():
    await nats_client.connect(
    "nats://nats:4222",
    connect_timeout=10,
    flush_timeout=10,
    reconnect_time_wait=2,
)

# Publish a message to a NATS subject
async def publish_message(subject, message):
    if not nats_client.is_connected:
        await connect_to_nats()
    try:
        await nats_client.publish(subject, message.encode(), timeout=5)
        await nats_client.flush()
    except Exception as e:
        print(f"Failed to publish message: {str(e)}")

# Close the NATS connection
async def close_nats():
    """Close the NATS connection."""
    if nats_client.is_connected:
        await nats_client.close()
