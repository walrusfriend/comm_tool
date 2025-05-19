import asyncio
import logging
import os
from dotenv import load_dotenv

from livekit import api, rtc

load_dotenv()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
ROOM_NAME = os.getenv("LIVEKIT_ROOM", "my-room")
IDENTITY = os.getenv("LIVEKIT_IDENTITY", "user2")

async def main():
    token = (
        api.AccessToken(api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET)
        .with_identity(IDENTITY)
        .with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME))
        .to_jwt()
    )

    room = rtc.Room()
    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"Participant connected: {participant.identity}")

    @room.on("participant_disconnected")
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        print(f"Participant disconnected: {participant.identity}")

    await room.connect(LIVEKIT_URL, token)
    print(f"Connected to room: {room.name}")
    print("Remote participants:", list(room.remote_participants.keys()))

    # Keep the client running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await room.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
