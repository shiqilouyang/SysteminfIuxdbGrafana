import configparser
import os
import json


class ConfManagement(object):
    def __init__(self,default="spark-sql"):
        self.section =default
        self.curpath = os.path.dirname(os.path.realpath(__file__))
        self.inipath = os.path.join(self.curpath, "conf.ini")
        self.json_path = os.path.join(self.curpath, "spark-sql.json")
        self.conf = configparser.ConfigParser()
        self.conf.read(self.inipath)

    def get_ini(self, value):
        try:
            return self.conf.get(self.section, value)
        except Exception as e:
            from logs import SetLog
            SetLog().error("it is not find %s from conf.int"%value)
            raise e

    def set_ini(self, session, value):
        self.conf.set(self.section, session, value)
        self.conf.write(open(self.inipath, "r+"))

    def get_json(self):
        with open(self.json_path, 'r') as f:
            return json.load(f)
