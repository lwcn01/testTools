#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys

__all__ = ['common',
           'cpcn',
           'DataCenter',
           'encryptApi',
           'IdentityCard',
           'mylog'
]
# os.path.dirname(os.path.abspath(__file__))当前init文件目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# def _JoinPath(*path_parts):
#   return os.path.abspath(os.path.join(*path_parts))

# def _AddDirToPythonPath(*path_parts):
#   path = _JoinPath(*path_parts)
#   if os.path.isdir(path) and path not in sys.path:
#     sys.path.insert(1, path)

# _CATAPULT_DIR = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir)

# _AddDirToPythonPath(_CATAPULT_DIR, 'code', 'mylog')
# _AddDirToPythonPath(_CATAPULT_DIR, 'code')
