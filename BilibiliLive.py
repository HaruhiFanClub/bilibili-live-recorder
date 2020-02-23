import time
import json
from bs4 import BeautifulSoup
import requests


class BiliBiliLive():
    def __init__(self, room_id):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.116 Safari/537.36 '
        }
        self.session = requests.session()
        self.room_id = room_id

    def common_request(self, method, url, params=None, data=None):
        connection = None
        if method == 'GET':
            connection = self.session.get(url, headers=self.headers, params=params, verify=False)
        if method == 'POST':
            connection = self.session.post(url, headers=self.headers, params=params, data=data, verify=False)
        return connection


    def get_room_info(self):
        data = {}
        room_info_url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
        user_info_url = 'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room'
        response = self.common_request('GET', room_info_url, {'room_id': self.room_id}).json()
        if response['msg'] == 'ok':
            data['roomname'] = response['data']['title']
            data['status'] = response['data']['live_status'] == 1
        self.room_id = str(response['data']['room_id'])  # 解析完整 room_id
        response = self.common_request('GET', user_info_url, {'roomid': self.room_id}).json()
        data['hostname'] = response['data']['info']['uname']
        return data

    def get_live_urls(self):
        live_urls = []
        url = 'https://api.live.bilibili.com/room/v1/Room/playUrl'
        stream_info = self.common_request('GET', url, {
            'cid': self.room_id,
            'otype': 'json',
            'quality': 0,
            'platform': 'h5'
        }).json()
        time.sleep(1.3)
        if stream_info['code'] is not 0:
            print("Old api Request Failed, get live_urls from web")
            print(f'https://live.bilibili.com/{self.room_id}')
            self.session = requests.session()
            self.common_request('GET', "https://live.bilibili.com/")
            time.sleep(1)
            web = self.common_request('GET', f'https://live.bilibili.com/{self.room_id}').text
            print(web)

            soup = BeautifulSoup(web, "html.parser") 
            script = soup.find("script", text=lambda text: text and 'window.__NEPTUNE_IS_MY_WAIFU__={"roomInitRes":' in text) 
            print(script.text)
            data = script.text.replace("window.__NEPTUNE_IS_MY_WAIFU__=","")
            js_data = json.loads(data)
            print(js_data)
            if js_data['roomInitRes']['data']['play_url'] is None:
                print("get failed")
                time.sleep(3)
                return self.get_live_urls()
            for durl in js_data['roomInitRes']['data']['play_url']['durl']:
                live_urls.append(durl['url'])
            print(live_urls)
            return live_urls
        best_quality=stream_info['data']['accept_quality'][0][0]
        stream_info = self.common_request('GET', url, {
            'cid': self.room_id,
            'otype': 'json',
            'quality': best_quality,
            'platform': 'h5'
        }).json()
        for durl in stream_info['data']['durl']:
            live_urls.append(durl['url'])
        return live_urls
