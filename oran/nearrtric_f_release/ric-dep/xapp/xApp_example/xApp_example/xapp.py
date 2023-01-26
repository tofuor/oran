# xApp Version 1.0
# © 2021 III All Rights Reserved

import logging
import json
import os
import sys
import threading
from ricxappframe.xapp_frame import Xapp
# from ricxappframe.xapp_frame import RMRXapp
from xapp.xapp_api3 import xApp
import redis
import csv

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

fileName = sys.argv[0]
fileName = os.path.splitext(fileName)[0]
counted = 0
xapp_port = 8132
xAppAPI = xApp(fileName, xapp_port)
RFID = 33
e2node_list = []
bo = True

# xAppAPI.initials(fileName)
#xapp_port= xAppAPI.get_xApp_port()


def messagefunction(self, message, jpay, flg, sbuf, count):
    global counted, RFID, e2node_list, bo
    # Routing Ack
    if message == xAppAPI.RT_RESPONSE:
        val = xAppAPI.sub_request(RFID, int(e2node_list[0]["SocketFD"]))
        self.rmr_send(val, xAppAPI.SUB_REQUEST)
        print("Send Subscription Request:\n", val)
    # Subscription Response
    if message == xAppAPI.SUB_RESPONSE:
        print("\nRecieved Subscription Response:\n", jpay)
        logging.info("Recieved Subscription Response")
        # print("Subscription Response Payload:\n", jpay)
        # SocketFD = jpay['SocketFD']
        
        # DelMessage = xAppAPI.sub_del_request(RFID)
        # print("\nSend Subscription Delet Request:\n", DelMessage)
        # self.rmr_send(DelMessage, xAppAPI.SUB_DELETE_REQUEST)

        self.rmr_send(build_control(RFID, [1, 1, 16, 26]), 120404200)
        
        # val = xAppAPI.reset_request()
        # self.rmr_send(val, 120084400)
    # Subscription Failure
    if message == xAppAPI.SUB_FAILURE:
        SocketFD = xAppAPI.get_SocketFD
        RFID = 0
        val = xAppAPI.report_query()
        self.rmr_send(val, xAppAPI.REPORT_QUERY_REQUEST)
    # Subscription Del Response
    if message == xAppAPI.SUB_DELETE_RESPONSE:
        print("\nRecieved Subscription Delete Response:\n", jpay)
        # print("Subscription Delete Response Payload:\n", jpay)
        # val = xAppAPI.report_query()
        # self.rmr_send(val, xAppAPI.REPORT_QUERY_REQUEST)
    # Control Response
    if message == xAppAPI.CTL_RESPONSE:
        print("\nRecieved Control Response:\n", jpay)
        # print("Control Response Payload:\n", jpay)
        
        DelMessage = xAppAPI.sub_del_request(RFID)
        print("sub del req:\n", DelMessage)
        self.rmr_send(DelMessage, xAppAPI.SUB_DELETE_REQUEST)
    # Indiction Report
    if message == xAppAPI.INDI_REPORT:
        print("\nRecieved Indication Report:\n", jpay)  
        savecsv(jpay);

        # print("Indication Report Payload:\n", jpay)
        if 'Serving_Cell_PCI' in jpay:
            # if jpay['Serving_Cell_PCI'] != 0 :#and  jpay[''] != 0 and jpay[''] != 0 :
            # if jpay['Serving_Cell_PCI'] != 0 and  jpay['Neighboring_Cell_PCI'] != 0 and jpay['UEID'] != 0 :
            print("\ncount= ", counted)
            if counted == 100:
                # UEID = r.get("{UEID},get")
                # print("\nUE ID= ", UEID)
                # UEID = int(UEID) ** 2
                # print("\nUE ID**2= ", UEID)
                # controlmessage = build_control()
                # print("\nControlmessage: ", controlmessage)

                # #self.rmr_send(controlmessage, 6104200)
                # self.rmr_send(controlmessage, 120404200)
                counted = 0
            counted += 1
    # Indiction insert
    if message == xAppAPI.INDI_INSERT:
        print("\nRecieved Indication Insert:\n", jpay)
        # print("Indication Insert Payload:", jpay)

        DelMessage = xAppAPI.sub_del_request()
        self.rmr_send(DelMessage, xAppAPI.SUB_DELETE_REQUEST)
        #control_request(self, summary, sbuf)
    if message == xAppAPI.REPORT_QUERY_RESPONSE:
        print("\nRecieved Report Query Response:\n", jpay)
        # print("Report Query Payload:", len(str(jpay)))
    self.rmr_free(sbuf)


def savecsv(data: dict) -> dict:
    global bo

    # print("type: ", type(data))
    # print("keys: ", data.keys())
    # print("data: ", data)

    file = "xian.csv"

    # header = ["UEID", "Counter-Long", "BLER-LongTerm", "Counter-Short", "BLER-ShortTerm", "SINR", "Latency", "Throughput", "Serving_Cell_PCI", "Neighboring_Cell_PCI"]
    
    with open("/xappInfo/"+file, "a", newline="") as f:
        # w = csv.DictWriter(f, fieldnames=header)
        w = csv.DictWriter(f, data.keys())
        if bo:
            w.writeheader()
            bo = False
        w.writerow(data)
        f.close


def change_to_hex(temp):
    # print("len = ", len(temp))
    if len(temp)%4 == 0:
        for i in range(len(temp)):
            if i % 4 == 0:
                if temp[i] != 1:
                    print("!= 1")
                    os._exit(0)
                else:
                    temp[i] = str(temp[i])
            elif i % 4 == 1:
                temp[i] = hex(temp[i]).split("x")[1]
            elif i % 4 == 2:
                temp[i] = hex(temp[i]).split("x")[1].zfill(8)
            elif i % 4 == 3:
                temp[i] = hex(temp[i]).split("x")[1].zfill(8)
    else:
        print("error formaat")
        os._exit(0)
    return temp


def build_control(RFID, value_list):
    # print("[1, UE ID, Serving Cell-PCI, Target Cell-PCI]: ", value_list)
    text = change_to_hex(value_list)
    #print("\ntext= ", text);
    str1 = ','.join(str(e) for e in text)
    # print("control message= ", str1)
    controlmessage = json.dumps({
        "RIC Request ID": {"RIC Requestor ID": xAppAPI.get_xAppPort(), "RIC Instance ID": 1},
        "RAN Function ID": RFID,
        "RAN Function Revision": 1,
        "RIC Control Header": 0x00,
        "RIC Control Message": str1,
        "RIC Control Ack Request": 1,
        "Procedure Code": 4,
        "SocketFD": xAppAPI.get_SocketFD()
    }).encode()
    print("\nSend Control Request: \n", controlmessage)
    return controlmessage


def check_RFID(RFID):
    global e2node_list
    e2node_list= xAppAPI.get_matched_E2Node(RFID)
    matched = False;
    if len(e2node_list) != 0:
        if len(e2node_list) == 1:
            print("match: one")
            matched = True;
        else:
            print("match: more than one")
    else:
        print("no matched E2 Node")
    return matched;    
    

# send to other component
def entry(self):
    global xapp_port, RFID, e2node_list
    count = 0
    flg = True

    if check_RFID(RFID) != True:
        RFID = 0;
        e2node_list = [];
        os._exit(0) 

    Ask = xAppAPI.do_xApp_initial(xapp_port)
    # xAppAPI.createTimer()
    self.rmr_send(Ask, xAppAPI.RT_REQUEST)

    while True:
        # rmr receive
        for (summary, sbuf) in self.rmr_get_messages():
            message = xAppAPI.get_mtype(summary)
            jpay = xAppAPI.get_payload(summary)

            t = threading.Thread(target=messagefunction, args=(
                self, message, jpay, flg, sbuf, count))
            t.start()


xapp = Xapp(entrypoint=entry, rmr_port=xapp_port)
# xapp = RMRXapp(rmr_port= xapp_port, default_handler=entry,  post_init=entry, use_fake_sdl=False) 
xapp.run()
