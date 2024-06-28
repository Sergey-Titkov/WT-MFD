# svg_timer.py - update an SVG text/color on a timer
#
import sys
import random
from lxml import etree
from PyQt5 import QtCore, QtGui, QtSvg
from PyQt5.QtWidgets import QApplication, QWidget


angle = 0

def timerEvent():
    global angle
    # set the flowval object text to a number 1-10
    find_text(root)[0].text = 'BLDD'
    find_text(root)[0].set('x', "30")
    find_text(root)[0].set('style', 'font: 32px sans-serif; inline-size: 250px;direction: rtl;')
    find_text1(root)[0].set('transform', "rotate({},75,93)".format(angle,int(svgWidget.width()/2),int(svgWidget.height()/2)))
    print("rotate({} {} {})".format(angle,int(svgWidget.width()/2),int(svgWidget.height()/2)))
    angle = angle + 10
    if angle > 360:
        angle = 0

    #name = find_text(root).getElementsByTagName('tspan')
    #name[0].childNodes[0].nodeValue = '100'

    #f.write(doc.toprettyxml())

    print (root.xpath("//n:text[@id='angle']/text()", namespaces={'n': "http://www.w3.org/2000/svg"}))
    print(root.xpath("//n:text[@id='angle']/n:tspan/text()", namespaces={'n': "http://www.w3.org/2000/svg"}))
    #str(random.randint(1, 10)))
    # reload the SVG widget with the text
    svgWidget.load(etree.tostring(root))
#    print(root.xpath("//n:text[@id='angle']", namespaces={'n': "http://www.w3.org/2000/svg"}))
#    print (root.xpath("//n:text[@id='angle']/n:tspan/text()", namespaces={'n': "http://www.w3.org/2000/svg"}))




root = etree.parse(r'рисунок-11.svg')

# create an object for the flowval
find_text = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='angle']")
find_text1 = etree.ETXPath("//{http://www.w3.org/2000/svg}g[@id='Arrow']")

print (root.xpath("//n:text[@id='angle']/n:tspan/text()", namespaces={'n': "http://www.w3.org/2000/svg"}))

app = QApplication(sys.argv)

svgWidget = QtSvg.QSvgWidget()

svgWidget.load(r'рисунок-11.svg')
svgWidget.setGeometry(300, 300, 200, 300)

# Setup a timer event
timer = QtCore.QTimer()
timer.timeout.connect(timerEvent)
timer.start(1000)

svgWidget.show()

sys.exit(app.exec_())