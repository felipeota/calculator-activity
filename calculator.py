#!/usr/bin/env python

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
    pass
try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)

from parse import run_calculator

tokens = {
	"add": "+",
	"subtract": "-",
	"multiply": "*",
	"divide": "/",
	"decimal": "."
}

for i in xrange(0,10):
	tokens[str(i)] = str(i)

class Calculator:
	def __init__(self, accel_group = None):
		self.accel_group = accel_group or gtk.AccelGroup()
		self.expression = "" 
		self.gladefile = "calculator.glade" 
		self.glade = gtk.Builder()
		try:
			self.glade.add_from_file(self.gladefile)
		except:
			print("error loading calculator.glade file!")
		self.main_window = self.glade.get_object("main")
		if self.main_window != None:
			self.main_widget = self.main_window.get_child()
		for key, value in tokens.iteritems():
			def scope(key, value):
				button = self.glade.get_object("button_" + key)
				if button == None:
					return
				button.connect("clicked", lambda _: self.on_button_token_clicked(value))
				button.add_accelerator("clicked", self.accel_group, ord(value), 0, gtk.ACCEL_VISIBLE)
				button.add_accelerator("clicked", self.accel_group, getattr(gtk.keysyms, "KP_" + key.capitalize()), 0, gtk.ACCEL_VISIBLE)

			scope(key, value)

		equal = self.glade.get_object("button_equal")
		if equal != None:
			equal.connect("clicked", self.on_equal_clicked)
			equal.add_accelerator("clicked", self.accel_group, gtk.keysyms.KP_Enter, 0, gtk.ACCEL_VISIBLE)

		self.display = self.glade.get_object("label_display")
		if self.display != None:
			self.display.set_use_markup(True)
			self.display_expression("0")


	def on_equal_clicked(self, widget):
		try:
			self.expression = str(run_calculator(self.expression)[0].evaluate())
			self.display_expression()
		except:
			self.expression = ""
			self.display_expression("error")
			raise

	def on_button_token_clicked(self, key):
		self.expression += key
		self.display_expression()

	def display_expression(self, expression = None):
		if self.display == None:
			return
		expression = expression or self.expression
		self.display.set_use_markup(True)
		self.display.set_markup("<span font_weight='bold' size='x-large'>%s</span>" % expression)

	def setup_main_window(self):
		if self.main_window == None:
			return
		self.main_window.add_accel_group(self.accel_group)
		self.main_window.show_all()
		self.main_window.connect("destroy", gtk.main_quit)		

	def release_main_widget(self):
		"Needed by sugar activity, so the main_widget can be added to the activity's top level"
		if self.main_window != None:
			self.main_window.remove(self.main_widget)

	def main(self):
		self.setup_main_window()
		gtk.main()

if __name__ == "__main__":
	calc = Calculator()
	calc.main()