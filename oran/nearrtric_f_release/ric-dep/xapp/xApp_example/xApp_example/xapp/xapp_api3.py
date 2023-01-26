# xApp API Version 1.0

import os,sys,logging,random,socket,threading,json,time
#from ricxappframe.xapp_frame import Xapp
from ricsdl.syncstorage import SyncStorage
from ricsdl.exceptions import RejectedByBackend, NotConnected, BackendError
import redis

xapp_port = 1234
RIC_ID = xapp_port
mtype = int("901"+str(xapp_port))
xApp_list_N = None
xApp_list_K = None
SocketFD = 0

redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

class xApp:
    #Define Message Type
    RT_REQUEST = 9004600
    RT_RESPONSE = int("901"+str(xapp_port))
    SUB_REQUEST  = 120104400
    SUB_RESPONSE = int("12011"+str(xapp_port))
    SUB_FAILURE = int("12012"+str(xapp_port))
    SUB_DELETE_REQUEST  = 120204400
    SUB_DELETE_RESPONSE  = int("12021"+str(xapp_port))
    SUB_DELETE_FAILURE = int("12022"+str(xapp_port))
    CTL_REQUEST = 120404200
    CTL_RESPONSE = int("12040"+str(xapp_port))
    INDI_REPORT = int("12050"+str(xapp_port))
    INDI_INSERT = int("710"+str(xapp_port))
    Handover = int("520"+str(xapp_port))
    REPORT_QUERY_REQUEST = 8704200
    REPORT_QUERY_RESPONSE = int("871"+str(xapp_port))
    initial_check = 0

    fileName = "test"

    #Database function
    def _try_func_return(self,func):
        try:
            return func()
        except RejectedByBackend as exp:
            print(f'SDL function {func.__name__} failed: {str(exp)}')
            raise
        except (NotConnected, BackendError) as exp:
            print(f'SDL function {func.__name__} failed for a temporal error: {str(exp)}')


    def createTimer(self):
        t = threading.Timer(60, self.initial_TimeOut())
        t.start()


    def initial_TimeOut(self):
        if self.initial_check == 0:
            print("xApp Initialization Time Out!! Please enter RIGHT xApp ID!!\n")


    def __init__(self,fileNames, xapp_port_):
        global xapp_port,check_in,RIC_ID,SocketFD, ContainerIp

        self.fileName = fileNames+".txt"
        os.environ['DBAAS_SERVICE_PORT'] = '6379'
        os.environ['DBAAS_SERVICE_HOST'] = '127.0.0.1'
        #os.environ['DBAAS_SERVICE_HOST'] = '192.168.43.9'
        os.environ['RMR_SEED_RT'] = 'test_route.rt'
        os.environ['RMR_LOG_VLEVEL'] = '0'
        os.environ['RMR_RTG_SVC']='-1'
        ContainerIp = os.getenv('ContainerIP')

        try:
            pass
            #os.remove("port.txt")
        except:
            print("No port file --> ok")

        print("*******************************\n")
        print("xApp is ready for works!!!\n")
        print("*******************************\n")
        logging.info("xApp is ready for works!!!\n")

        #write data in port file
        if os.path.isfile('./xappInfo/'+self.fileName):
            f = open('/xappInfo/'+self.fileName,'r+')
            line = f.readlines()
            xapp_port = line[0]
            xapp_port = int(xapp_port)
            check_in = line[1]
            check_in = int(check_in)
            SocketFD = line[2]
            SocketFD = int(SocketFD)
            RIC_ID = xapp_port
            f.close() 
            print("Use exist port!!!")
            print("xapp_port:%d" % xapp_port)
            print("check_in:",check_in)
            self.RT_RESPONSE = int("901"+str(xapp_port))
            self.SUB_RESPONSE = int("12011"+str(xapp_port))
            self.SUB_FAILURE = int("12012"+str(xapp_port))
            self.SUB_DELETE_RESPONSE  = int("12021"+str(xapp_port))
            self.SUB_DELETE_FAILURE = int("12022"+str(xapp_port))
            self.CTL_RESPONSE = int("12041"+str(xapp_port))
            self.INDI_REPORT = int("12050"+str(xapp_port))
            self.INDI_INSERT = int("710"+str(xapp_port))
            self.Handover = int("520"+str(xapp_port))
            self.REPORT_QUERY_RESPONSE = int("871"+str(xapp_port))
        else:
            print("Create new port for initialise\n")
            f = open('/xappInfo/'+self.fileName,'w+')
            xapp_port = xapp_port_
#            xapp_port = self.check_port(random.randint(8000,65535))
            RIC_ID = xapp_port_
            self.RT_RESPONSE = int("901"+str(xapp_port))
            self.SUB_RESPONSE = int("12011"+str(xapp_port))
            self.SUB_FAILURE = int("12012"+str(xapp_port))
            self.SUB_DELETE_RESPONSE  = int("12021"+str(xapp_port))
            self.SUB_DELETE_FAILURE = int("12022"+str(xapp_port))
            self.CTL_RESPONSE = int("12041"+str(xapp_port))
            self.INDI_REPORT = int("12050"+str(xapp_port))
            self.INDI_INSERT = int("710"+str(xapp_port))
            self.Handover = int("520"+str(xapp_port))
            self.REPORT_QUERY_RESPONSE = int("871"+str(xapp_port))

            print("xapp_port:%d" % xapp_port)
            f.write(str(xapp_port_)+"\n")
            f.write("1\n")
            f.write("0\n")
            
            check_in = 1
            f.seek(0)
            f.close()


    def get_SocketFD(self):
        global SocketFD
        return SocketFD


    def get_xAppPort(self):
        global xapp_port
        return xapp_port


    def do_xApp_initial(self,xapp_port):
        global ContainerIp

        print("Asking for the RIC ID!!")
        logging.info("Asking for the RIC ID!\n")
        message = json.dumps({
            "Ip":ContainerIp,
            "Port":xapp_port
        }).encode()
        return message


    def countdown(self,t):
        print("Waiting Time:")
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        print('Done!!\n')


    #return xApp port
    def get_xApp_port(self):
        global xapp_port,check_in
        return xapp_port


    #return message type
    def get_mtype(self,summary):
        global mtype
        mtype= summary['message type']
        return mtype


    #return paylaod
    def get_payload(self,summary):
        global mtype,xapp_port,xApp_list_N,xApp_list_K,SocketFD
        try:
            jpay = json.loads(summary['payload'])
        except:
            print("Use UTF-8 Decode\n")
            jpay = summary['payload']
            jpay = jpay.decode('utf-8')
        if mtype== int("901"+str(xapp_port)):
            logging.info("Received the 901 Routing Ack!!")
            print("Received the Routing Ack!!\n")
            #print("901 Payload:",jpay,"\n")
            logging.info("Got the port number"+str(jpay['Port'])+"\n")
            self.initial_check = 1
            #Check port is same or not
            if xapp_port != jpay['Port']:
                print("Need to Reset port number of xapp!!")
                logging.info("Need to reset port number of xapp!!")
                print("xapp_port:%d" % xapp_port)
                xapp_port = jpay['Port']
                f = open('/xappInfo/'+self.fileName,'w+')
                f.write(str(xapp_port)+"\n")
                f.write("0\n")
                f.write(str(SocketFD)+"\n")
                f.seek(0)
                f.close()
            else:
                print("Can use origin port!!\n")
                print("Completed xApp initial!!!\n")

                NS = jpay['Routing Table']['Namespace']
                key1 = jpay['Routing Table']['Key']
                xApp_list_N = jpay['xApp list']['Namespace']
                xApp_list_K  = jpay['xApp list']['Key']

                f = open('/xappInfo/'+self.fileName,'r')
                line= f.readlines()
                line[1]="0\n"

                f = open('/xappInfo/'+self.fileName,'w+')
                f.writelines(line)
                f.seek(0)
                #txt=f.read()
                #print(txt)
                f.close()
                #self.write_routing_table(NS,key1)

                print("Ready for send 'Subscription Request' after 60 seconds\n")
                self.countdown(60)

                #xAppAPI.sub_request()
        if mtype == int("12011"+str(xapp_port)):
            SocketFD = jpay['SocketFD']
            f = open('/xappInfo/'+self.fileName,'r')
            line= f.readlines()
            line[2]=str(SocketFD)
            f = open('/xappInfo/'+self.fileName,'w+')
            f.writelines(line)
            f.seek(0)
            f.close()
        if mtype == int("20"+str(xapp_port)):
            logging.info("Received the 1000 Routing Restart!!")
            #print("Received the 1000 Routing Restart!!\n")
            #print("1000 Payload:",jpay,"\n")
            NS = jpay['Routing Table']['Namespace']
            key1 = jpay['Routing Table']['Key']
            #self.write_routing_table(NS,key1)
        if mtype == int("12012"+str(xapp_port)):
            print("Recieve the Subscription Failure\n")
            #RIC_Action_ID = jpay["Actions Not Admitted List"]["RIC Action ID"]
            #Cause = jpay["Actions Not Admitted List"]["Cause"]
            SocketFD = jpay['Cause']['SocketFD']
            f = open('/xappInfo/'+self.fileName,'r')
            line= f.readlines()
            line[2]=str(SocketFD)
            f = open('/xappInfo/'+self.fileName,'w+')
            f.writelines(line)
            f.seek(0)
            f.close()

            RIC_Action_ID = jpay["RIC Action ID"]
            Cause = jpay["Cause"]
            print("RIC Action ID",RIC_Action_ID,"\n")
            print("Cause",Cause,"\n")
            try:
                SocketFD = Cause['SocketFD']
                print("Cause['SocketFD']:",Cause['SocketFD'])
                print("\nSocketFD:",SocketFD)
                f = open('/xappInfo/'+self.fileName,'r')
                line= f.readlines()
                line[2]=str(SocketFD)
                f = open('/xappInfo/'+self.fileName,'w+')
                f.writelines(line)
                f.seek(0)
                f.close()
            except:
                pass
        if mtype == int("12022"+str(xapp_port)):
            print("Recieve the 514 Subscription Delete Failure\n")
            print("514 Payload:",jpay,"\n")
            Cause = jpay["Cause"]
            print("Cause",Cause,"\n")
        if mtype == int("12042"+str(xapp_port)):
            print("Recieve the 614 Control Failure\n")
            print("614 Payload:",jpay,"\n")
            Cause = jpay["Cause"]
            print("Cause",Cause,"\n")
        #Indiction Error
        if mtype == int("10030"+str(xapp_port)):
            print("Recieve 740 the Error Indication\n")
            print("740 Payload:",jpay,"\n")
        return jpay


    def get_xApp_list(self):
        global xApp_list_N, xApp_list_K
        return xApp_list_N, xApp_list_K


    def sub_del_request(self, RFID):
        DelMessage = json.dumps({
            "RIC Request ID":{"RIC Requestor ID":RIC_ID,"RIC Instance ID":1},
            "RAN Function ID":RFID,
            "Procedure Code":9,
            "SocketFD":SocketFD
            }).encode()
        return DelMessage


    def report_query(self):
        print("Ready for Report Information Request!!\n")
        val = json.dumps({
            "RIC Requestor ID":RIC_ID,
            "RAN Function ID":1,
            "SocketFD":SocketFD
        }).encode()

        return val


    def control_request(self,xApp_ID, SocketFD, DL_MCS=0, UL_MCS=0,
                 DL_maxHARQ=0, UL_maxHARQ=0, repetition=0, max_Num_UE=0,Grandfree=0 ):

        if DL_MCS == DL_maxHARQ == UL_MCS == UL_maxHARQ == repetition == max_Num_UE == Grandfree == 0:
            
            print("Hello World!!")
            controlmessage = json.dumps({
            'DL_MCS':DL_MCS,
            'UL_MCS':UL_MCS,
            'max DL HARQ':DL_maxHARQ,
            'max UL HARQ':UL_maxHARQ,
            'Repetition':float(repetition),
            'max Num UE':max_Num_UE,
            'Grant-free Ind':Grandfree
            }).encode()
            print("Control Example:",controlmessage,"\n")
        elif ((DL_MCS in [i for i in range(17,29)])== False and DL_MCS != 0) and ((UL_MCS in [i for i in range(17,29)])== False and UL_MCS != 0) and ((DL_maxHARQ in [i for i in range(1,17)])==False and DL_maxHARQ != 0) and ((UL_maxHARQ in [i for i in range(1,17)])== False and UL_maxHARQ != 0) and ((repetition in [i for i in range(1,9)])==False and repetition!=0) and ((max_Num_UE in [i for i in range(1,65)])== False and max_Num_UE != 0) and (Grandfree in [i for i in range(0,2)])==False: 
            print("Error input value!!!\n")
            print("Please rewrite input value：\n")
            
        else:
            print("Ready for Conrol Request!!!\n")
            controlmessage = json.dumps({
                "RIC Request ID":{"RIC Requestor ID":xApp_ID,"RIC Instance ID":1},
                "RAN Function ID":1,
                "RAN Function Revision":1,
                "RIC Control Header":0x00,
                "RIC Control Message":{'DL_MCS':DL_MCS,
                                        'UL_MCS':UL_MCS,
                                        'max DL HARQ':DL_maxHARQ,
                                        'max UL HARQ':UL_maxHARQ,
                                        'Repetition':float(repetition),
                                        'max Num UE':max_Num_UE,
                                        'Grant-free Ind':Grandfree
                                    },
                "RIC Control Ack Request":1,
                "Procedure Code":4,
                "SocketFD":SocketFD
            }).encode()

            return controlmessage


    def sub_request(self, RAN_Function_ID, socketfd):
        global RIC_ID
        f = open('/xappInfo/'+self.fileName,'r')
        line= f.readlines()
        print(line)
        if line[2] == "0\n":
            SocketFD = socketfd
            print("Ready for Subscription Request!!!\n")
            val = json.dumps({
                "RIC Request ID":{"RIC Requestor ID":RIC_ID,"RIC Instance ID":1},
                "RAN Function ID":RAN_Function_ID,
                "RAN Function Revision":1,
                "RIC Subscription Details":{"RIC Event Trigger Definition":0x00,
                                            "Sequence of Actions":{"RIC Action ID":1,"RIC Action Type":1}
                                            },
                "Procedure Code":8,
                "SocketFD":socketfd
            }).encode()
            f.seek(0)
            f.close()
            return val
        else:
            print("You have been Subscribe before!!\n")
            return None


    def reset_request(self):
        global SocketFD
        
        resetmessage = json.dumps({
            "Procedure Code":3,
            "Type of Message": 0,
            "SocketFD": SocketFD
        }).encode()
        return resetmessage


    def report_query(self):
        global RIC_ID, SocketFD
        print("Ready for Report Query Request!!!\n")
        val = json.dumps({
            "RIC Requestor ID":RIC_ID,
            "RAN Function ID":1,
            "SocketFD":SocketFD
        }).encode()
        print("report_query SocketFD:",SocketFD)
        return val


    #check port can use or not
    #def check_port(self,port, ip='127.0.0.1'):
    def check_port(self,port, ip= "192.168.43.9"):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
            s.shutdown(2)
            print('sorry, %d is used' % port)
            logging.info('sorry, %d is used' % port)
            self.check_port(random.randint(8000,65535))
        except:
            print('Congratulations %d can use!!' % port)
            logging.info('Congratulations %d can use!!' % port)
            return port


    #write in local routing table
    def write_routing_table(self,NameSpace,Key):
        mysdl = self._try_func_return(SyncStorage)
        is_active = mysdl.is_active()
        assert is_active is True

        print("Write the xApp information into the routing table!!!\n")
        
        f =open("test_route.rt",'w+')
        f.write('newrt|start\n')
        data = eval(self._try_func_return(lambda: mysdl.get(NameSpace, {str(Key)}))[Key].decode())
        for  key in data.keys():
            ip = data[key]['IP']
            port = str(data[key]['port'])
            messagetype = str(data[key]['massage_type'])+port
            f.write('rte|'+messagetype+'|'+ip+':'+port+"\n")
        f.write('newrt|end\n')
        f.seek(0)
        #txt=f.read()
        #print(txt)
        f.close()
        print("Write in routing table succussful!!!")
    

    def get_matched_E2Node(self, RFID):
        e2node = [];
        for index in range(0, redis.llen("E2_Setup_List")):
            e2_node= redis.lindex("E2_Setup_List", index);
            #print(" ["+ str(index)+"] "+"E2_Setup_List = ", e2_node)
            info=  json.loads(redis.get(e2_node));
            #print("[redis] E2 Node Info", info)
            if(RFID in info["RAN Function ID"]):
                e2node.append(info);
        return e2node;