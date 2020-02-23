from Live import BiliBiliLive
import os, sys
import requests
import time
import config
import utils
import re
import multiprocessing
import urllib3
urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id, check_interval=5*60):
        super().__init__(room_id)
        self.inform = utils.inform
        self.print = utils.print_log
        self.check_interval = check_interval

    def check(self, interval):
        while True:
            self.print(self.room_id, "Checking...")
            try:
                room_info = self.get_room_info()
                if room_info['status']:
                    self.inform(room_id=self.room_id,desp=room_info['roomname'])
                    self.print(self.room_id, room_info['roomname'])
                    break
                else:
                    self.print(self.room_id, '等待开播')
            except Exception as e:
                self.print(self.room_id, 'Error:' + str(e))
            time.sleep(interval)
        return self.get_live_urls()

    def record(self, record_url, output_filename):
        try:
            self.print(self.room_id, '正在录制...' + self.room_id)
            self.print(self.room_id, record_url)
            os.system(f"wget \"{record_url}\" -O {output_filename} --no-proxy")
        except Exception as e:
            self.print(self.room_id, 'Error while recording:' + str(e))

    def run(self):
        while True:
            try:
                urls = self.check(interval=self.check_interval)
                filename = utils.generate_filename(self.room_id)
                c_filename = os.path.join(os.getcwd(), 'files', filename)
                self.record(urls[0], c_filename)
                self.print(self.room_id, '录制完成' + c_filename)
            except Exception as e:
                self.print(self.room_id, 'Error while checking or recording:' + str(e))


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        room_id = str(sys.argv[1])
    elif len(sys.argv) == 1:
        room_id = config.room  # input_id = '917766' '1075'
    else:
        raise RuntimeError('请检查输入的命令是否正确 例如：python3 run.py 10086')
    BiliBiliLiveRecorder(room_id, check_interval=3*60).run()
    
