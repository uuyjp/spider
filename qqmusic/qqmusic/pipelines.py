# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
os_path = os.getcwd() + '/mv'
if not os.path.exists(os_path):
    os.mkdir(os_path)
class QqmusicPipeline(object):

    def process_item(self, item, spider):
        print("正在下载歌曲{}".format(item['name']))
        with open(os_path + '/{}.mp4'.format(item['name']), 'wb') as f:
            f.write(item['content'])

