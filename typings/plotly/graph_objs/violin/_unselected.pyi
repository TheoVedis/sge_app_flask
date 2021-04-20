"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Unselected(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def marker(self):
        """
        The 'marker' property is an instance of Marker
        that may be specified as:
          - An instance of :class:`plotly.graph_objs.violin.unselected.Marker`
          - A dict of string/value properties that will be passed
            to the Marker constructor
    
            Supported dict properties:
                
                color
                    Sets the marker color of unselected points,
                    applied only when a selection exists.
                opacity
                    Sets the marker opacity of unselected points,
                    applied only when a selection exists.
                size
                    Sets the marker size of unselected points,
                    applied only when a selection exists.

        Returns
        -------
        plotly.graph_objs.violin.unselected.Marker
        """
        ...
    
    @marker.setter
    def marker(self, val):
        ...
    
    def __init__(self, arg=..., marker=..., **kwargs) -> None:
        """
        Construct a new Unselected object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.violin.Unselected`
        marker
            :class:`plotly.graph_objects.violin.unselected.Marker`
            instance or dict with compatible properties

        Returns
        -------
        Unselected
        """
        ...
    


