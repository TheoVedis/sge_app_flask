"""
This type stub file was generated by pyright.
"""

pd = ...
REQUIRED_GANTT_KEYS = ...
def validate_gantt(df):
    """
    Validates the inputted dataframe or list
    """
    ...

def gantt(chart, colors, title, bar_width, showgrid_x, showgrid_y, height, width, tasks=..., task_names=..., data=..., group_tasks=..., show_hover_fill=..., show_colorbar=...):
    """
    Refer to create_gantt() for docstring
    """
    ...

def gantt_colorscale(chart, colors, title, index_col, show_colorbar, bar_width, showgrid_x, showgrid_y, height, width, tasks=..., task_names=..., data=..., group_tasks=..., show_hover_fill=...):
    """
    Refer to FigureFactory.create_gantt() for docstring
    """
    ...

def gantt_dict(chart, colors, title, index_col, show_colorbar, bar_width, showgrid_x, showgrid_y, height, width, tasks=..., task_names=..., data=..., group_tasks=..., show_hover_fill=...):
    """
    Refer to FigureFactory.create_gantt() for docstring
    """
    ...

def create_gantt(df, colors=..., index_col=..., show_colorbar=..., reverse_colors=..., title=..., bar_width=..., showgrid_x=..., showgrid_y=..., height=..., width=..., tasks=..., task_names=..., data=..., group_tasks=..., show_hover_fill=...):
    """
    Returns figure for a gantt chart

    :param (array|list) df: input data for gantt chart. Must be either a
        a dataframe or a list. If dataframe, the columns must include
        'Task', 'Start' and 'Finish'. Other columns can be included and
        used for indexing. If a list, its elements must be dictionaries
        with the same required column headers: 'Task', 'Start' and
        'Finish'.
    :param (str|list|dict|tuple) colors: either a plotly scale name, an
        rgb or hex color, a color tuple or a list of colors. An rgb color
        is of the form 'rgb(x, y, z)' where x, y, z belong to the interval
        [0, 255] and a color tuple is a tuple of the form (a, b, c) where
        a, b and c belong to [0, 1]. If colors is a list, it must
        contain the valid color types aforementioned as its members.
        If a dictionary, all values of the indexing column must be keys in
        colors.
    :param (str|float) index_col: the column header (if df is a data
        frame) that will function as the indexing column. If df is a list,
        index_col must be one of the keys in all the items of df.
    :param (bool) show_colorbar: determines if colorbar will be visible.
        Only applies if values in the index column are numeric.
    :param (bool) show_hover_fill: enables/disables the hovertext for the
        filled area of the chart.
    :param (bool) reverse_colors: reverses the order of selected colors
    :param (str) title: the title of the chart
    :param (float) bar_width: the width of the horizontal bars in the plot
    :param (bool) showgrid_x: show/hide the x-axis grid
    :param (bool) showgrid_y: show/hide the y-axis grid
    :param (float) height: the height of the chart
    :param (float) width: the width of the chart

    Example 1: Simple Gantt Chart

    >>> from plotly.figure_factory import create_gantt

    >>> # Make data for chart
    >>> df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-30'),
    ...       dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
    ...       dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')]

    >>> # Create a figure
    >>> fig = create_gantt(df)
    >>> fig.show()


    Example 2: Index by Column with Numerical Entries

    >>> from plotly.figure_factory import create_gantt

    >>> # Make data for chart
    >>> df = [dict(Task="Job A", Start='2009-01-01',
    ...            Finish='2009-02-30', Complete=10),
    ...       dict(Task="Job B", Start='2009-03-05',
    ...            Finish='2009-04-15', Complete=60),
    ...       dict(Task="Job C", Start='2009-02-20',
    ...            Finish='2009-05-30', Complete=95)]

    >>> # Create a figure with Plotly colorscale
    >>> fig = create_gantt(df, colors='Blues', index_col='Complete',
    ...                    show_colorbar=True, bar_width=0.5,
    ...                    showgrid_x=True, showgrid_y=True)
    >>> fig.show()


    Example 3: Index by Column with String Entries

    >>> from plotly.figure_factory import create_gantt

    >>> # Make data for chart
    >>> df = [dict(Task="Job A", Start='2009-01-01',
    ...            Finish='2009-02-30', Resource='Apple'),
    ...       dict(Task="Job B", Start='2009-03-05',
    ...            Finish='2009-04-15', Resource='Grape'),
    ...       dict(Task="Job C", Start='2009-02-20',
    ...            Finish='2009-05-30', Resource='Banana')]

    >>> # Create a figure with Plotly colorscale
    >>> fig = create_gantt(df, colors=['rgb(200, 50, 25)', (1, 0, 1), '#6c4774'],
    ...                    index_col='Resource', reverse_colors=True,
    ...                    show_colorbar=True)
    >>> fig.show()


    Example 4: Use a dictionary for colors

    >>> from plotly.figure_factory import create_gantt
    >>> # Make data for chart
    >>> df = [dict(Task="Job A", Start='2009-01-01',
    ...            Finish='2009-02-30', Resource='Apple'),
    ...       dict(Task="Job B", Start='2009-03-05',
    ...            Finish='2009-04-15', Resource='Grape'),
    ...       dict(Task="Job C", Start='2009-02-20',
    ...            Finish='2009-05-30', Resource='Banana')]

    >>> # Make a dictionary of colors
    >>> colors = {'Apple': 'rgb(255, 0, 0)',
    ...           'Grape': 'rgb(170, 14, 200)',
    ...           'Banana': (1, 1, 0.2)}

    >>> # Create a figure with Plotly colorscale
    >>> fig = create_gantt(df, colors=colors, index_col='Resource',
    ...                    show_colorbar=True)

    >>> fig.show()

    Example 5: Use a pandas dataframe

    >>> from plotly.figure_factory import create_gantt
    >>> import pandas as pd

    >>> # Make data as a dataframe
    >>> df = pd.DataFrame([['Run', '2010-01-01', '2011-02-02', 10],
    ...                    ['Fast', '2011-01-01', '2012-06-05', 55],
    ...                    ['Eat', '2012-01-05', '2013-07-05', 94]],
    ...                   columns=['Task', 'Start', 'Finish', 'Complete'])

    >>> # Create a figure with Plotly colorscale
    >>> fig = create_gantt(df, colors='Blues', index_col='Complete',
    ...                    show_colorbar=True, bar_width=0.5,
    ...                    showgrid_x=True, showgrid_y=True)
    >>> fig.show()
    """
    ...

