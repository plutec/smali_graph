import os
import random
import json

folder = "smali_test/"

nodes = list()


def generate_filelist(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]
    return result

class SmaliJson(object):
    def __init__(self, files):
        self.nodes = list()
        self.node_id = 0
        self.files = files
        self.edges = list()
        self.edge_id = 0
        self.coords = dict()
        self.json = json.load(open('template.json', 'rt'))

    def parseSmali(self):
        for file in self.files:
            with open(file, 'rt') as fd:
                for line in fd.readlines():
                    line = line.strip()
                    if line.startswith('.super'):
                        node = self.addSuperNode(node, line.split(' ')[-1])

                    if line.startswith('.class'):
                        name = line.split(' ')[-1]
                        node = self.addNode(name)

                    if line.startswith("invoke-static") or \
                       line.startswith("invoke-super") or \
                       line.startswith("invoke-direct"):
                        cname, method = self._parseInvoke(line)
                        self.addEdge(node['name'], cname, method)

    @staticmethod
    def _parseInvoke(line):
        #invoke-super {p0, p1, p2}, Landroid/app/admin/DeviceAdminReceiver;->onDisableRequested(Landroid/content/Context;Landroid/content/Intent;)Ljava/lang/CharSequence;
        #invoke-direct {p0}, Landroid/app/admin/DeviceAdminReceiver;-><init>()V
        #invoke-static {p1, v0, v1}, Lcom/kk/liushiwu/com/zz/c;->a(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V
        name = line.split(' ')[-1]
        method = name.split('->')[1].split('(')[0]
        classname = name.split('->')[0][1:-1].replace('/', '.')
        return classname, method

    def addSuperNode(self, node, superclass):
        name = superclass[1:-1].replace('/', '.')
        node['super'] = name
        return node

    def addNode(self, name):
        name = name[1:-1].replace('/', '.')
        node = {"name": name, "id": "n%d" % self.node_id}
        self.nodes.append(node)
        self.node_id += 1
        return node

    def getNodeId(self, name):
        for node in self.nodes:
            if node['name'] == name:
                return node['id'] 

    def addEdge(self, origin, dst, method):
        node_id_origin = self.getNodeId(origin)
        node_id_dst = self.getNodeId(dst)
        if not node_id_origin or not node_id_dst:
            return

        #If the edge already exists, add the method, but not another edge
        for edge in self.edges:
            if edge['from'] == node_id_origin and edge['to'] == node_id_dst:
                edge['name'].append(method)
                return

        edge = {'from': node_id_origin,
                'to': node_id_dst,
                'name': list(method,),
                'id': 'e%d' % self.edge_id}
        self.edge_id += 1
        self.edges.append(edge)

    def showNodes(self):
        print self.nodes

    def showEdges(self):
        print self.edges

    def generateJson(self, filename):

        for node in self.nodes:
            self.json['class'].append({
                    "id" : node['id'],
                    "type" : "owl:Class"
                  })

            self.json['classAttribute'].append({
                    "id" : node['id'],
                    "label" : {
                      "IRI-based" : node['name'],
                      "undefined" : node['name']
                    },
                    "iri" : "http://xmlns.com/foaf/0.1/OnlineAccount",
                    "comment" : {
                      "undefined" : "An online account."
                    },
                    "isDefinedBy" : "http://xmlns.com/foaf/0.1/",
                    "subClasses" : [ ],
                    "annotations" : {
                      "term_status" : [ {
                        "identifier" : "term_status",
                        "language" : "undefined",
                        "value" : "testing",
                        "type" : "label"
                      } ]
                    },
                   #"instances" : 0
                  })

        for edge in self.edges:
            self.json['property'].append(
                {
                "id" : edge['id'],
                "type" : "owl:objectProperty"
              }
                )
            self.json['propertyAttribute'].append(
                 {
                    "id" : edge['id'],
                    "label" : {
                      "IRI-based" : ", ".join(list(set(edge['name']))),
                      "undefined" : ", ".join(list(set(edge['name'])))
                    },
                    #"iri" : "http://xmlns.com/foaf/0.1/workplaceHomepage",
                    #"comment" : {
                    #  "undefined" : "Comentario"
                    #},
                    #"isDefinedBy" : "http://xmlns.com/foaf/0.1/",
                    #"annotations" : {
                    #  "term_status" : [ {
                    #    "identifier" : "term_status",
                    #    "language" : "undefined",
                    #    "value" : "testing",
                    #    "type" : "label"
                    #  } ]
                    #},
                    "domain" : edge['from'],
                    "range" : edge['to']
                  })

        json.dump(self.json, open('secondGraph.json', 'wt'))

def main():
    files = generate_filelist(folder)
    sm = SmaliJson(files)
    sm.parseSmali()
    #sm.showNodes()
    #sm.showEdges()
    sm.generateJson('graph.json')

if __name__ == '__main__':
    main()
