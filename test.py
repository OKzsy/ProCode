#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

items = os.listdir(".")
newlist = []
for names in items:
    if names.endswith((".py", ".txt")):
        newlist.append(names)
print(newlist)
