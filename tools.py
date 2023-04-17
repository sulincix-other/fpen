import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
class DrawTools(Gtk.Box):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        move = Gtk.Button("...")
        move.set_relief(False)
        self.add(move)
        move.connect("motion-notify-event",self.move_event)
    def move_event(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            alloc = self.parent.get_allocation()
            curalloc = self.get_allocation()
            wgalloc = self.get_allocation()
            newx = event.x_root - curalloc.width / 2
            newy = event.y_root - wgalloc.height / 2
            if newx > alloc.width - curalloc.width:
                newx = alloc.width - curalloc.width
            if newy > alloc.height - curalloc.height:
                newy = alloc.height - curalloc.height
            self.parent.move(self, newx, newy)
