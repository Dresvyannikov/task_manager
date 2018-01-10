#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from app import app
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
app.run(debug=True)
