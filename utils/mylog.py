#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''/**
 * LOG
 *
 * <pre>
 * Modify Information:
 * Author        Date          Description
 * ============ =========== ============================
 * liuwei     2022年08月20日       Create this file
 * </pre>
 */'''
import os,re,sys,time,socket
import logging,tempfile,traceback
from functools import wraps
#from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

class MyLogger(object):
    def __init__(self, tag='L', dashboard=0):
        # # os.sep添加系统分隔符
        self.__sysTime = time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time())) 
        self.__log_path = os.path.join(os.sep,tempfile.gettempdir(),"test_tools","Log_test_tools.log")
        self.mylog = self.initLog(tag,dashboard)
    
    def __call__(self, func):
        # 判断入参是类还是函数
        lineNo = '0' if isinstance(func, type) else func.__code__.co_firstlineno
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.mylog.info('{}:{}|Execute|{}|Request: {}|{}'.format(func.__module__,lineNo,func.__name__,args,kwargs))
            try:
                resp = func(*args, **kwargs)
            except Exception as e:
                resp = traceback.format_exc()
                self.mylog.error('{}:{}|Execute|{}|Response: {}'.format(func.__module__,lineNo,func.__name__,resp))
            else:
                self.mylog.info('{}:{}|Execute|{}|Response: {}'.format(func.__module__,lineNo,func.__name__,resp))            
            return resp
        return wrapper

    def getHostip(self, localip='127.0.0.1', hostname='localhost'):
        try:
            serverCon = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            serverCon.connect(('8.8.8.8',80))
            localip = serverCon.getsockname()[0]
            hostname = socket.gethostname()
        finally:
            serverCon.close()
        return localip, hostname
        
    def initLog(self, tag, dashboard):
        #tempfile.gettempdir() C:\Users\dell\AppData\Local\Temp
        tmp_dir = os.path.dirname(self.__log_path)
        history_log = "{0}.{1}".format(self.__log_path, (self.__sysTime+".log")) 
        hostname = '-'.join(self.getHostip())
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)  
        if dashboard==1 or tag==1:
            dashboard=True
        taged = hostname + '|' + str(tag)
        return self.logger(taged,dashboard)  
    
    def logger(self, tag, dashboard):
        # 获取mylog实例，tag赋值给%(name)s
        Loggerx = logging.getLogger(tag)
        # 为了防止logger被创建很多个handler, 导致日志重复问题，先判断
        if not Loggerx.handlers:
            # LOG最低输出级别，默认为WARN级别
            Loggerx.setLevel(logging.DEBUG)
            # LOG输出格式 |2022-08-16 14:00:21,356|INFO|172.28.3.20-DELL|L|8792|MainThread-thread-25996|encryptApi:150|Execute|encrypt|Response: None|
            formatter = logging.Formatter('|%(asctime)s|%(levelname)s|%(name)s|%(process)d|%(threadName)s-thread-%(thread)d|%(message)s|')
            # when=midnight，interval=1每天0点更新，生成一个日志。backupCount保留的文件数量
            # f_handler = TimedRotatingFileHandler(filename=self.log_path, when="MIDNIGHT", interval=1, backupCount=30, encoding='utf-8', delay=True)
            # 历史日志文件设置，suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除
            # f_handler.suffix = "%Y-%m-%d-%H%M%S.log"
            # f_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{6}.log$")
            f_handler = RotatingFileHandler(filename=self.__log_path,maxBytes=10*1000*1000, backupCount=10, encoding='utf-8', delay=True)
            f_handler.namer = lambda log_path: "{0}.{1}".format(log_path[:-2], (self.__sysTime+".log"))  # 默认app.log.1, app.log.2...
            f_handler.setFormatter(formatter)
            # 文件日志 中文乱码encoding='utf-8'
            # f_handler = logging.FileHandler(self.log_path, encoding='utf-8') 
            # 添加日志处理器
            Loggerx.addHandler(f_handler)
            if dashboard:
                # 控制台日志
                d_console = logging.StreamHandler(sys.stdout)
                d_console.setFormatter(formatter)
                Loggerx.addHandler(d_console) 
        return Loggerx
    
    #@classmethod
    def debug(self, msg):
        self.mylog.debug(msg)
    
    #@classmethod    
    def info(self, msg):
        self.mylog.info(msg)
    
    #@classmethod
    def warn(self, msg):
        self.mylog.warning(msg)
    
    #@classmethod    
    def error(self, msg):
        self.mylog.error(msg)        
    
    #@classmethod
    def critical(self, msg):
        self.mylog.critical(msg)    
    