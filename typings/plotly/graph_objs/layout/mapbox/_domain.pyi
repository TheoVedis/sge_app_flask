"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseLayoutHierarchyType as _BaseLayoutHierarchyType

class Domain(_BaseLayoutHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def column(self):
        """
        If there is a layout grid, use the domain for this column in
        the grid for this mapbox subplot .
    
        The 'column' property is a integer and may be specified as:
          - An int (or float that will be cast to an int)
            in the interval [0, 9223372036854775807]

        Returns
        -------
        int
        """
        ...
    
    @column.setter
    def column(self, val):
        ...
    
    @property
    def row(self):
        """
        If there is a layout grid, use the domain for this row in the
        grid for this mapbox subplot .
    
        The 'row' property is a integer and may be specified as:
          - An int (or float that will be cast to an int)
            in the interval [0, 9223372036854775807]

        Returns
        -------
        int
        """
        ...
    
    @row.setter
    def row(self, val):
        ...
    
    @property
    def x(self):
        """
        Sets the horizontal domain of this mapbox subplot (in plot
        fraction).
    
        The 'x' property is an info array that may be specified as:
    
        * a list or tuple of 2 elements where:
    (0) The 'x[0]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]
    (1) The 'x[1]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        list
        """
        ...
    
    @x.setter
    def x(self, val):
        ...
    
    @property
    def y(self):
        """
        Sets the vertical domain of this mapbox subplot (in plot
        fraction).
    
        The 'y' property is an info array that may be specified as:
    
        * a list or tuple of 2 elements where:
    (0) The 'y[0]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]
    (1) The 'y[1]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        list
        """
        ...
    
    @y.setter
    def y(self, val):
        ...
    
    def __init__(self, arg=..., column=..., row=..., x=..., y=..., **kwargs) -> None:
        """
        Construct a new Domain object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.layout.mapbox.Domain`
        column
            If there is a layout grid, use the domain for this
            column in the grid for this mapbox subplot .
        row
            If there is a layout grid, use the domain for this row
            in the grid for this mapbox subplot .
        x
            Sets the horizontal domain of this mapbox subplot (in
            plot fraction).
        y
            Sets the vertical domain of this mapbox subplot (in
            plot fraction).

        Returns
        -------
        Domain
        """
        ...
    


