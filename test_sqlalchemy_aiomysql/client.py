# -*- encoding: utf-8 -*-
import asyncio
import random


async def tcp_echo_client(num, loop):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888,
        loop=loop
    )

    print('Send: %r' % num)
    writer.write(bytes([num, ]))

    data = await reader.read(100)
    print('Received: %s' % data.decode())

    print('Close the socket')
    writer.close()


if __name__ == '__main__':
    num = random.randint(0, 0xff)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(num, loop))
    loop.close()
