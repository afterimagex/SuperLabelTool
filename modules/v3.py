#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : PascalVoc.py
# @Author: Afterimagex
# @Date  : 2017/11/30
# @Desc  :
# @Contact : 563853580@qq.com
# @Software : PyCharm
# @license : Copyright(C), Your Company


import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class VocElement(ET.ElementTree):
    def __init__(self):
        super(VocElement, self).__init__('annotation')

    def _template(self):
        try:
            self.folder
        except:
            self.folder = ET.SubElement(self, 'folder')
            self.folder.text = 'VOC2007'
        try:
            self.filename
        except:
            self.filename = ET.SubElement(self, 'filename')
            self.filename.text = 'None'
        try:
            self.__source
        except:
            self.__source = ET.SubElement(self, 'source')
            self.database = ET.SubElement(self.__source, 'database')
            self.database.text = 'The VOC2007 Database'
            self.annotation = ET.SubElement(self.__source, 'annotation')
            self.annotation.text = 'PASCAL VOC2007'
            self.image = ET.SubElement(self.__source, 'image')
            self.image.text = 'flickr'
        try:
            self.__size
        except:
            self.__size = ET.SubElement(self, 'size')
            self.width = ET.SubElement(self.__size, 'width')
            self.width.text = '0'
            self.height = ET.SubElement(self.__size, 'height')
            self.height.text = '0'
            self.depth = ET.SubElement(self.__size, 'depth')
            self.depth.text = '3'
        try:
            self.segflag
        except:
            self.segflag = ET.SubElement(self, 'segmented')
            self.segflag.text = '0'



def xml2dict(element, parent, rst_list):
    for child in element.getchildren():
        if len(child) > 0:
            p = [i for i in parent]
            p.append(child.tag)
            xml2dict(child, p, rst_list)
        else:
            path = '/'.join(parent)
            if 'object' in path:
                continue
            print(path, child.tag, child.text)
    return rst_list




if __name__ == '__main__':
    # dic = {
    #     'folder': 'VOC2007',
    #     'filename': 'None',
    #     'segmented': 0,
    #     'source': {
    #         'database': 'The VOC2007 Database',
    #         'annotation': 'PASCAL VOC2007',
    #         'image': 'flickr'
    #     },
    #     'size': {
    #         'width': {
    #             'ch1': 1
    #         },
    #         'height': 0,
    #         'depth': 3
    #     }
    # }
    # reduce_dict(dic, ['root'])
    # a = VocElement()
    # rough_string = ET.tostring(a, encoding='utf-8')
    # print(rough_string)
    element = ET.parse(r'test\Annotations\01.xml').getroot()
    a = xml2dict(element, [element.tag], [])
    for i in a:
        print(i)