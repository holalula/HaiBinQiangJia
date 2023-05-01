import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox
from QCandyUi import CandyWindow
import json
import os
import mysql.connector
import json
import datetime
import hashlib
#from Crypto.Cipher import AES
from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64
def stringtomd5(originstr):
    signaturemd5 = hashlib.md5()
    signaturemd5.update(originstr.encode('utf8'))
    return signaturemd5.hexdigest()
salt = "neversmile"
key = "wjsycdmm"
def rpad(text, divisor: int, suffix):
    remain = len(text) % divisor
    if remain > 0:
        text += suffix * (divisor - remain)
    return text

def encrypt(text, salt, key):
    fmtkey, fmtiv = map(lambda s: s.encode()[:16].ljust(16, b'\0'), (key, salt))
    cryptor = AES.new(fmtkey, AES.MODE_CBC, fmtiv)
    fmttext = rpad(text.encode(), 16, b'\0')
    ciphertext = cryptor.encrypt(fmttext)
    return str(b2a_base64(ciphertext))[2:-3].rstrip('=')

def decrypt(text, salt, key):
    fmtkey, fmtiv = map(lambda s: s.encode()[:16].ljust(16, b'\0'), (key, salt))
    cryptor = AES.new(fmtkey, AES.MODE_CBC, fmtiv)
    fmttext = rpad(text, 4, '=')
    return cryptor.decrypt(a2b_base64(fmttext)).rstrip(b'\0').decode()
class UploadHousing(QWidget):
    def __init__(self):
        super(UploadHousing,self).__init__()
        self.InitUI()
        self.imagepath = ""
        self.itemspath = ""
        self.filetype = ""
        self.itemsjsondict = {}
        self.btn_image.clicked.connect(self.Btn_image)
        self.btn_items.clicked.connect(self.Btn_items)
        self.btn_upload.clicked.connect(self.Btn_upload)

    def InitUI(self):
        layout = QFormLayout()

        self.label_housingname = QLabel("装修名：")
        self.label_uploader = QLabel("上传者：")
        self.label_email = QLabel("联系方式：")
        self.label_housingsize = QLabel("房屋大小：")
        self.label_furcount = QLabel("家具总数：")
        self.label_tags = QLabel("描述tags：")
        self.label_image = QLabel("预览图")
        self.label_items = QLabel("装修文件：")

        self.le_housingname = QLineEdit("")
        self.le_uploader = QLineEdit("")
        self.le_email = QLineEdit("")
        self.box_housingsize = QComboBox()
        self.box_housingsize.addItems(["S","M","L"])
        self.le_furcount = QLineEdit("")
        self.le_tags = QLineEdit("#tag1#tag2")
        self.btn_image = QPushButton("上传预览图")
        self.btn_items = QPushButton("上传装修文件")

        layout.addRow(self.label_housingname,self.le_housingname)
        layout.addRow(self.label_uploader,self.le_uploader)
        layout.addRow(self.label_email,self.le_email)
        layout.addRow(self.label_housingsize,self.box_housingsize)
        layout.addRow(self.label_furcount,self.le_furcount)
        layout.addRow(self.label_tags,self.le_tags)
        layout.addRow(self.label_image,self.btn_image)
        layout.addRow(self.label_items,self.btn_items)

        self.btn_upload = QPushButton("上传")
        self.btn_upload.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        wg = QWidget()
        wg.setLayout(layout)

        layout2 = QVBoxLayout()
        layout2.addWidget(wg)
        layout2.addWidget(self.btn_upload)

        self.setLayout(layout2)
    
    def Btn_image(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"选择装修预览图","","Image(*.jpg;*.png)")
        if(os.path.getsize(filepath)>5*1024*1024):
            QMessageBox.information(self,"太大了，服务器忍不下！","确保预览图小于5MB哦")
            return
        self.imagepath = filepath
        
    def checkJson(self,filepath):
        with open(filepath,'r') as f:
            res = json.load(f)
        ks = list(res.keys())
        if 'size' in ks and 'list' in ks:
            return True
        else:
            return False

    def checkJsonDict(self,jsondict):
        res = jsondict
        ks = list(res.keys())
        if 'size' in ks and 'list' in ks:
            return True
        else:
            return False

    def Btn_items(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"选择装修文件","","装修数据(*.hbqj);;装修数据(*.json))")
        if(os.path.getsize(filepath)>5*1024*1024):
            QMessageBox.information(self,"???","你要传啥？屏幕已截图，本机FF14游戏账号信息已上传，请自便。")
            return
        if 'hbqj' in filetype:
            with open(filepath,'r') as f:
                encrystr = f.read()
            destr = decrypt(encrystr,salt,key)
            jsondict = json.loads(destr)
            if(not self.checkJsonDict(jsondict)):
                QMessageBox.information(self,"???","格式错误。")
                return
            self.filetype = "hbqj"
            self.itemsjsondict = jsondict
            self.itemspath = "*.hbqj"
        else: #.json
            if(not self.checkJson(filepath)):
                QMessageBox.information(self,"???","格式错误。")
                return
            self.itemspath = filepath
            self.filetype = "json"

    def Btn_upload(self):
        print(self.box_housingsize.currentIndex())
        return 
        reply = QMessageBox.question(self,"没点错吧?","你确认要上传吗？",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.No:
            return
        #query Server CanWeUpload

        mycursor = mydb.cursor()
        sql = "SELECT curversion FROM updateinfo WHERE id=5"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        mydb.close()
        if res[0][0]!="onupload":
            QMessageBox.information(self,"上传失败","服务器遭到恶意攻击，暂停上传,如果你想分享装修可以去NGA联系作者或者加QQ群：956020235")
            return
        #end query
        housingname = self.le_housingname.text()
        uploader = self.le_uploader.text()
        housesize = self.box_housingsize.currentIndex()
        tags = self.le_tags.text()
        furcount = self.le_furcount.text()
        today_time = str(datetime.datetime.now()).split('.')[0]
        uploadtime = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
        email = self.le_email.text()

        #images = img
        #items = json.dumps(res)
        #itemshash = stringtomd5(items)
        img = bytes()
        if self.imagepath!="":
            with open(self.imagepath,'rb') as fp:
                img = fp.read()
        if self.itemspath=="":
            QMessageBox.warning(self,"???","至少要上传装修文件")
            return
        else:
            if self.filetype == "json":
                with open(self.itemspath,'r') as f:
                    res = json.load(f)
                items = json.dumps(res)
            elif self.filetype == "hbqj":
                items = json.dumps(self.itemsjsondict)
            else:
                QMessageBox.warning(self,"???","文件格式错误！")
                return
            itemshash = stringtomd5(items)

        sql = "INSERT INTO upload_housing (items,itemshash,images,housingname,uploader,email,housesize,tags,furcount,uploadtime) VALUES (%s,%s,_binary %s,%s,%s,%s,%s,%s,%s,%s)"
        val = (items,itemshash,img,housingname,uploader,email,housesize,tags,furcount,uploadtime)

        cursor = mydb.cursor()
        try:
            cursor.execute(sql,val)
        except mysql.connector.errors.IntegrityError:
            QMessageBox.warning(self,"重复上传","这个文件已经上传过了")
        else:
            mydb.commit()
            QMessageBox.information(self,"上传成功","上传成功，审核后才会显示，感谢你的分享~(欢迎你加入装修分享QQ群：956020235)")
        mydb.close()

        

    
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = UploadHousing()
    main = CandyWindow.createWindow(main,'green')
    main.resize(400,450)
    main.setWindowTitle('holalula')
    main.show()
    sys.exit(app.exec_())