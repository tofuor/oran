import time
import json
import requests

counter = {}
counter['index'] = 0
positions = []
jsonType = {'Content-Type': 'application/json'}
additionalUeIds = []

def readPosition():
  pos = positions[counter['index']]
  counter['index'] += 1
  if counter['index'] == len(positions):
    counter['index'] = 0
  return pos

f = open("uav_traj_1.csv", "r")
positions = f.read().split('\n')
positions.pop()
f.close()
for lineData in positions:
  rawData = lineData.split(',')
  posData = {}
  posData['id'] = '1'
  timestamp = int(float(rawData[0]))
  posData['timestamp'] = timestamp
  posData['tags'] = []
  ueData = {}
  ueData['imsi'] = '0000000000000'
  ueData['posX'] = float(rawData[1])
  ueData['posY'] = float(rawData[2])
  ueData['posZ'] = float(rawData[3])
  ueData['timestamp'] = timestamp
  posData['tags'].append(ueData)

  #print(json.dumps(posData))
  response = requests.put("http://192.168.122.65:32080/a1mediator/a1-p/update_ue_position", data = json.dumps(posData), headers = jsonType)
  if response.status_code != 201:
    print("error! response code = " + str(response.status_code))
    break
  time.sleep(0.02)
  #time.sleep(1)
