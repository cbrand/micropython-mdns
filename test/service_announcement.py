import uasyncio as asyncio

from mdns_client import Client
from mdns_client.responder import Responder, generate_random_postfix

print("Connected to WIFI!")


async def serve_client(reader, writer):
    writer.write("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    writer.write("<h1>test response</h1>")
    await writer.drain()
    await writer.wait_closed()
    print("disconnected")
    
    
async def setup_mdns():
    local_ip = "0.0.0.0"
    print(f"Setting up MDNS on local ip: {local_ip}")
    client = Client(local_ip)
    host = "pico-{}".format(generate_random_postfix())
    responder = Responder(
        client,
        own_ip=lambda: local_ip,
        host=lambda: host,
    )
    responder.debug = True
    responder.advertise("_myawesomeservice", "_tcp", port=1234)
    


async def run():
    await setup_mdns()
    await asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 1234)) # open port 1234 

    while True:
        await asyncio.sleep(3)


asyncio.run(run())
