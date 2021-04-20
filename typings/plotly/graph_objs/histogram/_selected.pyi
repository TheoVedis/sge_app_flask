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
          - An instance of :class:`plotly.graph_objs.histogram.selected.Marker`
          - A dict of string/value properties that will be passed
            to the Marker constructor
    
            Supported dict properties:
                
                color
                    Sets the marker color of selected points.
                opacity
                    Sets the marker opacity of selected points.

        Returns
        -------
        plotly.graph_objs.histogram.selected.Marker
        """
        ...
    
    @marker.setter
    def marker(self, val):
        ...
    
    @property
    def textfont(self):
        """
        The 'textfont' property is an instance of Textfont
        that may be specified as:
          - An instance of :class:`plotly.graph_objs.histogram.selected.Textfont`
          - A dict of string/value properties that will be passed
            to the Textfont constructor
    
            Supported dict properties:
                
                color
                    Sets the text font color of selected points.

        Returns
        -------
        plotly.graph_objs.histogram.selected.Textfont
        """
        ...
    
    @textfont.setter
    def textfont(self, val):
        ...
    
    def __init__(self, arg=..., marker=..., textfont=..., **kwargs) -> None:
        """
        Construct a new Selected object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.histogram.Selected`
        marker
            :class:`plotly.graph_objects.histogram.selected.Marker`
            instance or dict with compatible properties
        textfont
            :class:`plotly.graph_objects.histogram.selected.Textfon
            t` instance or dict with compatible properties

        Returns
        -------
        Selected
        """
        ...
    


