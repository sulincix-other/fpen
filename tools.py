import gi
from gi.repository import Gtk, Gdk

class DrawTools(Gtk.Box):
    def __init__(self, parent):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.parent = parent
        move = Gtk.Button("...")
        move.set_relief(False)
        self.pack_start(move,False,False,0)
        move.connect("motion-notify-event", self.move_event)

    def move_event(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            alloc = self.parent.get_allocation()
            curalloc = self.get_allocation()

            newx = event.x_root - curalloc.width / 2
            newy = event.y_root - curalloc.height / 2

            # Ensure the button stays within the bounds of the parent widget
            newx = max(0, min(newx, alloc.width - curalloc.width))
            newy = max(0, min(newy, alloc.height - curalloc.height))

            self.parent.move(self, newx, newy)


