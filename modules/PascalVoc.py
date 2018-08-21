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


class AnnoDefault(object):

    def __init__(self):
        self.folder = 'VOC2007'
        self.filename = 'None'
        self.database = 'The VOC2007 Database'
        self.annotation = 'PASCAL VOC2007'
        self.image = 'flickr'
        self.width = '0'
        self.height = '0'
        self.depth = '3'
        self.segflag = '0'


class WorkSpace(object):

    def __init__(self, voc_dir):
        self.workspace = voc_dir
        # self.check_ws()

    def mkdr(self, dr):
        if not os.path.exists(dr):
            os.mkdir(dr)
            return os.path.abspath(dr), True
        else:
            return os.path.abspath(dr), False

    def check_ws(self):
        self.Root = self.mkdr(self.workspace)
        self.Annotations = self.mkdr(os.path.join(self.Root[0], 'Annotations'))
        self.JPEGImages = self.mkdr(os.path.join(self.Root[0], 'JPEGImages'))
        self.SegmentationClass = self.mkdr(os.path.join(self.Root[0], 'SegmentationClass'))
        self.SegmentationObject = self.mkdr(os.path.join(self.Root[0], 'SegmentationObject'))
        self.imageSets = self.mkdr(os.path.join(self.Root[0], 'ImageSets'))
        self.imageSets_Action = self.mkdr(os.path.join(self.imageSets[0], 'Action'))
        self.imageSets_Layout = self.mkdr(os.path.join(self.imageSets[0], 'Layout'))
        self.imageSets_Main = self.mkdr(os.path.join(self.imageSets[0], 'Main'))
        self.imageSets_Segmentation = self.mkdr(os.path.join(self.imageSets[0], 'Segmentation'))


class ObjectItem(object):

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

    def set_bndbox_old(self, bndbox):
        '''
        :param bndbox: [xmin, ymin, xmax, ymax]
        :return:
        '''
        bndbox = list(map(str, bndbox))
        try:
            self.obj.remove(self.bndbox)
            delattr(self, 'bndbox')
        except:
            pass
        self.bndbox = ET.SubElement(self.obj, 'bndbox')
        self.bndbox_xmin = ET.SubElement(self.bndbox, 'xmin')
        self.bndbox_ymin = ET.SubElement(self.bndbox, 'ymin')
        self.bndbox_xmax = ET.SubElement(self.bndbox, 'xmax')
        self.bndbox_ymax = ET.SubElement(self.bndbox, 'ymax')
        self.bndbox_xmin.text = bndbox[0]
        self.bndbox_ymin.text = bndbox[1]
        self.bndbox_xmax.text = bndbox[2]
        self.bndbox_ymax.text = bndbox[3]
        return self.bndbox

    def set_textbox(self, str_text):
        '''
        :param bndbox: str_text
        :return:
        '''
        try:
            self.obj.remove(self.textbox)
            delattr(self, 'textbox')
        except:
            pass
        self.textbox = ET.SubElement(self.obj, 'textbox')
        self.text = ET.SubElement(self.textbox, 'string')
        self.text.text = str_text
        return self.textbox

    def set_bndbox(self, bndbox):
        '''
        :param bndbox: dict like {'xmin': 10, 'ymin': 20}
        :return: Element
        '''
        try:
            self.obj.remove(self.bndbox)
            delattr(self, 'bndbox')
        except:
            pass
        self.bndbox = ET.SubElement(self.obj, 'bndbox')
        for i in sorted(bndbox.keys()):
            attr = 'bndbox_' + i
            setattr(self, attr, ET.SubElement(self.bndbox, i))
            getattr(self, attr).text = str(bndbox[i])
        return self.bndbox

    def set_point(self, point):
        '''
        :param point: dict like {'p1': [10, 20, 1], 'p2': [11, 22, 0]}
        :return:
        '''
        try:
            self.obj.remove(self.point)
            delattr(self, 'point')
        except:
            pass
        self.point = ET.SubElement(self.obj, 'point')
        for i in sorted(point.keys()):
            attr = 'point_' + i
            setattr(self, attr, ET.SubElement(self.point, i))
            setattr(self, attr + '_x', ET.SubElement(getattr(self, attr), 'x'))
            setattr(self, attr + '_y', ET.SubElement(getattr(self, attr), 'y'))
            setattr(self, attr + '_v', ET.SubElement(getattr(self, attr), 'v'))
            getattr(self, attr + '_x').text = str(point[i][0])
            getattr(self, attr + '_y').text = str(point[i][1])
            getattr(self, attr + '_v').text = str(point[i][2])
        return self.point

    def set_polygon(self, polygon):
        '''
        :param polygon: dict like {'p1': 10, 'p2': 20}
        :return: None
        '''
        try:
            self.obj.remove(self.polygon)
            delattr(self, 'polygon')
        except:
            pass
        self.polygon = ET.SubElement(self.obj, 'polygon')
        for i in sorted(polygon.keys()):
            attr = 'polygon_' + i
            setattr(self, attr, ET.SubElement(self.polygon, i))
            getattr(self, attr).text = str(polygon[i])
        return self.polygon

    def drop(self):
        self.parent.remove(self.obj)
        del self.parent


class VocElement(object):

    def __init__(self):
        self.root = ET.Element('annotation')
        self._template()

    def _set_default(self):
        self.folder = ET.SubElement(self.root, 'folder')
        self.filename = ET.SubElement(self.root, 'filename')
        self.editor = ET.SubElement(self.root, 'editor')
        self.segmented = ET.SubElement(self.root, 'segmented')
        self.source = ET.SubElement(self.root, 'source')
        self.database = ET.SubElement(self.source, 'database')
        self.annotation = ET.SubElement(self.source, 'annotation')
        self.image = ET.SubElement(self.source, 'image')
        self.size = ET.SubElement(self.root, 'size')
        self.width = ET.SubElement(self.size, 'width')
        self.height = ET.SubElement(self.size, 'height')
        self.depth = ET.SubElement(self.size, 'depth')

    def dict2xml(self, dic, parent):
        for key in sorted(dic.keys()):
            if isinstance(dic[key], dict):
                p = [i for i in parent]
                p.append(key)
                self.dict2xml(dic[key], p)
            else:
                for i, node in enumerate(parent[1:]):
                    try:
                        getattr(self, node)
                    except:
                        setattr(self, node, ET.SubElement(getattr(self, parent[i]), node))
                setattr(self, key, ET.SubElement(getattr(self, parent[-1]), key))
                getattr(self, key).text = str(dic[key])
        return dic

    def xml2dict(self, element, parent, rst_list):
        for child in element.getchildren():
            if len(child) > 0:
                p = [i for i in parent]
                p.append(child.tag)
                self.xml2dict(child, p, rst_list)
            else:
                path = '/'.join(parent)
                if 'object' in path:
                    continue
                print(path, child.tag, child.text)
        return rst_list

    def _template(self):
        default_dic = {
            'folder': 'VOC2007',
            'filename': 'None',
            'editor': 'unknow',
            'segmented': 0,
            'source': {
                'database': 'The VOC2007 Database',
                'annotation': 'PASCAL VOC2007',
                'image': 'flickr'
            },
            'size': {
                'width': 0,
                'height': 0,
                'depth': 3
            }
        }
        self.dict2xml(default_dic, ['root'])


class Writer(VocElement):

    def __init__(self):
        super(Writer, self).__init__()
        self._index = 0
        self.objects = []

    def add_object(self, name, pose='Unspecified', truncated=0, difficult=0):
        new_object = ObjectItem(self.root, name)
        new_object.index.text = str(self._index)
        new_object.pose.text = pose
        new_object.truncated.text = str(truncated)
        new_object.difficult.text = str(difficult)
        self.objects.append(new_object)
        self._index += 1
        return new_object

    def remove_object(self, index):
        self.objects[index].drop()
        del self.objects[index]
        self._index -= 1
        for obj in self.objects[index:]:
            obj.index.text = str(int(obj.index.text) - 1)

    def save(self, path):
        try:
            rough_string = ET.tostring(self.root, encoding='utf-8')
            reared_content = minidom.parseString(rough_string)
            with open(path, 'w') as fs:
                reared_content.writexml(fs, indent="", addindent="\t", newl="\n", encoding="utf-8")
            return True
        except:
            return False

    def get_items(self, item):
        '''
        :param item:  str(bndbox, polygon)
        :return: element
        '''
        element = []
        for obj in self.objects:
            if hasattr(obj, item):
                element.append(getattr(obj, item))
        return element


class Reader(Writer):
    def __init__(self, xml=''):
        super(Reader, self).__init__()
        if xml != '':
            self.parse(xml)

    def check_tag(self, element, tag, default):
        if not element.find(tag) is None:
            return element.find(tag).text
        else:
            return default

    def parse(self, xml_path):
        assert xml_path.endswith('.xml')
        element = ET.parse(xml_path).getroot()

        self.folder.text = self.check_tag(element, 'folder', self.folder.text)
        self.filename.text = self.check_tag(element, 'filename', self.filename.text)
        self.editor.text = self.check_tag(element, 'editor', self.editor.text)
        self.database.text = self.check_tag(element, 'source/database', self.database.text)
        self.annotation.text = self.check_tag(element, 'source/annotation', self.annotation.text)
        self.image.text = self.check_tag(element, 'source/image', self.image.text)
        self.width.text = self.check_tag(element, 'size/width', self.width.text)
        self.height.text = self.check_tag(element, 'size/height', self.height.text)
        self.depth.text = self.check_tag(element, 'size/depth', self.depth.text)
        self.segmented.text = self.check_tag(element, 'segmented', self.segmented.text)

        self._set_object(element)

    def _set_object(self, element):
        if not element.findall('object') is None:
            objects = element.findall('object')
            for obj in objects:
                pose = self.check_tag(obj, 'pose', 'Unspecified')
                truncated = self.check_tag(obj, 'truncated', 0)
                difficult = self.check_tag(obj, 'difficult', 0)
                new_obj = self.add_object(obj.find('name').text, pose=pose, truncated=truncated, difficult=difficult)
                if not obj.find('bndbox') is None:
                    box_dict = {}
                    for box in list(obj.find('bndbox')):
                        box_dict[box.tag] = box.text
                    new_obj.set_bndbox(box_dict)

                if not obj.find('polygon') is None:
                    ploy_dict = {}
                    for ploy in list(obj.find('polygon')):
                        ploy_dict[ploy.tag] = ploy.text
                    new_obj.set_polygon(ploy_dict)

                if not obj.find('textbox') is None:
                    textbox_dict = {}
                    for text in list(obj.find('textbox')):
                        textbox_dict[text.tag] = text.text
                    new_obj.set_textbox(textbox_dict)


class PascalVocEngine():
    def __init__(self, root_dir):
        self.ws = WorkSpace(root_dir)

    def reader(self, path):
        self.rd = Reader(path)
        return self.rd

    def writer(self):
        self.wt = Writer()
        return self.wt


if __name__ == '__main__':
    pascal_voc = PascalVocEngine('test')
    # save_dir = pascal_voc.ws.Annotations[0]
    rd = pascal_voc.reader(os.path.join('D:\DATA\OCRX\OUTPUT\SP_CROP_LABEL', '150e5731-9e88-4ab9-81a6-8cebd4460238_01.xml'))
    for box in rd.get_items('textbox'):
        print(box.find('string').text)