import asyncio
import json
import random
from time import sleep, time
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from matplotlib import container
import GA_Newest as n_ga

app = FastAPI()
@app.get("/")
def get():
    return "You're in"
@app.websocket('/ws')
async def websocket_server(web_socket: WebSocket):
    client = await web_socket.accept()
    #print(client.host)
    remaining_stacks = None
    container_arr = None
    parcels_data = None
    parcels_weight = None
    i = 0
    try :
        while True: 
            data = await web_socket.receive_json()
            if data['Status'] == 0:
                result = n_ga.run_two(data['ContainersType'][data['ContainerIndex']], data['Parcels'], data['ParcelsWeight'], first_run=True)
                remaining_stacks = result[1].copy()
                container_arr = data['ContainersType']
                parcels_data = data['Parcels']
                parcels_weight = data['ParcelsWeight']
                result[0]['ContainerIndex'] = data['ContainerIndex']
                result[0]['RemainingStacks'] = len(remaining_stacks)
                result[0]['Status'] = 1
                await web_socket.send_json(result[0])
            else :
                if is_all_zero(remaining_stacks):
                    await web_socket.send_json({"Status" : 2})
                    break
                result = n_ga.run_two(container_arr[data['ContainerIndex']], parcels_data, parcels_weight, first_run=False, remaining_stacks_input=remaining_stacks.copy())
                remaining_stacks = result[1].copy()
                result[0]['ContainerIndex'] = data['ContainerIndex']
                result[0]['RemainingStacks'] = len(remaining_stacks)
                result[0]['Status'] = 1
                for j in remaining_stacks:
                    print(j.name)
                await web_socket.send_json(result[0])
                #await web_socket.send_text(str(len(remaining_stacks)))
    except:
        print("Client disconnected")
        #time.sleep(0.1)
    # await web_socket.accept()
    # #await web_socket.send_text("Connected.")
    # while True:
    #     data = await web_socket.receive_json()
    #     await web_socket.send_text("Processing . . .")
    #     con_index = 0
    #     containers_arr = data['ContainersType']
    #     result = n_ga.run_two(containers_arr[data['ContainerIndex']], data['Parcels'], data['ParcelsWeight'], first_run=True)
    #     result[0]['RemainingParcels'] = result[2]
    #     print(result[2])
    #     if len(result[1]) < 24:
    #         break
    #     con_index += 1
    #     if con_index + 1 > len(containers_arr) - 1:
    #         con_index = 0
    #     else :
    #         con_index += 1
    #     await web_socket.send_text(json.dumps(result[0]))
def is_all_zero(remaining_stacks):
    zeros_counted = 0
    for j in remaining_stacks:
        if j.name == 0:
            zeros_counted += 1
    if zeros_counted == len(remaining_stacks):
        return True
    else :
        return False