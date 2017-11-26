"""Module QApplicationWindow

RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
http://blogs.upm.es/compsoftmatter/software/reptate/
https://github.com/jorge-ramirez-upm/RepTate
http://reptate.readthedocs.io
Jorge Ramirez, jorge.ramirez@upm.es
Victor Boudara, mmvahb@leeds.ac.uk

Module that defines the basic GUI class from which all GUI applications are derived.
It is the GUI counterpart of Application.

Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
This software is distributed under the GNU General Public License. 
""" 
import sys
import os
import logging
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import seaborn as sns   
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
import itertools
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QHeaderView, QColorDialog, QDialog
from QDataSet import *
from SubQTreeWidgetItem import *
from DataSet import ColorMode, SymbolMode
from Application import *
from DraggableArtists import *

#To recompile the symbol-settings dialog:
#pyuic5 gui/markerSettings.ui -o gui/markerSettings.py
from markerSettings import *


from SubQTableWidget import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
path = os.path.dirname(os.path.abspath(__file__))
Ui_AppWindow, QMainWindow = loadUiType(os.path.join(path,'QApplicationWindow.ui'))

class QApplicationWindow(Application, QMainWindow, Ui_AppWindow):
    def __init__(self, name='Application Template', parent=None):
        super().__init__(name, parent)

        if CmdBase.mode!=CmdMode.GUI:
            return None
        
        QMainWindow.__init__(self)
        Ui_AppWindow.__init__(self)
        
        self.setupUi(self)
        self.logger = logging.getLogger('ReptateLogger')
        self.name = name
        self.parent_application = parent
        self.canvas = 0
        self.tab_count = 0
        self.curves = []
        self.zorder = 100
        #self.views={} # we use 'views' of Application.py
       
        # Accept Drag and drop events
        self.setAcceptDrops(True)

        # DataSet Tabs behaviour ##########
        self.DataSettabWidget.setTabsClosable(True)
        self.DataSettabWidget.setUsesScrollButtons(True)
        self.DataSettabWidget.setMovable(True)
        
        ################
        # SETUP TOOLBARS
        # Data Inspector Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionCopy)
        tb.addAction(self.actionPaste)
        tb.addAction(self.actionShiftVertically)
        tb.addAction(self.actionShiftHorizontally)
        self.LayoutDataInspector.insertWidget(0, tb)
        #custom QTable to have the copy/pastefeature
        self.tableWidget = SubQTableWidget(self)
        self.LayoutDataInspector.insertWidget(-1, self.tableWidget)

        # Dataset Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionNew_Empty_Dataset)
        tb.addAction(self.actionNew_Dataset_From_File)
        tb.addAction(self.actionView_All_Sets)
        tb.addAction(self.actionMarkerSettings)
        tb.addAction(self.actionReload_Data)
        tb.addAction(self.actionInspect_Data)
        tb.addAction(self.actionShowFigureTools)
        self.ViewDataTheoryLayout.insertWidget(1, tb)
        self.ViewDataTheorydockWidget.Width=500
        self.ViewDataTheorydockWidget.setTitleBarWidget(QWidget())                

        # Tests TableWidget
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(['x','y','z','a','b','c','d','e','f','g'])

        # Hide Data Inspector
        self.DataInspectordockWidget.hide()

        # PLOT Style
        # sns.set_style("white")
        # sns.set_style("ticks")
        # #plt.style.use('seaborn-talk')
        # #plt.style.use('seaborn-paper')
        # plt.style.use('seaborn-poster')
        # self.figure=plt.figure()
        # self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()
        self.mplvl.addWidget(self.canvas)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        self.mpl_toolbar.setIconSize(QSize(16, 16))
        self.mpl_toolbar.setFixedHeight(36)
        self.mpl_toolbar.layout().setSpacing(0)
        self.mpl_toolbar.addAction(self.actionTrack_data)
        self.mpl_toolbar.setVisible(False)
        self.mplvl.addWidget(self.mpl_toolbar)

                
        # self.canvas.draw()
        # self.update_Qplot()
        # sns.despine() # Remove up and right side of plot box
        # LEGEND STUFF
        # leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        # if leg:
        #     leg.draggable()
                

        # EVENT HANDLING
        #connection_id = self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        #connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)   
        connection_id = self.actionShowFigureTools.triggered.connect(self.viewMPLToolbar)
        connection_id = self.actionInspect_Data.triggered.connect(self.showDataInspector)
        connection_id = self.actionNew_Empty_Dataset.triggered.connect(self.createNew_Empty_Dataset)
        connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.openDataset)
        connection_id = self.actionReload_Data.triggered.connect(self.handle_actionReload_Data)

        connection_id = self.viewComboBox.currentIndexChanged.connect(self.change_view)

        connection_id = self.DataSettabWidget.tabCloseRequested.connect(self.close_data_tab_handler)
        connection_id = self.DataSettabWidget.tabBarDoubleClicked.connect(self.handle_doubleClickTab)
        connection_id = self.DataSettabWidget.currentChanged.connect(self.handle_currentChanged)
        connection_id = self.actionView_All_Sets.toggled.connect(self.handle_actionView_All_Sets)
        connection_id = self.actionShiftVertically.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.actionShiftHorizontally.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.DataInspectordockWidget.visibilityChanged.connect(self.handle_inspectorVisibilityChanged)
        
        connection_id = self.actionMarkerSettings.triggered.connect(self.handle_actionMarkerSettings)
        
        connection_id = self.actionCopy.triggered.connect(self.tableWidget.copy)
        connection_id = self.actionPaste.triggered.connect(self.tableWidget.paste)


        # Annotation stuff
        connection_id = self.actionTrack_data.triggered.connect(self.handle_annotation)
        plt.connect('motion_notify_event', self.mpl_motion_event)

        #Setting up the marker-settings dialog
        # self.marker_dic = {'square': 's', 'plus (filled)': 'P', 'point': '.', 'triangle_right': '>', 'hline': '_', 'vline': '|', 'pentagon': 'p', 'tri_left': '3', 'tri_up': '2', 'circle': 'o', 'diamond': 'D', 'star': '*', 'hexagon1': 'h', 'octagon': '8', 'hexagon2': 'H', 'tri_right': '4', 'x (filled)': 'X', 'thin_diamond': 'd', 'tri_down': '1', 'triangle_left': '<', 'plus': '+', 'triangle_down': 'v', 'triangle_up': '^', 'x': 'x'}
        self.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.populate_cbSymbolType()
        self.populate_cbPalette()
        self.color1 = None
        self.color2 = None
        # self.populate_markers() 
        self.fparam_backup = [] #temporary storage of the file parameters
        self.dialog.ui.spinBox.setSingleStep(3) #increment in the marker size dialog
        connection_id = self.dialog.ui.pickColor1.clicked.connect(self.handle_pickColor1)
        connection_id = self.dialog.ui.pickColor2.clicked.connect(self.handle_pickColor2)
        connection_id = self.dialog.ui.rbEmpty.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.rbFilled.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.pushApply.clicked.connect(self.handle_apply_button_pressed)


        self.dataset_actions_disabled(True)

        # connection_id = self.checkBoxColor.toggled.connect(self)
        # TEST GET CLICKABLE OBJECTS ON THE X AXIS
        #xaxis = self.ax.get_xticklabels()
        #print (xaxis)  


    def dataset_actions_disabled(self, state):
        """Disable buttons when there is no file in the dataset"""
        self.actionMarkerSettings.setDisabled(state)
        self.viewComboBox.setDisabled(state)
        self.actionReload_Data.setDisabled(state)
        self.actionInspect_Data.setDisabled(state)
        self.actionShowFigureTools.setDisabled(state)
        self.actionView_All_Sets.setDisabled(state)

        ds = self.DataSettabWidget.currentWidget()
        if ds:
            ds.actionNew_Theory.setDisabled(state)
            ds.cbtheory.setDisabled(state)

    def mpl_motion_event(self, event):
        if not self.handle_annotation.checked:
            return
        # Code to draw annotation. It doesn't work!
        
    def handle_annotation(self, checked):
        if (checked):
            """Draw and hide the annotation box."""
            self.annotation = self.ax.annotate(
                '', xy=(0, 0), ha = 'left',
                xytext = (-40, 40), textcoords = 'offset points', va = 'center',
                bbox = dict(
                    boxstyle='roundtooth,pad=0.3', fc='yellow', alpha=0.20),
                arrowprops = dict(
                    arrowstyle="-|>", connectionstyle="arc3,rad=-0.2")
                )
            self.canvas.draw()
        else:
            self.annotation.remove()
            self.canvas.draw()

    def populate_cbPalette(self):
        """Populate the list color palettes of the marker-settings dialog"""
        for palette in sorted(ColorMode.colorpalettes.value):
            self.dialog.ui.cbPalette.addItem(palette)

    def populate_cbSymbolType(self):
        """Populate the list of the markers of the marker-settings dialog
        with filled or empty markers, depending on the user's choice"""
        self.dialog.ui.cbSymbolType.clear()
        if self.dialog.ui.rbFilled.isChecked(): #combobox with fillable symbols only
            for m in SymbolMode.filledmarkernames.value:
                ipath = ':/Markers/Images/Matplotlib_markers/marker_%s.png'%m
                self.dialog.ui.cbSymbolType.addItem(QIcon(ipath), m)
        else: #combobox with all symbols only
            for m in SymbolMode.allmarkernames.value:
                ipath = ':/Markers/Images/Matplotlib_markers/marker_%s.png'%m
                self.dialog.ui.cbSymbolType.addItem(QIcon(ipath), m)
    
    def handle_pickColor1(self):
        """Call the colocr picker and save the selected color to `color1` in RGB format"""
        color = self.showColorDialog()
        if color: #check for none
            self.dialog.ui.labelPickedColor1.setStyleSheet("background: %s"%color.name())
            self.color1 = color.getRgbF()
            print("handle_pickColor1 ", self.color1)

    def handle_pickColor2(self):
        """Call the colocr picker and save the selected color to `color2` in 
        RGB format used for gradient color type"""
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelPickedColor2.setStyleSheet("background: %s"%color.name())
            self.color2 = color.getRgbF()

    def showColorDialog(self):
        """Show the color picker and return the picked QtColor or `None`"""
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            wtitle = "Select color for %s"%ds.name
            color = QColorDialog.getColor(title=wtitle, 
                options=QColorDialog.DontUseNativeDialog)
            if not color.isValid():
                color = None
            return color

    def handle_actionMarkerSettings(self):
        """Show the dialog box where the user can change
          the marker properties: size, shape, color, fill"""
        ds = self.DataSettabWidget.currentWidget()
        if not ds:
            return
        self.fparam_backup = []
        for file in ds.files:
            self.fparam_backup.append([file.color, file.marker, file.size, file.filled])

        #preset the colors in the labels
        col = QColor(ds.color1[0]*255, ds.color1[1]*255, ds.color1[2]*255)
        self.dialog.ui.labelPickedColor1.setStyleSheet("background: %s"%col.name())
        col = QColor(ds.color2[0]*255, ds.color2[1]*255, ds.color2[2]*255)
        self.dialog.ui.labelPickedColor2.setStyleSheet("background: %s"%col.name())
        #preset the spinbox
        self.dialog.ui.spinBox.setValue(ds.marker_size)
        self.dialog.ui.spinBoxLineW.setValue(ds.line_width)
        #preset radioButtons
            #symbols
        is_fixed = ds.symbolmode == SymbolMode.fixed
        self.dialog.ui.rbFixedSymbol.setChecked(is_fixed)
        # self.dialog.ui.rbVariableSymbol.setChecked(not is_fixed)
        self.dialog.ui.cbSymbolType.setDisabled(not is_fixed)

            #colors
        # self.dialog.ui.rbFixedColor.setChecked(False)
        # self.dialog.ui.rbGradientColor.setChecked(False)
        # self.dialog.ui.rbPalette.setChecked(False)
        if ds.colormode == ColorMode.fixed:
            self.dialog.ui.rbFixedColor.setChecked(True)
        elif ds.colormode == ColorMode.gradient:
            self.dialog.ui.rbGradientColor.setChecked(True)
        else:
            self.dialog.ui.rbPalette.setChecked(True)
        
        success = self.dialog.exec_() #this blocks the rest of the app as opposed to .show()
        if success == 1:
            self.handle_apply_button_pressed()
        else:
            ds.do_plot()

    def handle_apply_button_pressed(self):
        """Apply the selected marker properties to all the files in the current dataset"""
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            # #restore the file attributes to previous values before making changes
            # for i, file in enumerate(ds.files):
            #     file.color, file.marker, file.size, file.filled = self.fparam_backup[i]
            
            #find the color mode
            if self.dialog.ui.rbFixedColor.isChecked(): #fixed color?
                ds.colormode = ColorMode.fixed
                ds.color1 = self.color1 if self.color1 else ColorMode.color1.value
            elif self.dialog.ui.rbPalette.isChecked(): #color from palette?
                ds.colormode = ColorMode.variable
                palette_name = self.dialog.ui.cbPalette.currentText()
                ds.palette = ColorMode.colorpalettes.value[palette_name]
            else: # color from gradient
                ds.colormode = ColorMode.gradient
                ds.color1 = self.color1 if self.color1 else ColorMode.color1.value
                ds.color2 = self.color2 if self.color2 else ColorMode.color2.value
            
            #find the shape mode
            if self.dialog.ui.rbVariableSymbol.isChecked(): #variable symbols?
                if self.dialog.ui.rbFilled.isChecked(): #filled?
                    ds.symbolmode = SymbolMode.variablefilled
                else: #empty
                    ds.symbolmode = SymbolMode.variable
            else: #single symbol
                ind = self.dialog.ui.cbSymbolType.currentIndex()
                if self.dialog.ui.rbFilled.isChecked(): #filled?
                    ds.symbolmode = SymbolMode.fixedfilled
                    ds.symbol1 = SymbolMode.filledmarkers.value[ind]
                    ds.symbol1_name = self.dialog.ui.cbSymbolType.currentText()
                else: #empty
                    ds.symbolmode = SymbolMode.fixed
                    ds.symbol1 = SymbolMode.allmarkers.value[ind]
                    ds.symbol1_name = self.dialog.ui.cbSymbolType.currentText()


            #get the marker size    
            ds.marker_size = self.dialog.ui.spinBox.value()
            #get the line width 
            ds.line_width = self.dialog.ui.spinBoxLineW.value()

            ds.do_plot()
            # ds.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a call to do_plot()
            ds.set_table_icons(ds.table_icon_list)
            # ds.DataSettreeWidget.blockSignals(False) 

    def handle_inspectorVisibilityChanged(self, visible):
        """Handle the hide/show event of the data inspector"""
        self.actionInspect_Data.setChecked(visible)
        if visible:
            ds = self.DataSettabWidget.currentWidget()
            if ds:
                ds.populate_inspector()           
        else:
            self.disconnect_curve_drag()
    
    def handle_actionShiftTriggered(self):
        """Allow the current 'selected_file' to be dragged"""
        ds = self.DataSettabWidget.currentWidget()
        if not ds.selected_file:
            return
        moveH = self.actionShiftHorizontally.isChecked()
        moveV = self.actionShiftVertically.isChecked()
        if moveH and moveV:
            mode = DragType.both
        elif moveH:
            mode = DragType.horizontal
        elif moveV:
            mode = DragType.vertical
        else:
            self.disconnect_curve_drag()
            return
        for curve in self.curves:
            curve.disconnect()
        self.curves.clear()
        for curve in ds.selected_file.data_table.series:
            cur = DraggableSeries(curve, mode, self.current_view.log_x, self.current_view.log_y)
            self.curves.append(cur)

    def disconnect_curve_drag(self):
        """Remove the Matplotlib drag connections
        and reset the shift buttons in the data inspector"""
        for curve in self.curves:
            curve.disconnect()
        self.curves.clear()
        self.actionShiftHorizontally.setChecked(False)
        self.actionShiftVertically.setChecked(False)
        
    def handle_actionReload_Data(self):
        """Reload the data files: remove and reopen the current files"""
        ds = self.DataSettabWidget.currentWidget()
        if not ds:
            return
        self.disconnect_curve_drag()
        paths_to_reopen, th_to_reopen= self.clear_files_and_th_from_dataset(ds)
        if paths_to_reopen:
            self.new_tables_from_files(paths_to_reopen)
        for th_name, tab_name in th_to_reopen:
            ds.new_theory(th_name, tab_name)

    def clear_files_and_th_from_dataset(self, ds):
        """Remove all files from dataset and widgetTree,
        return a list with the full path of deleted files"""
        file_paths_cleaned = []
        th_cleaned = []
        #save file names
        for file in ds.files:
            file_paths_cleaned.append(file.file_full_path)
        #remove lines from figure
        self.remove_ds_ax_lines(ds.name) 
        ds.set_no_limits(ds.current_theory) 
        #remove tables from ds
        ntable = ds.DataSettreeWidget.topLevelItemCount()
        for i in range(ntable):
            ds.DataSettreeWidget.takeTopLevelItem(0)
        #save theory tabs of ds
        ntabs = ds.TheorytabWidget.count()
        for i in range(ntabs):
            thname = ds.TheorytabWidget.widget(0).name.rstrip("0123456789")
            thtabname = ds.TheorytabWidget.tabText(0)
            th_cleaned.append((thname, thtabname))
            ds.TheorytabWidget.removeTab(0)
        
        ds.files.clear()
        ds.theories.clear()
        return file_paths_cleaned, th_cleaned

    def handle_actionView_All_Sets(self, checked):
        """Show all datasets simultaneously"""
        if len(self.datasets) < 2:
            return
        if checked:
            for ds in self.datasets.values():
                ds.Qshow_all()
                ds.highlight_series()
        else:
            #trigger a false change of tab to hide other dataset files from figure
            self.handle_currentChanged(self.DataSettabWidget.currentIndex())
        self.update_Qplot()

    def handle_currentChanged(self, index):
        """Change figure when the active DataSet tab is changed
        and empty the dataInspector"""
        if self.actionView_All_Sets.isChecked():
            return
        ds = self.DataSettabWidget.widget(index)
        if ds:
            disable_buttons = True if not ds.files else False
            self.dataset_actions_disabled(disable_buttons) # disable/activate buttons buttons
            ds.Qshow_all() #show all data of current dataset, except previously unticked files
            ntab = self.DataSettabWidget.count()
            for i in range(ntab): 
                if i!=index:
                    ds_to_hide = self.DataSettabWidget.widget(i) #hide files of all datasets except current one
                    ds_to_hide.do_hide_all()
                    ds_to_hide.set_no_limits(ds_to_hide.current_theory) 
            ds.highlight_series()
            ds.populate_inspector()
        else: # handle case where no dataset is left
            self.dataset_actions_disabled(True)
            self.tableWidget.setRowCount(0) #empty the inspector
            self.DataInspectordockWidget.setWindowTitle("File:")
        self.update_Qplot()

    def handle_doubleClickTab(self, index):
        """Edit DataSet-tab name"""
        old_name = self.DataSettabWidget.tabText(index)
        new_tab_name, success = QInputDialog.getText (
                self, "Change Name",
                "Insert New Tab Name",
                QLineEdit.Normal,
                old_name)
        if (success and new_tab_name!=""):    
            self.DataSettabWidget.setTabText(index, new_tab_name)

    def close_data_tab_handler(self, index):
        """Delete a dataset tab from the current application"""
        ds = self.DataSettabWidget.widget(index)
        if index == self.DataSettabWidget.currentIndex():
            self.disconnect_curve_drag()
            ds.set_no_limits(ds.current_theory) 
        self.delete(ds.name) #call Application.delete to delete DataSet
        self.DataSettabWidget.removeTab(index)

    def change_view(self):
        """Change plot view"""
        selected_view_name = self.viewComboBox.currentText()
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            ds.set_no_limits(ds.current_theory) 
        self.view_switch(selected_view_name) #view_switch of Application
        self.update_Qplot()
        self.disconnect_curve_drag()
        if ds:
            ds.highlight_series()
            
    def populate_views(self):
        """Assign availiable view labels to ComboBox"""
        selectedview = self.current_view.name
        for i in sorted(self.views):
            #add keys of 'views' dict to the list of views avaliable 
            self.viewComboBox.addItem(i) 
        index = self.viewComboBox.findText(selectedview, QtCore.Qt.MatchFixedString)
        self.viewComboBox.setCurrentIndex(index)

    def dragEnterEvent(self, e):      
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        reptatelogger = logging.getLogger('ReptateLogger')
        paths_to_open = []
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                paths_to_open.append(path)
        self.new_tables_from_files(paths_to_open)

    def update_Qplot(self):
        plt.tight_layout(pad=1.2)
        # self.canvas = FigureCanvas(self.figure)
        #self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def addTableToCurrentDataSet(self, dt, ext):
        """Add file table to curent dataset tab"""
        ds = self.DataSettabWidget.currentWidget()
        lnew = []
        for param in self.filetypes[ext].basic_file_parameters[:]:
            try:
                lnew.append(str(dt.file_parameters[param]))
            except KeyError as e:
                header = "Missing Parameter"
                message = "Parameter %s not found in file '%s'."%(e, dt.file_name_short)
                QMessageBox.warning(self, header, message)
                
        file_name_short = dt.file_name_short
        lnew.insert(0, file_name_short)
        newitem = SubQTreeWidgetItem(ds.DataSettreeWidget, lnew)
        newitem.setCheckState(0, 2)
        
        self.dataset_actions_disabled(False) #activate buttons
        
        
    def createNew_Empty_Dataset(self):
        """Add New empty tab to DataSettabWidget"""
        self.num_datasets += 1 #increment counter of Application
        num = self.num_datasets
        ds_name = 'Set%d'%num
        ds = QDataSet(name=ds_name, parent=self)
        self.datasets[ds_name] = ds
        ind = self.DataSettabWidget.addTab(ds, ds_name)

        #Set the new tab the active tab
        self.DataSettabWidget.setCurrentIndex(ind)
        #Define the tab column names (header)
        dfile = list(self.filetypes.values())[0] 
        dataset_header=dfile.basic_file_parameters[:]
        dataset_header.insert(0, "File")
        ds.DataSettreeWidget.setHeaderItem(QTreeWidgetItem(dataset_header))  
        ds.DataSettreeWidget.setSortingEnabled(True)

        hd=ds.DataSettreeWidget.header()
        hd.setSectionsClickable(True)
        w=ds.DataSettreeWidget.width()
        w/=hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            #hd.setTextAlignment(i, Qt.AlignHCenter)
        
        #Define the inspector column names (header)
        if num == 1:
            #inspect_header = dfile.col_names[:]
            inspect_header = [a+' [' + b + ']' for a,b in zip(dfile.col_names,dfile.col_units)]
            inspec_tab = self.tableWidget.setHorizontalHeaderLabels(inspect_header)


    def openDataset(self):
        # 'allowed_ext' defines the allowed file extensions
        # should be of form, e.g., "LVE (*.tts *.osc);;Text file (*.txt)"
        allowed_ext = ""
        for ftype in self.filetypes.values():
            allowed_ext += "%s (*%s);;" %(ftype.name, ftype.extension)
        allowed_ext = allowed_ext.rstrip(";")
        paths_to_open = self.openFileNamesDialog(allowed_ext)
        if not paths_to_open:
            return
        self.new_tables_from_files(paths_to_open)
        
    def new_tables_from_files(self, paths_to_open):
        if (self.DataSettabWidget.count()==0):
                self.createNew_Empty_Dataset()
        ds = self.DataSettabWidget.currentWidget()
        success, newtables, ext = ds.do_open(paths_to_open)
        self.check_no_param_missing(newtables, ext)
        if success==True:
            for dt in newtables:
                self.addTableToCurrentDataSet(dt, ext)
            ds.do_plot()
            self.update_Qplot()
            # ds.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a call to do_plot()
            ds.set_table_icons(ds.table_icon_list)
            # ds.DataSettreeWidget.blockSignals(False) 

        else:
            QMessageBox.about(self, "Open", success)
    
    def check_no_param_missing(self, newtables, ext):
        for dt in newtables:
            e_list = []
            for param in self.filetypes[ext].basic_file_parameters[:]:
                try:
                    temp = dt.file_parameters[param]
                except KeyError:
                    e_list.append(param)
            if len(e_list)>0:
                message = "Parameter(s) {%s} not found in file '%s'\n Value(s) set to 0"%(", ".join(e_list), dt.file_name_short)
                header = "Missing Parameter"
                QMessageBox.warning(self, header, message)
                for e_param in e_list:
                    dt.file_parameters[e_param] = "0"

    def openFileNamesDialog(self, ext_filter="All Files (*)"):  
        # file browser window  
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/"
        dilogue_name = "Open"
        selected_files, _ = QFileDialog.getOpenFileNames(self, dilogue_name, dir_start, ext_filter, options=options)
        return selected_files

    def showDataInspector(self, checked):
        if checked:
            self.DataInspectordockWidget.show()
        else:
            self.DataInspectordockWidget.hide()

    def viewMPLToolbar(self, checked):
        if checked:
            self.mpl_toolbar.show()
        else:
            self.mpl_toolbar.hide()
        
    def printPlot(self):
        fileName = QFileDialog.getSaveFileName(self,
            "Export plot", "", "Image (*.png);;PDF (*.pdf);; Postscript (*.ps);; EPS (*.eps);; Vector graphics (*.svg)");
        # TODO: Set DPI, FILETYPE, etc
        plt.savefig(fileName[0])
        
    def on_plot_hover(self, event):
        pass
        
    def onclick(self, event):
        if event.dblclick:
            pickedtick = event.artist
            print(event)
            print(pickedtick)

    def resizeplot(self, event=""):
        # TIGHT LAYOUT in order to view axes and everything
        plt.tight_layout(pad=1.2)


    # def No_Limits(self):
    #     self.actionShow_Limits.setIcon(self.actionNo_Limits.icon())

    # def Vertical_Limits(self):
    #     self.actionShow_Limits.setIcon(self.actionVertical_Limits.icon())

    # def Horizontal_Limits(self):
    #     self.actionShow_Limits.setIcon(self.actionHorizontal_Limits.icon())

    # def Both_Limits(self):
    #     self.actionShow_Limits.setIcon(self.actionBoth_Limits.icon())
        
    def Smaller_Symbols(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return
        ds = self.datasets[tab.name]
        msize = ds.marker_size - 5
        ds.marker_size = msize if msize>0 else 2
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionShow_Smaller_Symbols.icon())

    def ResetSymbolsSize(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return        
        ds = self.datasets[tab.name]
        ds.marker_size = 12
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionResetSymbolsSize.icon()) 
   
    def Larger_Symbols(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return
        ds = self.datasets[tab.name]
        msize = ds.marker_size + 5
        ds.marker_size = msize if msize<26 else 26
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionShow_Larger_Symbols.icon())
    
