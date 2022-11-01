#!/usr/bin/env python
# coding=utf-8
'''
Author        : zhenghaoming
Date          : 2022-10-26 23:41:20
FilePath      : \script\render_setting.py
version       : 
LastEditors   : zhenghaoming
LastEditTime  : 2022-11-01 09:01:19
'''
import sys,os,json
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
 

class RENDER_SETTING_CUSTOM_PRESET(object):

    WINDOW_TITLE = u"参数设置"

    RENDERER_TITLE = ['Arnold','Redshift']

    RENDER_QUALITY_TITLE = ['LowSetting','HighSetting']

    RENDER_SIZE_TITLE = [["Width","widthObjName",'width'],["High","highObjName",'height']]

    RENDER_SIZE_VALUE = ["960","540"]

    ARNOLD_SAMPLE = [['  Camera(AA)','camera_aaObjName','AASamples'],
                    ['     Diffuse','diffuseObjName','GIDiffuseSamples'],
                    ['    Specular','specularObjName','GISpecularSamples'],
                    ['Transmission','transmissionObjName','GITransmissionSamples'],
                    ['         SSS','sssObjName','GIVolumeSamples']]
    
    ARNOLD_SAMPLE_DEFAULT_VALUE = ['3','2','2','2','2']

    REDSHIFT_UNIFIEDSAMPLE = [['Min Sample','minsample','unifiedMinSamples'],['Max Sample','maxsample','unifiedMaxSamples']]

    REDSHIFT_UNIFIEDSAMPLE_VALUE = ['4','16']

    REDSHIFT_SAMPLING_OVERRIDES = [['Reflection','reflection','reflectionSamplesOverride'],
                                    ['Refraction','refraction','refractionSamplesOverride'],
                                    ['AO','ao','AOSamplesOverride'],
                                    ['Light','light','lightSamplesOverride'],
                                    ['Volume','volume','volumeSamplesOverride'],
                                    ['Single Scattering','single_scatter','singleScatteringSamplesOverride'],
                                    ['Sub-Surface Multiple Scattering','ss_multi_scatter','multipleScatteringSamplesOverride']]

    REDSHIFT_SAMPLING_OVERRIDES_VALUE = '64'

class CMB_PARAMETER_KIT(QWidget):
    def __init__(self,label_name,object_name,attr_name,value,parent=None):
        super(CMB_PARAMETER_KIT,self).__init__(parent)
        
        self.label_name = label_name
        self.object_name = object_name
        self.attr_name = attr_name
        self.value = value

        self.create_widgets()
        self.create_layouts()
        self.create_connects()

    def create_widgets(self):
        self.cb = QCheckBox(format(self.label_name,'<31'))
        self.cb.setObjectName("%s_cmb" % self.object_name)
        self.cb.setStatusTip("%sEnable" % self.attr_name)
        self.cb.setToolTip("%sEnable" % self.attr_name)
        self.tx = QLineEdit()
        self.tx.setEnabled(False)
        self.tx.setText(self.value)
        self.tx.setObjectName("%s_le" % self.object_name)
        self.tx.setStatusTip("%sReplace" % self.attr_name)
        self.tx.setToolTip("%sReplace" % self.attr_name)
    
    def create_layouts(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.cb)
        self.layout.addWidget(self.tx)

    def create_connects(self):
        self.cb.toggled.connect(self.tx.setEnabled)
        
class PARAMETER_KIT(QWidget):

    def __init__(self,label_name,object_name,atrr_name,value,parent=None):
        super(PARAMETER_KIT,self).__init__(parent)
        
        self.label_name = label_name
        self.object_name = object_name
        self.atrr_name = atrr_name
        self.value = value

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        self.label = QLabel(self.label_name)
        self.tx = QLineEdit()
        self.tx.setText(self.value)
        self.tx.setObjectName(self.object_name)
        self.tx.setStatusTip(self.atrr_name)
        self.tx.setToolTip(self.atrr_name)
    
    def create_layouts(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tx)

class Rs_Widget(QWidget):

    def __init__(self,parent=None):
        super(Rs_Widget,self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
    
    def create_widgets(self):
        self.quality_mode_label = QLabel(u'质量模式切换')
        quality_mode_label_sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        quality_mode_label_sizePolicy.setHorizontalStretch(0)
        quality_mode_label_sizePolicy.setVerticalStretch(0)
        quality_mode_label_sizePolicy.setHeightForWidth(self.quality_mode_label.sizePolicy().hasHeightForWidth())
        self.quality_mode_label.setSizePolicy(quality_mode_label_sizePolicy)

        self.quality_mode_CMB = QComboBox()
        self.quality_mode_CMB.setObjectName("qualityModeCMB")
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.quality_mode_CMB.addItems(RENDER_SETTING_CUSTOM_PRESET.RENDER_QUALITY_TITLE)

        render_title = RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_TITLE
        render_size_value = RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_VALUE
        self.rs_ren_w = PARAMETER_KIT(render_title[0][0],render_title[0][1],render_title[0][2],render_size_value[0])
        self.rs_ren_h = PARAMETER_KIT(render_title[1][0],render_title[1][1],render_title[1][2],render_size_value[1])

        self.aovs_changle_cb = QCheckBox(u'是否激活应用Aovs')
        self.aovs_changle_cb.setObjectName("aovs_cb")
        self.spacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ren_size_GB = QGroupBox(u'Render Size')
        self.unifiedsample_GB = QGroupBox(u'Unified Sampleling')
        self.sampling_overrides_GB = QGroupBox(u'Sampling Overrides')
        self.aovs_GB = QGroupBox(u'Aovs')

    def create_layouts(self):
        self.quality_mode_layout = QHBoxLayout()
        self.quality_mode_layout.addWidget(self.quality_mode_label)
        self.quality_mode_layout.addWidget(self.quality_mode_CMB)
        self.quality_mode_layout.addItem(self.spacer1)

        self.ren_size_GB_layout = QHBoxLayout(self.ren_size_GB)
        self.ren_size_GB_layout.addLayout(self.rs_ren_w.layout)
        self.ren_size_GB_layout.addLayout(self.rs_ren_h.layout)

        self.unifiedsample_GB_layout = QVBoxLayout(self.unifiedsample_GB)
        unifiedsample = RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_UNIFIEDSAMPLE
        unifiedsampleValue = RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_UNIFIEDSAMPLE_VALUE
        for sample in range(len(unifiedsample)):
            sample_control = PARAMETER_KIT(unifiedsample[sample][0],
                                            unifiedsample[sample][1],
                                            unifiedsample[sample][2],
                                            unifiedsampleValue[sample])
            self.unifiedsample_GB_layout.addLayout(sample_control.layout)


        self.sampling_overrides_GB_layout = QVBoxLayout(self.sampling_overrides_GB)
        samplingOverrides = RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_SAMPLING_OVERRIDES
        for sample in range(len(samplingOverrides)):
            rs_sample_control = CMB_PARAMETER_KIT(samplingOverrides[sample][0],
                                                    samplingOverrides[sample][1],
                                                    samplingOverrides[sample][2],
                                                    RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_SAMPLING_OVERRIDES_VALUE)
            self.sampling_overrides_GB_layout.addLayout(rs_sample_control.layout)

        self.aovs_GB_layout = QVBoxLayout(self.aovs_GB)
        self.aovs_GB_layout.addWidget(self.aovs_changle_cb)

        self.rs_low_lay = QVBoxLayout()
        self.rs_low_lay.addLayout(self.quality_mode_layout)
        self.rs_low_lay.addWidget(self.ren_size_GB)
        self.rs_low_lay.addWidget(self.unifiedsample_GB)
        self.rs_low_lay.addWidget(self.sampling_overrides_GB)
        self.rs_low_lay.addWidget(self.aovs_GB)
        self.rs_low_lay.addItem(self.spacer2)

class Ar_Widget(QWidget):

    def __init__(self,parent=None):
        super(Ar_Widget,self).__init__(parent)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):

        self.quality_mode_label = QLabel(u'质量模式切换')
        quality_mode_label_sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        quality_mode_label_sizePolicy.setHorizontalStretch(0)
        quality_mode_label_sizePolicy.setVerticalStretch(0)
        quality_mode_label_sizePolicy.setHeightForWidth(self.quality_mode_label.sizePolicy().hasHeightForWidth())
        self.quality_mode_label.setSizePolicy(quality_mode_label_sizePolicy)

        self.quality_mode_CMB = QComboBox()
        self.quality_mode_CMB.setObjectName("qualityModeCMB")
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.quality_mode_CMB.addItems(RENDER_SETTING_CUSTOM_PRESET.RENDER_QUALITY_TITLE)

        render_title = RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_TITLE
        render_size_value = RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_VALUE
        self.ar_ren_w = PARAMETER_KIT(render_title[0][0],render_title[0][1],render_title[0][2],render_size_value[0])
        self.ar_ren_h = PARAMETER_KIT(render_title[1][0],render_title[1][1],render_title[1][2],render_size_value[1])

        self.aovs_changle_cb = QCheckBox(u'是否激活应用Aovs')
        self.aovs_changle_cb.setObjectName("aovs_cb")
        self.spacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.ren_size_GB = QGroupBox(u'Render Size')
        self.sample_GB = QGroupBox(u'Sample')
        self.aovs_GB = QGroupBox(u'Aovs')

    def create_layouts(self):

        self.quality_mode_layout = QHBoxLayout()
        self.quality_mode_layout.addWidget(self.quality_mode_label)
        self.quality_mode_layout.addWidget(self.quality_mode_CMB)
        self.quality_mode_layout.addItem(self.spacer1)

        self.ren_size_GB_layout = QHBoxLayout(self.ren_size_GB)
        self.ren_size_GB_layout.addLayout(self.ar_ren_w.layout)
        self.ren_size_GB_layout.addLayout(self.ar_ren_h.layout)

        self.sample_GB_layout = QVBoxLayout(self.sample_GB)
        
        ar_sample = RENDER_SETTING_CUSTOM_PRESET.ARNOLD_SAMPLE
        ar_sampleValue = RENDER_SETTING_CUSTOM_PRESET.ARNOLD_SAMPLE_DEFAULT_VALUE
        for sample in range(len(ar_sample)):
            sample_control = PARAMETER_KIT(ar_sample[sample][0],
                                            ar_sample[sample][1],
                                            ar_sample[sample][2],
                                            ar_sampleValue[sample])
            self.sample_GB_layout.addLayout(sample_control.layout)

        self.aovs_GB_layout = QVBoxLayout(self.aovs_GB)
        self.aovs_GB_layout.addWidget(self.aovs_changle_cb)

        self.ar_low_lay = QVBoxLayout()
        self.ar_low_lay.addLayout(self.quality_mode_layout)
        self.ar_low_lay.addWidget(self.ren_size_GB)
        self.ar_low_lay.addWidget(self.sample_GB)
        self.ar_low_lay.addWidget(self.aovs_GB)
        self.ar_low_lay.addItem(self.spacer2)

class Ui_MainWindow(QWidget):
    # 建立信号，str 是字符类型，int整书类型，list列表类型
    _signal = Signal(bool)

    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent)
        # self.setupUi(self)

        self.ren_data = {}

        self.setWindowTitle(RENDER_SETTING_CUSTOM_PRESET.WINDOW_TITLE)
        self.resize(400,700)
    
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.fileName_label = QLabel(u"File Name: ")
        self.fileName_tx = QLineEdit()
        self.fileName_tx.setPlaceholderText(u'填写项目名字，如已存在会自动覆盖')

        self.create_btn = QPushButton(u'确认')
        self.create_btn.setFixedHeight(30)

    def create_layouts(self):
        
        ar_mode_tab_widget = Ar_Widget()
        rs_mode_tab_widget = Rs_Widget()

        filename_layout = QHBoxLayout()
        filename_layout.addWidget(self.fileName_label)
        filename_layout.addWidget(self.fileName_tx)

        self.ar_tab_widget = QWidget()
        self.rs_tab_widget = QWidget()
        self.ar_rs_ren_tab_widget = QTabWidget()
        self.ar_rs_ren_tab_widget.addTab(self.ar_tab_widget,RENDER_SETTING_CUSTOM_PRESET.RENDERER_TITLE[0])
        self.ar_rs_ren_tab_widget.addTab(self.rs_tab_widget,RENDER_SETTING_CUSTOM_PRESET.RENDERER_TITLE[1])
        
        ar_tab_lay = QVBoxLayout(self.ar_tab_widget)
        ar_tab_lay.addLayout(ar_mode_tab_widget.ar_low_lay)

        rs_tab_lay = QVBoxLayout(self.rs_tab_widget)
        rs_tab_lay.addLayout(rs_mode_tab_widget.rs_low_lay)      

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(2)
        main_layout.addLayout(filename_layout)
        main_layout.addWidget(self.ar_rs_ren_tab_widget)
        main_layout.addWidget(self.create_btn)

    def create_connections(self):
        # pass
        self.create_btn.clicked.connect(self.create_setting_json)
        
    def create_setting_json(self):

        tab_index =  (self.ar_rs_ren_tab_widget.currentIndex())

        if tab_index == 0:
            dict_data = self.ar_get_data()
            file_name = self.ar_tab_widget.findChild(QComboBox,"qualityModeCMB").currentText()
        elif tab_index == 1:
            dict_data = self.rs_get_data()
            file_name = self.rs_tab_widget.findChild(QComboBox,"qualityModeCMB").currentText()

        if not self.fileName_tx.text():
            QMessageBox.question(self, '提示',
                    "输入项目名字",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        else:
            json_file = self.json_file(file_name,self.fileName_tx.text())

        if self.get_file_exits(json_file):
            os.remove(json_file)
        
        if self.fileName_tx.text() and self.writeJson(json_file,dict_data):
            single_Slot = True
        else:
            single_Slot = False

        # 发射型号
        self._signal.emit(single_Slot)
        self.close()

    def ar_get_data(self):
        '''
        setAttr "defaultArnoldRenderOptions.AASamples" 1;
        setAttr "defaultArnoldRenderOptions.GIDiffuseSamples" 1;
        setAttr "defaultArnoldRenderOptions.GISpecularSamples" 1;
        setAttr "defaultArnoldRenderOptions.GITransmissionSamples" 1;
        setAttr "defaultArnoldRenderOptions.GISssSamples" 1;
        setAttr "defaultArnoldRenderOptions.GIVolumeSamples" 1;
        ''' 
        renSizeData = []
        renParData = []
        for label,name,value in RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_TITLE:
            attri_value = (self.ar_tab_widget.findChild(QLineEdit,name).text())
            attri_name = (self.ar_tab_widget.findChild(QLineEdit,name).statusTip())
            renData = [attri_name,attri_value]
            renSizeData.append(renData)

        self.ren_data["size"] = renSizeData

        for label,objectname,attri in RENDER_SETTING_CUSTOM_PRESET.ARNOLD_SAMPLE:
            attri_value = (self.ar_tab_widget.findChild(QLineEdit,objectname).text())
            attri_name = (self.ar_tab_widget.findChild(QLineEdit,objectname).statusTip())
            renData = [attri_name,attri_value]
            renParData.append(renData)

        self.ren_data["Sample"] = renParData

        aov_value = str(0)
        if self.ar_tab_widget.findChild(QCheckBox,"aovs_cb").isChecked():
            aov_value = str(1)
        self.ren_data["Aovs"] = ["aovMode",aov_value]
        self.ren_data["Arnold"] = ["aiOptions","defaultArnoldRenderOptions"]

        return (self.ren_data)
    
    def rs_get_data(self):
        '''
        setAttr "redshiftOptions.reflectionSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.reflectionSamplesOverrideReplace" 98;
        setAttr "redshiftOptions.refractionSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.refractionSamplesOverrideReplace" 65;
        setAttr "redshiftOptions.AOSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.AOSamplesOverrideReplace" 95;
        setAttr "redshiftOptions.lightSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.lightSamplesOverrideReplace" 91;
        setAttr "redshiftOptions.volumeSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.volumeSamplesOverrideReplace" 76.8;
        setAttr "redshiftOptions.singleScatteringSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.singleScatteringSamplesOverrideReplace" 135;
        setAttr "redshiftOptions.multipleScatteringSamplesOverrideEnable" 1;
        setAttr "redshiftOptions.multipleScatteringSamplesOverrideReplace" 102;
        '''
        renSizeData = []
        renSampleData = []
        renSampleOverrideData = []
        for label,name,value in RENDER_SETTING_CUSTOM_PRESET.RENDER_SIZE_TITLE:
            attri_value = (self.rs_tab_widget.findChild(QLineEdit,name).text())
            attri_name = (self.rs_tab_widget.findChild(QLineEdit,name).statusTip())
            renData = [attri_name,attri_value]
            renSizeData.append(renData)

        self.ren_data["size"] = renSizeData

        for label,objectname,attri in RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_UNIFIEDSAMPLE:
            attri_value = (self.rs_tab_widget.findChild(QLineEdit,objectname).text())
            attri_name = (self.rs_tab_widget.findChild(QLineEdit,objectname).statusTip())
            renData = [attri_name,attri_value]
            renSampleData.append(renData)
        self.ren_data["UnifiedSample"] = renSampleData

        for label,objectname,attri in RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_SAMPLING_OVERRIDES:
            _value = str(0)
            if (self.rs_tab_widget.findChild(QCheckBox,("%s_cmb"%objectname)).isChecked()):
                _value = str(1)
            attri_name = (self.rs_tab_widget.findChild(QCheckBox,("%s_cmb"%objectname)).statusTip())
            renData = [attri_name,_value]
            renSampleOverrideData.append(renData)
        
        for label,objectname,attri in RENDER_SETTING_CUSTOM_PRESET.REDSHIFT_SAMPLING_OVERRIDES:
            attri_value = (self.rs_tab_widget.findChild(QLineEdit,("%s_le"%objectname)).text())
            attri_name = (self.rs_tab_widget.findChild(QLineEdit,("%s_le"%objectname)).statusTip())
            renData = [attri_name,attri_value]
            renSampleOverrideData.append(renData)

        self.ren_data["SampleOverride"] = renSampleOverrideData

        aov_value = str(0)
        if self.rs_tab_widget.findChild(QCheckBox,"aovs_cb").isChecked():
            aov_value = str(1)
        self.ren_data["Aovs"] = ["aovGlobalEnableMode",aov_value]
        self.ren_data["Redshift"] = ["RedshiftOptions","redshiftOptions"]

        return (self.ren_data)

    def json_file(self,file_name,proj_name=None):
        if proj_name is not None:
            json_path = "%s/ren_config/%s/%s.json" % (os.path.abspath('.').replace("\\","/"),proj_name,file_name)
    
        return json_path

    def get_file_exits(self,json_file):
        
        if not os.path.isdir(os.path.split(json_file)[0]):
            os.makedirs(os.path.split(json_file)[0])
        return os.path.exists(json_file)

    def writeJson(self,path=None,data={}):
        '''
        @给json文件写入数据
        '''
        if not path:
            return False
        else:
            with open(path,'w') as f:
                json.dump(data,f,indent=4,ensure_ascii=False,sort_keys=True)

            return True

if __name__ == '__main__':
    app = QApplication([])
    stats = Ui_MainWindow()
    stats.show()

    sys.exit(app.exec_())