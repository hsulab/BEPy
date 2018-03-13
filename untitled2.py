# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:20:33 2017

@author: Alexander
"""

try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
    
xsdfile = ET.parse(r'./database/example1.xsd')
root = xsdfile.getroot()

for i in root.iter(r'Atom3d'):  # 循环根节点的孩子节点
    print(i.tag)# 打印孩子节点的标签和属性值