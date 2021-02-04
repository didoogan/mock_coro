import asyncio
import asynctest



async def some_coro():
    return 'Hello, mock'


class Client:

    async def do_something(self):
        return 10

    async def request(self):
        return 'some response'


client = Client()


class TestCoro(asynctest.TestCase):

    async def test_coro(self):
        result = await some_coro()
        self.assertEqual(result, 'Hello, mock')

    
    async def test_mocked_coro(self):
        some_coro = asynctest.CoroutineMock(return_value='dich')
        result = await some_coro()
        self.assertEqual(result, 'dich')

    async def test_client(self):
        client = asynctest.Mock(Client())
        client.request.return_value = asyncio.Future()
        client.request.return_value.set_result('mocked value')
        res = await client.do_something()
        self.assertEqual(await client.request(), 'mocked value')

    @asynctest.patch.object(client, 'request', return_value='mocked')
    async def test_client_with_patch(self, _):
        self.assertEqual(await client.request(), 'mocked')
        self.assertEqual(await client.do_something(), 10)


if __name__ == '__main__':
    test_case = TestCoro('test_coro_test')
    rest_case.run()

