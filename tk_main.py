# ||||||||||||||||||||||||||||||||||||||||||||||||||
# |||||||||     hotBox marking menu     ||||||||||||
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PySide2 import QtCore, QtGui, QtWidgets
from ctypes import windll, Structure, c_long, byref

import sys, os.path

from tk_switchboard import Switchboard
import tk_styleSheet as styleSheet

try: import MaxPlus
except: pass





# ------------------------------------------------
#	Mouse Tracking
# ------------------------------------------------
class Point(Structure):
	_fields_ = [("x", c_long), ("y", c_long)]

def getMousePosition():
	pt = Point()
	windll.user32.GetCursorPos(byref(pt))
	return { "x": pt.x, "y": pt.y}

def moveWindow(window, x, y):
	#args: [object], [int], [int]
	mPos = getMousePosition()
	x = mPos['x']+x
	y = mPos['y']+y
	window.move(x, y)




# ------------------------------------------------
# Custom HotBox Widget
# ------------------------------------------------
class HotBox(QtWidgets.QWidget):

	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self)

		self.setObjectName(self.__class__.__name__) #set object name to: 'HotBox'

		#set window style
		self.setWindowFlags(QtCore.Qt.Tool|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyle(QtWidgets.QStyleFactory.create("plastique"))
		self.setStyleSheet(styleSheet.css)
		
		# self.setMouseTracking(True)
		self.mousePosition = None
		self.mousePressEventOn = True
		self.mouseDoubleClickEventOn = True

		self.sb = Switchboard()
		
		self.app = self.sb.setApp(parent)

		self.sb.setClass(self) #add hotbox instance to switchboard dict
		self.signal = self.sb.setClass('tk_signals.Signal')()

		self.layoutStack('init') #initialize layout
		# self.overlay = Overlay(self)
		self.overlay = OverlayFactoryFilter(self)
		self.overlay.setWidget(self)

	def layoutStack(self, index):
		'''
		#args:
			index=int - index for ui in stacked layout
				*or string - name of ui in stacked layout
		'''
		# import timeit
		# t0=timeit.default_timer()

		if type(index)==str:
			index = self.sb.getUiIndex(index)

		if not self.layout(): #if layout doesnt exist; initialize stackedLayout.
			self.stackedLayout = QtWidgets.QStackedLayout()

			for name, ui in self.sb.uiList():
				# store size info for each ui
				self.sb.setUiSize(name, [ui.frameGeometry().width(), ui.frameGeometry().height()])
				# ui.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
				# add ui to layoutStack
				self.stackedLayout.addWidget(ui) #add each ui
			self.setLayout(self.stackedLayout)


		self.index = index
		self.name = self.sb.setUiName(self.index) #get/set current ui name from index
		self.ui = self.sb.getUi() #get the current dymanic ui

		#set ui from stackedLayout
		self.stackedLayout.setCurrentIndex(self.index)

		
		#get ui size for current ui and resize window
		self.width = self.sb.getUiSize(width=1)
		self.height = self.sb.getUiSize(height=1)
		# self.ui.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.resize(self.width, self.height) #window size
		
		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		

		if not self.sb.hasKey(self.name, 'connectionDict'):
			self.signal.buildConnectionDict() #construct the signals and slots for the ui


		if self.name=='init':
			self.sb.getClass('init')().info()
		else:
			#remove old and add new signals for current ui from connectionDict
			if self.name!=self.sb.previousName(allowDuplicates=1):
				if self.sb.previousName():
					# prevUi = self.sb.getUi(self.sb.previousName())
					# prevUi.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
					self.signal.removeSignal(self.sb.previousName())
					self.signal.addSignal(self.name)
				else: #if no previous ui exists
					self.signal.addSignal(self.name)



		#close window when pin unchecked
		# if hasattr (self.ui, 'chkpin'):
		try: self.ui.chkpin.released.connect(self.hide_)
		except: pass

		# t1=timeit.default_timer()
		# print 'time:',t1-t0


		self.mousePressEventOn = True



# ------------------------------------------------
# overrides
# ------------------------------------------------





# ------------------------------------------------


	def hoverEvent(self, event):
		#args: [QEvent]
		print "hover"


	def keyPressEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat(): #Key_Meta or Key_Menu =windows key
			if all ([self.name!="init", self.name!="main", self.name!="viewport"]):
				self.layoutStack('init') #reset layout back to init on keyPressEvent
			
			
	def keyReleaseEvent(self, event):
		#args: [QEvent]
		if event.key()==QtCore.Qt.Key_F12 and not event.isAutoRepeat():
			self.hide_()


	def mousePressEvent(self, event):
		#args: [QEvent]
		if self.mousePressEventOn:
			if any ([self.name=="main", self.name=="viewport", self.name=="init", self.name=="display"]):
				if event.button()==QtCore.Qt.LeftButton:
					self.layoutStack('viewport')
				elif event.button()==QtCore.Qt.RightButton:
					self.layoutStack('main')

					# self.mousePressEventOn = False
					# # self.mouseDoubleClickEventOn = False
					# windll.user32.mouse_event(0x10, 0, 0, 0,0) #right up
					# # windll.user32.mouse_event(0x8, 0, 0, 0,0) #right down
					# self.mousePressEventOn = True
					# # self.mouseDoubleClickEventOn = True
				
				elif event.button()==QtCore.Qt.MiddleButton:
					self.layoutStack('display')


	def mouseDoubleClickEvent(self, event):
		#args: [QEvent]
		#show last used submenu on double mouseclick 
		if self.mouseDoubleClickEventOn:
			if event.button()==QtCore.Qt.RightButton:
				try: self.layoutStack(self.sb.previousName(previousIndex=True))
				except: pass

			if event.button()==QtCore.Qt.LeftButton:
				try:
					self.repeatLastCommand()
				except Exception as error: 
					if not self.sb.prevCommand():
						print "# Warning: No recent commands in history. #"
					else:
						print error


	def mouseMoveEvent(self, event):
		#args: [QEvent]
		if (self.name=="main") or (self.name=="viewport"):
			self.mousePosition = event.pos()
			self.update()
		elif self.name!="init" and event.buttons()==QtCore.Qt.LeftButton:
			if (event.buttons() & QtCore.Qt.LeftButton): #drag window and pin
				moveWindow(self, -self.point.x(), -self.point.y()*.1) #set mouse position and move window with mouse down
				self.ui.chkpin.setChecked(True)


	def showEvent(self, event):
		try: MaxPlus.CUI.DisableAccelerators()
		except: pass
		#move window to cursor position and offset from left corner to center
		if any([self.name=="init", self.name=="main", self.name=="viewport"]):
			moveWindow(self, -self.point.x(), -self.point.y())
		else:
			moveWindow(self, -self.point.x(), -self.point.y()/2)



	def hide_(self):
		try:
			if hasattr (self.ui, 'chkpin') and self.ui.chkpin.isChecked(): 
				pass
			else:
				self.hide()
		except Exception as error:
			if error!=RuntimeWarning: print error

	def hideEvent(self, event):
		try: MaxPlus.CUI.EnableAccelerators()
		except: pass
		self.layoutStack('init')


	def repeatLastCommand(self):
		self.sb.prevCommand()() #execute command object
		print self.sb.prevCommand(docString=1) #print command name string
		






# ------------------------------------------------
# PaintEvent Overlay
# ------------------------------------------------
class Overlay(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Overlay, self).__init__(parent)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
		self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

		self.sb = Switchboard()
		self.point = QtCore.QPoint(self.sb.getUiSize(percentWidth=50), self.sb.getUiSize(percentHeight=50)) #set point to the middle of the layout
		self.start_line, self.end_line = self.point, QtCore.QPoint()


	def paintEvent(self, event):
		painter = QtGui.QPainter(self) #Initialize painter
		painter.fillRect(self.rect(), QtGui.QColor(127, 127, 127, 0))
		pen = QtGui.QPen(QtGui.QColor(115, 115, 115), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
		painter.setPen(pen)
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		painter.setBrush(QtGui.QColor(115, 115, 115))
		painter.drawEllipse(self.point, 5, 5)
		if not self.end_line.isNull():
			painter.drawLine(self.start_line, self.end_line)
			painter.drawEllipse(self.end_line, 5, 5)

	def mousePressEvent(self, event):
		self.start_line = self.point
		self.end_line = event.pos()
		self.update()

	def mouseMoveEvent(self, event):
		self.end_line = event.pos()
		self.update()

	def mouseReleaseEvent(self, event):
		self.start_line = self.point
		self.end_line = QtCore.QPoint()




class OverlayFactoryFilter(QtCore.QObject):
	def __init__(self, parent=None):
		super(OverlayFactoryFilter, self).__init__(parent)
		self.m_overlay = None

	def setWidget(self, w):
		w.installEventFilter(self)
		if self.m_overlay is None:
			self.m_overlay = Overlay()
		self.m_overlay.setParent(w)

	def eventFilter(self, obj, event):
		if not obj.isWidgetType():
			return False

		if event.type() == QtCore.QEvent.MouseButtonPress:
			self.m_overlay.mousePressEvent(event)
		elif event.type() == QtCore.QEvent.MouseButtonRelease:
			self.m_overlay.mouseReleaseEvent(event)
		elif event.type() == QtCore.QEvent.MouseMove:
			self.m_overlay.mouseMoveEvent(event)
		elif event.type() == QtCore.QEvent.MouseButtonDblClick:
			self.m_overlay.mouseDoubleClickEvent(event)

		elif event.type() == QtCore.QEvent.Resize:
			if self.m_overlay and self.m_overlay.parentWidget() == obj:
				self.m_overlay.resize(obj.size())
		elif event.type() == QtCore.QEvent.Show:
			self.m_overlay.raise_()
			# self.m_overlay.activateWindow()
		return super(OverlayFactoryFilter, self).eventFilter(obj, event)







# ------------------------------------------------
# Popup Window
# ------------------------------------------------
class Popup(QtWidgets.QWidget):
	def __init__(self, parent = None, ui=None):
		QtWidgets.QWidget.__init__(self, parent)

		layout = QtWidgets.QGridLayout(self)
		layout.addWidget(ui)

		layout.setContentsMargins(0, 0, 0, 0) #adjust the margins or you will get an invisible, unintended border

		self.setLayout(layout)
		self.adjustSize()

		self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint) #tag this widget as a popup
		
		# point = ui.rect().bottomRight() #calculate the botoom right point from the parents rectangle
		# global_point = ui.mapToGlobal(point) #map that point as a global position

		# self.move(global_point - QtCore.QPoint(self.width(), 0)) #widget will be placed from its top-left corner, move it to the left based on the widgets width








# ------------------------------------------------
# Garbage-collection-management
# ------------------------------------------------
class _GCProtector(object):
	widgets = []


# ------------------------------------------------
# Initialize
# ------------------------------------------------
def createInstance():

	app = QtWidgets.QApplication.instance()
	if not app:
		app = QtWidgets.QApplication([])

	try: mainWindow = MaxPlus.GetQMaxMainWindow(); mainWindow.setObjectName('MaxWindow')
	except: mainWindow = [x for x in app.topLevelWidgets() if x.objectName() == 'MayaWindow'][0]
	
	hotBox = HotBox(parent=mainWindow)
	_GCProtector.widgets.append(hotBox)

	return hotBox




#module name
print os.path.splitext(os.path.basename(__file__))[0]


# -----------------------------------------------
# Notes
# -----------------------------------------------

# ------------------------------------------------
	# def mouseReleaseEvent(self, event):
	# 	# if event.button() == QtCore.Qt.LeftButton:
	# 	if self.mouseHover:
	# 		# self.buttonObject.click()
	# 		pass
	# 		# print "mouseReleaseEvent", self.mouseHover
			

	# def leaveEvent(self, event):
	# 	#args: [QEvent]
	# 	#can be temp set with; self.leaveEventOn = bool
	# 	pass

# ------------------------------------------------


