#!/usr/bin/python

from __future__ import division
import math
import time
import cairo
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
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

        # Enable anti-aliasing
        cr.set_antialias(cairo.ANTIALIAS_BEST)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        for brush in self.brushes:
            cr.set_source_rgba(*brush.rgba_color)
            cr.set_line_width(brush.width)
        
            if len(brush.stroke) > 1:
                # Move to the first point
                x, y = brush.stroke[0]
                cr.move_to(x, y)

                # Draw curves through intermediate points
                for i in range(1, len(brush.stroke) - 2):
                    x1, y1 = brush.stroke[i]
                    x2, y2 = brush.stroke[i + 1]
                    ctrl_x, ctrl_y = (x1 + x2) / 2, (y1 + y2) / 2
                    cr.curve_to(x1, y1, ctrl_x, ctrl_y, x2, y2)

                # Connect the last two points with a straight line
                x, y = brush.stroke[-1]
                cr.line_to(x, y)

                cr.stroke()

    def clear(self):
        self.brushes = []
        GLib.idle_add(self.draw_area.queue_draw)

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
            if self.mode == "draw":
                
                
                curr_brush.add_point((event.x, event.y))

                start_point = curr_brush.stroke[-2]
                end_point = (event.x, event.y)
                # Only redraw the area between the last and new points
                self.draw_partial(widget, start_point, end_point)
                #
            elif self.mode == "eraser":
                for brush in self.brushes:
                    if brush == curr_brush:
                        continue
                    for x, y in brush.stroke:
                        if (x - event.x)**2 + (y - event.y)**2 < self.eraser_size:
                            if brush in self.brushes:
                                self.brushes.remove(brush)
                GLib.idle_add(widget.queue_draw)

    def draw_partial(self, widget, last_point, new_point):
        if last_point:
            # Get the bounding box of the area to redraw
            x1, y1 = last_point
            x2, y2 = new_point
            x_min, y_min, x_max, y_max = min(x1, x2)-10, min(y1, y2)-10, max(x1, x2)+10, max(y1, y2)+10

            # Queue a draw only for the specified area
            widget.queue_draw_area(int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min))


    def mouse_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            brush = Brush(self.brush_width, self.rgba_color)
            brush.add_point((event.x, event.y))
            self.brushes.append(brush)
            widget.queue_draw()
        elif event.button == Gdk.BUTTON_SECONDARY:
            if self.mode == "draw":
                self.mode = "eraser"
            else:
                self.mode = "draw"
            #self.brushes = []

    def mouse_release(self, widget, event):
        widget.queue_draw()


