import uvicorn
from fastapi import FastAPI
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint
from GA_Newest import *

# Methods to expose to the clients
# class ConcatServer(RpcMethodsBase):
#     async def concat(self, a=0, b=0):
#         return a + b
class SocketGA(RpcMethodsBase):
    async def run(self):
        i = 0
        while i < 20:
            i = await self.run_by_one(i)
        # return json.dumps({
        #     "Test" : "GG"
        # })
        return i
    async def run_by_one(self, i):
        return i + 1


# Init the FAST-API app
app =  FastAPI()
# Create an endpoint and load it with the methods to expose
endpoint = WebsocketRPCEndpoint(SocketGA())
# add the endpoint to the app
endpoint.register_route(app, "/ws")

# Start the server itself
uvicorn.run(app, host="0.0.0.0", port=9000)