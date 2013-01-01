#!/usr/bin/env python2.7

"""cairo_tear_test"""

from gi.repository import Gtk, GObject #pylint: disable=E0611
from datetime import datetime
from math import sin, pi

class Clock():
    """Allow tracking framerate and total ellapsed time."""

    def __init__(self):
        self.last_tick = None
        self.start_time = None

    def tick(self):
        """Update last_tick."""
        now = datetime.now()
        if self.last_tick:
            elapsed = now - self.last_tick # TODO: use this to track actual fps
        else:
            self.start_time = now
        self.last_tick = now

    def get_time_millis(self):
        """Return milliseconds since first tick."""
        elapsed = datetime.now() - self.start_time
        return elapsed.total_seconds() * 1000

class MainWindow():
    """Wrapper for the GtkWindow."""

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("window1.glade")
        builder.connect_signals(self)

        self.window = builder.get_object("window1")
        self.drawingarea = builder.get_object("drawingarea1")
        self.db_window_check = builder.get_object("db_window_check")
        self.db_drawing_area_check = builder.get_object("db_drawing_area_check")
        self.fps_spin = builder.get_object("fps_spin")

        self.tick_period = 0
        self.on_option_changed(None) # sync options with defaults
        self.clock = Clock()

        self.window.show()
        self.tick() # start ticking

    def tick(self):
        """Redraw the drawing area and set timeout to call again."""
        self.clock.tick()
        self.drawingarea.queue_draw()
        GObject.timeout_add(self.tick_period, self.tick)
        return False # stop timeout from reoccurring automatically

    def on_window1_destroy(self, widget, data=None):
        """End process when window is closed."""
        Gtk.main_quit()

    def on_option_changed(self, widget, data=None):
        """Apply changes to options."""
        self.window.set_double_buffered(self.db_window_check.get_active())
        self.drawingarea.set_double_buffered(
                self.db_drawing_area_check.get_active())
        self.tick_period = 1000 / self.fps_spin.get_value_as_int()

    def on_drawingarea1_draw(self, widget, cr, data=None):
        "Draw in the drawing area."""
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()

        # fill black background
        cr.set_source_rgb(0, 0, 0)
        cr.paint()

        # draw vertical white bar moving side to side
        cr.set_source_rgb(1, 1, 1)
        bar_width = width/10
        period_millis = 2000
        cr.set_line_width(bar_width)
        time = self.clock.get_time_millis() % period_millis
        bar_center_x = (sin(2 * pi * time / period_millis) + 1) * (width / 2)
        cr.move_to(bar_center_x, 0)
        cr.line_to(bar_center_x, height)
        cr.stroke()

if __name__ == "__main__":
    MainWindow()
    Gtk.main()
