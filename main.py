from canvas import *
from background import *
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
        self.background = Background()
        self.tools = DrawTools(self.fixed)

        self.fixed.put(self.background, 0, 0)
        self.fixed.put(self.canvas.draw_area, 0, 0)
        self.fixed.put(self.tools, 0, 0)

        
        exit_button = Gtk.Button(label="Exit")
        exit_button.connect("clicked", Gtk.main_quit)
        self.tools.pack_start(exit_button, False, False, 0)


        def draw_event(widget=None):
            self.canvas.mode = "draw"
        draw_button = Gtk.Button(label="Draw")
        draw_button.connect("clicked", draw_event)
        self.tools.pack_start(draw_button, False, False, 0)

        def erase_event(widget=None):
            self.canvas.mode = "eraser"
        erase_button = Gtk.Button(label="Erase")
        erase_button.connect("clicked", erase_event)
        self.tools.pack_start(erase_button, False, False, 0)
        

        def clear_event(widget=None):
            self.canvas.clear()
        clear_button = Gtk.Button(label="Clear")
        clear_button.connect("clicked", clear_event)
        self.tools.pack_start(clear_button, False, False, 0)


        def blank_event(widget=None):
            if self.background.type == "blank":
                self.background.set_type("transparent")
            else:
                self.background.set_type("blank")            
        blank_button = Gtk.Button(label="blank_button")
        blank_button.connect("clicked", blank_event)
        self.tools.pack_start(blank_button, False, False, 0)

        self.window.show_all()
        self.window.fullscreen()
        self.window.connect("size-allocate", self.resize)


    def resize(self, widget, event):
        w, h = widget.get_size()
        self.canvas.draw_area.set_size_request(w, h)
        self.background.set_size_request(w, h)
        self.window.fullscreen()

if __name__ == "__main__":
    draw = DrawingApp(400, 400)
    Gtk.main()
