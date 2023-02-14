# ==================================================================================
#
#       Copyright (c) 2020 Samsung Electronics Co., Ltd. All Rights Reserved.
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
#
# ==================================================================================

from os import getenv
from ricxappframe.xapp_frame import RMRXapp, rmr
from ricxappframe.xapp_sdl import SDLWrapper
# from keras.models import load_model
# import numpy as np
import json
import time

from .utils.constants import Constants
from .manager import *

from .handler import *
from mdclogpy import Logger

A1NS = "A1m_ns"
UE_KEY = "ue.position.0000000000000"

UE_NS = "TS-UE-metrics"
CELL_NS = "TS-cell-metrics"

mdc_logger = Logger(name=__name__)
mdc_logger.set_level(10)
SDL = SDLWrapper(use_fake_sdl=False)

class HWXapp:

    def __init__(self):
        fake_sdl = getenv("USE_FAKE_SDL", False)
        self._rmr_xapp = RMRXapp(self._default_handler,
                                 config_handler=self._handle_config_change,
                                 rmr_port=4560,
                                 post_init=self._post_init,
                                 use_fake_sdl=bool(fake_sdl))

    def read_csv(self):
        mdc_logger.info("reading uav_traj_1.csv ..............")
        f = open("/tmp/uav_traj_1.csv", "r")
        positions = f.read().split('\n')
        positions.pop()
        f.close()
        mdc_logger.info("finish reading")
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

            data = json.dumps(posData).encode('utf-8')
            SDL.set(A1NS, UE_KEY, data, usemsgpack=False)
            #print(json.dumps(posData))
            # response = requests.put("http://192.168.122.65:32080/a1mediator/a1-p/update_ue_position", data = json.dumps(posData), headers = jsonType)
            # if response.status_code != 201:
            #     print("error! response code = " + str(response.status_code))
            # break
            time.sleep(0.02)

    # def decode_and_store(self):
        # for lineData in positions:
        #     rawData = lineData.split(',')
        #     posData = {}
        #     posData['id'] = '1'
        #     timestamp = int(float(rawData[0]))
        #     posData['timestamp'] = timestamp
        #     posData['tags'] = []
        #     ueData = {}
        #     ueData['imsi'] = '0000000000000'
        #     ueData['posX'] = float(rawData[1])
        #     ueData['posY'] = float(rawData[2])
        #     ueData['posZ'] = float(rawData[3])
        #     ueData['timestamp'] = timestamp
        #     posData['tags'].append(ueData)

        #     data = json.dumps(posData).encode('utf-8')
        #     SDL.set(A1NS, UE_KEY, data, usemsgpack=False)
        #     #print(json.dumps(posData))
        #     # response = requests.put("http://192.168.122.65:32080/a1mediator/a1-p/update_ue_position", data = json.dumps(posData), headers = jsonType)
        #     # if response.status_code != 201:
        #     #     print("error! response code = " + str(response.status_code))
        #     # break
        #     time.sleep(0.02)

    def _post_init(self, rmr_xapp):
        """
        Function that runs when xapp initialization is complete
        """
        mdc_logger.info("HWXapp.post_init :: post_init called")
        self.read_csv()
        
        mdc_logger.info("show values")

        values = SDL.find_and_get(A1NS, UE_KEY, usemsgpack=False).values()
        mdc_logger.info("show CELL_NS values")
        cell_data_list = list(SDL.find_and_get(CELL_NS, "", usemsgpack=False).values())
        mdc_logger.info(list(json.loads(v.decode()) for v in cell_data_list))
        if values != None:
            mdc_logger.info(list(json.loads(v.decode()) for v in values))
        else:
            mdc_logger.info("uav path is empty.")
        # self.sdl_alarm_mgr = SdlAlarmManager()
        # sdl_mgr = SdlManager(rmr_xapp)
        # sdl_mgr.sdlGetGnbList()
        a1_mgr = A1PolicyManager(rmr_xapp)
        a1_mgr.startup()
        # sub_mgr = SubscriptionManager(rmr_xapp)
        # enb_list = sub_mgr.get_enb_list()
        # for enb in enb_list:
        #     sub_mgr.send_subscription_request(enb)
        # gnb_list = sub_mgr.get_gnb_list()
        # for gnb in gnb_list:
        #     sub_mgr.send_subscription_request(gnb)
        # metric_mgr = MetricManager(rmr_xapp)
        # metric_mgr.send_metric()

        while True:
            cell_data = []
            cell_data_list = list(SDL.find_and_get(CELL_NS, "", usemsgpack=False).values())
            if cell_data_list != None:
                for cell_data_bytes in cell_data_list:
                    cell_data.append(json.loads(cell_data_bytes.decode()))

            print(cell_data)

            ue_data = []
            ue_data_list = list(SDL.find_and_get(UE_NS, "", usemsgpack=False).values())
            if ue_data_list != None:
                for ue_data_bytes in ue_data_list:
                    ue_data.append(json.loads(ue_data_bytes.decode()))

            print(ue_data)
            time.sleep(1)

    def _handle_config_change(self, rmr_xapp, config):
        """
        Function that runs at start and on every configuration file change.
        """
        mdc_logger.info("HWXapp.handle_config_change:: config: {}".format(config))
        rmr_xapp.config = config  # No mutex required due to GIL

    def _default_handler(self, rmr_xapp, summary, sbuf):
        """
        Function that processes messages for which no handler is defined
        """
        mdc_logger.info("HWXapp.default_handler called for msg type = " +
                                   str(summary[rmr.RMR_MS_MSG_TYPE]))
        rmr_xapp.rmr_free(sbuf)
        # print SDL ue position data
        values = SDL.find_and_get(A1NS, UE_KEY, usemsgpack=False).values()
        if values != None:
            mdc_logger.info(list(json.loads(v.decode()) for v in values))
        else:
            mdc_logger.info("uav path is empty.")

    def createHandlers(self):
        """
        Function that creates all the handlers for RMR Messages
        """
        HealthCheckHandler(self._rmr_xapp, Constants.RIC_HEALTH_CHECK_REQ)
        A1PolicyHandler(self._rmr_xapp, Constants.A1_POLICY_REQ)
        SubscriptionHandler(self._rmr_xapp,Constants.SUBSCRIPTION_REQ)
    
    # def model_start(self):
    #     model = load_model('/tmp/model/LSTM_test.h5')

    #     ##### predict
    #     # mdc_logger.info("values type = " + str(type(values))) 
    #     # mdc_logger.info("values = " + str(values))
    #     ten_values = list(json.loads(v.decode()) for v in values)
    #     # mdc_logger.info("ten_values = " + str(ten_values))
    #     data = []
    #     delta_xyz = []
    #     for i in range(0,10):
    #         timestamp = ten_values[i]['meas_timestamp_pos']
    #         if i == 0:
    #             speed_x = 0
    #             speed_y = 0
    #             speed_z = 0
    #         else:
    #             speed_x = ten_values[i]['pos_x'] - ten_values[i-1]['pos_x']
    #             speed_y = ten_values[i]['pos_y'] - ten_values[i-1]['pos_y']
    #             speed_z = ten_values[i]['pos_z'] - ten_values[i-1]['pos_z']
    #         data.append([ten_values[i]['pos_x'], ten_values[i]['pos_y'], ten_values[i]['pos_z'], speed_x, speed_y, speed_z])
    #     # mdc_logger.info("============================")
    #     # mdc_logger.info(data)
    #     data = np.array(data)
    #     data_3 = np.reshape(data, (1, data.shape[0], data.shape[1]))
    #     # mdc_logger.info(data_3.shape)
    #     # mdc_logger.info("============================")
    #     predict_test = model.predict(data_3)
    #     # mdc_logger.info("predict_test = " + str(predict_test))
    #     # mdc_logger.info("timestamp = " + str(ten_values[9]['meas_timestamp_pos']))
    #     predict_json = {
    #              "meas_timestamp_pos": 0,
    #              "pos_x": -100.0000000001,
    #              "pos_y": -10.0000000001,
    #              "pos_z": -1.00000000001,
    #              "process_time": 0
    #     }
    #     values = SDL.find_and_get(A1NS, UE_KEY, usemsgpack=False).values()
    #     # mdc_logger.info("values = " + str(values))
    #     measure = list(json.loads(v.decode()) for v in values)
    #     # mdc_logger.info("xx = " + str(xx))
    #     predict_time = time.time() - start
    #     predict_json['meas_timestamp_pos'] = timestamp
    #     predict_json['pos_x'] = predict_test[0][0]
    #     predict_json['pos_y'] = predict_test[0][1]
    #     predict_json['pos_z'] = predict_test[0][2]
    #     predict_json['process_time'] = predict_time
    #     # mdc_logger.info("predict_json = " + str(type(predict_json))) 
    #     # mdc_logger.info(str(predict_json))
    #     # mdc_logger.info("========*********************=========")
    #     SDL.set(POS, UE_KEY, json.dumps(str(predict_json)).encode(), usemsgpack=False)
    #     py_values = SDL.find_and_get(POS, UE_KEY, usemsgpack=False).values()
    #     # mdc_logger.info("========*********************=========")
    #     end = time.time()
    #     mdc_logger.info("After sending data to SDL, spend time(second) : " + str(end-start))
    #     mdc_logger.info("delta_xyz % = " + str(delta_xyz))
    #     # mdc_logger.info("**************User add *****************")

    def start(self, thread=False):
        """
        This is a convenience function that allows this xapp to run in Docker
        for "real" (no thread, real SDL), but also easily modified for unit testing
        (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
        """
        self.createHandlers()
        self._rmr_xapp.run(thread)
        # self.model_start()

    def stop(self):
        """
        can only be called if thread=True when started
        TODO: could we register a signal handler for Docker SIGTERM that calls this?
        """
        self._rmr_xapp.stop()
