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
from tank.platform.qt import QtCore, QtGui


class WidgetDelegate(QtGui.QStyledItemDelegate):
    """
    Convenience wrapper that makes it straight forward to use
    widgets inside of delegates.
    """

    def __init__(self, view):
        """
        Constructor
        """
        QtGui.QStyledItemDelegate.__init__(self, view)
        self._view = view        
        
        # set up the widget instance we will use 
        # when 'painting' large number of cells 
        self._paint_widget = self._create_widget(view)
        
        # tracks the currently active cell
        self._current_editor_index = None    
        self._current_widget = None
        
        # when mouse enters into a cell
        self._view.clicked.connect( self._on_cell_clicked )
                
    def _on_cell_clicked(self, model_index):
        """
        Event handler called whenever the mouse enters into a cell
        """
        if self._current_editor_index:
            self._view.closePersistentEditor(self._current_editor_index)
            self._current_editor_index = None
            self._current_widget = None
        
        # select it in the view
        self._view.selectionModel().select(model_index, QtGui.QItemSelectionModel.ClearAndSelect)
        
        # create an editor widget that we use for the selected item
        self._current_editor_index = model_index
        self._view.openPersistentEditor(model_index)
        
    def createEditor(self, parent_widget, style_options, model_index):
        """
        Subclassed implementation which is typically called from
        the delegate framework whenever the mouse enters a cell
        """        
        # create a new widget for this since it will persist
        widget = self._create_widget(parent_widget)
        self._current_widget = widget
        # and let the subclass implemenation set up its hover state
        self._configure_widget(widget, model_index, style_options)
        return widget
        
        
    def updateEditorGeometry(self, editor_widget, style_options, model_index):        
        """
        Subclassed implementation which is typically called 
        whenever a hover/editor widget is set up and needs resizing
        """
        editor_widget.resize(style_options.rect.size())
        editor_widget.move(style_options.rect.topLeft())
        
    def paint(self, painter, style_options, model_index):
        """
        Paint method to handle all cells that are not being currently edited.
        """        
        if model_index == self._current_editor_index and self._current_widget is not None:
            self._configure_widget(self._current_widget, model_index, style_options)
        
        else:
            # for performance reasons, we are not creating a widget every time
            # but merely moving the same widget around. 
            self._configure_widget(self._paint_widget, model_index, style_options)
                    
            painter.save()
            self._paint_widget.resize(style_options.rect.size())
            painter.translate(style_options.rect.topLeft())
            # note that we set the render flags NOT to render the background of the widget
            # this makes it consistent with the way the editor widget is mounted inside 
            # each element upon hover.
            self._paint_widget.render(painter, 
                                      QtCore.QPoint(0,0), 
                                      renderFlags=QtGui.QWidget.DrawChildren)
            painter.restore()
        
    ########################################################################################
    # implemented by deriving classes
    
    def _create_widget(self, parent):
        """
        This needs to be implemented by any deriving classes.
        
        Should return a widget that will be used both for editing and displaying a view cell
        """
        raise Exception("Needs to be implemented!")
    
    def _configure_widget(self, widget, model_index, style_options):
        """
        This needs to be implemented by any deriving classes.
        
        Callback that is called whenever the delegate needs the widget to update itself
        with a particular set of model data, in this case for viewing.
        """
        raise Exception("Needs to be implemented!")
            


