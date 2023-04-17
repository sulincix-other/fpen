#!/usr/bin/python

from __future__ import division
import math
import time
import cairo
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import random

class Brush(object):
    def __init__(self, width, rgba_color):
        self.width = width
        self.rgba_color = rgba_color
        self.stroke = []

    def add_point(self, point):
        self.stroke.append(point)

class Canvas(object):
    def __init__(self):
        self.draw_area = self.init_draw_area()
        self.brushes = []
        self.rgba_color = (252/255, 161/255, 3/255, 1)
        self.brush_width = 3
        self.eraser_size = 50**2
        self.mode = "draw"

    def draw(self, widget, cr):
        da = widget
        cr.set_source_rgba(1, 1, 1, 0.1)
        cr.paint()
        #cr.set_operator(cairo.OPERATOR_SOURCE)#gets rid over overlap, but problematic with multiple colors
        for brush in self.brushes:
            cr.set_source_rgba(*brush.rgba_color)
            cr.set_line_width(brush.width)
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in brush.stroke:
                cr.line_to(x, y)
            cr.stroke()

    def init_draw_area(self):
        draw_area = Gtk.DrawingArea()
        draw_area.connect('draw', self.draw)
        draw_area.connect('motion-notify-event', self.mouse_move)
        draw_area.connect('button-press-event', self.mouse_press)
        draw_area.connect('button-release-event', self.mouse_release)
        draw_area.set_events(draw_area.get_events() |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK)
        return draw_area

    def mouse_move(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            curr_brush = self.brushes[-1]
            curr_brush.add_point((event.x, event.y))
            widget.queue_draw()
            if self.mode == "eraser":
                for brush in self.brushes:
                    if brush == curr_brush:
                        continue
                    for x, y in brush.stroke:
                        if (x - event.x)**2 + (y - event.y)**2 < self.eraser_size:
                            if brush in self.brushes:
                                self.brushes.remove(brush)

    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            brush = Brush(self.brush_width, self.rgba_color)
            brush.add_point((event.x, event.y))
            self.brushes.append(brush)
            widget.queue_draw()
        elif event.button == Gdk.BUTTON_SECONDARY:
            self.brushes = []

    def mouse_release(self, widget, event):
        widget.queue_draw()


