# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module ToolFindPeaks

FindPeaks file for creating a new Tool
"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType
from Tool import Tool
from QTool import QTool
from DataTable import DataTable


class ToolFindPeaks(CmdBase):
    """[summary]
    
    [description]
    """
    toolname = 'FindPeaksTool'
    description = 'FindPeaks Tool'
    citations = ''

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """[summary]
        
        [description]
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        return GUIToolFindPeaks(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLToolFindPeaks(
                name, parent_dataset, axarr)


class BaseToolFindPeaks:
    """[summary]
    
    [description]
    """
    #help_file = 'http://reptate.readthedocs.io/en/latest/manual/Tools/FindPeaks.html'
    toolname = ToolFindPeaks.toolname
    citations = ToolFindPeaks.citations

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)
        self.function = self.findpeaks  # main Tool function
        self.parameters['threshold'] = Parameter(
            name='threshold',
            value=0.3,
            description='threshold for peak detection',
            type=ParameterType.real)
        self.parameters['minimum_distance'] = Parameter(
            name='minimum_distance',
            value=5,
            description='minimum distance (in datapoints) between peaks',
            type=ParameterType.integer)


    def destructor(self):
        """[summary]
        
        [description]
        
        Arguments:

        """
        pass

    def findpeaks(self, f=None, v=None):
        """FindPeaks function that returns the square of the y, according to the view
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        
        Returns:
            - [type] -- [description]
        """
        n = v.n
        threshold = self.parameters["threshold"].value
        minimum_distance = self.parameters["minimum_distance"].value

        tt = self.tables[f.file_name_short]
        tt.num_columns = n+1
        # Here, we assume that all series have the same x axis
        s = f.data_table.series[0][0]
        x = np.array(s.get_xdata())
        tt.num_rows = len(x)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = x

        for i in range(n):
            s = f.data_table.series[0][i]
            y = np.array(s.get_ydata())
            thresholdnow = threshold * (np.max(y) - np.min(y)) + np.min(y)

            dy = np.diff(y)
            zeros,=np.where(dy == 0)
            if len(zeros) == len(y) - 1:
                print("", end='')
                continue
            while len(zeros):
                zerosr = np.hstack([dy[1:], 0.])
                zerosl = np.hstack([0., dy[:-1]])
                dy[zeros]=zerosr[zeros]
                zeros,=np.where(dy == 0)
                dy[zeros]=zerosl[zeros]
                zeros,=np.where(dy == 0)
            peaks = np.where((np.hstack([dy, 0.]) < 0.)
                 & (np.hstack([0., dy]) > 0.)
                 & (y > thresholdnow))[0]
            if peaks.size > 1 and minimum_distance > 1:
                highest = peaks[np.argsort(y[peaks])][::-1]
                rem = np.ones(y.size, dtype=bool)
                rem[peaks] = False

                for peak in highest:
                    if not rem[peak]:
                        sl = slice(max(0, peak - minimum_distance), peak + minimum_distance + 1)
                        rem[sl] = True
                        rem[peak] = False
                peaks = np.arange(y.size)[~rem]
            for d in peaks:
                tt.data[d, i+1] = y[d]
                print(" %g"%x[d],end='')
                print(" %g"%y[d],end='')
            print("")

class CLToolFindPeaks(BaseToolFindPeaks, Tool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUIToolFindPeaks(BaseToolFindPeaks, QTool):
    """[summary]
    
    [description]
    """

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {''})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the Tool here:
