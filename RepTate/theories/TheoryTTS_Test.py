# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module TheoryTTS

Module for the pseudo theory for Time-Temperature superposition shift of LVE data.

""" 
import os
import time
import getpass
import numpy as np
from scipy import interp
from scipy.optimize import minimize
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QStyle, QFileDialog
from PyQt5.QtCore import QSize

class TheoryWLFShiftTest(CmdBase):
    """Basic theory for Time-Temperature Superposition, based on the WLF equation
    
    [description]
    """
    thname="WLFShiftTest"
    description="Basic theory for Time-Temperature Superposition, based on the WLF equation"
    cite=""

    def __new__(cls, name="ThWLFShifTest", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThWLFShiftTest"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        
        Returns:
            [type] -- [description]
        """
        return GUITheoryWLFShiftTest(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryWLFShiftTest(name, parent_dataset, ax)

class BaseTheoryWLFShiftTest:
    """[summary]
    
    [description]
    """
    single_file = False 

    def __init__(self, name="ThWLFShiftTest", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThWLFShiftTest"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.TheoryWLFShiftTest
        self.parameters["C1"] = Parameter("C1", 6.85, "Material parameter C1 for WLF Shift", ParameterType.real, opt_type=OptType.opt)
        self.parameters["C2"] = Parameter("C2", 150, "Material parameter C2 for WLF Shift", ParameterType.real, opt_type=OptType.opt)
        self.parameters["rho0"] = Parameter("rho0", 0.928, "Density of polymer at 0 °C", ParameterType.real, opt_type=OptType.const)
        self.parameters["C3"] = Parameter("C3", 0.61, "Density parameter", ParameterType.real, opt_type=OptType.const)
        self.parameters["Tr"] = Parameter("Tr", 25, "Material parameter Tr Reference T WLF shift", ParameterType.real, opt_type=OptType.const)
        self.parameters["T"] = Parameter("T", 25, "Temperature to shift WLF to, in °C", ParameterType.real, opt_type=OptType.const)
        self.parameters["CTg"] = Parameter("CTg", 14.65, "Molecular weight dependence of Tg", ParameterType.real, opt_type=OptType.const)
        self.parameters["dx12"] = Parameter("dx12", 0, "For PBd", ParameterType.real, opt_type=OptType.const)
        self.parameters["vert"] = Parameter(name="vert", value=True, description="Shift vertically", 
                                            type=ParameterType.boolean, opt_type=OptType.const, display_flag=False)
        self.parameters["iso"] = Parameter(name="iso", value=True, description="Isofrictional state", 
                                           type=ParameterType.boolean, opt_type=OptType.const, display_flag=False)

    def TheoryWLFShiftTest(self, f=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            f {[type]} -- [description] (default: {None})
        """
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))

        T=self.parameters["T"].value
        Tr=self.parameters["Tr"].value
        C1=self.parameters["C1"].value
        C2=self.parameters["C2"].value
        C3=self.parameters["C3"].value
        rho0=self.parameters["rho0"].value
        CTg=self.parameters["CTg"].value
        dx12=self.parameters["dx12"].value
        iso=self.parameters["iso"].value
        vert=self.parameters["vert"].value

        Tf=f.file_parameters["T"]
        Mw=f.file_parameters["Mw"]

        #if iso:
        #    C2 += CTg / Mw - 68.7 * dx12
        #    T0corrected = T0 - CTg / Mw + 68.7 * dx12
        #else:
        #    T0corrected = T0
        #tt.data[:,0] = ft.data[:,0]*np.power(10.0, -(T - T0corrected) * (C1 / (T + C2)))

        # Trying a new expression for the shift
        if iso:
            Trcorrected = Tr - CTg / Mw + 68.7 * dx12
        else:
            Trcorrected = Tr
        tt.data[:,0] = ft.data[:,0]*np.power(10.0, -C1*C2*(Tf - T)/(C2 + T - Trcorrected)/(C2 + Tf - Trcorrected))
        
        if vert:
            bT = (rho0 - Tf * C3 * 1E-3) * (Tf + 273.15) / ((rho0 - T * C3 * 1E-3) * (T + 273.15))
        else:
            bT = 1
        tt.data[:,1] = ft.data[:,1] / bT
        tt.data[:,2] = ft.data[:,2] / bT

    def do_error(self, line):
        """Override the error calculation for TTS
        
        The error is calculated as the vertical distance between theory points, in the current view,\
        calculated over all possible pairs of theory tables, when the theories overlap in the horizontal direction and\
        they correspond to files with the same Mw (if the parameters Mw2 and phi exist, their values are also
        used to classify the error). 1/2 of the error is added to each file.
        Report the error of the current theory on all the files.\n\
        File error is calculated as the mean square of the residual, averaged over all calculated points in the shifted tables.\n\
        Total error is the mean square of the residual, averaged over all points considered in all files.
        
        Arguments:
            line {[type]} -- [description]
        """
        total_error=0
        npoints=0
        view = self.parent_dataset.parent_application.current_view
        nfiles=len(self.parent_dataset.files)
        file_error=np.zeros(nfiles)
        file_points=np.zeros(nfiles,dtype=np.int)
        xth=[]
        yth=[]
        Mw=[]
        xmin=np.zeros((nfiles,view.n))
        xmax=np.zeros((nfiles,view.n))
        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            Mwi=Filei.file_parameters["Mw"]
            if "Mw2" in Filei.file_parameters:
                Mw2i=Filei.file_parameters["Mw2"]
            else:
                Mw2i=0
            if "phi" in Filei.file_parameters:
                phii=Filei.file_parameters["phi"]
            else:
                phii=0
            if "phi2" in Filei.file_parameters:
                phi2i=Filei.file_parameters["phi2"]
            else:
                phi2i=0
            xthi, ythi, success = view.view_proc(self.tables[Filei.file_name_short], Filei.file_parameters)
            # We need to sort arrays
            for k in range(view.n):
                x = xthi[:,k]
                p = x.argsort()
                xthi[:,k] = xthi[p,k]
                ythi[:,k] = ythi[p,k]
            xth.append(xthi)
            yth.append(ythi)
            Mw.append((Mwi,Mw2i,phii,phi2i))
            
            xmin[i,:]=np.amin(xthi,0)
            xmax[i,:]=np.amax(xthi,0)

        MwUnique={}
        p = list(set(Mw))
        for o in p:
            MwUnique[o]=[0.0, 0]
            
        for i in range(nfiles):
            for j in range(i+1,nfiles):
                if (Mw[i] != Mw[j]): continue
                for k in range(view.n):
                    condition=(xth[j][:,k]>xmin[i,k])*(xth[j][:,k]<xmax[i,k])
                    x = np.extract(condition, xth[j][:,k])
                    y = np.extract(condition, yth[j][:,k])
                    yinterp=interp(x, xth[i][:,k], yth[i][:,k])
                    error=np.sum((yinterp-y)**2)
                    npt=len(y)
                    total_error+=error
                    npoints+=npt
                    MwUnique[Mw[i]][0]+=error
                    MwUnique[Mw[i]][1]+=npt
        
        if (line==""): 
            self.Qprint("%5s %5s %5s %5s %10s (%10s)"%("Mw","Mw2","phi","phi2","Error","# Points"))
            self.Qprint("=====================")
            p = list(MwUnique.keys())
            p.sort()
            for o in p:
                if (MwUnique[o][1]>0):
                    self.Qprint("%5gk %5gk %5g %5g %10.5g (%10d)"%(o[0], o[1], o[2], o[3],MwUnique[o][0]/MwUnique[o][1],MwUnique[o][1]))
                else:
                    self.Qprint("%5gk %5gk %5g %5g %10s (%10d)"%(o[0], o[1], o[2], o[3],"-",0))
        if (npoints>0):
            total_error/=npoints
        else:
            total_error=1e10;
        if (line==""): self.Qprint("%21s %10.5g (%10d)"%("TOTAL",total_error,npoints))
        return total_error
                
    def func_fitTTS(self, *param_in):
        """[summary]
        
        [description]
        
        Arguments:
            *param_in {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        ind=0
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.opt_type == OptType.opt:
                par.value=param_in[0][ind]
                ind+=1
        self.do_calculate("")
        error=self.do_error("none")
        return error

    def do_fit(self, line):
        """Minimize the error
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        self.fitting = True
        view = self.parent_dataset.parent_application.current_view

        # Mount the vector of parameters (Active ones only)
        initial_guess=[]
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.opt_type == OptType.opt: 
                initial_guess.append(par.value)

        res = minimize(self.func_fitTTS, initial_guess, method='Nelder-Mead')
        
        if (not res['success']):
            self.Qprint("Solution not found: %s"%res['message'])
            return

        self.Qprint("Solution found with %d function evaluations and error %g"%(res['nfev'],res.fun))

        ind=0
        k=list(self.parameters.keys())
        k.sort()
        self.Qprint("%10s   %10s"%("Parameter","Value"))
        self.Qprint("===========================")
        for p in k:
            par = self.parameters[p] 
            if par.opt_type == OptType.opt:
                ind+=1
                self.Qprint('*%9s = %10.5g'%(par.name, par.value))
            else:
                self.Qprint('%10s = %10.5g'%(par.name, par.value))
        self.fitting=False
        self.do_calculate(line)

    def do_print(self, line):
        """Print the theory table associated with the given file name
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found"%line)

    def complete_print(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            text {[type]} -- [description]
            line {[type]} -- [description]
            begidx {[type]} -- [description]
            endidx {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        file_names=list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [ f
                            for f in file_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_save(self, line):
        """Save the results from WLFShiftTest theory predictions to a TTS file
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        print('Saving prediction of '+self.thname+' theory')
        nfiles=len(self.parent_dataset.files)
        Mw=[]
        for i in range(nfiles):
            Filei=self.parent_dataset.files[i]
            Mwi=Filei.file_parameters["Mw"]
            if "Mw2" in Filei.file_parameters:
                Mw2i=Filei.file_parameters["Mw2"]
            else:
                Mw2i=0
            if "phi" in Filei.file_parameters:
                phii=Filei.file_parameters["phi"]
            else:
                phii=0
            if "phi2" in Filei.file_parameters:
                phi2i=Filei.file_parameters["phi2"]
            else:
                phi2i=0
            Mw.append((Mwi,Mw2i,phii,phi2i))
        MwUnique = list(set(Mw))
        MwUnique.sort()

        for m in MwUnique:
            data=np.zeros(0)
            fparam={}
            for i in range(nfiles):
                if (Mw[i] == m): 
                    Filei=self.parent_dataset.files[i]
                    ttable=self.tables[Filei.file_name_short]
                    data = np.append(data, ttable.data)
                    data=np.reshape(data, (-1, ttable.num_columns))
                    fparam.update(Filei.file_parameters)
            data=data[data[:, 0].argsort()]
            fparam["T"]=self.parameters["T0"].value

            if line=="":
                ofilename=os.path.dirname(self.parent_dataset.files[0].file_full_path)+os.sep+fparam["chem"]+'_Mw'+str(m[0])+'k'+'_Mw2'+str(m[1])+'_phi'+str(m[2])+'_phiB'+str(m[3])+str(fparam["T"])+'.tts'
            else:
                ofilename=line+os.sep+fparam["chem"]+'_Mw'+str(m[0])+'k'+'_Mw2'+str(m[1])+'_phi'+str(m[2])+'_phiB'+str(m[3])+str(fparam["T"])+'.tts'            
            print('File: '+ofilename)
            fout=open(ofilename, 'w')
            for i in sorted(fparam):
                fout.write(i + "=" + str(fparam[i])+ ";")
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + ';')
            fout.write('\n')
            fout.write('# Master curve predicted with WLF Theory\n')
            fout.write('# Date: '+ time.strftime("%Y-%m-%d %H:%M:%S") + ' - User: ' + getpass.getuser() + '\n')
            k = Filei.file_type.col_names
            for i in k: 
                fout.write(i+'\t')
            fout.write('\n')
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    fout.write(str(data[i, j])+'\t')
                fout.write('\n')
            fout.close()

class CLTheoryWLFShiftTest(BaseTheoryWLFShiftTest, Theory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThWLFShiftTest", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThWLFShiftTest"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryWLFShiftTest(BaseTheoryWLFShiftTest, QTheory):
    """[summary]
    
    [description]
    """
    def __init__(self, name="ThWLFShiftTest", parent_dataset=None, ax=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            name {[type]} -- [description] (default: {"ThWLFShiftTest"})
            parent_dataset {[type]} -- [description] (default: {None})
            ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.verticalshift = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')), 'Vertical shift')
        self.verticalshift.setCheckable(True)
        self.verticalshift.setChecked(True)
        self.isofrictional = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogInfoView')), 'Shift to isofrictional state')
        self.isofrictional.setCheckable(True)
        self.isofrictional.setChecked(True)
        self.savemaster = tb.addAction(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')), 'Save Master Curve')
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.verticalshift.triggered.connect(self.do_vertical_shift)
        connection_id = self.isofrictional.triggered.connect(self.do_isofrictional)
        connection_id = self.savemaster.triggered.connect(self.do_save_dialog)

    def do_vertical_shift(self):
        self.set_param_value("vert", self.verticalshift.isChecked())

    def do_isofrictional(self):
        self.set_param_value("iso", self.isofrictional.isChecked())

    def do_save_dialog(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory to save Master curves"))
        self.do_save(folder)