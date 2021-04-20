"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseLayoutHierarchyType as _BaseLayoutHierarchyType

class Line(_BaseLayoutHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def dash(self):
        """
        Sets the length of dashes and gaps (mapbox.layer.paint.line-
        dasharray). Has an effect only when `type` is set to "line".
    
        The 'dash' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        ...
    
    @dash.setter
    def dash(self, val):
        ...
    
    @property
    def dashsrc(self):
        """
        Sets the source reference on Chart Studio Cloud for  dash .
    
        The 'dashsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        ...
    
    @dashsrc.setter
    def dashsrc(self, val):
        ...
    
    @property
    def width(self):
        """
        Sets the line width (mapbox.layer.paint.line-width). Has an
        effect only when `type` is set to "line".
    
        The 'width' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        ...
    
    @width.setter
    def width(self, val):
        ...
    
    def __init__(self, arg=..., dash=..., dashsrc=..., width=..., **kwargs) -> None:
        """
        Construct a new Line object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.layout.mapbox.layer.Line`
        dash
            Sets the length of dashes and gaps
            (mapbox.layer.paint.line-dasharray). Has an effect only
            when `type` is set to "line".
        dashsrc
            Sets the source reference on Chart Studio Cloud for
            dash .
        width
            Sets the line width (mapbox.layer.paint.line-width).
            Has an effect only when `type` is set to "line".

        Returns
        -------
        Line
        """
        ...
    


