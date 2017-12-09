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
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def mkdr(dr):
    if not os.path.exists(dr):
        os.mkdir(dr)
        return os.path.abspath(dr), True
    else:
        return os.path.abspath(dr), False


class WorkSpace(object):
    def __init__(self, voc_dir):
        self.workspace = voc_dir
        self.check_ws()

    def check_ws(self):
        self.Root = mkdr(self.workspace)
        self.Annotations = mkdr(os.path.join(self.Root[0], 'Annotations'))
        self.JPEGImages = mkdr(os.path.join(self.Root[0], 'JPEGImages'))
        self.SegmentationClass = mkdr(os.path.join(self.Root[0], 'SegmentationClass'))
        self.SegmentationObject = mkdr(os.path.join(self.Root[0], 'SegmentationObject'))
        self.imageSets = mkdr(os.path.join(self.Root[0], 'ImageSets'))
        self.imageSets_Action = mkdr(os.path.join(self.imageSets[0], 'Action'))
        self.imageSets_Layout = mkdr(os.path.join(self.imageSets[0], 'Layout'))
        self.imageSets_Main = mkdr(os.path.join(self.imageSets[0], 'Main'))
        self.imageSets_Segmentation = mkdr(os.path.join(self.imageSets[0], 'Segmentation'))


class Object(object):

    def __init__(self, element, name):
        self.parent = element
        self.obj = ET.SubElement(self.parent, 'object')
        self.name = ET.SubElement(self.obj, 'name')
        self.index = ET.SubElement(self.obj, 'index')
        self.pose = ET.SubElement(self.obj, 'pose')
        self.truncated = ET.SubElement(self.obj, 'truncated')
        self.difficult = ET.SubElement(self.obj, 'difficult')
        self.name.text = str(name)
        self.index.text = str(0)
        self.pose.text = 'Unspecified'
        self.truncated.text = str(0)
        self.difficult.text = str(0)

    def set_bndbox(self, bndbox):
        try:
            self.bndbox
        except:
            self.bndbox = ET.SubElement(self.obj, 'bndbox')
            self.bndbox_xmin = ET.SubElement(self.bndbox, 'xmin')
            self.bndbox_ymin = ET.SubElement(self.bndbox, 'ymin')
            self.bndbox_xmax = ET.SubElement(self.bndbox, 'xmax')
            self.bndbox_ymax = ET.SubElement(self.bndbox, 'ymax')
        bndbox = list(map(str, bndbox))
        self.bndbox_xmin.text = bndbox[0]
        self.bndbox_ymin.text = bndbox[1]
        self.bndbox_xmax.text = bndbox[2]
        self.bndbox_ymax.text = bndbox[3]

    def set_polygon(self, *polygon):
        try:
            self.polygon
        except:
            self.polygon = ET.SubElement(self.obj, 'polygon')

    def drop(self):
        self.parent.remove(self.obj)


class PascalVoc(object):

    def __init__(self):
        self.root = ET.Element('annotation')
        self.__voc_template()
        self._obj_index = 0
        self._object = locals()

    def __voc_template(self):
        try:
            self.folder
        except:
            self.folder = ET.SubElement(self.root, 'folder')
            self.folder.text = 'VOC2007'
        try:
            self.filename
        except:
            self.filename = ET.SubElement(self.root, 'filename')
            self.filename.text = 'None'
        try:
            self.__source
        except:
            self.__source = ET.SubElement(self.root, 'source')
            self.database = ET.SubElement(self.__source, 'database')
            self.database.text = 'The VOC2007 Database'
            self.annotation = ET.SubElement(self.__source, 'annotation')
            self.annotation.text = 'PASCAL VOC2007'
            self.image = ET.SubElement(self.__source, 'image')
            self.image.text = 'flickr'
        try:
            self.__size
        except:
            self.__size = ET.SubElement(self.root, 'size')
            self.width = ET.SubElement(self.__size, 'width')
            self.width.text = '0'
            self.height = ET.SubElement(self.__size, 'height')
            self.height.text = '0'
            self.depth = ET.SubElement(self.__size, 'depth')
            self.depth.text = '3'
        try:
            self.segflag
        except:
            self.segflag = ET.SubElement(self.root, 'segmented')
            self.segflag.text = '0'

    def check_tag(self, element, tag, default):
        if not element.find(tag) is None:
            return element.find(tag).text
        else:
            return default

    def load_file(self, xml_path):
        assert xml_path.endswith('.xml')
        self._obj_index = 0
        element = ET.parse(xml_path).getroot()

        self.folder.text = self.check_tag(element, 'folder', self.folder.text)
        self.filename.text = self.check_tag(element, 'filename', self.filename.text)
        self.database.text = self.check_tag(element, 'source/database', self.database.text)
        self.annotation.text = self.check_tag(element, 'source/annotation', self.annotation.text)
        self.image.text = self.check_tag(element, 'source/image', self.image.text)
        self.width.text = self.check_tag(element, 'size/width', self.width.text)
        self.height.text = self.check_tag(element, 'size/height', self.height.text)
        self.depth.text = self.check_tag(element, 'size/depth', self.depth.text)
        self.segflag.text = self.check_tag(element, 'segmented', self.segflag.text)

        for last_obj in self.root.findall('object'):
            self.root.remove(last_obj)

        if not element.findall('object') is None:
            for obj in element.findall('object'):
                _obj = self.new_object(obj.find('name').text)
                _obj.pose.text = self.check_tag(obj, 'pose', _obj.pose.text)
                _obj.truncated.text = self.check_tag(obj, 'truncated', _obj.truncated.text)
                _obj.difficult.text = self.check_tag(obj, 'difficult', _obj.difficult.text)
                _obj.difficult.text = self.check_tag(obj, 'difficult', _obj.difficult.text)
                _obj.set_bndbox([obj.find('bndbox/xmin').text, obj.find('bndbox/ymin').text,
                                 obj.find('bndbox/xmax').text, obj.find('bndbox/ymax').text])

    def new_object(self, name, pose='Unspecified', truncated=0, difficult=0):
        index = str(self._obj_index)
        self._object[index] = Object(self.root, name)
        self._object[index].index.text = index
        self._object[index].pose.text = pose
        self._object[index].truncated.text = str(truncated)
        self._object[index].difficult.text = str(difficult)
        self._obj_index += 1
        return self._object[index]

    def save(self, path):
        self.__save(path)
        self.load_file(path)
        self.__save(path)

    def __save(self, path):
        rough_string = ET.tostring(self.root, encoding='utf-8')
        reared_content = minidom.parseString(rough_string)
        with open(path, 'w') as fs:
            reared_content.writexml(fs, indent="", addindent="\t", newl="\n", encoding="utf-8")


############
class VocReader(object):
    def __init__(self, xml_path):
        assert xml_path.endswith('.xml')
        self.filepath = xml_path
        self.root = ET.parse(xml_path).getroot()
        self.folder = self.root.find('folder')
        self.filename = self.root.find('filename')
        self.__source = self.root.find('source')
        self.database = self.__source.find('database')
        self.annotation = self.__source.find('annotation')
        self.image = self.__source.find('image')
        self.segflag = self.root.find('segflag')

        self._object = locals()
        self.all_obj = self.root.findall('object')
        self.num_obj = len(self.all_obj)

        for i, obj in enumerate(self.root.findall('object')):
            idx = str(i)
            self._object[idx] = obj


class VocWriter(object):
    def __init__(self):
        self.root = ET.Element('annotation')
        self.__voc_build()
        self._object = locals()
        self._obj_index = 0

    class Object(object):

        def __init__(self, element, name):
            self.parent = element
            self.obj = ET.SubElement(self.parent, 'object')
            self.name = ET.SubElement(self.obj, 'name')
            self.pose = ET.SubElement(self.obj, 'pose')
            self.truncated = ET.SubElement(self.obj, 'truncated')
            self.difficult = ET.SubElement(self.obj, 'difficult')
            self.name.text = str(name)
            self.pose.text = 'Unspecified'
            self.truncated.text = str(0)
            self.difficult.text = str(0)

        def set_bndbox(self, bndbox):
            try:
                self.bndbox
            except:
                self.bndbox = ET.SubElement(self.obj, 'bndbox')
                self.bndbox_xmin = ET.SubElement(self.bndbox, 'xmin')
                self.bndbox_ymin = ET.SubElement(self.bndbox, 'ymin')
                self.bndbox_xmax = ET.SubElement(self.bndbox, 'xmax')
                self.bndbox_ymax = ET.SubElement(self.bndbox, 'ymax')
            bndbox = list(map(str, bndbox))
            self.bndbox_xmin.text = bndbox[0]
            self.bndbox_ymin.text = bndbox[1]
            self.bndbox_xmax.text = bndbox[2]
            self.bndbox_ymax.text = bndbox[3]

        def set_polygon(self, *polygon):
            try:
                self.polygon
            except:
                self.polygon = ET.SubElement(self.obj, 'polygon')

        def drop(self):
            self.parent.remove(self.obj)

    def __voc_build(self):
        try:
            self.folder
        except:
            self.folder = ET.SubElement(self.root, 'folder')
            self.folder.text = 'VOC2007'
        try:
            self.filename
        except:
            self.filename = ET.SubElement(self.root, 'filename')
            self.filename.text = 'None'
        try:
            self.__source
        except:
            self.__source = ET.SubElement(self.root, 'source')
            self.database = ET.SubElement(self.__source, 'database')
            self.database.text = 'The VOC2007 Database'
            self.annotation = ET.SubElement(self.__source, 'annotation')
            self.annotation.text = 'PASCAL VOC2007'
            self.image = ET.SubElement(self.__source, 'image')
            self.image.text = 'flickr'
        try:
            self.__size
        except:
            self.__size = ET.SubElement(self.root, 'size')
            self.width = ET.SubElement(self.__size, 'width')
            self.width.text = '0'
            self.height = ET.SubElement(self.__size, 'height')
            self.height.text = '0'
            self.depth = ET.SubElement(self.__size, 'depth')
            self.depth.text = '3'
        try:
            self.segflag
        except:
            self.segflag = ET.SubElement(self.root, 'segmented')
            self.segflag.text = '0'

    def new_object(self, name, pose='Unspecified', truncated=0, difficult=0):
        index = str(self._obj_index)
        self._object[index] = self.Object(self.root, name)
        self._object[index].pose.text = pose
        self._object[index].truncated.text = str(truncated)
        self._object[index].difficult.text = str(difficult)
        self._obj_index += 1
        return self._object[index]

    def save(self, path):
        # tree = ET.ElementTree(self.root)
        rough_string = ET.tostring(self.root, encoding='utf-8')
        reared_content = minidom.parseString(rough_string)
        with open(path, 'w') as fs:
            reared_content.writexml(fs, indent="", addindent="\t", newl="\n", encoding="utf-8")
        return True
        # tree = ET.ElementTree(self.root)
        # tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    # vw = VocWriter()
    # vw.filename.text = 'pptv'
    # plane = vw.add_object('plane')
    # plane.set_bndbox([10, 20, 30, 40])
    # ship = vw.add_object('ship')
    # ship.set_bndbox([1, 2, 3, 4])
    # tank = vw.add_object('tank')
    # tank.set_bndbox([2,2,2,2])
    # vw.save('./1.xml')

    vr = PascalVoc()
    # vr.load_file('1.xml')
    apple = vr.new_object('apple')
    apple.set_bndbox([9, 6, 3, 1])

    vr.save('1.xml')

    # vr = PascalVoc()
    # vr.load_file('1.xml')
    # vr.save('1/Annotations/1.xml')
