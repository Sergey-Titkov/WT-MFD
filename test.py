import copy
from lxml import etree

namespaces = {'svg': 'http://www.w3.org/2000/svg'}
file_path = "main.svg"

# Парсим SVG как XML
svg_tree = etree.parse(file_path)
svg_root = svg_tree.getroot()

# Работать будем с копией изначальной картинки, иначе задолбаешься потом находить и показывать все скрытые элементы.
svg_work_copy = copy.deepcopy(svg_root)
# Находим все элементы с атрибутом data-sensor-name во всем дереве
elements = svg_work_copy.findall('.//*[@data-sensor-name]', namespaces=namespaces)
for indicator in elements:
    indicator.set('guid','Z13')
    print(indicator)