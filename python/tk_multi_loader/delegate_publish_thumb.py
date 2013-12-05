# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
import os
import hashlib
import tempfile
from . import utils

from tank.platform.qt import QtCore, QtGui
from .shotgun_widgets import WidgetDelegate
from .shotgun_widgets import ThumbWidget
from .model_latestpublish import SgLatestPublishModel
from .shotgun_model import ShotgunModel


class SgPublishDelegate(WidgetDelegate):
    """
    Delegate which 'glues up' the ThumbWidget with a QT View.
    """

    def __init__(self, view, status_model):
        WidgetDelegate.__init__(self, view)
        self._status_model = status_model
        
    def _create_widget(self, parent):
        """
        Widget factory as required by base class
        """
        return ThumbWidget(parent)
    
    def _configure_widget(self, widget, model_index, style_options):
        """
        Called by the base class when the associated widget should be
        painted in the view.
        """
        if style_options.state & QtGui.QStyle.State_Selected:
            selected = True
        else:
            selected = False
        
        icon = model_index.data(QtCore.Qt.DecorationRole)
        thumb = icon.pixmap( 512 )
        widget.set_thumbnail(thumb)
        widget.set_selected(selected)
        
        sg_data = model_index.data(ShotgunModel.SG_DATA_ROLE)
        
        if sg_data is None:
            # this is an intermediate node with no metadata on it
            widget.set_text(model_index.data(SgLatestPublishModel.FOLDER_NAME_ROLE), "", "") 
        
        elif model_index.data(SgLatestPublishModel.IS_FOLDER_ROLE):
            # folder. The name is in the main text role.
            status_code = model_index.data(SgLatestPublishModel.FOLDER_STATUS_ROLE)
            if status_code is None:
                status_name = "No Status"
            else:
                status_name = self._status_model.get_long_name(status_code)
                        
            widget.set_text(model_index.data(SgLatestPublishModel.FOLDER_NAME_ROLE),
                            model_index.data(SgLatestPublishModel.FOLDER_TYPE_ROLE), 
                            "Status: %s" % status_name) 
        else:
            # this is a publish!
            widget.set_text(model_index.data(SgLatestPublishModel.PUBLISH_NAME_ROLE),
                            model_index.data(SgLatestPublishModel.PUBLISH_TYPE_NAME_ROLE), 
                            model_index.data(SgLatestPublishModel.ENTITY_NAME_ROLE)) 
        
    def sizeHint(self, style_options, model_index):
        """
        Base the size on the icon size property of the view
        """
        # base the size of each element off the icon size property of the view
        scale_factor = self._view.iconSize().width()        
        return ThumbWidget.calculate_size(scale_factor)
        
             
