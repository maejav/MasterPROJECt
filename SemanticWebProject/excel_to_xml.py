import xml.etree.ElementTree as ET
import xlrd
import xml.dom.minidom as minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


xml = ET.Element('xml')
col_name=[
    "name", "director", "writers", "year", "country", "budget", "opening_weekend_usa",
    "gross_usa", "cumulative_world_wide", "list_of_cast"
    ]
loc = ("output_final.xls") 
wb = xlrd.open_workbook(loc) 

sheet = wb.sheet_by_index(0) 
for i in range(1, 251):
    movie = ET.SubElement(xml, "movie")
    print(str(i))
    for j in range(10):
        cell = sheet.cell_value( i, j ) 
        if col_name[j]== "writers":
            writers=cell.split("_")
            for writer in writers:
                new = ET.SubElement(movie, "writer")
                new.text = writer
        
        elif col_name[j]== "list_of_cast":
            casts=cell.split("_")
            for cast in casts:
                new = ET.SubElement(movie, "cast")
                new.text = cast
        else:
            new = ET.SubElement(movie, col_name[j])
            new.text = cell


tree = ET.ElementTree(xml)
tree.write("filename.xml")