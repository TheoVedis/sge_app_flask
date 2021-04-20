"""
This type stub file was generated by pyright.
"""

_window_plotly_config = ...
_mathjax_config = ...
def to_html(fig, config=..., auto_play=..., include_plotlyjs=..., include_mathjax=..., post_script=..., full_html=..., animation_opts=..., default_width=..., default_height=..., validate=...):
    """
    Convert a figure to an HTML string representation.

    Parameters
    ----------
    fig:
        Figure object or dict representing a figure
    config: dict or None (default None)
        Plotly.js figure config options
    auto_play: bool (default=True)
        Whether to automatically start the animation sequence on page load
        if the figure contains frames. Has no effect if the figure does not
        contain frames.
    include_plotlyjs: bool or string (default True)
        Specifies how the plotly.js library is included/loaded in the output
        div string.

        If True, a script tag containing the plotly.js source code (~3MB)
        is included in the output.  HTML files generated with this option are
        fully self-contained and can be used offline.

        If 'cdn', a script tag that references the plotly.js CDN is included
        in the output. HTML files generated with this option are about 3MB
        smaller than those generated with include_plotlyjs=True, but they
        require an active internet connection in order to load the plotly.js
        library.

        If 'directory', a script tag is included that references an external
        plotly.min.js bundle that is assumed to reside in the same
        directory as the HTML file.

        If 'require', Plotly.js is loaded using require.js.  This option
        assumes that require.js is globally available and that it has been
        globally configured to know how to find Plotly.js as 'plotly'.
        This option is not advised when full_html=True as it will result
        in a non-functional html file.

        If a string that ends in '.js', a script tag is included that
        references the specified path. This approach can be used to point
        the resulting HTML file to an alternative CDN or local bundle.

        If False, no script tag referencing plotly.js is included. This is
        useful when the resulting div string will be placed inside an HTML
        document that already loads plotly.js. This option is not advised
        when full_html=True as it will result in a non-functional html file.
    include_mathjax: bool or string (default False)
        Specifies how the MathJax.js library is included in the output html
        div string.  MathJax is required in order to display labels
        with LaTeX typesetting.

        If False, no script tag referencing MathJax.js will be included in the
        output.

        If 'cdn', a script tag that references a MathJax CDN location will be
        included in the output.  HTML div strings generated with this option
        will be able to display LaTeX typesetting as long as internet access
        is available.

        If a string that ends in '.js', a script tag is included that
        references the specified path. This approach can be used to point the
        resulting HTML div string to an alternative CDN.
    post_script: str or list or None (default None)
        JavaScript snippet(s) to be included in the resulting div just after
        plot creation.  The string(s) may include '{plot_id}' placeholders
        that will then be replaced by the `id` of the div element that the
        plotly.js figure is associated with.  One application for this script
        is to install custom plotly.js event handlers.
    full_html: bool (default True)
        If True, produce a string containing a complete HTML document
        starting with an <html> tag.  If False, produce a string containing
        a single <div> element.
    animation_opts: dict or None (default None)
        dict of custom animation parameters to be passed to the function
        Plotly.animate in Plotly.js. See
        https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
        for available options. Has no effect if the figure does not contain
        frames, or auto_play is False.
    default_width, default_height: number or str (default '100%')
        The default figure width/height to use if the provided figure does not
        specify its own layout.width/layout.height property.  May be
        specified in pixels as an integer (e.g. 500), or as a css width style
        string (e.g. '500px', '100%').
    validate: bool (default True)
        True if the figure should be validated before being converted to
        JSON, False otherwise.
    Returns
    -------
    str
        Representation of figure as an HTML div string
    """
    ...

def write_html(fig, file, config=..., auto_play=..., include_plotlyjs=..., include_mathjax=..., post_script=..., full_html=..., animation_opts=..., validate=..., default_width=..., default_height=..., auto_open=...):
    """
    Write a figure to an HTML file representation

    Parameters
    ----------
    fig:
        Figure object or dict representing a figure
    file: str or writeable
        A string representing a local file path or a writeable object
        (e.g. an open file descriptor)
    config: dict or None (default None)
        Plotly.js figure config options
    auto_play: bool (default=True)
        Whether to automatically start the animation sequence on page load
        if the figure contains frames. Has no effect if the figure does not
        contain frames.
    include_plotlyjs: bool or string (default True)
        Specifies how the plotly.js library is included/loaded in the output
        div string.

        If True, a script tag containing the plotly.js source code (~3MB)
        is included in the output.  HTML files generated with this option are
        fully self-contained and can be used offline.

        If 'cdn', a script tag that references the plotly.js CDN is included
        in the output. HTML files generated with this option are about 3MB
        smaller than those generated with include_plotlyjs=True, but they
        require an active internet connection in order to load the plotly.js
        library.

        If 'directory', a script tag is included that references an external
        plotly.min.js bundle that is assumed to reside in the same
        directory as the HTML file. If `file` is a string to a local file path
        and `full_html` is True then

        If 'directory', a script tag is included that references an external
        plotly.min.js bundle that is assumed to reside in the same
        directory as the HTML file.  If `file` is a string to a local file
        path and `full_html` is True, then the plotly.min.js bundle is copied
        into the directory of the resulting HTML file. If a file named
        plotly.min.js already exists in the output directory then this file
        is left unmodified and no copy is performed. HTML files generated
        with this option can be used offline, but they require a copy of
        the plotly.min.js bundle in the same directory. This option is
        useful when many figures will be saved as HTML files in the same
        directory because the plotly.js source code will be included only
        once per output directory, rather than once per output file.

        If 'require', Plotly.js is loaded using require.js.  This option
        assumes that require.js is globally available and that it has been
        globally configured to know how to find Plotly.js as 'plotly'.
        This option is not advised when full_html=True as it will result
        in a non-functional html file.

        If a string that ends in '.js', a script tag is included that
        references the specified path. This approach can be used to point
        the resulting HTML file to an alternative CDN or local bundle.

        If False, no script tag referencing plotly.js is included. This is
        useful when the resulting div string will be placed inside an HTML
        document that already loads plotly.js.  This option is not advised
        when full_html=True as it will result in a non-functional html file.

    include_mathjax: bool or string (default False)
        Specifies how the MathJax.js library is included in the output html
        div string.  MathJax is required in order to display labels
        with LaTeX typesetting.

        If False, no script tag referencing MathJax.js will be included in the
        output.

        If 'cdn', a script tag that references a MathJax CDN location will be
        included in the output.  HTML div strings generated with this option
        will be able to display LaTeX typesetting as long as internet access
        is available.

        If a string that ends in '.js', a script tag is included that
        references the specified path. This approach can be used to point the
        resulting HTML div string to an alternative CDN.
    post_script: str or list or None (default None)
        JavaScript snippet(s) to be included in the resulting div just after
        plot creation.  The string(s) may include '{plot_id}' placeholders
        that will then be replaced by the `id` of the div element that the
        plotly.js figure is associated with.  One application for this script
        is to install custom plotly.js event handlers.
    full_html: bool (default True)
        If True, produce a string containing a complete HTML document
        starting with an <html> tag.  If False, produce a string containing
        a single <div> element.
    animation_opts: dict or None (default None)
        dict of custom animation parameters to be passed to the function
        Plotly.animate in Plotly.js. See
        https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
        for available options. Has no effect if the figure does not contain
        frames, or auto_play is False.
    default_width, default_height: number or str (default '100%')
        The default figure width/height to use if the provided figure does not
        specify its own layout.width/layout.height property.  May be
        specified in pixels as an integer (e.g. 500), or as a css width style
        string (e.g. '500px', '100%').
    validate: bool (default True)
        True if the figure should be validated before being converted to
        JSON, False otherwise.
    auto_open: bool (default True
        If True, open the saved file in a web browser after saving.
        This argument only applies if `full_html` is True.
    Returns
    -------
    str
        Representation of figure as an HTML div string
    """
    ...

