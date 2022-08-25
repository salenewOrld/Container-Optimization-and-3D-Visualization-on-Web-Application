import json
import random
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
    #json.dumps({
#     "Response": {
#         "Containers": [
#             {
#                 "ArrangementPattern": [
#                     [
#                         103,
#                         103,
#                         102
#                     ],
#                     [
#                         103,
#                         103,
#                         102
#                     ],
#                     [
#                         103,
#                         103,
#                         103
#                     ],
#                     [
#                         103,
#                         102,
#                         103
#                     ],
#                     [
#                         105,
#                         0,
#                         105
#                     ],
#                     [
#                         103,
#                         103,
#                         103
#                     ],
#                     [
#                         106,
#                         103,
#                         0
#                     ],
#                     [
#                         103,
#                         103,
#                         103
#                     ],
#                     [
#                         103,
#                         103,
#                         101
#                     ],
#                     [
#                         0,
#                         0,
#                         0
#                     ],
#                     [
#                         0,
#                         0,
#                         0
#                     ]
#                 ],
#                 "ContainerType": "Large"
#             }
#         ]
#     }
# })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data_test = [101, 102, 103, 104, 105, 106, 201, 202, 203, 204, 205, 206, 207, 208]
    while True:
        testing_data = {
    "Response": {
        "Containers": [
            {
                "ArrangementPattern": [
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ],
                    [
                        random.choice(data_test),
                        random.choice(data_test),
                        random.choice(data_test)
                    ]
                ],
                "ContainerType": random.choice(["Large", "Small"])
            }
        ]
    }}
        await websocket.send_json(testing_data)
        data = await websocket.receive_json()
        # await web_socket.recv()
        is_identical = False
        if data == testing_data:
            is_identical = True
        print(is_identical)