import gi
from gi.repository import Gtk, Gdk, GLib

class Background(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.connect("draw", self.draw)
        self.type = "blank"

    def set_type(self, new):
        self.type = new
        GLib.idle_add(self.queue_draw)

    def draw(self, widget, context):


        if self.type == "blank":
            context.set_source_rgb(1, 1, 1)  # RGB values for white
            context.paint()

        context.stroke()
