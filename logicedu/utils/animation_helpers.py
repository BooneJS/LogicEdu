"""
Animation helper functions for LogicEdu.

This module provides utility functions for common animation patterns
used in circuit construction and visualization.
"""

from manim import VGroup, Scene
from typing import List, Any


def dim_all_objects(scene: Scene, objects: VGroup, dim_value: float = 0.3):
    """
    Dim all objects in a VGroup to reduce visual clutter.

    Args:
        scene: The Manim scene
        objects: VGroup containing objects to dim
        dim_value: Opacity value for dimmed objects (0.0 to 1.0)
    """
    for obj in objects:
        if hasattr(obj, "dim_all"):
            obj.dim_all()
        else:
            obj.set_opacity(dim_value)
    scene.wait(1)


def undim_all_objects(scene: Scene, objects: VGroup):
    """
    Restore full opacity to all objects in a VGroup.

    Args:
        scene: The Manim scene
        objects: VGroup containing objects to undim
    """
    for obj in objects:
        if hasattr(obj, "undim_all"):
            obj.undim_all()
        else:
            obj.set_opacity(1)
    scene.wait(1)
