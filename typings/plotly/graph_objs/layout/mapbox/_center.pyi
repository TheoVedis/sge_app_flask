"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseLayoutHierarchyType as _BaseLayoutHierarchyType

class Center(_BaseLayoutHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def lat(self):
        """
        Sets the latitude of the center of the map (in degrees North).
    
        The 'lat' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        ...
    
    @lat.setter
    def lat(self, val):
        ...
    
    @property
    def lon(self):
        """
        Sets the longitude of the center of the map (in degrees East).
    
        The 'lon' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        ...
    
    @lon.setter
    def lon(self, val):
        ...
    
    def __init__(self, arg=..., lat=..., lon=..., **kwargs) -> None:
        """
        Construct a new Center object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.layout.mapbox.Center`
        lat
            Sets the latitude of the center of the map (in degrees
            North).
        lon
            Sets the longitude of the center of the map (in degrees
            East).

        Returns
        -------
        Center
        """
        ...
    


