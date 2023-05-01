import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox
from QCandyUi import CandyWindow
import Ui_mover
import json
import os
from collections import defaultdict,Counter
from housingcloud import HousingCloud
from uploadhousing import UploadHousing
import datetime
import hashlib
import uuid
from ctypes import *
import mysql.connector
from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64
from config import *
from storage import *
def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac
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
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

class FurnitureInstance(object):
    def __init__(self,c=0,x=0,y=0,z=0,r=0,color=0):
        self.category= c
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.r = r

class CategoryInstance(object):
    def __init__(self,_cid,_count=0,__p=0):
        self.cid = _cid
        self.count = _count
        self.posX = []
        self.posY = []
        self.posZ = []
        self.Rotation = []
        self.Color = []
        self._p = __p

class Mover(QWidget):
    def __init__(self,dll):
        super(Mover, self).__init__()
        self.tableWidget = QTableWidget()
        self.dll = dll
        #if self.dll.GameOn()==1:
        #    self.shadow()
        self.LoadFurJson()
        self.ui = Ui_mover.Ui_Form()
        self.ui.setupUi(self)

        # self.intro()

        self.ui.btn_loadlocal.clicked.connect(self.Btn_Loadlocal)
        self.ui.btn_check.clicked.connect(self.Btn_Check)
        #self.ui.btn_layoutcheck.clicked.connect(self.Btn_Layoutcheck)
        self.ui.btn_arrange.clicked.connect(self.Btn_Arrange)
        self.ui.btn_preview.clicked.connect(self.Btn_Preview)

        self.ui.btn_ImportFile.clicked.connect(self.Btn_OpenAJsonFile)
        self.ui.btn_ExportFile.clicked.connect(self.Btn_ExportAJsonFile)
        self.ui.btn_countfur.clicked.connect(self.CountFurniture)
        
        self.ui.input.textChanged.connect(self.searchchange)

        self.ui.btn_ImportCloud.clicked.connect(self.Btn_LoadCloud)
        self.ui.btn_ExportCloud.clicked.connect(self.Btn_ExportCloud)

        self.timer_importprogress = QTimer()
        self.timer_importprogress.timeout.connect(self.UpdateImportProgress)


        self.SetTable()
   
    def intro(self):
        self.ui.intro.setOpenExternalLinks(True)
        font = QFont("Microsoft YaHei",10,63)
        self.ui.intro.setFont(font)
        self.ui.intro.setText(GetIntroduction())

    #NewWindow
    def Btn_ExportCloud(self):
        self.upload = UploadHousing()
        self.upload = CandyWindow.createWindow(self.upload,'green')
        self.upload.resize(450,450)
        self.upload.setWindowTitle('海滨墙架云导出')
        self.upload.setWindowIcon(QIcon('hbqj.ico'))
        self.upload.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.upload.show()
    #NewWindow
    def Btn_LoadCloud(self):
        self.housingcloud = HousingCloud(self)
        self.cloud = CandyWindow.createWindow(self.housingcloud,'green')
        self.cloud.resize(1200,600)
        self.cloud.setWindowTitle('海滨墙架云导入')
        self.cloud.setWindowIcon(QIcon('hbqj.ico'))
        self.cloud.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.cloud.show()

    def Btn_Loadlocal(self):
        housing = self.dll.IsHousingOn()
        #print("ishouing:"+str(self.dll.IsHousingOn()))
        if(housing==0):
            QMessageBox.information(self,"权限错误","用旋转状态选中任意家具再导出")
            return
        res = self.dll.ExportHousing()
        self.LoadAJsonFile("__tempcate.hbqj")
        os.remove(self.GetHBQJAppPath("__tempcate.hbqj"))
        
    def Btn_Layoutcheck(self):
        inslist = self.Table2InsList()
        _cidlist = []
        for ins in inslist:
            if ins.y not in[-7.0,0.0,7.0]:
                _cidlist.append(ins.category)
        strck = ""
        _cidlist = list(set(_cidlist))
        if(len(_cidlist)>0):
            strck += "下面家具可能有粘连:\n"
            for cid in _cidlist:
                strck += self.id2name[cid]
                strck +="\n"
        if(strck==""):
            strck = "似乎没家具粘连，但也不一定"
        QInputDialog.getMultiLineText(self,"家具摆放检查","检查结果",strck)


    def Btn_Arrange(self):
        #WriteFile __boogiepop_import.hbqj
        filepath = self.GetHBQJAppPath("__boogiepop_import.hbqj")
        if(filepath!=""):
            inslist = self.Table2InsList()
            catelist = self.InsList2CateList(inslist)
            jsondict = self.CateList2JsonDict(catelist)
            with open(filepath,'w') as f:
                json.dump(jsondict,f)        
        res = self.dll.BeginArranging()
        self.timer_importprogress.start(1000)
    def Btn_Preview(self):
        #WriteFile __boogiepop_preview.hbqj
        filepath = self.GetHBQJAppPath("__boogiepop_preview.hbqj")
        if(filepath!=""):
            inslist = self.Table2InsList()
            catelist = self.InsList2CateList(inslist)
            jsondict = self.CateList2JsonDict(catelist)
            with open(filepath,'w') as f:
                json.dump(jsondict,f) 
        res = self.dll.PreviewHousing()   
        QMessageBox.information(self,"预览装修","现在重新进屋~")

    def UpdateImportProgress(self):
        _c = self.dll.GetImportProgress()
        _count = self.ui.tableWidget.rowCount()
        self.ui.le_clickcount.setText('%d\\%d'%(_c,_count))

    def ClearTable(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
    
    def OpenAFile(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"选择一个装修文件","","装修数据(*.hbqj);;装修数据(*.json)")
        return filepath,filetype

    def JsonDictList2CateList(self,jsonlist):
        _res = []
        for t in jsonlist:
            cateins = CategoryInstance(t['categoryId'])
            cateins.count = t['count']
            cateins.posX = t['posX']
            cateins.posY = t['posY']
            cateins.posZ = t['posZ']
            cateins.Rotation = t['Rotation']
            if 'Color' in t.keys():
                cateins.Color = t['Color']
            else:
                cateins.Color = [0] * len(cateins.posX)
            _res.append(cateins)
        return _res

    def Btn_Check(self):
        filepath,filetype = self.OpenAFile()
        if(filepath!=""):
            if 'json' in filetype:
                with open(filepath,'r') as f:
                    _dict = json.load(f)
            elif 'hbqj' in filetype:
                with open(filepath,'r') as f:
                    encrystr = f.read()
                destr = decrypt(encrystr,salt,key)
                _dict = json.loads(destr)
            _d2 = self.JsonDictList2CateList(_dict['list'])
            _d1 = self.InsList2CateList(self.Table2InsList())
            _d1_cid = []
            _d2_cid = []
            for t2 in _d2:
                _d2_cid.append(t2.cid)
            for t1 in _d1:
                _d1_cid.append(t1.cid)
            d1md2 = list(set(_d1_cid)-set(_d2_cid))
            d2md1 = list(set(_d2_cid)-set(_d1_cid))
            cod1d2 = list(set(_d1_cid)&set(_d2_cid))
            cmpres = ""
            if(len(d1md2)!=0):
                cmpres += "这些家具没有出现在目标文件里:\n"
                for cid in d1md2:
                    cmpres += self.id2name[cid]
                    cmpres += "\n"
            if(len(d2md1)!=0):
                cmpres += "这些家具你还没有摆放出来:\n"
                for cid in d2md1:
                    cmpres += self.id2name[cid]
                    cmpres += '\n'
            for cid in cod1d2:
                for catelist in _d1:
                    if(catelist.cid == cid):
                        count1 = catelist.count
                for catelist in _d2:
                    if(catelist.cid == cid):
                        count2 = catelist.count
                if(count1!=count2):
                    cmpres += '(数量差异)'
                    cmpres += self.id2name[cid]
                    cmpres += " 现有:"+str(count1) + ",但应该是:"+str(count2)
            if(cmpres==""):
                cmpres = "类别数量检查无误"
            QInputDialog.getMultiLineText(self,"类别数量比较","比较结果",cmpres)

    def Btn_OpenAJsonFile(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"选择一个装修文件","","装修数据(*.hbqj);;装修数据(*.json)")
        if(filepath!=""):
            if 'json' in filetype:
                self.LoadAJsonFile(filepath)
            else:
                if 'hbqj' in filetype:
                    with open(filepath,'r') as f:
                        encrystr = f.read()
                    destr = decrypt(encrystr,salt,key)
                    jsondict = json.loads(destr)
                    self.LoadJsonDict(jsondict)
    
    def Btn_ExportAJsonFile(self):
        filepath, filetype = QFileDialog.getSaveFileName(self,"保存文件","","装修数据(*.hbqj)")
        if(filepath!=""):
            inslist = self.Table2InsList()
            catelist = self.InsList2CateList(inslist)
            jsondict = self.CateList2JsonDict(catelist)
            jsonstr = json.dumps(jsondict)
            enjson = encrypt(jsonstr,salt,key)
            with open(filepath,'w') as f:
                f.write(enjson)
            #with open(filepath,'w') as f:
            #    json.dump(jsondict,f)
    
    def CateList2JsonDict(self,catelist):
        _list = []
        for cateins in catelist:
            catedict = {}
            catedict['categoryId'] = cateins.cid
            catedict['count'] = cateins.count
            catedict['posX'] =cateins.posX
            catedict['posY'] = cateins.posY
            catedict['posZ'] = cateins.posZ
            catedict['Rotation'] =cateins.Rotation
            catedict['Color'] = cateins.Color
            _list.append(catedict)
        res_dict = {'size':len(_list),'list':_list}
        return res_dict

    def searchchange(self,_s):
        if _s not in self.furnames:
            return
        cid = self.name2id[_s]
        items = self.ui.tableWidget.findItems(str(cid), Qt.MatchExactly)
        if len(items) > 0:
            item = items[0]
            #item.setBackground(QBrush(QColor(0, 255, 0)))
            #item.setForeground(QBrush(QColor(255, 0, 0)))
            row = item.row()
            self.ui.tableWidget.verticalScrollBar().setSliderPosition(row)

    def LoadFurJson(self):
        with open("fur") as f:
            fur = json.load(f)
        self.name2id = fur
        self.id2name2 = {value:key for key,value in fur.items()}
        self.id2name = defaultdict(lambda:"未知家具")
        self.id2name.update(self.id2name2)
        self.furnames = list(fur.keys())
        self.furnames.append("未知家具")
        with open("color") as f:
            cs = json.load(f)
        self.colors = cs
        self.colorname2id = {value:key for key,value in self.colors.items()}

    def NameComboxChanged(self,index,row):
        #print('NameChang:'+str(index)+" "+str(row))
        self.ui.tableWidget.setItem(row,7,QTableWidgetItem(str(self.name2id[self.furnames[index]])))

    def ReconnectNameId(self):
        #print('count:'+str(self.ui.tableWidget.rowCount()))
        #print(self.furnames[self.ui.tableWidget.cellWidget(0,0).currentIndex()])
        for i in range(self.ui.tableWidget.rowCount()):
            cmb = self.ui.tableWidget.cellWidget(i,0)
            cmb.currentIndexChanged.disconnect()
        for i in range(self.ui.tableWidget.rowCount()):
            cmb = self.ui.tableWidget.cellWidget(i,0)
            cmb.currentIndexChanged.connect(lambda :self.NameComboxChanged(cmb.currentIndex(),i))

    def AddRow(self,name,order,color,x,y,z,rotation,cls):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        r = self.ui.tableWidget.rowCount()-1
        combox = ExtendedComboBox()
        combox.addItems(self.furnames)
        #combox.setStyleSheet('QComboBox{margin:3px};')
        if name not in self.furnames:
            combox.setCurrentIndex(len(self.furnames)-1)
        else:
            combox.setCurrentIndex(self.furnames.index(name))
        combox.currentIndexChanged.connect(lambda :self.NameComboxChanged(combox.currentIndex(),r))
        self.ui.tableWidget.setCellWidget(r, 0, combox)
        self.ui.tableWidget.setItem(r,1,QTableWidgetItem(str(order)))
        color = str(int(color))
        if color not in self.colors.keys():
            colorname = "未知染剂"
        else:
            colorname = self.colors[color]
        self.ui.tableWidget.setItem(r,2,QTableWidgetItem(colorname))
        self.ui.tableWidget.setItem(r,3,QTableWidgetItem("%.3f"%x))
        self.ui.tableWidget.setItem(r,4,QTableWidgetItem("%.3f"%y))
        self.ui.tableWidget.setItem(r,5,QTableWidgetItem("%.3f"%z))
        self.ui.tableWidget.setItem(r,6,QTableWidgetItem("%.3f"%rotation))
        self.ui.tableWidget.setItem(r,7,QTableWidgetItem(str(cls)))
        return self.ui.tableWidget.rowCount()

    def GetHBQJAppPath(self,filename):
        appdata = os.environ['APPDATA']
        folder = os.path.join(appdata,'HaiBinQiangJia')
        #filename = "__boogiepop_preview.hbqj"
        return os.path.join(folder,filename)

    def LoadJsonDict(self,jsondict, cloud = False):
        self.ClearTable()
        res = jsondict
        self.total_import_count = res["size"]
        self.import_count = 0
        for catelist in res['list']:
            for j in range(catelist['count']):
                cid = catelist['categoryId']
                X = catelist['posX']
                Y = catelist['posY']
                Z = catelist['posZ']
                R = catelist['Rotation']
                if 'Color' in catelist.keys():
                    C = catelist['Color']
                    color = C[j]
                else:
                    color = 0
                self.import_count += 1
                self.AddRow(self.id2name[cid],j,color,X[j],Y[j],Z[j],R[j],cid)

    def LoadAJsonDict(self,res):
        for catelist in res['list']:
            for j in range(catelist['count']):
                cid = catelist['categoryId']
                X = catelist['posX']
                Y = catelist['posY']
                Z = catelist['posZ']
                R = catelist['Rotation']
                if 'Color' in catelist.keys():
                    C = catelist['Color']
                    color = C[j]
                else:
                    color = 0
                self.AddRow(self.id2name[cid],j,color,X[j],Y[j],Z[j],R[j],cid)

    def LoadAJsonFile(self,filename):
        self.ClearTable()
        with open(self.GetHBQJAppPath(filename),'r') as f:
            res = json.load(f)
        for catelist in res['list']:
            for j in range(catelist['count']):
                cid = catelist['categoryId']
                X = catelist['posX']
                Y = catelist['posY']
                Z = catelist['posZ']
                R = catelist['Rotation']
                if 'Color' in catelist.keys():
                    C = catelist['Color']
                    color = C[j]
                else:
                    color = 0
                self.AddRow(self.id2name[cid],j,color,X[j],Y[j],Z[j],R[j],cid)

    def Table2InsList(self,ignore_row=-1):
        inslist = []
        if not isinstance(ignore_row,list):
            ignore_row = [ignore_row]
        for i in range(self.ui.tableWidget.rowCount()):
            if i in ignore_row:
                continue
            cid = int(self.ui.tableWidget.item(i,7).text())
            x = float(self.ui.tableWidget.item(i,3).text())
            y = float(self.ui.tableWidget.item(i,4).text())
            z = float(self.ui.tableWidget.item(i,5).text())
            r = float(self.ui.tableWidget.item(i,6).text())
            colorstr = self.ui.tableWidget.item(i,2).text()
            if colorstr in self.colorname2id.keys():
                colorid = self.colorname2id[colorstr]
            else:
                colorid = 0
            color = int(colorid)
            furins = FurnitureInstance(cid,x,y,z,r,color)
            inslist.append(furins)
        return inslist

    def InsList2CateList(self,inslist):
        catex = defaultdict(lambda: -1)
        catelist = []
        for i in range(len(inslist)):
            if(catex[inslist[i].category]==-1):
                _tci = CategoryInstance(inslist[i].category)
                _tci.count = 1
                _tci.posX.append(inslist[i].x)
                _tci.posY.append(inslist[i].y)
                _tci.posZ.append(inslist[i].z)
                _tci.Rotation.append(inslist[i].r)
                _tci.Color.append(inslist[i].color)
                catelist.append(_tci)
                catex[inslist[i].category] = len(catelist) - 1
            else:
                catelist[catex[inslist[i].category]].count += 1
                catelist[catex[inslist[i].category]].posX.append(inslist[i].x)
                catelist[catex[inslist[i].category]].posY.append(inslist[i].y)
                catelist[catex[inslist[i].category]].posZ.append(inslist[i].z)
                catelist[catex[inslist[i].category]].Rotation.append(inslist[i].r)
                catelist[catex[inslist[i].category]].Color.append(inslist[i].color)
        return catelist

    def LoadCateList(self,catelist):
        for cateins in catelist:
            for j in range(cateins.count):
                cid = cateins.cid 
                X = cateins.posX
                Y = cateins.posY
                Z = cateins.posZ
                R = cateins.Rotation
                Color = cateins.Color
                self.AddRow(self.id2name[cid],j,Color[j],X[j],Y[j],Z[j],R[j],cid)

    def AddFur(self):
        inputfurname,ok = QInputDialog.getText(self,'增加一个家具','输入家具名字')
        if(inputfurname not in self.furnames):
            QMessageBox.warning(self,"家具名错误","家具名错误")
            return 0
        intlist = self.Table2InsList(-1)
        intlist.append(FurnitureInstance(self.name2id[inputfurname],0.,0.,0.,0.,0.))
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.LoadCateList(self.InsList2CateList(intlist))
        return 1

    def CountFurniture(self):
        inslist = self.Table2InsList()
        catelist = self.InsList2CateList(inslist)
        total_count = 0
        furnum =""
        colors=[]
        for cate in catelist:
            furnum += (str(self.id2name[cate.cid]) + " : "+str(cate.count)+"\n")
            total_count += cate.count
            colors+=cate.Color
        furnum += "\n家具总数:" +str(total_count)
        furnum += "\n\n 染剂： \n"
        count_colors = dict(Counter(colors))
        #print(type(count_colors))
        #print(count_colors)
        for k,v in count_colors.items():
            if k==0:
                continue
            colorname = "未知染剂"
            k = str(int(k))
            if k not in self.colors.keys():
                colorname = "未知染剂"
            else:
                colorname = self.colors[k]
            furnum = furnum + colorname + ": " + str(v) +"\n"
        QInputDialog.getMultiLineText(self,"家具数量统计","家具数量",furnum)
    def DeleteFur(self,row):
        #self.ui.tableWidget.removeRow(row)
        #self.ReconnectNameId()
        new_inslist = self.Table2InsList([row])
        new_catelist = self.InsList2CateList(new_inslist)
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        #print('before load')
        self.LoadCateList(new_catelist)
        #print('after load')

    def generateMenu(self, pos):
        #print(pos)
        row_num = -1
        for i in self.ui.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        #print(row_num)
        if True:
            menu = QMenu()
            item1 = menu.addAction("删除这个家具")
            item2 = menu.addAction("增加一个家具")
            gpos = self.ui.tableWidget.mapToGlobal(pos)
            action = menu.exec_(QPoint(gpos.x()+30,gpos.y()+30))
            #action = menu.exec_(pos)
            if action == item1:
                self.DeleteFur(row_num)
            elif action == item2:
                self.AddFur()
            else:
                return

    def SetTable(self):
        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setHorizontalHeaderLabels(['家具', '序列', '染色','X','Y','Z','R','类别码'])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # Allow right click to generate submenu
        self.ui.tableWidget.customContextMenuRequested.connect(self.generateMenu)  # right click menu
        #self.LoadAJsonFile("__boogiepop_preview.hbqj")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Mover(0)
    main = CandyWindow.createWindow(main, GetTheme())
    main.resize(1000,600)
    main.setWindowTitle('holalula')
    main.show()
    sys.exit(app.exec_())