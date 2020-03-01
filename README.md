# bilibili_live_recorder

    下载 bilibili 直播 视频流  

## Installation

    - Use requests that support socks! : `pip install -U requests[socks]`

## Usage

**修改`.config.py`为`config.py`，（如有需要）并填入 [Server酱](http://sc.ftqq.com/3.version) 通知的密钥**

### cli 模式（仅支持单直播间）

    - `python run.py [room_id]`  
    - room_id: 直播间id

### config.py 模式（支持多直播间）

    1. 打开 `config.py` 

## Example

    code>python run.py 1075</code>
