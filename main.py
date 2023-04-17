from canvas import *
from tools import *
class DrawingApp(object):
    def __init__(self, width, height):
        self.window = Gtk.Window()
        # Transparent background
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.window.set_visual(visual)
        self.window.set_app_paintable(True)


        self.window.connect('destroy', Gtk.main_quit)
        self.fixed = Gtk.Fixed()
        self.window.add(self.fixed)
        self.canvas = Canvas()
        self.tools = DrawTools(self.fixed)

        self.fixed.put(self.canvas.draw_area, 0, 0)
        self.fixed.put(self.tools, 0, 0)

        self.window.show_all()
        self.window.fullscreen()
        self.window.connect("size-allocate", self.resize)

    def resize(self, widget, event):
        w, h = widget.get_size()
        self.canvas.draw_area.set_size_request(w, h)

if __name__ == "__main__":
    draw = DrawingApp(400, 400)
    Gtk.main()
