from sugar.activity import activity
import logging

import sys, os
import gtk
from calculator import Calculator

class CalculatorActivity(activity.Activity):

   def __init__(self, handle):
      activity.Activity.__init__(self, handle)

      toolbox = activity.ActivityToolbox(self)
      self.set_toolbox(toolbox)
      toolbox.show()

      self.calculator = Calculator(self.get_data('sugar-accel-group'))
      self.calculator.release_main_widget()
      self.set_canvas(self.calculator.main_widget)