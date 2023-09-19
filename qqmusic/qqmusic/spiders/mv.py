# -*- coding: utf-8 -*-
import json
import scrapy
import time
import execjs
from itemadapter import ItemAdapter

from ..items import QqmusicItem
class MvSpider(scrapy.Spider):
    name = 'mv'
    @staticmethod
    def get_sign(data):
        with open("qsign.js", 'r', encoding='utf-8') as f:
            js_code = f.read()
        return execjs.compile(js_code).call("sign", data)
    def start_requests(self):
        for page in range(1000):
            print(f"page {page+1} is scraping")
            _ = int(round(time.time() * 1000))
            form_data = {
                "comm": {"cv": 4747474, "ct": 24, "format": "json", "inCharset": "utf-8", "outCharset": "utf-8",
                         "notice": 0, "platform": "yqq.json", "needNewCode": 1, "uin": 657927171,
                         "g_tk_new_20200303": 5381, "g_tk": 5381},
                "req_1": {"module": "MvService.MvInfoProServer", "method": "GetAllocMvInfo",
                          "param": {"order": 1, "start": page*20, "size": 20, "version_id": 7, "area_id": 15}}}
            form_data_str = json.dumps(form_data, separators=(',', ':'))
            sign = self.get_sign(form_data_str)
            # print(sign)
            url = "https://u.y.qq.com/cgi-bin/musics.fcg?_={}&sign={}".format(_, sign)
            yield scrapy.Request(url=url, method="POST", body=form_data_str, callback=self.parse)
    def parse(self, response):
        response_json = json.loads(response.text)
        mv_list = response_json['req_1']['data']['list']
        for mv in mv_list:
            form_data = json.dumps({
                "comm": {
                    "ct": 6,
                    "cv": 0,
                    "g_tk": 5381,
                    "uin": 657927171,
                    "format": "json",
                    "platform": "yqq"
                },
                "mvInfo": {
                    "module": "music.video.VideoData",
                    "method": "get_video_info_batch",
                    "param": {
                        "vidlist": [mv['vid']],
                        "required": ["vid", "type", "sid", "cover_pic", "duration", "singers", "new_switch_str",
                                     "video_pay", "hint", "code", "msg", "name", "desc", "playcnt", "pubdate", "isfav",
                                     "fileid", "filesize_v2", "switch_pay_type", "pay", "pay_info", "uploader_headurl",
                                     "uploader_nick", "uploader_uin", "uploader_encuin", "play_forbid_reason"]
                    }
                },
                "mvUrl": {
                    "module": "music.stream.MvUrlProxy",
                    "method": "GetMvUrls",
                    "param": {
                        "vids": [mv['vid']],
                        "request_type": 10003,
                        "addrtype": 3,
                        "format": 264,
                        "maxFiletype": 60
                    }
                }
            })
            url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
            data = {
                'vid': mv['vid']
            }
            yield scrapy.Request(url=url, method="POST", body=form_data, callback=self.parse_detailed_page, meta=data)
    def parse_detailed_page(self, response):
        response_json = json.loads(response.text)
        mp4_list = response_json['mvUrl']['data'][response.meta['vid']]['mp4']
        newFileType = 0
        mp4 = {}
        for i in mp4_list:
            if newFileType <= i['newFileType']:
                newFileType = i['newFileType']
                mp4 = i
        data = {
            'vid':response.meta['vid'],
            'name':response_json['mvInfo']['data'][response.meta['vid']]['name'],
            'url':mp4['freeflow_url'][0]
        }
        yield scrapy.Request(url=data['url'], method="GET", callback=self.parse_mp4_url, meta=data,dont_filter=True)
    def parse_mp4_url(self, response):
        item = QqmusicItem()
        adapter = ItemAdapter(item)
        adapter['vid'] = response.meta['vid']
        adapter['name'] = response.meta['name']
        adapter['url'] = response.meta['url']
        adapter['content'] = response.body
        yield item