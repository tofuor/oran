# xApp API Version 1.0

import os,sys,logging,random,socket,threading,json,time
#from ricxappframe.xapp_frame import Xapp
from ricsdl.syncstorage import SyncStorage
from ricsdl.exceptions import RejectedByBackend, NotConnected, BackendError

xapp_port = 1234
RIC_ID = xapp_port
mtype = int("901"+str(xapp_port))
xApp_list_N = None
xApp_list_K = None
SocketFD = 0


class xApp:
    #Define Message Type
    RT_REQUEST = 9004600
    RT_RESPONSE = int("901"+str(xapp_port))
    SUB_REQUEST  = 4104400
    SUB_RESPONSE = int("411"+str(xapp_port))
    SUB_DELETE_REQUEST  = 5104400
    SUB_DELETE_RESPONSE  = int("511"+str(xapp_port))
    CTL_REQUEST = 6104200
    CTL_RESPONSE = int("611"+str(xapp_port))
    INDI_REPORT = int("700"+str(xapp_port))
    INDI_INSERT = int("710"+str(xapp_port))
    REPORT_INFO_REQUEST = 8704200
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

    def __init__(self,fileNames):
        global xapp_port,check_in,RIC_ID,ContainerIp

        self.fileName = fileNames+".txt"
        os.environ['DBAAS_SERVICE_PORT'] = '6379'
        os.environ['DBAAS_SERVICE_HOST'] = '127.0.0.1'
        os.environ['RMR_SEED_RT'] = 'test_route.rt'
        os.environ['RMR_LOG_VLEVEL'] = '0'
        os.environ['RMR_RTG_SVC']='-1'
        ContainerIp = os.getenv('ContainerIP')

        try:
            pass
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
            RIC_ID = xapp_port
            f.close() 
            print("Use exist port!!!")
            print("check_in:"+check_in)
        else:
            print("Create new xApp for initialize\n")
            print("*******************************\n")
            f = open('/xappInfo/'+self.fileName,'w+')
            
            xapp_port = self.check_port(8000)#random.randint(8000,65535))
            RIC_ID = xapp_port
            self.RT_RESPONSE = int("901"+str(xapp_port))
            self.SUB_RESPONSE = int("411"+str(xapp_port))
            self.SUB_DELETE_RESPONSE  = int("511"+str(xapp_port))
            self.CTL_RESPONSE = int("611"+str(xapp_port))
            self.INDI_REPORT = int("700"+str(xapp_port))
            self.INDI_INSERT = int("710"+str(xapp_port))

            f.write(str(xapp_port)+"\n")
            f.write("1\n")
            check_in = 1
            f.seek(0)
            f.close()

    def do_xApp_initial(self,xapp_port):
        global ContainerIp
        
        print("Asking for the RIC ID!!")
        logging.info("Asking for the RIC ID!\n\n")
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
            logging.info("Got the port number"+str(jpay['Port'])+"\n")

            #Check port is same or not
            if xapp_port != jpay['Port']:
                print("Need to Reset port number of xapp!!")
                logging.info("Need to reset port number of xapp!!")
                xapp_port = jpay['Port']
                f = open('/xappInfo/'+self.fileName,'w+')
                f.write(str(xapp_port)+"\n")
                f.write("0\n")
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
                line[1]="0"

                f = open('/xappInfo/'+self.fileName,'w+')
                f.writelines(line)
                f.close()

                print("Ready for send 'Subscription Request' after 60 seconds\n")
                self.countdown(60)


        if mtype == int("411"+str(xapp_port)):
            SocketFD = jpay['SocketFD']


        if mtype == int("414"+str(xapp_port)):
            RIC_Action_ID = jpay["RIC Action ID"]
            Cause = jpay["Cause"]
            print("RIC Action ID",RIC_Action_ID,"\n")
            print("Cause",Cause,"\n")

        if mtype == int("514"+str(xapp_port)):
            print("Recieve the 514 Subscription Delete Failure\n")
            print("514 Payload:",jpay,"\n")
            Cause = jpay["Cause"]
            print("Cause",Cause,"\n")

        if mtype == int("614"+str(xapp_port)):
            print("Recieve the 614 Control Failure\n")
            print("614 Payload:",jpay,"\n")
            Cause = jpay["Cause"]
            print("Cause",Cause,"\n")

        #Indiction Error
        if mtype == int("740"+str(xapp_port)):
            print("Recieve 740 the Error Indication\n")
            print("740 Payload:",jpay,"\n")

        return jpay

    def get_xApp_list(self):
        global xApp_list_N, xApp_list_K
        return xApp_list_N, xApp_list_K

    def sub_del_request(self):
        print("Delete Subscrition Start!!\n")
        print("Ready for Subscription Delete Request!!\n")
        DelMessage = json.dumps({
            "RIC Request ID":{"RIC Requestor ID":RIC_ID,"RIC Instance ID":1},
            "RAN Function ID":1,
            "Procedure Code":9,
            "SocketFD":SocketFD
            }).encode()

        return DelMessage

    def report_info_request(self, TIME_RANGE):
        print("Ready for Report Information Request!!\n")
        ReportMessage = json.dumps({
            "RIC Requestor ID":RIC_ID,
            "Time Range":TIME_RANGE,
            }).encode()

        return ReportMessage

    def control_request_message(self,control_request_message):
        controlmessageJson=json.loads(control_request_message)
        controlmessageJson={"RIC Requestor ID":controlmessageJson['RIC Request ID']['RIC Requestor ID'], "RIC Control Message": controlmessageJson['RIC Control Message']}
        return controlmessageJson

    def control_request(self, DL_MCS=0, UL_MCS=0,
    DL_maxHARQ=0, UL_maxHARQ=0, repetition=0, maxUE=0, Grandfree=0,G_Period=0,
    time_offset=0, time_alloc=0, feq_alloc=0, G_repetition=0,G_maxHARQ=0, G_MCS=0 ):
        global RIC_ID
        if DL_MCS == DL_maxHARQ == UL_MCS == UL_maxHARQ == repetition == maxUE == Grandfree == G_Period == time_offset == time_alloc == feq_alloc == G_repetition == G_maxHARQ == G_MCS == 0:
            print("Hello World!!")
            controlmessage = json.dumps({
            'DL MCS':DL_MCS,
            'UL MCS':UL_MCS,
            'max DL HARQ':DL_maxHARQ,
            'max UL HARQ':UL_maxHARQ,
            'Repetition':repetition,
            'max Num UE':maxUE,
            'Grant-free':{'Grant-free Ind':Grandfree,
                            'Periodicity':G_Period,
                            'timeDomainOffset':time_offset,
                            'timeDomainAllocation':time_alloc,
                            'frequencyDomainAllocation':feq_alloc,
                            'Repetition':G_repetition,
                            'maxHARQ':G_maxHARQ,
                            'MCS':G_MCS
                        }
            }).encode()
            print("Cotrol Example:",controlmessage,"\n")
        elif ((DL_MCS in [i for i in range(17,29)])== False and DL_MCS != 0) or ((UL_MCS in [i for i in range(17,29)])== False and UL_MCS != 0) or ((DL_maxHARQ in [i for i in range(1,17)])==False and DL_maxHARQ != 0) or ((UL_maxHARQ in [i for i in range(1,17)])== False and UL_maxHARQ != 0) or ((repetition in [i for i in range(1,9)])==False and repetition!=0) or ((maxUE in [i for i in range(1,65)])==False and maxUE!=0) or (Grandfree in [i for i in range(0,2)])==False: 
            print("Error input value!!!\n")
        else:
            print("\nReady for Conrol Request!!!")
            controlmessage = json.dumps({
                "RIC Request ID":{"RIC Requestor ID":RIC_ID,"RIC Instance ID":1},
                "RAN Function ID":1,
                "RAN Function Revision":1,
                "RIC Control Header":0x00,
                "RIC Control Message":{
                                        'MCS_DL':DL_MCS,
                                        'MCS_UL':DL_MCS,
                                        'max_DL_HARQ':DL_maxHARQ,
                                        'max_UL_HARQ':UL_maxHARQ,
                                        'Repetition':repetition,
                                        'Grantfree_Ind':0,
                                    },
                "RIC Control Ack Request":1,
                "Procedure Code":4,
                "SocketFD":SocketFD
            }).encode()

            return controlmessage

    #initial sockfd=0, it will be update after ack.
    def sub_request(self):
        global RIC_ID
        print("Ready for Subscription Request!!!\n")
        val = json.dumps({
            "RIC Request ID":{"RIC Requestor ID":RIC_ID,"RIC Instance ID":1},
            "RAN Function ID":1,
            "RAN Function Revision":1,
            "RIC Subscription Details":{"RIC Event Trigger Definition":0x00,
                                        "Sequence of Actions":{"RIC Action ID":1,"RIC Action Type":1}
                                        },
            "Procedure Code":8,
            "SocketFD":SocketFD
        }).encode()

        return val

    def report_query(self,SocketFD):
        global RIC_ID
        print("Ready for Report Query Request!!!\n")
        val = json.dumps({
            "RIC Requestor ID":RIC_ID,
            "RAN Function ID":1,
            "SocketFD":SocketFD
        }).encode()
        return val


    #check port can use or not
    def check_port(self,port, ip='127.0.0.1'):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
            s.shutdown(2)
            print('sorry, %d is used' % port)
            logging.info('sorry, %d is used' % port)
            self.check_port(random.randint(8000,65535))
        except:
            return port


    #write in local routing table
    def write_routing_table(self,NameSpace,Key):
        mysdl = self._try_func_return(SyncStorage)
        is_active = mysdl.is_active()
        assert is_active is True

        
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
        f.close()
