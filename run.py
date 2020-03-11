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
from urllib.parse import urlparse
import m3u8_ff_downloader


urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id, check_interval=5*60, proxy=None, use_option_link=False):
        super().__init__(room_id, proxy=proxy)
        self.inform = utils.inform
        self.print = utils.print_log
        self.check_interval = check_interval
        self.room_id=room_id
        self.use_option_link = use_option_link

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

    def flvrecord(self, record_url, output_filename):
        self.print(self.room_id, '正在录制...' + self.room_id)
        self.print(self.room_id, record_url)
        print(f"wget \"{record_url}\" -O {output_filename} --no-proxy")
        print()
        os.system(f"wget \"{record_url}\" -O {output_filename} --no-proxy")

    def m3u8record(self, record_url, output_filename):
        self.print(self.room_id, '正在录制...' + self.room_id)
        self.print(self.room_id, record_url) 
        downloader = m3u8_ff_downloader.M3U8Downloader(
            uri=record_url,
            timeout=20,
            ffmpeg_path='ffmpeg',
            ffmpeg_loglevel='info',
        )
        downloader.download(output=output_filename)

    def run(self):
        while True:
            try:
                status, info = self.check(interval=self.check_interval)
                if not status:
                    self.print(room_id=self.room_id, content='Not Broadcasting...')
                    time.sleep(self.check_interval)
                    continue
                
                self.print(room_id=self.room_id, content='Start Broadcasting!')
                self.inform(text=f"{self.room_id}开播了", desp=info['roomname'])

                # time.sleep(1.5)
                # status, urls = self.get_live_urls_byapi()
                # url = urls[0]
                # print(urls)
                # print("url:" + url)
                # path = urlparse(url).path
                # ext = str(os.path.splitext(path)[1])
                # print(ext)
                # Directly use get_live_urls_byweb, prevent m3u8sucks


                time.sleep(1)
                status, urls = self.get_live_urls_byweb()
                if not status:
                    self.print("Error! Getting play_url From Web Failed.")
                    self.inform(text=f"Error! Getting play_url From Web Failed. Room:{self.room_id}", desp=info['roomname'])
                    time.sleep(3)
                    continue
                print(urls)
                ext = str(os.path.splitext(urlparse(urls[0]).path)[1])
                print(ext)       

                # generate file name
                filename = utils.generate_filename(self.room_id)
                c_filename = os.path.join(os.getcwd(), 'files', filename)

                if self.use_option_link:
                    # If you use this tool overseas, you maybe set use_option_link to True and use a proxy.
                    # use the last url in urls, which is generally available for overseas user.
                    url = urls[len(urls)-1]
                else:
                    # use the first url in urls, which is generally available for domenstic user.
                    url = urls[0]

                if ext == '.flv':
                    self.flvrecord(url, c_filename + ".flv")
                elif ext == '.m3u8':
                    self.print(f"Warning! Recording in m3u8 mode, maybe the record file is not complete.")
                    self.inform(text=f"Warning! Recording in m3u8 mode, maybe the record file is not complete. Room:{self.room_id}", desp=info['roomname'])
                    self.m3u8record(url, c_filename + ".mp4")

                self.print(self.room_id, '录制完成' + c_filename)
                self.inform(text=f"{self.room_id}录制结束", desp="")
            except Exception as e:
                self.print(self.room_id, 'Error while checking or recording:' + str(e))
                traceback.print_exc()
                self.inform(text=f"Error!", desp=str(e))


if __name__ == '__main__':
    print(sys.argv)
    # prevent from downloading via clashX or shadowsocks
    os.system("unset http_proxy")
    os.system("unset https_proxy")
    os.system("unset all_proxy")
    if len(sys.argv) == 2:
        room_id = str(sys.argv[1])
    elif len(sys.argv) == 1:
        room_id = config.room
    else:
        raise RuntimeError('请检查输入的命令是否正确 例如：python3 run.py 10086')
    if config.enable_proxy:
        proxy = config.proxy
    else:
        proxy = None
    BiliBiliLiveRecorder(room_id, check_interval=0.5*60, proxy=proxy, use_option_link=config.use_option_link).run()
    
