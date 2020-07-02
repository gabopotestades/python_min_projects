import sys
import xml.etree.ElementTree as etree

#Get all attributes from root, children and sub children
def get_attr_number(root):
    n = 0
    for a in root.iter():
        n+= len(a.attrib)
    return n

#Print number of attributes
if __name__ == '__main__':
    sys.stdin.readline()
    xml = sys.stdin.read()
    tree = etree.ElementTree(etree.fromstring(xml))
    root = tree.getroot()
    print(get_attr_number(root))
