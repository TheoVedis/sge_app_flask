"""
This type stub file was generated by pyright.
"""

from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType

class Diagonal(_BaseTraceHierarchyType):
    _parent_path_str = ...
    _path_str = ...
    _valid_props = ...
    @property
    def visible(self):
        """
        Determines whether or not subplots on the diagonal are
        displayed.
    
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
    
    def __init__(self, arg=..., visible=..., **kwargs) -> None:
        """
        Construct a new Diagonal object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            :class:`plotly.graph_objs.splom.Diagonal`
        visible
            Determines whether or not subplots on the diagonal are
            displayed.

        Returns
        -------
        Diagonal
        """
        ...
    


