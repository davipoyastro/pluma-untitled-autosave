#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Save unsaved documents when losing focus.
# Gautier Portet <kassoulet gmail.com>
# Davi Poyastro

from gi.repository import GObject, Gtk, Gdk, Pluma, Gio
import datetime
import os

# You can change here the default folder for unsaved files.
dirname = "file://" + str(os.path.expanduser("~/.pluma_unsaved/"))

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
            os.makedirs(dir)

class FocusAutoSavePlugin(GObject.Object, Pluma.WindowActivatable):
    __gtype_name__ = "FocusAutoSavePlugin"
    window = GObject.property(type=Pluma.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def on_focus_out_event(self, widget, focus):
        for n, doc in enumerate(self.window.get_unsaved_documents()):
            if doc.is_untouched():
                # nothing to do
                continue
            if doc.get_readonly():
                # nothing to do
                continue
            if doc.get_uri() is None:
                # provide a default filename
                now = datetime.datetime.now()
                assure_path_exists(dirname)
                filename = now.strftime(dirname + "unsaved_%Y%m%d-%H%M%S-%%d.txt") % (n + 1)
                print("autosaved " + str(filename))
                doc.set_uri(str(filename))
                Pluma.commands_save_document(self.window, doc)
            elif dirname in str(doc.get_uri()):
                Pluma.commands_save_document(self.window, doc)

    def do_activate(self):
        self.signal = self.window.connect("focus-out-event", self.on_focus_out_event)

    def do_deactivate(self):
        self.window.disconnect(self.signal)
        del self.signal



