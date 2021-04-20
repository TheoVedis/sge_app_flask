"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Starts(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def x(self):
        """
        Sets the x components of the starting position of the
        streamtubes
    
        The 'x' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        ...
    
    @x.setter
    def x(self, val):
        ...
    
    @property
    def xsrc(self):
        """
        Sets the source reference on Chart Studio Cloud for  x .
    
        The 'xsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        ...
    
    @xsrc.setter
    def xsrc(self, val):
        ...
    
    @property
    def y(self):
        """
        Sets the y components of the starting position of the
        streamtubes
    
        The 'y' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        ...
    
    @y.setter
    def y(self, val):
        ...
    
    @property
    def ysrc(self):
        """
        Sets the source reference on Chart Studio Cloud for  y .
    
        The 'ysrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        ...
    
    @ysrc.setter
    def ysrc(self, val):
        ...
    
    @property
    def z(self):
        """
        Sets the z components of the starting position of the
        streamtubes
    
        The 'z' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        ...
    
    @z.setter
    def z(self, val):
        ...
    
    @property
    def zsrc(self):
        """
        Sets the source reference on Chart Studio Cloud for  z .
    
        The 'zsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        ...
    
    @zsrc.setter
    def zsrc(self, val):
        ...
    
    def __init__(self, arg=..., x=..., xsrc=..., y=..., ysrc=..., z=..., zsrc=..., **kwargs) -> None:
        """
        Construct a new Starts object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.streamtube.Starts`
        x
            Sets the x components of the starting position of the
            streamtubes
        xsrc
            Sets the source reference on Chart Studio Cloud for  x
            .
        y
            Sets the y components of the starting position of the
            streamtubes
        ysrc
            Sets the source reference on Chart Studio Cloud for  y
            .
        z
            Sets the z components of the starting position of the
            streamtubes
        zsrc
            Sets the source reference on Chart Studio Cloud for  z
            .

        Returns
        -------
        Starts
        """
        ...
    


