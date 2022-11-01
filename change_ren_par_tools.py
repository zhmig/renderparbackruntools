#!/usr/bin/env python
# coding=utf-8
'''
Author        : zhenghaoming
Date          : 2022-10-25 11:53:35
FilePath      : \change_ren_par_tools.py
version       : 
LastEditors   : zhenghaoming
LastEditTime  : 2022-11-01 09:01:48
'''

import os,sys,subprocess,logging,re,shutil,io
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from functools import partial

proj_path=os.path.abspath('.')
print (proj_path)
config_path = os.path.abspath(__file__)

sys.path.append(proj_path)


from ui.tools import *
from get_maya_version import *
from script.maFile_replace_content import *

class Table(QTableWidget):
    TABLE_WIDTHER = [120, 330]
    def __init__(self,*args, **kwargs):
        super(Table,self).__init__(*args, **kwargs)
        self.setColumnCount(2)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setHorizontalHeaderLabels([u"File Name", u"File Full Path"])
        for i, w in enumerate(Table.TABLE_WIDTHER):
            self.setColumnWidth(i, w)

        self.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        self.connect_widgets()

    def connect_widgets(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_popup_button)

    @Slot(QPoint)
    def create_popup_button(self,pos):

        self.popup_menu = QMenu(self)
        self.addLine = self.popup_menu.addAction(u'新增',self.add_table_line)
        self.delItem = self.popup_menu.addAction(u'删除',self.del_table_line)
        self.clearItem = self.popup_menu.addAction(u'清空',self.refresh_table)

        screenPos = self.mapToGlobal(pos)
        self.popup_menu.exec_(screenPos)

    def refresh_table(self):
        # print ("\nclean table item")
        self.setRowCount(0)

    def add_table_line(self):
        self.setRowCount(self.rowCount()+1)
        # print ("\nadd a new row")
        # print ("\nrow count num: %s" % (self.rowCount()+1))

    def del_table_line(self):

        index_list = []                                                          
        for model_index in self.selectionModel().selectedRows():       
            index = QPersistentModelIndex(model_index)         
            index_list.append(index)                                             

        for index in index_list:                                      
            self.removeRow(index.row()) 

    def dropEvent(self, event):

        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))

            rows_to_move = []
            for row_index in rows:
                items = dict()
                for column_index in range(self.columnCount()):
                    # get the widget or item of current cell
                    widget = self.cellWidget(row_index, column_index)
                    if isinstance(widget, type(None)):
                        # if widget is NoneType, it is a QTableWidgetItem
                        items[column_index] = {"kind": "QTableWidgetItem",
                                            "item": QTableWidgetItem(self.item(row_index, column_index))}
                    else:
                        # otherwise it is any other kind of widget. So we catch the widgets unique (hopefully) objectname
                        items[column_index] = {"kind": "QWidget",
                                            "item": widget.objectName()}

                rows_to_move.append(items)

            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)

                for column_index, column_data in data.items():
                    if column_data["kind"] == "QTableWidgetItem":
                        # for QTableWidgetItem we can re-create the item directly
                        self.setItem(row_index, column_index, column_data["item"])
                    else:
                        # for others we call the parents callback function to get the widget
                        _widget = self._parent.get_table_widget(column_data["item"])
                        if _widget is not None:
                            self.setCellWidget(row_index, column_index, _widget)

            event.accept()

        super(Table,self).dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()

class MainWindow(QMainWindow):

    WINDOW_TITLE = u"渲染质量批量切换工具 1.0"

    def __init__(self):
        super(MainWindow,self).__init__()

        self.maya_exe = ''
        self.json_path = ''

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(MainWindow.WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon("%s\icon\huitailang.png"%proj_path))
        self.maya_vers = get_maya_ver()

        self.read_qss()
        self.create_widgets()
        self.create_layers()
        self.connect_widget()
        self.refresh_menu()

    def read_qss(self):
        from script import window_qss
        self.app_style = window_qss.window_qss1()
        self.setStyleSheet(self.app_style)

    def create_widgets(self):

        self.mayaver_menu = self.menuBar().addMenu(u"Maya版本")

        for mayaName,mayaPath in self.maya_vers:
                mayaver = self.mayaver_menu.addAction(mayaName)
                mayaver.setCheckable(True)
                mayaver.setStatusTip(u"{}Bin\mayabatch.exe".format(mayaPath).replace("\\","/"))
                mayaver.setToolTip(u"{}Bin\mayabatch.exe".format(mayaPath).replace("\\","/"))
                mayaver.setData(u"{}Bin\mayabatch.exe".format(mayaPath).replace("\\","/"))
                self.mayaver_menu.addAction(mayaver)

        self.value_type_group = QActionGroup(self)
        self.table = Table()
        self.run_Btn =QPushButton(u'运行')
        self.prossgress = QProgressBar()
        self.prossgress.setRange(0,100)
    
    def create_layers(self):
        self.ui.main_layer.addWidget(self.table)
        self.ui.main_layer.addWidget(self.run_Btn)
        self.ui.main_layer.addWidget(self.prossgress)

    def connect_widget(self):
        self.mayaver_menu.triggered.connect(self.maya_cb_state)
        self.ui.proj_setting_menu.triggered.connect(self.open_setting_win)
        self.ui.updataMenu.triggered.connect(partial(self.refresh_menu))
        self.ui.filepath_Btn.clicked.connect(self.get_file_dialog)
        self.run_Btn.clicked.connect(self.batch_run_command)
        self.value_type_group.triggered.connect(self._current_fileItem)
    
    def maya_cb_state(self,action):
        self.maya_exe = action.data()
        # print ('{0}-{1}'.format(action.text(), action.isChecked()))
        for i, item in enumerate(self.mayaver_menu.actions()):
            if action.text() != item.text():
                item.setChecked(False)
    
    def open_setting_win(self):
        from script import render_setting

        self.setting_win = render_setting.Ui_MainWindow()
        self.setting_win.setStyleSheet(self.app_style)
        self.setting_win.setWindowModality(Qt.ApplicationModal)#弹出设置窗口时禁用主窗口操作
        self.setting_win.show()
        # 接收信号内容
        bool_info = self.setting_win._signal.connect(self._get_data)
        
        if bool_info:
            self.refresh_menu()
            return bool_info

    def get_file_dialog(self):

        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        
        if path:
            self.ui.filepath_Le.setText(path.replace("\\", "/"))
            self.get_maya_file(path)

    def get_maya_file(self,path):
        list_files = []
        for root, dirs, files in os.walk(path):
            for f in files:
                list_files.append(os.path.join(root, f).replace("\\", "/"))

        list_files = list(filter(self.file_filter, list_files))

        for i in range(len(list_files)):
            list_files[i] = [os.path.basename(list_files[i])[:-3],
                            list_files[i]]

        self.create_table_items(list_files)

    def create_table_items(self,list_files):

        for i in range(len(list_files)):
            item = list_files[i]
            row = self.table.rowCount()
            self.table.insertRow(row)
            # print (item)
            for j in range(len(item)):
                str_item = QTableWidgetItem(str(list_files[i][j]))
                self.table.setItem(row,j,str_item)

    def file_filter(self,file_name):
        mayaFilters = ['.ma','.MA']#'.ma','.mb','.MA','.MB'
        if file_name[-3:] in mayaFilters :
            return True
        else:
            return False

    def _get_data(self,parameter=False):

        return (parameter)

    def get_menuItem_name(self):
        file_array = []
        folder_file = {}
        menu_file_path = ("%s/ren_config" % proj_path)
        try:
            for files in (os.listdir(menu_file_path)):
                for f in os.listdir(os.path.join(menu_file_path,files)):
                    filepath_temp = [f,os.path.join(menu_file_path,files,f).replace("\\","/")]
                    file_array.append(filepath_temp)
                folder_file[files] = file_array
                file_array = []
        except:
            folder_file = {}

        return folder_file

    def get_current_menuItem_objname(self):
        menuItem_names = []
        listMenu = self.findChildren(QMenu)
        pattern = "_menuItem"
        for i in listMenu:
            if re.search(pattern,i.objectName()):
                menuItem_names.append(i.objectName())
        return menuItem_names

    def get_current_qaction_objname(self):
        qaction_data = []
        list_qactions = self.value_type_group.actions()
        for i in list_qactions:
            qaction_data.append(i.data())
        return qaction_data
        
    def get_config_all_json_file(self):
        qaction_arrys = []
        suffix = 'json'
        paths = os.walk(("%s/ren_config" % proj_path))
        for root,dirs,files in paths:
            for f in files:
                if suffix in f:
                    qaction_arrys.append(os.path.join(root,f).replace("\\","/"))#带路径的文件名
        return qaction_arrys
        
    def refresh_menu(self):

        all_menu_name = []
        current_menuItem = self.get_current_menuItem_objname()
        all_menu_names = self.get_menuItem_name()
        for key,value in all_menu_names.items():
            all_menu_name.append(key)
        result_menu_name = ['{}_menuItem'.format(a) for a in all_menu_name]
        new_menuItems = list(set(result_menu_name) - set(current_menuItem))

        for name in range(len(new_menuItems)):
            menu_name = QMenu(new_menuItems[name][:-9],self)
            menu_name.setObjectName(new_menuItems[name])
            menu_name.setContextMenuPolicy(Qt.CustomContextMenu)
            menu_name.customContextMenuRequested.connect(partial(self.json_menu_rightItem,new_menuItems[name]))
            file_values = new_menuItems[name][:-9]
            for action in all_menu_names[file_values]:
                qaction_item = QAction(action[0],self)
                qaction_item.setCheckable(True)
                qaction_item.setActionGroup(self.value_type_group)
                qaction_item.setData(action[1])
                menu_name.addAction(qaction_item)
            self.ui.proj_menu.addMenu(menu_name)

        all_qactions = self.get_config_all_json_file()
        get_qactions = self.get_current_qaction_objname()
        actions = (list(set(all_qactions) - set(get_qactions)))
        for ac_item in actions:
            ac_file = os.path.split(ac_item)[1]
            up_file_name = os.path.basename(os.path.dirname(os.path.realpath(ac_item)))
            file_menu_name = '{}_menuItem'.format(up_file_name)
            qaction_item = QAction(ac_file,self)
            qaction_item.setCheckable(True)
            qaction_item.setActionGroup(self.value_type_group)
            qaction_item.setData(ac_item)
            parent_menu = self.findChild(QMenu,file_menu_name)
            parent_menu.addAction(qaction_item)

    def json_menu_rightItem(self,objname,pointPos):
        try:
            self.del_menu = QMenu(self)
            self.del_menu.setObjectName('delete_menuItem')
            self.del_action = self.del_menu.addAction(u'删除')
            self.del_action.triggered.connect(lambda :self.delete_menu(objname))
            self.del_menu.popup(QCursor().pos())
        except Exception as e:
            print (e)

    def _current_fileItem(self,action):
        self.json_path = action.data()

        for i, item in enumerate(self.value_type_group.actions()):
            if action.text() != item.text():
                item.setChecked(False)

    def delete_menu(self,objname):
        current_item = self.findChild(QMenu,objname)
        item_folder_path = "{0}/{1}".format(("%s/ren_config" % proj_path),current_item.title())
        if os.path.isdir(item_folder_path): 
            shutil.rmtree(item_folder_path)
            current_item.deleteLater()
        else:
            pass

    def ma_alter(self,mayafile,old_str,new_str):
    
        with io.open(mayafile, "r", encoding="utf-8") as f1,io.open("%s.bak" % mayafile, "w", encoding="utf-8") as f2:
            for line in f1:
                f2.write(re.sub(old_str,new_str,line))
        os.remove(mayafile)
        os.rename("%s.bak" % mayafile, mayafile)
        # ma_alter(r"Z:\Project\ScriptProjs\XYY\renderparbackruntools\config\test1.ma", "1920", "200")

    def get_all_items(self):
        items = []
        for row in range(self.table.rowCount()):
            itemsCount = []
            for col in range(self.table.columnCount()):
                if self.table.item(row,col).text() != None: 
                    itemsCount.append(self.table.item(row,col).text())
            
            items.append(itemsCount)
        return items
    
    def get_all_item_files(self):
        all_items = self.get_all_items()
        item_file = []
        for item in all_items:
            item_file.append(item[1])
        return item_file

    def write_ma_file(self,file_path,fileContent=None):
        with io.open(file_path, 'r+',newline='',encoding='utf-8') as f:
            f.read()
            f.seek(0, 2)
            f.write(fileContent.decode('utf-8')) 

    def batch_run_command(self):
        all_items = self.get_all_item_files()
        contents = content(self.json_path)
        step = 0
        step_val = 100 /(len(all_items))
        if self.json_path and self.maya_exe:
            # print (self.json_path)
            # print (self.maya_exe)
            # print (all_items)
            
            for item in range(len(all_items)):
                self.write_ma_file(all_items[item],contents)
                step += step_val
                self.prossgress.setValue(step)
        
            self.prossgress.setValue(100)
            QMessageBox.question(self, '提示',
                "操作已完成",
                QMessageBox.Yes)

        else:
            QMessageBox.question(self, '提示',
                    "没有选择maya版本或执行脚本?",
                    QMessageBox.Yes)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示',
                    "是否要关闭所有窗口?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)   # 退出程序
        else:
            event.ignore()

if __name__ == '__main__':
    from PySide2.QtGui import QIcon
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("%s\icon\huitailang.png"%proj_path))
    stats = MainWindow()
    stats.show()

    sys.exit(app.exec_())
