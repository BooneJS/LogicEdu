# LogicEdu Tips and Tricks

## Objects

Objects, like AND2 or RegisterFile, contain a shape and one or more Pins.

- shape is often an ArcPolygon unless a Manim shape already exists.
- Pin contains a Manim [Line](https://docs.manim.community/en/stable/reference/manim.mobject.geometry.line.Line.html) and [Dot](https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Dot.html). These Pins can be used by ConnectorLine and ArbitrarySegmentLine for connecting objects in a scene.

## Focusing the viewer's attention

When introducing an architecture, as happens in [examples/cod6_fig4_17.py](examples/cod6_fig4_17.py), dimming the existing architecture and displaying and discussing the new block can be useful to draw the viewer's attention. All objects extend from VGroup and dim_all()/undim_all() are useful helpers.

## Scaling

If an object starts out large and centered, it can be challenging to compute final alignment if, say, you desire this object's input pin to be on the same y-axis location as an existing object's output pin such that ConnectorLine doesn't need Manhatten routing. Manim's scale() function offers kwarg about_point to help; use the new object's `<input_pin>.dot.get_center()` to make computation easier for a smooth animation for scale+shift. [examples/cod6_fig4_17.py](examples/cod6_fig4_17.py) has an example using `about_point`.