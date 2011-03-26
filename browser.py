#!/usr/bin/python
import sys

from PyQt4.QtCore import QUrl, Qt, SIGNAL, SLOT, pyqtSignal, pyqtSlot, QString
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView, QWebPage

activeImage = QString()

class QPonyComboBox(QComboBox):
	pass

class QPony(QLabel):
	imageSelected = pyqtSignal(QString)

	def __init__(self, name, parent=None):
		QLabel.__init__(self, parent)

		image = QPixmap("ponies/%s" % name).scaledToWidth(200)
		self.setPixmap(image)

		self.name = name
	
	@pyqtSlot()
	def mousePressEvent(self, event):
		self.imageSelected.emit(self.name)

class QPonyWebView(QWebView):
	def __init__(self, parent=None):
		QWebView.__init__(self, parent)
		self.setPage(QPonyWebPage(self))

class QPonyWebPage(QWebPage):
	def chooseFile(self, originatingFrame, oldFile):
		global activeImage
		return activeImage

class Ui_MainWindow(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		wrapper = QHBoxLayout()

		imageList = QWidget()
		imageListLayout = QVBoxLayout(imageList)

		imageListLayout.addWidget(QLabel('Emotion:'))
		emotion = QPonyComboBox()
		emotion.addItems(['any', 'determination', 'fear', 'happy'])
		imageListLayout.addWidget(emotion)

		imageListLayout.addWidget(QLabel('Captioned:'))
		captioned = QPonyComboBox()
		captioned.addItems(['any', 'yes', 'no'])
		imageListLayout.addWidget(captioned)

		imageListLayout.addWidget(QLabel('Character:'))
		character = QPonyComboBox()
		character.addItems(['any', 'Applejack', 'Pinkie Pie', 'Spike'])
		imageListLayout.addWidget(character)

		for ponyImage in [
			'86200554077f4b74a643b1672060952c.png',
			'fbed97882ec2007d53125e4a03183d1b.gif',
			'fd1445006df5b4dbfcc918d34be0adec.jpg']:
			pony = QPony(ponyImage)
			pony.imageSelected.connect(self.select_image)
			imageListLayout.addWidget(pony)
		imageList.setMaximumWidth(200)

		scrollArea = QScrollArea()
		scrollArea.setWidget(imageList)
		scrollArea.setMinimumWidth(220)
		scrollArea.setMaximumWidth(220)

		wrapper.addWidget(scrollArea)

		self.web = QPonyWebView()
		self.web.setUrl(QUrl('http://ponychan.net/chan/meta/'))
		wrapper.addWidget(self.web)

		self.setLayout(wrapper)
	
	def select_image(self, name):
		#frame = self.web.page().mainFrame()
		#html = frame.toHtml()
		#print unicode(html)
		#html.replace('type="file"', 'value="file://%s"' % name)
		#frame.setHtml(html, QUrl('http://ponychan.net/chan/meta/'))
		global activeImage
		activeImage = name

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myapp = Ui_MainWindow()
	myapp.show()
	sys.exit(app.exec_())

#from PyQt4 import QtCore; QtCore.pyqtRemoveInputHook(); import pudb; pudb.set_trace()

