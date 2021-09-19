import asyncio
import json
import random
import string
import time

import websockets

"""
This module is work in progress...
"""


def sample_task():
    time.sleep(3)
    print("print me second")


async def start():
    # uri = "ws://127.0.0.1:8000/ws/v1/worker/register"
    uri = "ws://aide.comp.nus.edu.sg/ws/v1/worker/register"
    async with websockets.connect(uri) as ws:
        name = "test_worker_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print(name)
        await ws.send(json.dumps({
            "method": "register",
            "name": name
        }))
        while True:
            msg = await ws.recv()
            try:
                obj = json.loads(msg)
                print(obj)
                obj_type = obj["type"]
                if obj_type == "response":
                    pass
                elif obj_type == "request":
                    method = obj["method"]
                    if method == "close":
                        await ws.close()
                        break
                else:
                    raise Exception("Unsupported message type: " + obj_type)
            except Exception as e:
                await ws.close()
                raise e


async def main():
    loop = asyncio.get_event_loop()
    await start()
    # f = loop.run_in_executor(None, sample_task)


if __name__ == "__main__":
    asyncio.run(main())
