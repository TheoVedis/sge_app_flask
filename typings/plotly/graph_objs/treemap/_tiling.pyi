"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Tiling(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def flip(self):
        """
        Determines if the positions obtained from solver are flipped on
        each axis.
    
        The 'flip' property is a flaglist and may be specified
        as a string containing:
          - Any combination of ['x', 'y'] joined with '+' characters
            (e.g. 'x+y')

        Returns
        -------
        Any
        """
        ...
    
    @flip.setter
    def flip(self, val):
        ...
    
    @property
    def packing(self):
        """
        Determines d3 treemap solver. For more info please refer to
        https://github.com/d3/d3-hierarchy#treemap-tiling
    
        The 'packing' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['squarify', 'binary', 'dice', 'slice', 'slice-dice',
                'dice-slice']

        Returns
        -------
        Any
        """
        ...
    
    @packing.setter
    def packing(self, val):
        ...
    
    @property
    def pad(self):
        """
        Sets the inner padding (in px).
    
        The 'pad' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        ...
    
    @pad.setter
    def pad(self, val):
        ...
    
    @property
    def squarifyratio(self):
        """
        When using "squarify" `packing` algorithm, according to https:/
        /github.com/d3/d3-hierarchy/blob/master/README.md#squarify_rati
        o this option specifies the desired aspect ratio of the
        generated rectangles. The ratio must be specified as a number
        greater than or equal to one. Note that the orientation of the
        generated rectangles (tall or wide) is not implied by the
        ratio; for example, a ratio of two will attempt to produce a
        mixture of rectangles whose width:height ratio is either 2:1 or
        1:2. When using "squarify", unlike d3 which uses the Golden
        Ratio i.e. 1.618034, Plotly applies 1 to increase squares in
        treemap layouts.
    
        The 'squarifyratio' property is a number and may be specified as:
          - An int or float in the interval [1, inf]

        Returns
        -------
        int|float
        """
        ...
    
    @squarifyratio.setter
    def squarifyratio(self, val):
        ...
    
    def __init__(self, arg=..., flip=..., packing=..., pad=..., squarifyratio=..., **kwargs) -> None:
        """
        Construct a new Tiling object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.treemap.Tiling`
        flip
            Determines if the positions obtained from solver are
            flipped on each axis.
        packing
            Determines d3 treemap solver. For more info please
            refer to https://github.com/d3/d3-hierarchy#treemap-
            tiling
        pad
            Sets the inner padding (in px).
        squarifyratio
            When using "squarify" `packing` algorithm, according to
            https://github.com/d3/d3-hierarchy/blob/master/README.m
            d#squarify_ratio this option specifies the desired
            aspect ratio of the generated rectangles. The ratio
            must be specified as a number greater than or equal to
            one. Note that the orientation of the generated
            rectangles (tall or wide) is not implied by the ratio;
            for example, a ratio of two will attempt to produce a
            mixture of rectangles whose width:height ratio is
            either 2:1 or 1:2. When using "squarify", unlike d3
            which uses the Golden Ratio i.e. 1.618034, Plotly
            applies 1 to increase squares in treemap layouts.

        Returns
        -------
        Tiling
        """
        ...
    


