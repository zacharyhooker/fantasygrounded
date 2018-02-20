from lxml import etree
from collections import defaultdict
import json

'''
Big thanks to k3-rnc for providing the Xml two-way converters. I've found
it to be faster than other modules.
https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree/10076823#10076823
'''



def checkAction(func):
    """Check to see if the called action is in our existing action pool.
    """
    def wrapper(self, *args, **kwargs):
        if args[0] in [x for v in self.actions.values() for x in v]:
            return func(self, *args, **kwargs)
        else:
            pass
    return wrapper


def xmltodict(path):
    """Translates the XML into a python dictionary.
    
    Args:
        path (TYPE): File path to attempt to parse the XML from.
    
    Returns:
        Dictionary filled with the XML data.
    """
    def _to_dict(tree):
        data = {tree.tag: {} if tree.attrib else None}
        children = list(tree)
        if children:
            dd = defaultdict(list)
            for dc in map(_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            data= {tree.tag: {k: v[0] if len(v) == 1 else v
                         for k, v in dd.items()}}
        if tree.attrib:
            data[tree.tag].update(('@' + k, v)
                            for k, v in tree.attrib.items())
        if tree.text:
            text = tree.text.strip()
            if children or tree.attrib:
                if text:
                  data[tree.tag]['#text'] = text
            else:
                data[tree.tag] = text
        return data
    tree = etree.parse(path)
    return _to_dict(tree.getroot())

def _dicttoxml(dict_):
    """Translates the dictionary back into valid XML.
    
    Args:
        dict_: A dictionary using @ and # reserved formatting.
    
    Returns:
        An etree._Element
    """
    def _to_etree(dict_, root):
        if not dict_:
            pass
        elif isinstance(dict_, str):
            root.text = dict_
        elif isinstance(dict_, dict):
            for k,v in dict_.items():
                assert isinstance(k, str)
                if k.startswith('#'):
                    assert k == '#text' and isinstance(v, str)
                    root.text = v
                elif k.startswith('@'):
                    assert isinstance(v, str)
                    root.set(k[1:], v)
                elif isinstance(v, list):
                    for e in v:
                        _to_etree(e, etree.SubElement(root, k))
                else:
                    _to_etree(v, etree.SubElement(root, k))
        else:
            assert dict_ == 'invalid type', (type(dict_), dict_)
    assert isinstance(dict_, dict) and len(dict_) == 1
    tag, body = next(iter(dict_.items()))
    node = etree.Element(tag)
    for elem in node.iter():
        if not elem.text:
            elem.text=''
    _to_etree(body, node)
    return node

def renderXML(xml, file=None, rootdata = None):
    '''Renders a beautified, valid, XML.
    Args:
        xml: Either the (preferred) etree.Element or the dict of XML.
        file (optional):  Path for string to be rendered and saved out.
    
    Returns:
        Beautified XML string.
    '''
    data = {}

    if isinstance(xml, dict):
        if(len(xml)>1):
            data['root'] = xml
        else:
            data = xml
        xml = _dicttoxml(data)
    parser = etree.XMLParser(remove_blank_text=True)
    reparsed = etree.fromstring(etree.tostring(xml), parser=parser)
    if rootdata:
        for key, value in rootdata.items():
            reparsed.attrib[key] = str(value)
    if file:
        print(file)
        etree.ElementTree(reparsed).write(file, xml_declaration=True,
            encoding='iso-8859-1', pretty_print=True)
    return etree.tostring(reparsed, pretty_print=True)

def renderJSON(dict_, file=None):
    """Renders a beautiful JSON string.
    
    Args:
        dict_: Either the (preferred) dictionary or the etree.Element of
        XML.
        file (optional): Path for string to be rendered and saved out.
    
    Returns:
        Beautified JSON string.
    """
    if isinstance(dict_, etree._ElementTree):
        dict_ = dicttoxml(dict_)
    data = json.dumps(dict_, indent=4)
    if file:
        with open(file, 'w') as f:
            f.write(data)
    return data

def remove_keys(obj, rubbish):
    if isinstance(obj, dict):
        obj = {
            key: remove_keys(value, rubbish) 
            for key, value in obj.items()
            if key not in rubbish}
   
    return obj

def findKey(dict_, search):
    data = {}
    for ret, value in dict_.items():
        if search in ret:
            return value['#text']