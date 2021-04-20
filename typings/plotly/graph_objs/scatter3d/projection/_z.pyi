"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Z(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def opacity(self):
        """
        Sets the projection color.
    
        The 'opacity' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        ...
    
    @opacity.setter
    def opacity(self, val):
        ...
    
    @property
    def scale(self):
        """
        Sets the scale factor determining the size of the projection
        marker points.
    
        The 'scale' property is a number and may be specified as:
          - An int or float in the interval [0, 10]

        Returns
        -------
        int|float
        """
        ...
    
    @scale.setter
    def scale(self, val):
        ...
    
    @property
    def show(self):
        """
        Sets whether or not projections are shown along the z axis.
    
        The 'show' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        ...
    
    @show.setter
    def show(self, val):
        ...
    
    def __init__(self, arg=..., opacity=..., scale=..., show=..., **kwargs) -> None:
        """
        Construct a new Z object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.scatter3d.projection.Z`
        opacity
            Sets the projection color.
        scale
            Sets the scale factor determining the size of the
            projection marker points.
        show
            Sets whether or not projections are shown along the z
            axis.

        Returns
        -------
        Z
        """
        ...
    


