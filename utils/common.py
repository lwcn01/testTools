#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''/**
 *
 * <pre>
 * Modify Information:
 * Author        Date          Description
 * ============ =========== ============================
 * liuwei     2022年08月20日       Create this file
 * </pre>
 */'''
import os,sys,re,time,datetime,base64
import tempfile,webbrowser,jpype,qrcode
import socket,threading,subprocess,urllib
from multiprocessing import Process
from multiprocessing import Pool
from PIL import Image as pilImage
from PIL import ImageTk as pilImageTk
from mylog import MyLogger as myLog
# pip install jpype1 安装jpype 调用jar包

class MutilProcess(object):
    """docstring for MutilProcess"""
    def __init__(self):
        self.results = []
        
    @classmethod 
    @myLog()   
    def mutilThread(cls,proc,*arg):
        # 避免线程间资源竞争影响，需要加锁；重复执行也会导致资源紧张
        task_lock = threading.Lock()
        task_lock.acquire() ##加锁
        cls.results=[]
        t_list = []
        def getResult(*arg):
            _result = proc(*arg)
            cls.results.append(_result)
        threads = threading.Thread(target=proc,args=(*arg,))
        t_list.append(threads)
        for t in t_list:
            getResult(*arg)
            t.setDaemon(True) #得置后台，不然UI界面会卡
            # t.start() # 不注释，导致batchEncrypt加密方法被执行了2次
            #t.join()   #不能等待一个线程至结束，等待导致UI界面卡住   
        task_lock.release() ##释放锁
        
    @classmethod
    @myLog()
    def repeatThreadDetection(cls, tName):
        # 在线程未运行结束时，避免重复开启多线程
        # 判断线程名称为tName的线程，是否处于活跃状态
        for item in threading.enumerate():
            if tName == item.name:
                return True
        return False

class TaskClass(object):
    def __init__(self):
        self.htmlPath = None
        self.imgPath = None  

    @myLog()    
    def createTempFile(self,suffix,data,delete=False,fileType='file'):
        if fileType=='dir':
            return tempfile.gettempdir()
        else:
            #html_bytes = str.encode(html)
            data_bytes = bytes(data, encoding = "utf8")
            # https://docs.python.org/zh-cn/3.8/library/tempfile.html 已弃用mkstemp
            #tempfile.TemporaryFile(mode, bufsize, suffix, prefix, dir)在文件系统中找不到文件的 
            #tempfile.NamedTemporaryFile(mode, bufsize, suffix, prefix, dir, delete)     
            f = tempfile.NamedTemporaryFile(suffix=suffix,delete=delete)
            f.write(data_bytes)
            f.seek(0) #写入b''时，需要使用seek()，为了以后读取数据       
            return f
            
    @myLog()    
    def visitWeb(self):
        html="""<!DOCTYPE html>
            <html>
                <body>
                <h1>404</h1>
                <p>访问的网页不存在！</p>
                </body>
            </html>"""
        url = "http://172.31.3.110/tools/index.html"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except:
            htmlPath = self.createTempFile(suffix='.html',data=html,delete=False)
            self.htmlPath = htmlPath.name
            #new=0, 在同一个浏览器窗口中打开；new=1，新的浏览器窗口会被打开;new=2 新的浏览器tab会被打开
            webbrowser.open(self.htmlPath, new=0, autoraise=True)
            htmlPath.close()
    
    @myLog()
    def makeQRcode(self,data,err_c,version,border,logo_path,box_size=8):
        """#QRCode类参数有四个参数：version、err_correction、box_size、border
        version：参数是（1-40）的整数，该参数用来控制二维码的尺寸（最小，version=1，该version的尺寸是21*21）。把version设置为None且使用fit参数会自动生成二维码。
        err_correction:参数控制生成二维的误差。qrcode包中有四个可用的常量：
        ERROR_CORRECT_L：该常量表示误差率低于7%(包含7%)
        ERROR_CORRECT_M(默认值)：该常量表示误差率低于15%(包含15%)
        ERROR_CORRECT_Q：该常量表示误差率低于25%(包含25%)
        ERROR_CORRECT_H：该常量表示误差率低于30%(包含30%)
        box_size:参数用来控制二维码的每个单元(box)格有多少像素点
        border: 参数用控制每条边有多少个单元格0到4(默认值是4，这是规格的最小值)
        二维码像素尺寸：(21+(version-1)*4+border*2)*box_size"""
        if self.imgPath:
            os.remove(self.imgPath)
        img_path = self.createTempFile(suffix='.png',data='',delete=False)
        if version > 20:           # 尺寸1-40间
            version = 20
        if version < 1:
            version = 1
        if err_c == 'M 15%':
            error_correction=qrcode.constants.ERROR_CORRECT_M
        elif err_c == 'Q 25%':
            error_correction=qrcode.constants.ERROR_CORRECT_Q       
        elif err_c == 'H 30%':
            error_correction=qrcode.constants.ERROR_CORRECT_H
        else:
            error_correction=qrcode.constants.ERROR_CORRECT_L
        qr = qrcode.QRCode(version=version, error_correction=error_correction, box_size=box_size, border=border,)
        qr.add_data(data)  # 添加数据
        qr.make(fit=True)  # 填充数据
        img = qr.make_image(fill_color="black", back_color="white") # 生成图片
        if logo_path and os.path.exists(logo_path):                 # 添加logo
            if os.path.splitext(logo_path)[1] in ('.png','.jpg','.jpeg','.bmp','.gif'):
                img = img.convert("RGBA")  
                icon = pilImage.open(logo_path) # 打开logo照片
                img_w, img_h = img.size         # 获取图片的宽高
                factor = 6                      # 参数设置logo的大小
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                icon_w, icon_h = icon.size
                if icon_w > size_w:
                    icon_w = size_w
                if icon_h > size_h:
                    icon_h = size_h
                # 重新设置logo的尺寸    
                icon = icon.resize((icon_w, icon_h), pilImage.ANTIALIAS) 
                # 得到画图的x，y坐标，居中显示 # 黏贴logo照
                w = int((img_w - icon_w) / 2)
                h = int((img_h - icon_h) / 2) 
                img.paste(icon, (w, h), mask=None) 
        #img.show() # 显示图片
        img.save(img_path) # 保存img
        self.imgPath = img_path.name
        img_path.close()
        #终端显示图片
        # img_open = pilImage.open(img_path)
        # img_open = img_open.convert('RGB') #解决jpg报错，OSError: cannot write mode RGBA as JPEG
        # img_show = pilImageTk.PhotoImage(img_open)
    
    @myLog()
    def imageToBase64(self,path):
        suffix = os.path.splitext(path)[-1]
        if suffix not in ('.png','.jpg','.jpeg','.bmp','.gif'):
            return ""
        with open(path,"rb") as img:
            base64bytes = base64.b64encode(img.read())
            base64_str =  base64bytes.decode()
        return "data:image/{0};base64,{1}".format(suffix[1:], base64_str)   
    
    @myLog()
    def base64ToImage(self,string,name='tmp.png'):
        base64_str = string.split(",")[1] if "," in string else string
        img_decode = base64.b64decode(base64_str)
        with open(name,'wb+') as tmp:
            tmp.write(img_decode)
        self.imgPath = os.path.abspath(name)
        return os.path.abspath(name)    

    @myLog()
    def imageToFaviconIco(self,src_path,dist_path='favicon.ico',default_size=256):
        suffix = os.path.splitext(src_path)[-1]
        ico_size = {16: (16,16), 32: (32,32), 48: (48,48),
                    64: (64,64), 128: (128,128), 256: (256,256),}
        ico_size_value = ico_size.get(default_size)
        #dist_path = self.createTempFile(suffix='.ico',data='',delete=False)
        if ico_size_value and os.path.isfile(src_path) and suffix in ('.png','.jpg','.jpeg','.bmp','.gif','.ico'):
            ico_image = pilImage.open(src_path)
            ico_image = ico_image.resize(ico_size_value)
            ico_image.save(dist_path)
            #dist_path.close()
            return os.path.abspath(dist_path)
        return ""    

class Common(TaskClass):
    def __init__(self):
        # super(TaskClass, self).__init__() 只继承方法？
        super().__init__() # 继承属性和方法

    @myLog()
    def getSystime(self):
        current_time = datetime.datetime.now().strftime('%Y%m%d')
        return current_time
        
    @myLog()
    def getHostip(self, localip='127.0.0.1', hostname='localhost'):
        try:
            serverCon = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            serverCon.connect(('8.8.8.8',80))
            localip = serverCon.getsockname()[0]
            hostname = socket.gethostname()
        finally:
            serverCon.close()
        return localip, hostname

    @myLog()
    def getRealIP(self, url='cip.cc'):
        command = 'curl -s %s'%url
        out = self.shellCmd(command,timeout=10)
        # ip正则匹配(1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)){3}
        # ['IP\t: 222.244.100.9', '地址\t: 中国  湖南  长沙', '运营商\t: 电信']
        out = list(filter(lambda x: x,re.split("{|}|\n",out.replace('"',''))))
        # [('IP', '222.244.100.9'), ('地址', '中国  湖南  长沙'), ('运营商', '电信')]
        out = dict(map(lambda x: (x.split(':',1)[0].strip().upper(), x.split(':',1)[1].strip().strip(',')), out))
        ip4 = out.get('IP')
        numbers = list(map(int, ip4.split('.')))
        out['IPV6'] = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers)
        return out

    @myLog()
    def shellCmd(self, command, timeout=None, buffering=-1):
        # pyinstaller打包，subprocess报“句柄无效”错误。故需去掉-w
        proc = subprocess.Popen(command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                bufsize=buffering)
        stdoutdata, stderrdata = proc.communicate()
        proc.wait(timeout=timeout)
        return stdoutdata.decode("utf-8")

    @myLog()
    def decode(self, _bytes):
        #byte 使用 decode 方法就能转变成 str
        if '3' == sys.version_info.major:
            string = str(_bytes, encoding = "utf8").strip() 
            #string = _bytes.decode('utf-8')        
        else:
            string = str(_bytes).strip()    
        return string
        
    @myLog()
    def queryData(self, func, count, *args): #*args是元组, 传1。/**kwargs是字典，传cardType=1。
        result = []
        for _ in range(count):
            #if any(args):   #args=(20,)  but *args=20               
            out = lambda: func(*args)
            result.append(out())
        return "\n".join(result)
        
    @myLog()
    def getSize(self, filepath=''):
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
        else:
            size = filepath        
        if size > 1000*1000*1000:
            size = size/1024/1024/1024
            unit = 'GB'
        elif size > 1000*1000:
            size = size/1024/1024
            unit = 'MB'
        else:
            size = size/1024
            unit = 'KB'
        return size, unit
    
    @myLog()
    def isChinese(self, txt_string):
        for word in txt_string:
            if '\u4e00' <= word <= '\u9fff':
                return True
        return False
    
    @myLog()
    def jarService(self, plaintext, key, jar, jar_path, crypt='Encrypt'):
        className = {'XID':{'Encrypt':'org.aiav.xidlabelsoftsdk.service.generate.XidlabelGenerateService'},
                     'SM4':{'Encrypt':'hive.udf.SM4Encrypt',
                            'Decrypt':'hive.udf.SM4UDF'}}
        filePath = jar_path
        class_name = className[jar][crypt]
        if not os.path.isfile(filePath):
            return ''
        if not jpype.isJVMStarted():
            self.jarStartJVM(filePath) 
        JClass = jpype.JClass(class_name)
        jarClass = JClass()
        if jar == 'XID':
            jaroutput = jarClass.generateXidlabelById(key, plaintext)
            #jpype.shutdownJVM()
        else:
            jaroutput = jarClass.evaluate(plaintext)
        return '{}'.format(jaroutput)        
    
    @myLog()
    def jarStartJVM(self, filePath):
        jvmPath = jpype.getDefaultJVMPath()
        #jvmPath = "C:/Program Files/Java/jre1.8.0_131/bin/server/jvm.dll"
        #dependency = os.path.join(os.path.abspath('.'), 'F:/JPypeTestl/dependency')    
        #jpype.startJVM("%s"%dll_path, "-ea", "-Djava.class.path=%s" %filePath, "-Djava.ext.dirs=%s" %dependency)    #当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
        jpype.startJVM("%s"%jvmPath, "-ea", "-Djava.class.path=%s" %filePath)
        #jpype.java.lang.System.out.println("HelloWorld")
    
    @myLog()
    def jarShutdownJVM(self):
        #if not jpype.isStarted():
        if jpype.isJVMStarted():
            jpype.shutdownJVM()

    @myLog()
    def filePath(self, name, suffix, file_path):
        if os.path.isfile(file_path):
            _filePath = os.path.dirname(file_path)
        elif os.path.isdir(file_path):   
            _filePath = file_path
        else:
            _filePath = os.getcwd()
        fixFiles = [_file for _file in os.listdir(_filePath) if _file.endswith(suffix)]
        _file_path = ''
        if fixFiles:
            for _name in fixFiles:
                if (name.upper() in _name) or (name.lower() in _name):
                    _file_path = os.path.join(_filePath,_name)
                    if '.jar'==suffix and self.isChinese(_filePath):
                        _file_path = _name
                    break    
        return _file_path
        
    @myLog()
    def reporthook(self, downsize, totalsize, blocksize=1024*5):
        #'''回调函数
        # @downsize: 已经下载的数据块大小
        # @blocksize: 数据块的大小
        # @totalsize: 远程文件的大小
        percent = 100.0 * downsize / totalsize
        if percent > 100:
            percent = 100
        if downsize >= totalsize:
            ret = 1,"下载完成"    
        else:
            ret = 2,"下载中...\n"+"%.2f%%"%(percent)+"====>"+"%.2f"%(downsize/1024/1024)+"M/"+"%.2f"%(totalsize/1024/1024)+"M \r"
        return ret
