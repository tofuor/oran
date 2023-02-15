# ==================================================================================
#       Copyright (c) 2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================

import os, time
import json, requests
from mdclogpy import Logger
from ricxappframe.xapp_frame import RMRXapp, rmr
import traceback

# pylint: disable=invalid-name
ts_xapp = None
logger = Logger(name=__name__)
logger.set_level(10)
sdl = None
hostIP = "192.168.122.65"
aiml_IP_and_port = "192.168.122.65:6969"
ue_id = "22"

UE_NS = "TS-UE-metrics"
CELL_NS = "TS-cell-metrics"

def post_init(self):
    """
    Function that runs when xapp initialization is complete
    """
    global sdl
    sdl = self.sdl

    old_uedata = {}

    UENUM = 60
    sinr_threshold = 20

    for i in range(UENUM):
        old_uedata[str(i)] = None

    logger.debug(f"init var")

    data_buffer = [[1,1,1],[1,1,1],[1,1,1]]
    buffer_flag = 1

    while True:

        #tmp = a1policy(sinr_threshold)
        #sinr_threshold = tmp if tmp != -100 else sinr_threshold
        ue_data_22 = [0,0,0]
        sinr_threshold = 20

        cell_data = []
        cell_data_list = list(sdl.find_and_get(CELL_NS, "", usemsgpack=False).values())
        if cell_data_list != None:
            for cell_data_bytes in cell_data_list:
                cell_data.append(json.loads(cell_data_bytes.decode()))
        # print(cell_data)

        # ue_data = []
        ue_data_list = list(sdl.find_and_get(UE_NS, "", usemsgpack=False).values())
        # if ue_data_list != None:
        #     for ue_data_bytes in ue_data_list:
        #         ue_data.append(json.loads(ue_data_bytes.decode()))
        # print(ue_data)
        
        if ue_data_list != None:

            loggerStr = ""
            loggerStr2 = ""
            predDropData = 0

            serving_cell = {}
            for i in range(19):
                serving_cell[str(i)] = 0

            for ue_data_bytes in ue_data_list:
                ue_data = json.loads(ue_data_bytes.decode())
                CID = int(ue_data["Serving-Cell-ID"][-2:],16)
                serving_cell[str(CID)] = serving_cell[str(CID)] + 1

            for ue_data_bytes in ue_data_list:
                ue_data = json.loads(ue_data_bytes.decode())
                ueStatus = 0
                dropCnt = 0
                problem_count = 0
                same_cell_count = 0

                if old_uedata[ue_data["UE-ID"]] != None:

                    delta_x = ue_data["Meas-Timestamp-PRB"]["tv-sec"] - old_uedata[ue_data["UE-ID"]][2]
                    dropCnt = old_uedata[ue_data["UE-ID"]][4]
                    problem_count = old_uedata[ue_data["UE-ID"]][5]
                    printUEStatus = 0
                    targetCell = None
                    targetCell2 = None
                    neighborCells = None
                    sinr_list = list([])

                    x = ue_data["Meas-Timestamp-PRB"]["tv-sec"]
                    DL = ue_data["PDCP-Bytes-DL"]
                    CID = int(ue_data["Serving-Cell-ID"][-2:],16)

                    if ((delta_x > 0) or (delta_x == 0 and x >= 1200)) and DL < 4000000:
                         printUEStatus = 1
                         predDropData = predDropData + 6000000 - DL

                    if ((delta_x < 0) or (delta_x == 0 and x <= 800)) and DL < 1000000:
                         printUEStatus = 1
                         predDropData = predDropData + 1500000 - DL

                    if str(DL)[-4:] != "0000":
                        dropCnt = dropCnt + 1
                    else:
                        dropCnt = 0

                    if dropCnt > 20:
                        printUEStatus = 1

                    neighborCells = ue_data["Neighbor-Cell-RF"]
                    for neighborCell in neighborCells:
                        nbCID = int(neighborCell["CID"][-2:],16)
                        neighborCell["CID"] = nbCID
                        neighborCell["PRB"] = cell_data[nbCID-1]["Avail-PRB-DL"]
                    
                    # print(type(ue_data["Serving-Cell-RF"]["rsSinr"]))
                    if (ue_data["Serving-Cell-RF"]["rsSinr"]):
                        pass
                        
                    else:
                        ue_data["Serving-Cell-RF"]["rsSinr"] = 0

                    # print(ue_data["Serving-Cell-RF"]["rsSinr"])
                    # print(sinr_threshold)
                    if sinr_threshold <= ue_data["Serving-Cell-RF"]["rsSinr"]:
                        printUEStatus = 0

                    if (printUEStatus > 0):
                        #ue_data["Serving-Cell-RF"]["rsSinr"],
                        targetCell = [CID,
                                      ue_data["Serving-Cell-RF"]["rsSinr"],
                                      cell_data[CID-1]["Avail-PRB-DL"]]

                        for neighborCell in neighborCells:
                            condition1 = (neighborCell["Cell-RF"]["rsSinr"] > targetCell[1])
                            condition2 = True #(serving_cell[str(targetCell[0])]>serving_cell[str(nbCID)])
                            condition3 = (neighborCell["PRB"] > 0)
                            sinr_list.append(neighborCell["Cell-RF"]["rsSinr"]) 

                            if condition1 and condition2 and condition3:
                                targetCell = [neighborCell["CID"],neighborCell["Cell-RF"]["rsSinr"], neighborCell["PRB"]] 
                                problem_count = problem_count + 1
                            if (CID == targetCell[0]):
                                same_cell_count = same_cell_count + 1
                                if (neighborCell["Cell-RF"]["rsSinr"] == sinr_list[-1]):
                                    targetCell2 = [neighborCell["CID"], neighborCell["Cell-RF"]["rsSinr"], neighborCell["PRB"]]

                        sinr_list.sort()

                        if (same_cell_count >= 2):
                            for neighborCell in neighborCells:
                                if (neighborCell["Cell-RF"]["rsSinr"] == sinr_list[-1]):
                                    targetCell2 = [neighborCell["CID"], neighborCell["Cell-RF"]["rsSinr"], neighborCell["PRB"]]
                            base_url = f"http://{hostIP}:9099/handover"
                            headers = {'Content-Type': 'text/plain'}
                            data = f'{ue_data["UE-ID"]},{CID},{targetCell2[0]}'
                            response = requests.post(base_url, headers = headers, data = data)
                            same_cell_count = 0
                            # print(f'--HANDOVER--{data}, status_code={response.status_code}, text={response.text}')

                        loggerStr = loggerStr + f'--UEERROR--UEID={ue_data["UE-ID"]}, '
                        loggerStr = loggerStr + f'x= {ue_data["Meas-Timestamp-PRB"]["tv-sec"]}, '
                        loggerStr = loggerStr + f'delta_x= {delta_x}, '
                        loggerStr = loggerStr + f'dropCnt= {dropCnt}, '
                        loggerStr = loggerStr + f'problem_count= {problem_count}, '
                        loggerStr = loggerStr + f'sinr_list= {sinr_list}, '
                        loggerStr = loggerStr + f'same_cell_count= {same_cell_count}, '
                        #loggerStr = loggerStr + f'rsrp= {ue_data["Serving-Cell-RF"]["rsrp"]}, '
                        #loggerStr = loggerStr + f'rsSinr= {ue_data["Serving-Cell-RF"]["rsSinr"]}, '
                        #loggerStr = loggerStr + f'PRB(CELL)={cell_data[CID-1]["Avail-PRB-DL"]}, '
                        loggerStr = loggerStr + f'PRB(UE)= {ue_data["PRB-Usage-DL"]}, '
                        loggerStr = loggerStr + f'data={ue_data["PDCP-Bytes-DL"]}, '
                        loggerStr = loggerStr + f'CurrCell= [{CID},{ue_data["Serving-Cell-RF"]["rsSinr"]},{cell_data[CID-1]["Avail-PRB-DL"]}], '
                        loggerStr = loggerStr + f'targetCell= {str(targetCell)}, '
                        loggerStr = loggerStr + f'targetCell2= {str(targetCell2)}, '
                        loggerStr = loggerStr + f'others= {str(neighborCells)}\n'


                        if (CID != targetCell[0]) and (problem_count >= 2):
                            base_url = f"http://{hostIP}:9099/handover"
                            headers = {'Content-Type': 'text/plain'}
                            data = f'{ue_data["UE-ID"]},{CID},{targetCell[0]}'
                            response = requests.post(base_url, headers = headers, data = data)
                            problem_count = 0
                            # print(f'--HANDOVER--{data}, status_code={response.status_code}, text={response.text}')
                    else:
                        loggerStr2 = loggerStr2 + f'--UENORMAL--UEID={ue_data["UE-ID"]}, '
                        loggerStr2 = loggerStr2 + f'x= {ue_data["Meas-Timestamp-PRB"]["tv-sec"]}, '
                        loggerStr2 = loggerStr2 + f'delta_x= {delta_x}, '
                        loggerStr2 = loggerStr2 + f'dropCnt= {dropCnt}, '
                        loggerStr2 = loggerStr2 + f'problem_count= {problem_count}, '
                        loggerStr2 = loggerStr2 + f'same_cell_count= {same_cell_count}, '
                        loggerStr2 = loggerStr2 + f'CELLID= {CID}, '
                        loggerStr2 = loggerStr2 + f'rsrp= {ue_data["Serving-Cell-RF"]["rsrp"]}, '
                        loggerStr2 = loggerStr2 + f'rsSinr= {ue_data["Serving-Cell-RF"]["rsSinr"]}, '
                        loggerStr2 = loggerStr2 + f'PRB(CELL)={cell_data[CID-1]["Avail-PRB-DL"]}, '
                        loggerStr2 = loggerStr2 + f'PRB(UE)= {ue_data["PRB-Usage-DL"]}, '
                        loggerStr2 = loggerStr2 + f'data={ue_data["PDCP-Bytes-DL"]}, '
                        loggerStr2 = loggerStr2 + f'others= {str(neighborCells)}\n'

                    

                old_uedata[ue_data["UE-ID"]] = [ue_data["UE-ID"],
                                            ue_data["Serving-Cell-ID"],
                                            ue_data["Meas-Timestamp-PRB"]["tv-sec"],
                                            ueStatus,
                                            dropCnt,
                                            problem_count,
                                            same_cell_count,
                                            ue_data["PRB-Usage-DL"],
                                            ue_data["Serving-Cell-RF"]["rsrp"],
                                            ue_data["Serving-Cell-RF"]["rsrq"],
                                            ue_data["Serving-Cell-RF"]["rsSinr"],
                                            ue_data["Neighbor-Cell-RF"],
                                            ue_data["PDCP-Bytes-DL"]]

                if (ue_data["UE-ID"]) == ue_id:
                    ue_data_22 = ue_data["Meas-Timestamp-PRB"]["tv-sec"],ue_data["Meas-Timestamp-PRB"]["tv-nsec"],ue_data["Serving-Cell-RF"]["rsrp"]

            # print(f'--CELLSTATUS--{str(serving_cell)}')

            if loggerStr != "":
                # print(loggerStr[:-1])
                ueCnt = str(len(loggerStr[:-1].split("\n")))
                # print(f'--UEERROR--UE_count= {ueCnt}, drop data= {predDropData} bytes\n')

            # print(loggerStr2[:-1])
            ueCnt = str(len(loggerStr2.split("\n"))-1)
            # print(f'--UENORMAL--UE_count= {ueCnt}\n')

            # print(ue_data["UE-ID"])
            # print(type(ue_data["UE-ID"]))
            # # if (ue_data["UE-ID"]) == "9":
            # print(ueCnt)

            

        tmp={
            'X':[],
            'Y':[],
            'rsrp':[]
            }
        if buffer_flag >= 3:
            aiml_url = f"http://{aiml_IP_and_port}"
            headers = {'Content-Type': 'text/plain'}
            # data = [ue_data["Meas-Timestamp-PRB"]["tv-sec"],ue_data["Meas-Timestamp-PRB"]["tv-nsec"],ue_data["Serving-Cell-RF"]["rsrp"]]
            data_buffer[2] = data_buffer[1]
            data_buffer[1] = data_buffer[0]
            data_buffer[0] = ue_data_22
            for i in range(3):
                tmp['X'].append(data_buffer[i][0])
                tmp['Y'].append(data_buffer[i][1])
                tmp['rsrp'].append(data_buffer[i][2])
            for i in range(3):
                # print({'input': tmp['X']})
                response = requests.post(aiml_url, headers = headers, data = {'input': tmp['X']})
                response = requests.post(aiml_url, headers = headers, data = {'input': tmp['Y']})
                response = requests.post(aiml_url, headers = headers, data = {'input': tmp['rsrp']})                 

        else:
            print("data_buffer is not full")
            # data = ue_data["Meas-Timestamp-PRB"]["tv-sec"],ue_data["Meas-Timestamp-PRB"]["tv-nsec"],ue_data["Serving-Cell-RF"]["rsrp"]
            print(f'store data in data_buffer[{buffer_flag-1}]，data = {ue_data_22}')
            data_buffer[2] = data_buffer[1]
            data_buffer[1] = data_buffer[0]
            data_buffer[0] = ue_data_22
            buffer_flag = buffer_flag + 1
            

        
        time.sleep(1)

def a1policy(bt):
    """
    Function that processes messages for getting A1 Policy value
    """
    response = requests.get(f"http://{hostIP}:32080/a1mediator/a1-p/policytypes/1/policies?policytype_id=1")

    if response.status_code == 200:
        
        ins = response.text[5:-4]
        # print(ins)

        response = requests.get(f"http://{hostIP}:32080/a1mediator/a1-p/policytypes/1/policies/{ins}")

        if response.status_code == 200:
            if "ueId" in response.text:
                r = json.loads(response.text)["scope"]["qosId"]
                # print(f"A1 Policy changed. qosId= {r}")
        #     else:
        #         print(response.text)
        # else:
        #     print(response.text)

def ts_default_handler(self, summary, sbuf):
    """
    Function that processes messages for which no handler is defined
    """
    logger.debug("default handler received message type {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    # we don't use rts here; free this
    self.rmr_free(sbuf)


def start(thread=False):
    """
    This is a convenience function that allows this xapp to run in Docker
    for "real" (no thread, real SDL), but also easily modified for unit testing
    (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
    """
    logger.debug("TS xApp starting")
    global ts_xapp
    fake_sdl = os.environ.get("USE_FAKE_SDL", None)
    ts_xapp = RMRXapp(ts_default_handler, rmr_port=4560, post_init=post_init, use_fake_sdl=bool(fake_sdl))
    ts_xapp.run(thread)


def stop():
    """
    can only be called if thread=True when started
    TODO: could we register a signal handler for Docker SIGTERM that calls this?
    """
    global ts_xapp
    ts_xapp.stop()


