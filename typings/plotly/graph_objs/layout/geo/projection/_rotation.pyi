"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseLayoutHierarchyType as _BaseLayoutHierarchyType

class Rotation(_BaseLayoutHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def lat(self):
        """
        Rotates the map along meridians (in degrees North).
    
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
        Rotates the map along parallels (in degrees East). Defaults to
        the center of the `lonaxis.range` values.
    
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
    
    @property
    def roll(self):
        """
        Roll the map (in degrees) For example, a roll of 180 makes the
        map appear upside down.
    
        The 'roll' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        ...
    
    @roll.setter
    def roll(self, val):
        ...
    
    def __init__(self, arg=..., lat=..., lon=..., roll=..., **kwargs) -> None:
        """
        Construct a new Rotation object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of :class:`plotly.graph_objs.layout.geo.pro
            jection.Rotation`
        lat
            Rotates the map along meridians (in degrees North).
        lon
            Rotates the map along parallels (in degrees East).
            Defaults to the center of the `lonaxis.range` values.
        roll
            Roll the map (in degrees) For example, a roll of 180
            makes the map appear upside down.

        Returns
        -------
        Rotation
        """
        ...
    


