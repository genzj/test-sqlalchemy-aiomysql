# -*- encoding: utf-8 -*-
import asyncio
import json
from datetime import datetime

from test_sqlalchemy_aiomysql.model.counter import Counter
from test_sqlalchemy_aiomysql.model.db import db


async def handle_counter(reader, writer):
    data = await reader.read(1)
    addr = writer.get_extra_info('peername')

    num = int(data[0])
    print('Received %r from %r - record num %d' % (data, addr, num))

    answer = []

    async with db.engine.acquire() as conn:
        transaction = await conn.begin()
        result = await conn.execute(
            Counter.__table__.insert().values(counter=num, created_at=datetime.utcnow())
        )
        print('inserted id:', result.lastrowid)
        await transaction.commit()
        result = await conn.execute(
            Counter.__table__.select().where(Counter.counter == num)
        )
        for r in await result.fetchall():
            answer.append({
                'id': r.id,
                'counter': r.counter,
                'created_at': str(r.created_at),
            })

    writer.write(json.dumps(answer, indent=2).encode('ascii'))
    await writer.drain()

    print('Close the client socket')
    writer.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(
        db.init_engine(
            user='nbiot',
            db='test_aiomysql',
            host='192.168.44.128',
            password='nbiot'
        )
    )
    coro = asyncio.start_server(handle_counter, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
