# -*- coding:utf-8 -*-
import time
import os, sys
from datetime import datetime


__all__ = [
			'create_time'
			]

# Get Created time of file
def create_time(file_name):
	"""
	Get the create time of a file, return a string following format of:
	YYYY-MM-DD HH:MM:SS (Year-Month-Day Hour-Minute-Second)
	"""
	return datetime.fromtimestamp(os.path.getmtime(file_name)).strftime('%Y-%m-%d %H:%M:%S')

