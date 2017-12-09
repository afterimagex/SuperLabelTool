
import xml.etree.ElementTree as ET
import numpy as np


if __name__ == '__main__':
    root = ET.Element('annotation')
    ki = ET.Element('object')
    root.append(ki)
    rough_string = ET.tostring(root, encoding='utf-8')
    print(rough_string)
