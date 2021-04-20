"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Selected(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def marker(self):
        """
        The 'marker' property is an instance of Marker
        that may be specified as:
          - An instance of :class:`plotly.graph_objs.choroplethmapbox.selected.Marker`
          - A dict of string/value properties that will be passed
            to the Marker constructor
    
            Supported dict properties:
                
                opacity
                    Sets the marker opacity of selected points.

        Returns
        -------
        plotly.graph_objs.choroplethmapbox.selected.Marker
        """
        ...
    
    @marker.setter
    def marker(self, val):
        ...
    
    def __init__(self, arg=..., marker=..., **kwargs) -> None:
        """
        Construct a new Selected object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.choroplethmapbox.Selected`
        marker
            :class:`plotly.graph_objects.choroplethmapbox.selected.
            Marker` instance or dict with compatible properties

        Returns
        -------
        Selected
        """
        ...
    


