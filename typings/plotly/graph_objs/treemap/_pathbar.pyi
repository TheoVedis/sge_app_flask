"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Pathbar(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def edgeshape(self):
        """
        Determines which shape is used for edges between `barpath`
        labels.
    
        The 'edgeshape' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['>', '<', '|', '\\']
          - A string that matches one of the following regular expressions:
                ['']

        Returns
        -------
        Any
        """
        ...
    
    @edgeshape.setter
    def edgeshape(self, val):
        ...
    
    @property
    def side(self):
        """
        Determines on which side of the the treemap the `pathbar`
        should be presented.
    
        The 'side' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['top', 'bottom']

        Returns
        -------
        Any
        """
        ...
    
    @side.setter
    def side(self, val):
        ...
    
    @property
    def textfont(self):
        """
        Sets the font used inside `pathbar`.
    
        The 'textfont' property is an instance of Textfont
        that may be specified as:
          - An instance of :class:`plotly.graph_objs.treemap.pathbar.Textfont`
          - A dict of string/value properties that will be passed
            to the Textfont constructor
    
            Supported dict properties:
                
                color
    
                colorsrc
                    Sets the source reference on Chart Studio Cloud
                    for  color .
                family
                    HTML font family - the typeface that will be
                    applied by the web browser. The web browser
                    will only be able to apply a font if it is
                    available on the system which it operates.
                    Provide multiple font families, separated by
                    commas, to indicate the preference in which to
                    apply fonts if they aren't available on the
                    system. The Chart Studio Cloud (at
                    https://chart-studio.plotly.com or on-premise)
                    generates images on a server, where only a
                    select number of fonts are installed and
                    supported. These include "Arial", "Balto",
                    "Courier New", "Droid Sans",, "Droid Serif",
                    "Droid Sans Mono", "Gravitas One", "Old
                    Standard TT", "Open Sans", "Overpass", "PT Sans
                    Narrow", "Raleway", "Times New Roman".
                familysrc
                    Sets the source reference on Chart Studio Cloud
                    for  family .
                size
    
                sizesrc
                    Sets the source reference on Chart Studio Cloud
                    for  size .

        Returns
        -------
        plotly.graph_objs.treemap.pathbar.Textfont
        """
        ...
    
    @textfont.setter
    def textfont(self, val):
        ...
    
    @property
    def thickness(self):
        """
        Sets the thickness of `pathbar` (in px). If not specified the
        `pathbar.textfont.size` is used with 3 pixles extra padding on
        each side.
    
        The 'thickness' property is a number and may be specified as:
          - An int or float in the interval [12, inf]

        Returns
        -------
        int|float
        """
        ...
    
    @thickness.setter
    def thickness(self, val):
        ...
    
    @property
    def visible(self):
        """
        Determines if the path bar is drawn i.e. outside the trace
        `domain` and with one pixel gap.
    
        The 'visible' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        ...
    
    @visible.setter
    def visible(self, val):
        ...
    
    def __init__(self, arg=..., edgeshape=..., side=..., textfont=..., thickness=..., visible=..., **kwargs) -> None:
        """
        Construct a new Pathbar object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.treemap.Pathbar`
        edgeshape
            Determines which shape is used for edges between
            `barpath` labels.
        side
            Determines on which side of the the treemap the
            `pathbar` should be presented.
        textfont
            Sets the font used inside `pathbar`.
        thickness
            Sets the thickness of `pathbar` (in px). If not
            specified the `pathbar.textfont.size` is used with 3
            pixles extra padding on each side.
        visible
            Determines if the path bar is drawn i.e. outside the
            trace `domain` and with one pixel gap.

        Returns
        -------
        Pathbar
        """
        ...
    


