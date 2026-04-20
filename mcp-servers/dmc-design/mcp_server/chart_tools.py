"""
Chart creation tools using Plotly.

Provides tools for creating data visualizations with automatic theme integration.
"""
import base64
import logging
import os
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

# Check for kaleido availability
KALEIDO_AVAILABLE = False
try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    logger.debug("kaleido not installed - chart export will be unavailable")


# Default color palette based on Mantine theme
DEFAULT_COLORS = [
    "#228be6",  # blue
    "#40c057",  # green
    "#fa5252",  # red
    "#fab005",  # yellow
    "#7950f2",  # violet
    "#fd7e14",  # orange
    "#20c997",  # teal
    "#f783ac",  # pink
    "#868e96",  # gray
    "#15aabf",  # cyan
]


class ChartTools:
    """
    Plotly-based chart creation tools.

    Creates charts that integrate with DMC theming system.
    """

    def __init__(self, theme_store=None):
        """
        Initialize chart tools.

        Args:
            theme_store: Optional ThemeStore for theme token resolution
        """
        self.theme_store = theme_store
        self._active_theme = None

    def set_theme(self, theme: Dict[str, Any]) -> None:
        """Set the active theme for chart styling."""
        self._active_theme = theme

    def _get_color_palette(self) -> List[str]:
        """Get color palette from theme or defaults."""
        if self._active_theme and 'colors' in self._active_theme:
            colors = self._active_theme['colors']
            # Extract primary colors from theme
            palette = []
            for key in ['primary', 'secondary', 'success', 'warning', 'error']:
                if key in colors:
                    palette.append(colors[key])
            if palette:
                return palette + DEFAULT_COLORS[len(palette):]
        return DEFAULT_COLORS

    def _resolve_color(self, color: Optional[str]) -> str:
        """Resolve a color token to actual color value."""
        if not color:
            return self._get_color_palette()[0]

        # Check if it's a theme token
        if self._active_theme and 'colors' in self._active_theme:
            colors = self._active_theme['colors']
            if color in colors:
                return colors[color]

        # Check if it's already a valid color
        if color.startswith('#') or color.startswith('rgb'):
            return color

        # Map common color names to palette
        color_map = {
            'blue': DEFAULT_COLORS[0],
            'green': DEFAULT_COLORS[1],
            'red': DEFAULT_COLORS[2],
            'yellow': DEFAULT_COLORS[3],
            'violet': DEFAULT_COLORS[4],
            'orange': DEFAULT_COLORS[5],
            'teal': DEFAULT_COLORS[6],
            'pink': DEFAULT_COLORS[7],
            'gray': DEFAULT_COLORS[8],
            'cyan': DEFAULT_COLORS[9],
        }
        return color_map.get(color, color)

    async def chart_create(
        self,
        chart_type: str,
        data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Plotly chart.

        Args:
            chart_type: Type of chart (line, bar, scatter, pie, heatmap, histogram, area)
            data: Data specification with x, y values or labels/values for pie
            options: Optional chart options (title, color, layout settings)

        Returns:
            Dict with:
                - figure: Plotly figure JSON
                - chart_type: Type of chart created
                - error: Error message if creation failed
        """
        options = options or {}

        # Validate chart type
        valid_types = ['line', 'bar', 'scatter', 'pie', 'heatmap', 'histogram', 'area']
        if chart_type not in valid_types:
            return {
                "error": f"Invalid chart_type '{chart_type}'. Must be one of: {valid_types}",
                "chart_type": chart_type,
                "figure": None
            }

        try:
            # Build trace based on chart type
            trace = self._build_trace(chart_type, data, options)
            if 'error' in trace:
                return trace

            # Build layout
            layout = self._build_layout(options)

            # Create figure structure
            figure = {
                "data": [trace],
                "layout": layout
            }

            return {
                "figure": figure,
                "chart_type": chart_type,
                "trace_count": 1
            }

        except Exception as e:
            logger.error(f"Chart creation failed: {e}")
            return {
                "error": str(e),
                "chart_type": chart_type,
                "figure": None
            }

    def _build_trace(
        self,
        chart_type: str,
        data: Dict[str, Any],
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build Plotly trace for the chart type."""
        color = self._resolve_color(options.get('color'))
        palette = self._get_color_palette()

        # Common trace properties
        trace: Dict[str, Any] = {}

        if chart_type == 'line':
            trace = {
                "type": "scatter",
                "mode": "lines+markers",
                "x": data.get('x', []),
                "y": data.get('y', []),
                "line": {"color": color},
                "marker": {"color": color}
            }
            if 'name' in data:
                trace['name'] = data['name']

        elif chart_type == 'bar':
            trace = {
                "type": "bar",
                "x": data.get('x', []),
                "y": data.get('y', []),
                "marker": {"color": color}
            }
            if options.get('horizontal'):
                trace['orientation'] = 'h'
                trace['x'], trace['y'] = trace['y'], trace['x']
            if 'name' in data:
                trace['name'] = data['name']

        elif chart_type == 'scatter':
            trace = {
                "type": "scatter",
                "mode": "markers",
                "x": data.get('x', []),
                "y": data.get('y', []),
                "marker": {
                    "color": color,
                    "size": options.get('marker_size', 10)
                }
            }
            if 'size' in data:
                trace['marker']['size'] = data['size']
            if 'name' in data:
                trace['name'] = data['name']

        elif chart_type == 'pie':
            labels = data.get('labels', data.get('x', []))
            values = data.get('values', data.get('y', []))
            trace = {
                "type": "pie",
                "labels": labels,
                "values": values,
                "marker": {"colors": palette[:len(labels)]}
            }
            if options.get('donut'):
                trace['hole'] = options.get('hole', 0.4)

        elif chart_type == 'heatmap':
            trace = {
                "type": "heatmap",
                "z": data.get('z', data.get('values', [])),
                "x": data.get('x', []),
                "y": data.get('y', []),
                "colorscale": options.get('colorscale', 'Blues')
            }

        elif chart_type == 'histogram':
            trace = {
                "type": "histogram",
                "x": data.get('x', data.get('values', [])),
                "marker": {"color": color}
            }
            if 'nbins' in options:
                trace['nbinsx'] = options['nbins']

        elif chart_type == 'area':
            trace = {
                "type": "scatter",
                "mode": "lines",
                "x": data.get('x', []),
                "y": data.get('y', []),
                "fill": "tozeroy",
                "line": {"color": color},
                "fillcolor": color.replace(')', ', 0.3)').replace('rgb', 'rgba') if color.startswith('rgb') else color + '4D'
            }
            if 'name' in data:
                trace['name'] = data['name']

        else:
            return {"error": f"Unsupported chart type: {chart_type}"}

        return trace

    def _build_layout(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Build Plotly layout from options."""
        layout: Dict[str, Any] = {
            "autosize": True,
            "margin": {"l": 50, "r": 30, "t": 50, "b": 50}
        }

        # Title
        if 'title' in options:
            layout['title'] = {
                "text": options['title'],
                "x": 0.5,
                "xanchor": "center"
            }

        # Axis labels
        if 'x_label' in options:
            layout['xaxis'] = layout.get('xaxis', {})
            layout['xaxis']['title'] = options['x_label']

        if 'y_label' in options:
            layout['yaxis'] = layout.get('yaxis', {})
            layout['yaxis']['title'] = options['y_label']

        # Theme-based styling
        if self._active_theme:
            colors = self._active_theme.get('colors', {})
            bg = colors.get('background', {})

            if isinstance(bg, dict):
                layout['paper_bgcolor'] = bg.get('base', '#ffffff')
                layout['plot_bgcolor'] = bg.get('subtle', '#f8f9fa')
            elif isinstance(bg, str):
                layout['paper_bgcolor'] = bg
                layout['plot_bgcolor'] = bg

            text_color = colors.get('text', {})
            if isinstance(text_color, dict):
                layout['font'] = {'color': text_color.get('primary', '#212529')}
            elif isinstance(text_color, str):
                layout['font'] = {'color': text_color}

        # Additional layout options
        if 'showlegend' in options:
            layout['showlegend'] = options['showlegend']

        if 'height' in options:
            layout['height'] = options['height']

        if 'width' in options:
            layout['width'] = options['width']

        return layout

    async def chart_configure_interaction(
        self,
        figure: Dict[str, Any],
        interactions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configure interactions for a chart.

        Args:
            figure: Plotly figure JSON to modify
            interactions: Interaction configuration:
                - hover_template: Custom hover text template
                - click_data: Enable click data capture
                - selection: Enable selection (box, lasso)
                - zoom: Enable/disable zoom

        Returns:
            Dict with:
                - figure: Updated figure JSON
                - interactions_added: List of interactions configured
                - error: Error message if configuration failed
        """
        if not figure or 'data' not in figure:
            return {
                "error": "Invalid figure: must contain 'data' key",
                "figure": figure,
                "interactions_added": []
            }

        try:
            interactions_added = []

            # Process each trace
            for i, trace in enumerate(figure['data']):
                # Hover template
                if 'hover_template' in interactions:
                    trace['hovertemplate'] = interactions['hover_template']
                    if i == 0:
                        interactions_added.append('hover_template')

                # Custom hover info
                if 'hover_info' in interactions:
                    trace['hoverinfo'] = interactions['hover_info']
                    if i == 0:
                        interactions_added.append('hover_info')

            # Layout-level interactions
            layout = figure.get('layout', {})

            # Click data (Dash callback integration)
            if interactions.get('click_data', False):
                layout['clickmode'] = 'event+select'
                interactions_added.append('click_data')

            # Selection mode
            if 'selection' in interactions:
                sel_mode = interactions['selection']
                if sel_mode in ['box', 'lasso', 'box+lasso']:
                    layout['dragmode'] = 'select' if sel_mode == 'box' else sel_mode
                    interactions_added.append(f'selection:{sel_mode}')

            # Zoom configuration
            if 'zoom' in interactions:
                if not interactions['zoom']:
                    layout['xaxis'] = layout.get('xaxis', {})
                    layout['yaxis'] = layout.get('yaxis', {})
                    layout['xaxis']['fixedrange'] = True
                    layout['yaxis']['fixedrange'] = True
                    interactions_added.append('zoom:disabled')
                else:
                    interactions_added.append('zoom:enabled')

            # Modebar configuration
            if 'modebar' in interactions:
                layout['modebar'] = interactions['modebar']
                interactions_added.append('modebar')

            figure['layout'] = layout

            return {
                "figure": figure,
                "interactions_added": interactions_added
            }

        except Exception as e:
            logger.error(f"Interaction configuration failed: {e}")
            return {
                "error": str(e),
                "figure": figure,
                "interactions_added": []
            }

    async def chart_export(
        self,
        figure: Dict[str, Any],
        format: str = "png",
        width: Optional[int] = None,
        height: Optional[int] = None,
        scale: float = 2.0,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export a Plotly chart to a static image format.

        Args:
            figure: Plotly figure JSON to export
            format: Output format - png, svg, or pdf
            width: Image width in pixels (default: from figure or 1200)
            height: Image height in pixels (default: from figure or 800)
            scale: Resolution scale factor (default: 2 for retina)
            output_path: Optional file path to save the image

        Returns:
            Dict with:
                - image_data: Base64-encoded image (if no output_path)
                - file_path: Path to saved file (if output_path provided)
                - format: Export format used
                - dimensions: {width, height, scale}
                - error: Error message if export failed
        """
        # Validate format
        valid_formats = ['png', 'svg', 'pdf']
        format = format.lower()
        if format not in valid_formats:
            return {
                "error": f"Invalid format '{format}'. Must be one of: {valid_formats}",
                "format": format,
                "image_data": None
            }

        # Check kaleido availability
        if not KALEIDO_AVAILABLE:
            return {
                "error": "kaleido package not installed. Install with: pip install kaleido",
                "format": format,
                "image_data": None,
                "install_hint": "pip install kaleido"
            }

        # Validate figure
        if not figure or 'data' not in figure:
            return {
                "error": "Invalid figure: must contain 'data' key",
                "format": format,
                "image_data": None
            }

        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            # Create Plotly figure object
            fig = go.Figure(figure)

            # Determine dimensions
            layout = figure.get('layout', {})
            export_width = width or layout.get('width') or 1200
            export_height = height or layout.get('height') or 800

            # Export to bytes
            image_bytes = pio.to_image(
                fig,
                format=format,
                width=export_width,
                height=export_height,
                scale=scale
            )

            result = {
                "format": format,
                "dimensions": {
                    "width": export_width,
                    "height": export_height,
                    "scale": scale,
                    "effective_width": int(export_width * scale),
                    "effective_height": int(export_height * scale)
                }
            }

            # Save to file or return base64
            if output_path:
                # Ensure directory exists
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

                # Add extension if missing
                if not output_path.endswith(f'.{format}'):
                    output_path = f"{output_path}.{format}"

                with open(output_path, 'wb') as f:
                    f.write(image_bytes)

                result["file_path"] = output_path
                result["file_size_bytes"] = len(image_bytes)
            else:
                # Return as base64
                result["image_data"] = base64.b64encode(image_bytes).decode('utf-8')
                result["data_uri"] = f"data:image/{format};base64,{result['image_data']}"

            return result

        except ImportError as e:
            logger.error(f"Chart export failed - missing dependency: {e}")
            return {
                "error": f"Missing dependency for export: {e}",
                "format": format,
                "image_data": None,
                "install_hint": "pip install plotly kaleido"
            }
        except Exception as e:
            logger.error(f"Chart export failed: {e}")
            return {
                "error": str(e),
                "format": format,
                "image_data": None
            }
