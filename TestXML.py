# importing required librarie
from lxml import etree

#self.svgWidget.cstTarget = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='select-target']")
#self.svgWidget.cstAngle = etree.ETXPath("//{http://www.w3.org/2000/svg}text[@id='angle']")
#self.svgWidget.cstArrow = etree.ETXPath("//{http://www.w3.org/2000/svg}g[@id='Arrow']")
root = etree.parse('MFD - 01___.svg')
#z = root.find_element_by_xpath("//*[@class='im_editable'][@class='im-chat-input--t']")
print(root)
print(etree.tostring(root))
for element in root.iter():
    print(f"{element.tag}  - {element.text}")
z = etree.ETXPath("//{http://www.w3.org/2000/svg}text[starts-with(@id,'sens_')]");
k = z(root)
print(k)
print('-------------')
for element in k:
    print(f"{element.tag} - {element.get('id')} - {element.text}")
    element.text = '!Z!'

print(etree.tostring(root))
z = etree.ETXPath("//{http://www.w3.org/2000/svg}svg");
k = z(root)
print(k)
print('-------------')
for element in k:
    print(f"{element.tag} - {element.get('width')} - {element.get('height')}")

#self.svgWidget.cstTarget(self.svgWidget.cstRoot)[0].text = stroka
#self.svgWidget.cstAngle(self.svgWidget.cstRoot)[0].text = course_angle_text
#self.svgWidget.cstArrow(self.svgWidget.cstRoot)[0].set('transform', "rotate({},75,93)".format(int(course_angle)))


print('{:1.2f}'.format(-0.000018))