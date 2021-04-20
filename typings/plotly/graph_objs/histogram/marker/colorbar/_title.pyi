"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Title(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def font(self):
        """
        Sets this color bar's title font. Note that the title's font
        used to be set by the now deprecated `titlefont` attribute.
    
        The 'font' property is an instance of Font
        that may be specified as:
          - An instance of :class:`plotly.graph_objs.histogram.marker.colorbar.title.Font`
          - A dict of string/value properties that will be passed
            to the Font constructor
    
            Supported dict properties:
                
                color
    
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
                size

        Returns
        -------
        plotly.graph_objs.histogram.marker.colorbar.title.Font
        """
        ...
    
    @font.setter
    def font(self, val):
        ...
    
    @property
    def side(self):
        """
        Determines the location of color bar's title with respect to
        the color bar. Note that the title's location used to be set by
        the now deprecated `titleside` attribute.
    
        The 'side' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['right', 'top', 'bottom']

        Returns
        -------
        Any
        """
        ...
    
    @side.setter
    def side(self, val):
        ...
    
    @property
    def text(self):
        """
        Sets the title of the color bar. Note that before the existence
        of `title.text`, the title's contents used to be defined as the
        `title` attribute itself. This behavior has been deprecated.
    
        The 'text' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        ...
    
    @text.setter
    def text(self, val):
        ...
    
    def __init__(self, arg=..., font=..., side=..., text=..., **kwargs) -> None:
        """
        Construct a new Title object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of :class:`plotly.graph_objs.histogram.mark
            er.colorbar.Title`
        font
            Sets this color bar's title font. Note that the title's
            font used to be set by the now deprecated `titlefont`
            attribute.
        side
            Determines the location of color bar's title with
            respect to the color bar. Note that the title's
            location used to be set by the now deprecated
            `titleside` attribute.
        text
            Sets the title of the color bar. Note that before the
            existence of `title.text`, the title's contents used to
            be defined as the `title` attribute itself. This
            behavior has been deprecated.

        Returns
        -------
        Title
        """
        ...
    


