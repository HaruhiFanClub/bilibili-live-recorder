# bilibili_live_recorder

下载 bilibili 直播 视频流  



## Installation

- requests and socks5 support : `pip install -U requests[socks]`
- wget
- ffmpeg
- BeautifulSoup4
- m3u8
- ffmpy



## Usage

**修改`config_sample.py`为`config.py`，并填入 [Server酱](http://sc.ftqq.com/3.version) 通知的密钥**



### 参数说明:

- `enable_inform = True`		

  \#是否启用Server酱通知
  
- `inform_url = 'https://sc.ftqq.com/****.send'` 

  \# Server酱 api地址
  
- `room = '12694411'`

  \# 直播间地址(string)
  
- `enable_proxy = False`

   \# 是否启用代理服务器请求play_url
   
- `proxy = "socks5://127.0.0.1:1080"`

   \# 代理服务器地址
   
- `use_option_link = False`

  \# 是否使用次要play_url
  
  - 如果你是海外用户,请设置为True. 程序会使用play_url[4]中最后一个url,一般在海外有用
  - 如果你是国内用户,请设置为False. 程序会使用play_url[4]中第一个url,一般在国内有用
  - If you are oversea user, please set this to True. if so, the program will use the last url in play_url, which is generally available for oversea request
  - If you are domestic userm please set this to False. if so, the program will use the firt url in play_url, which is available for domestic request



