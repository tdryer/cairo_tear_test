# cairo\_tear\_test

A GTK+ 3 utility for testing screen tearing and frame rate. It draws a white vertical bar sweeping back and forth over a black background. Drawing is done using Cairo in a GtkDrawingArea. It should run without any extra dependencies on Ubuntu 12.04 and greater.

I wrote this is see how feasible it is to use Cairo for smooth tear-free animation on Linux.

Features:

 * double buffering toggles for window and drawing area
 * adjustable frame rate

Using Ubuntu 12.10, the NVIDIA 310 driver, and a 60 Hz LCD monitor, I did a few tests using different window managers:

* GNOME-shell (compositing window manager with vsync)
   * intermittent tearing near the top of the screen
   * turning off double buffering reduces tearing
* Compiz (compositing window manager with vsync)
   * absolutely no tearing
   * turning off double buffering can cause flickering
* Metacity/xfwm4/xmonad (non-compositing window managers)
   * constant tearing
   * changing the frame rate farther from the monitors refresh rate makes the tearing more severe
   * turning off double buffering causes a moving horizontal stripe of the screen to not be drawn rather than a simple tear

Conclusions:

 * 60 frames per second are required to make the animation look smooth
 * use a compositing window manager (with OpenGL vsync enabled) if you don't want tearing
 * GNOME-shell still has some tearing (it doesn't handle vsync as well as Compiz does?)
 * render as close as the monitor's refresh rate as possible, and use double buffering

