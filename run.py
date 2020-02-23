from BilibiliLive import BiliBiliLive
import os, sys
import requests
import time
import config
import utils
import re
import multiprocessing
import urllib3
import traceback


urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id, check_interval=5*60):
        super().__init__(room_id)
        self.inform = utils.inform
        self.print = utils.print_log
        self.check_interval = check_interval
        self.room_id=room_id

    def check(self, interval):
        self.print(self.room_id, "Checking...")
        try:
            room_info = self.get_room_info()
            if room_info['status']:
                return True, room_info
            else:
                return False, None
        except Exception as e:
            self.print(self.room_id, 'Error:' + str(e))
            return False, None

    
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
                status, info = self.check(interval=self.check_interval)
                if not status:
                    self.print(room_id=self.room_id, content='Not Broadcasting...')
                    time.sleep(self.check_interval)
                    continue
                print(self.room_id)
                self.print(room_id=self.room_id, content='Start Broadcasting!')
                self.inform(text=f"{self.room_id}开播了", desp=info['roomname'])

                time.sleep(1.5)
                urls = self.get_live_urls()
                time.sleep(1.5)

                filename = utils.generate_filename(self.room_id)
                c_filename = os.path.join(os.getcwd(), 'files', filename)
                self.record(urls[0], c_filename)
                self.print(self.room_id, '录制完成' + c_filename)
                self.inform(text=f"{self.room_id}录制结束", desp="")
            except Exception as e:
                self.print(self.room_id, 'Error while checking or recording:' + str(e))
                traceback.print_exc()
                self.inform(text=f"Error!", desp=str(e))


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        room_id = str(sys.argv[1])
    elif len(sys.argv) == 1:
        room_id = config.room
    else:
        raise RuntimeError('请检查输入的命令是否正确 例如：python3 run.py 10086')
    BiliBiliLiveRecorder(room_id, check_interval=3*60).run()
    
