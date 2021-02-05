# -*- coding: utf-8 -*-
from os import path, listdir
from configparser import ConfigParser

conf = ConfigParser()
for c in [ini for ini in listdir("conf") if ini.endswith(".ini")]:
    conf.read(path.join("conf", c))
