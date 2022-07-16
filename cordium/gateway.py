from __future__ import annotations

import asyncio
from platform import system
from random import random

from aiohttp import ClientSession

__all__ = ("Gateway",)


class Gateway:
    session: ClientSession
    token: str
    sequence: int | None = None
    session_id: int | None = None

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    ACK = 11

    def __init__(self, *, intents: int = 0) -> None:
        self.intents = intents

    async def send_heartbeat(self) -> None:
        await self.send(
            {
                "op": 1,
                "d": self.sequence,
            }
        )

    async def heartbeat(self, interval: float) -> None:
        self._heartbeat_ack = True
        await asyncio.sleep(interval * random())
        await self.send_heartbeat()
        while True:
            if self._heartbeat_ack:
                await asyncio.sleep(interval)
                await self.send_heartbeat()
                self._heartbeat_ack = False
            else:
                await self.close()

    async def connect(self) -> None:
        self.socket = await self.session.ws_connect(
            "wss://gateway.discord.gg?v=10&encoding=json"
        )
        if self.session_id:
            await self.resume()
        else:
            await self.identify()
        await asyncio.create_task(self.receive())

    async def identify(self) -> None:
        await self.send(
            {
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": self.intents,
                    "properties": {
                        "os": system(),
                        "browser": "Cordium",
                        "device": "Cordium",
                    },
                    "presence": {
                        "activities": [{"name": "with the API", "type": 0}],
                        "status": "idle",
                    },
                },
            }
        )

    async def process_event(self, name: str, data) -> None:
        ...

    async def send(self, payload) -> None:
        await self.socket.send_json(payload)

    async def receive(self) -> None:
        while True:
            raw_data = await self.socket.receive_json()
            data, op = raw_data.get("d", {}), raw_data["op"]

            if op == 0:
                self.sequence = raw_data["s"]
                if (event := raw_data["t"]) == "READY":
                    self.session_id = data["session_id"]
                await self.process_event(event, data)

            elif op == 1:
                await self.send_heartbeat()

            elif op == 10:
                await self.send_heartbeat()
                asyncio.run_coroutine_threadsafe(
                    self.heartbeat(data["heartbeat_interval"] / 1000),
                    asyncio.get_event_loop(),
                )

            elif op == 11:
                self._heartbeat_ack = True

    async def resume(self) -> None:
        await self.send(
            {
                "op": 6,
                "d": {
                    "token": self.token,
                    "session_id": self.session_id,
                    "seq": self.sequence,
                },
            }
        )

    async def close(self) -> None:
        await self.socket.close()
        await self.session.close()
