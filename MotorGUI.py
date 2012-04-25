###################################################################
#
#         		  		GUI for motor control
#
# 			Author          :   Marc-Olivier Schwartz
# 			E-Mail          :   marcolivier.schwartz@gmal.com
#
###################################################################

# Imports
from PyQt4 import QtGui, QtCore
import time
import os
import sys
import serial
import numpy

# Is the serial port available ?
try:
	ser = serial.Serial('/dev/tty.usbmodemfa131', 9600)
	time.sleep(1)
except:
	print 'No Arduino found'
	sys.exit()

# Main GUI class
class MotorGUI(QtGui.QMainWindow):

	# Initialize the GUI
	def __init__(self, parent=None):
		
		# Main GUI object
		QtGui.QMainWindow.__init__(self, parent)
		
		# Configure windows
		self.setWindowTitle('Motor Control')
		self.setStyleSheet("background-color: white;")
		
		# Create all elements of the window
		self.createWidgets()

		# Declare 
		self.motor_state = 0
		self.speed = 0

		# Start thread to measure speed
		self.workThread = WorkThread()
		self.connect(self.workThread, QtCore.SIGNAL("get_speed"),self.display_speed)
		self.workThread.start()

	# Create all widgets of the GUI
	def createWidgets(self):
		
		# Define fonts of the GUI elements
		buttons_font = QtGui.QFont("Helvetica", 15)
		apply_font = QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
		controls_font = QtGui.QFont("Helvetica", 15)
	
		# Title of the GUI window
		self.labelTitle = QtGui.QLabel("Motor Control")
		self.labelTitle.setFont(QtGui.QFont("Helvetica", 30, QtGui.QFont.Bold))

		# Create all buttons
		self.speed_plus = QtGui.QPushButton("+")
		self.speed_plus.setFont(buttons_font)
		
		self.speed_minus = QtGui.QPushButton("-")
		self.speed_minus.setFont(buttons_font)

		self.state = QtGui.QPushButton("On/Off")
		self.state.setFont(buttons_font)
		
		# LCD widget to display the motor speed
		self.speed_display = QtGui.QLCDNumber(self)

		# Connect different objects
		QtCore.QObject.connect(self.speed_plus, QtCore.SIGNAL("clicked()"), self.plus_clicked)
		QtCore.QObject.connect(self.state, QtCore.SIGNAL("clicked()"), self.state_clicked)
		QtCore.QObject.connect(self.speed_minus, QtCore.SIGNAL("clicked()"), self.minus_clicked)

		# Place different GUI elements
		vbox_left = QtGui.QVBoxLayout()
		vbox_right = QtGui.QVBoxLayout()
		vbox_center = QtGui.QVBoxLayout()

		vbox_center.addWidget(self.speed_plus)
		vbox_center.addWidget(self.speed_minus)

		vbox_right.addWidget(self.state)

		vbox_left.addWidget(self.speed_display)
	
		# Main box
		hbox = QtGui.QHBoxLayout()
		hbox.addLayout(vbox_left)
		hbox.addLayout(vbox_center)
		hbox.addLayout(vbox_right)
	
		# Create central widget, add layout and set
		central_widget = QtGui.QWidget()
		central_widget.setLayout(hbox)
		self.setCentralWidget(central_widget)

	# Actions when button is clicked

	# Increase speed if plus button is clicked
	def plus_clicked(self):
		ser.write('p')

	# Increase speed if plus button is clicked
	def minus_clicked(self):
		ser.write('m')

	# Put the motor on or off depending on the current state
	def state_clicked(self):
		if (self.motor_state == 0):
			ser.write('s')
			self.motor_state = 1

		elif (self.motor_state == 1):
			ser.write('0')
			self.motor_state = 0

	# Display a value on the LCD 
	def display_speed(self,value):

		self.speed_display.display(value)
	
# Thread class for speed measurements
class WorkThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

	# Run the thread and update the LCD driver with speed
	def run(self):
		time.sleep(1)	
		while (1):
			time.sleep(0.5)	

			try:
				ser.write("g")
				speed = ser.read() * 256;
				speed = speed + ser.read()

				s = numpy.frombuffer(speed, numpy.uint8)

				final_speed = 0
				for i in s:
					final_speed = final_speed + i 
				print final_speed
				self.emit(QtCore.SIGNAL("get_speed"), final_speed)
			except:
				print "Can't measure speed !"
  		return

# Init testmode
app = QtGui.QApplication(sys.argv)

qb = MotorGUI()
qb.show()
sys.exit(app.exec_())
