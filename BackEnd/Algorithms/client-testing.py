import asyncio
import random
import websockets
import time
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
async def send():
    async with websockets.connect("ws://localhost:8000/ws", ping_timeout=None) as web_socket:
        #web_socket.run_forever()
        min = 1
        max = 100
        dummy_parcels = {
            'ssp': random.randint(min, max),
            'smp': random.randint(min, max),
            'hssp': random.randint(min, max),
            'mlp': random.randint(min, max),
            'mp': random.randint(min, max),
            'lp': random.randint(min, max),
            'lhp': random.randint(min, max),
            'etc': random.randint(min, max)
        }
        dummy_weights = {
            'ssp': [random.randint(1, 100)],
            'smp': [random.randint(1, 100)],
            'hssp': [random.randint(1, 100)],
            'mlp': [random.randint(1, 100)],
            'mp': [random.randint(1, 100)],
            'lp': [random.randint(1, 100)],
            'lhp': [random.randint(1, 100)],
            'etc': [random.randint(1, 100)]
        }
        body = {
            "Parcels" : dummy_parcels,
            "ParcelsWeight" : dummy_weights,
            "ContainersType" : ["Small", "Large", '20Standard', '40HighCube'],
            "Status" : 0,
            "ContainerIndex" : 0
        }

        not_first_run = {
            "Status" : 1,
            "ContainerIndex" : 0
        }
        count = 0
        try :
            while True:
                #await asyncio.wait_for(web_socket.recv(), 3600)
                if count == 0:
                    print("Sending data...")
                    await web_socket.send(json.dumps(body))
                    print("Processing on GA. . .")
                    try:
                        data = await web_socket.recv()
                    except:
                        pass
                    #data_obj = json.loads(data)
                    print("Receiving data :")
                    print(data)
                    not_first_run['ContainerIndex'] += 1
                    await web_socket.send(json.dumps(not_first_run))
                else :
                #asyncio.sleep(0.1)
                    #await asyncio.wait_for(web_socket.recv(), 360.0)
                    try :
                        data = await web_socket.recv()
                    except:
                        pass
                    print("Receiving data :")
                    print(data)
                    data_obj = json.loads(data)
                    if data_obj['ContainerIndex'] + 1 == len(body['ContainersType']):
                      data_obj['ContainerIndex'] = 0
                    else :
                        data_obj['ContainerIndex'] += 1
                    not_first_run['ContainerIndex'] = data_obj['ContainerIndex']
                    await web_socket.send(json.dumps(not_first_run))
                # if data['Status'] == 2:
                #     break
                count += 1
        except:
            print("Connection terminated.")
            #web_socket = websockets.connect("ws://localhost:8000/ws", ping_timeout=None)
asyncio.get_event_loop().run_until_complete((send()))
#asyncio.run_forever()
