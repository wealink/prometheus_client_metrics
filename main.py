#!/usr/bin/env python3
#coding:utf-8

import prometheus_client
from prometheus_client import Counter,Gauge
import logging,datetime,logging.config
import tools
from os import path
from flask import Response,Flask
import configparser
from loguru import logger



app = Flask(__name__)
web_code = Gauge("web_code", "Web code of value",["project","env","service_name","host"])  # 数值可大可小

#eurake监控
@app.route("/metrics")
def eurake():
  urls=["http://tezign:tezign@10.80.82.203:30622/"]
  for index,url in enumerate(urls):
    code=tools.get_content(url)
    web_code.labels("sop","prod","eurake"+str(index),url).set(code)
    logger.info(prometheus_client.generate_latest(web_code))
  return Response(prometheus_client.generate_latest(web_code),mimetype="text/plain")





if __name__ == '__main__':
  config = configparser.ConfigParser()
  config.read(path.abspath(path.dirname(__file__)) + "/config/app.ini")
  appname = config['default']['appname']
  logging.config.fileConfig(path.abspath(path.dirname(__file__)) + "/config/log.conf")
  logger = logging.getLogger(appname)
  logger.info('server start：%s'% datetime.datetime.now())
  app.run(host='0.0.0.0',port=8080)
  logger.info('server close：%s'% datetime.datetime.now())

