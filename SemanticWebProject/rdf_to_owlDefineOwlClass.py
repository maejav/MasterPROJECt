import xlrd

class Owl:
    def __init__(self):
        self.myfile = open("test.owl", "w")
        wb = xlrd.open_workbook("output_final.xls")
        self.sheet = wb.sheet_by_index(0)

    def create_start(self):
        prefix = """<?xml version="1.0"?>
<Ontology xmlns="http://www.w3.org/2002/07/owl#"
    xml:base="http://www.semanticweb.org/tagh/ontologies/imdb"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    ontologyIRI="http://www.semanticweb.org/tagh/ontologies/imdb">
    <Prefix name="" IRI="http://www.semanticweb.org/tagh/ontologies/imdb"/>
    <Prefix name="owl" IRI="http://www.w3.org/2002/07/owl#"/>
    <Prefix name="rdf" IRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>
    <Prefix name="xml" IRI="http://www.w3.org/XML/1998/namespace"/>
    <Prefix name="xsd" IRI="http://www.w3.org/2001/XMLSchema#"/>
    <Prefix name="imdb" IRI="http://www.semanticweb.org/tagh/ontologies/imdb#"/>
    <Prefix name="rdfs" IRI="http://www.w3.org/2000/01/rdf-schema#"/>"""
        self.myfile.write(prefix)
    
    def create_class(self):
        classes = ["movie", "director", "writer", "cast", "person", "budget", "year", "country"]
        for i in classes :
            myclass = "\n\t<Declaration>\n\t\t<Class IRI=\"#{}\"/>\n\t</Declaration>".format(i)
            self.myfile.write(myclass)

    def create_object_property(self):
        obj_property = ["has_director", "has_writer", "has_cast", "has_year_publish", "has_budget",
        "has_country"]
        for i in obj_property :
            obj = "\n\t<Declaration>\n\t\t<ObjectProperty IRI=\"#{}\"/>\n\t</Declaration>".format(i)
            self.myfile.write(obj)

    def create_data_property(self):
        obj_property = ["name"]
        for i in obj_property :
            obj = "\n\t<Declaration>\n\t\t<DataProperty IRI=\"#{}\"/>\n\t</Declaration>".format(i)
            self.myfile.write(obj)

    def get_info_from_excel(self, col_name):
        mydict={"movie":0, "director":1, "writer":2, "year":3, "country":4, "budget":5, "cast":9}
        result = []
        for i in range(1, 251):
            item = self.sheet.cell_value(i, mydict[col_name])
            item = item.split("_")
            if len(item)==1 :
                result.append(item[0])
            else  :
                for j in item :
                    result.append(j)
        return result 

    def get_relation_from_excel(self, col_name1, rel_type, col_name2):
        mydict={"movie":0, "director":1, "writer":2, "year":3, "country":4, "budget":5, "cast":9}
        result = []
        j = 0
        for i in range(1, 251):
            item2 = self.sheet.cell_value(i, mydict[col_name2])
            item2 = item2.split("_")
            if len(item2)==1 :
                j+=1
                result.append((col_name1 + str(i), col_name2 + str(j)))
            else  :
                # print(str(j))
                for s in range(len(item2)) :
                    result.append((col_name1 + str(i), col_name2 + str(j + s + 1)))
                j+=len(item2)
        return result, rel_type

    def create_named_individual_property(self):
        col=["movie", "director", "writer", "year", "country", "budget", "cast"]
        for i in col :
            len_col = len(self.get_info_from_excel(i))
            for j in range(len_col):
                individual = "\n\t<Declaration>\n\t\t<NamedIndividual IRI=\"#{}\"/>\n\t</Declaration>"\
                .format(i+str(j+1))
                self.myfile.write(individual)

    def create_class_assertion(self):
        col=["movie", "director", "writer", "year", "country", "budget", "cast"]
        for i in col :
            len_col = len(self.get_info_from_excel(i))
            for j in range(len_col):
                individual = """\n\t<ClassAssertion>\n\t\t<Class IRI=\"#{}\"/>\n\t\t<NamedIndividual IRI=\"#{}\"/>\n\t</ClassAssertion>""".format(i, i+str(j+1))
                self.myfile.write(individual)            
    
    def create_object_property_assertion(self):
        relation=[("movie", "has_director", "director"), ("movie", "has_writer", "writer"),
        ("movie", "has_cast", "cast"), ("movie", "has_year_publish", "year"),
        ("movie", "has_country", "country"), ("movie", "has_budget", "budget")]
        for i in relation:
            rel, rel_type = self.get_relation_from_excel(i[0], i[1], i[2])
            for j in rel:
                individual = """\n\t<ObjectPropertyAssertion>\n\t\t<ObjectProperty IRI=\"#{}\"/>\n\t\t<NamedIndividual IRI=\"#{}\"/>\n\t\t<NamedIndividual IRI=\"#{}\"/>\n\t</ObjectPropertyAssertion>""".format(rel_type, j[0], j[1])
                self.myfile.write(individual)            
    
    def create_data_property_assertion(self):
        col=["movie", "director", "writer", "year", "country", "budget", "cast"]
        for i in col :
            col_value = self.get_info_from_excel(i)
            for j in range(len(col_value)):
                individual = "\n\t<DataPropertyAssertion>\n\t\t<DataProperty IRI=\"#{}\"/>\n\t\t<NamedIndividual IRI=\"#{}\"/>\n\t\t<Literal>{}</Literal>\n\t</DataPropertyAssertion>".format("name", i + str(j), col_value[j])
                self.myfile.write(individual)

    def create_end (self):
        self.myfile.write("\n</Ontology>")
        self.myfile.close()
if __name__ == "__main__":
    owl = Owl()
    owl.create_start()
    owl.create_class()
    owl.create_object_property()
    owl.create_data_property()
    owl.create_named_individual_property()
    owl.create_class_assertion()
    owl.create_object_property_assertion()
    owl.create_data_property_assertion()
    owl.create_end()
    myfile = open("test.owl", 'r').read()
    myfile = myfile.encode('ascii', 'ignore').decode('ascii')
    open("result.owl", "w").write(myfile)
