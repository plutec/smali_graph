import os
import json
import argparse

nodes = list()

well_known_classes = {
    'java.lang.Object': {'reduced_name':'Object', 'url': 'http://developer.android.com/intl/es/reference/java/lang/Object.html'},
    'android.telephony.PhoneStateListener': {'reduced_name':'PhoneStateListener', 'url': 'http://developer.android.com/reference/android/telephony/PhoneStateListener.html'},
    'android.app.admin.DeviceAdminReceiver': {'reduced_name': 'DeviceAdminReceiver', 'url':'http://developer.android.com/reference/android/app/admin/DeviceAdminReceiver.html'},
    'android.app.Service': {'reduced_name': 'Service', 'url': 'http://developer.android.com/reference/android/app/Service.html'},
    'android.content.BroadcastReceiver': {"reduced_name": "BroadcastReceiver", "url": "http://developer.android.com/reference/android/content/BroadcastReceiver.html"},
    "android.app.Activity": {"reduced_name": "Activity", "url": "http://developer.android.com/reference/android/app/Activity.html"},
    "android.os.Binder": {"reduced_name": "Binder", "url": "http://developer.android.com/reference/android/os/Binder.html"},
    "java.lang.Thread": {"reduced_name": "Thread", "url": "https://docs.oracle.com/javase/7/docs/api/java/lang/Thread.html"},
}

class SmaliJson(object):
    def __init__(self, folder):
        self.nodes = list()
        self.node_id = 0
        self.super_nodes = list()
        self.supernode_id = 0
        self.folder = folder
        self.from_smali = True
        self.from_apk = False
        self.from_dex = False
        self.files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]
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
        snode_id = None
        url_object = None
        if well_known_classes.has_key(name):
            url_object = well_known_classes[name]['url']
            name = well_known_classes[name]['reduced_name']
        for snode in self.super_nodes:
            if snode['name'] == name:
                snode_id = snode['id']
                node['super'] = snode_id
                break
        if snode_id == None:
            snode = {"name": name, "id": "sn_%d" % self.supernode_id,
                     "url": url_object}
            self.supernode_id += 1
            node['super'] = snode['id']
            self.super_nodes.append(snode)
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
        #Title
        self.json["header"]["title"]["undefined"] = "From Smali folder %s" % self.folder
        #Statistics
        self.json['metrics']["classCount"] = len(self.nodes)
        self.json['metrics']["methodCount"] = len(self.edges)
        #Supernodes
        for snode in self.super_nodes:
            supernode = {
                    "id" : snode['id'],
                    "type" : "Class"
                  }
            self.json['class'].append(supernode)

            class_attribute = {
                "id" : snode['id'],
                "label" : {
                  "IRI-based" : snode['name']
                },
                "iri" : snode['url'],
                "attributes" : [ "equivalent" ],
                #"instances" : 0
              }
            self.json['classAttribute'].append(class_attribute)
        #Nodes
        for node in self.nodes:
            self.json['class'].append({
                    "id" : node['id'],
                    "type" : "Class"
                  })

            class_attribute = {
                    "id" : node['id'],
                    "label" : {
                      "IRI-based" : node['name'],
                      "undefined" : node['name']
                    },
                    #"iri" : "http://xmlns.com/foaf/0.1/OnlineAccount",
                    #"comment" : {
                    #  "undefined" : "An online account."
                    #},
                    #"isDefinedBy" : "http://xmlns.com/foaf/0.1/",
                    #"subClasses" : [ ],
                    #"annotations" : {
                    #  "term_status" : [ {
                    #    "identifier" : "term_status",
                    #    "language" : "undefined",
                    #    "value" : "testing",
                    #    "type" : "label"
                    #  } ]
                    #},
                   #"instances" : 0
                   #"equivalent" : [ self.getNodeId(node['super']) ]
                  }
            if node.has_key('super'):
                class_attribute['attributes'] = [ "equivalent" ]
                class_attribute['equivalent'] = [ node['super'] ]
            #print class_attribute
            self.json['classAttribute'].append(class_attribute)

        for edge in self.edges:

            counter = 0
            for name in list(set(edge['name'])):
                propert = {
                                "id" : "%s_%d" % (edge['id'], counter),
                                "type" : "owl:objectProperty"
                                }
                self.json['property'].append(propert)
                property_attribute = {
                        "id" :  "%s_%d" % (edge['id'], counter),
                        "label" : {
                          "IRI-based" : name,
                          "undefined" : name
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
                      }
                counter += 1
                self.json['propertyAttribute'].append(property_attribute)

        json.dump(self.json, open(filename, 'wt'))

def main():
    parser = argparse.ArgumentParser(description='Generate Graph definition for APK/DEX')
    
    parser.add_argument('-s', '--smali', dest="smali", \
        help='Folder with smali code already decompressed', 
        default=None)

    parser.add_argument('-a', '--apk', dest="apk", \
        help='APK to decompress and generate graph (androguard required)', 
        default=None)

    #parser.add_argument('-d', '--dex', dest="dex", \
    #    help='DEX to decompress and generate graph (androguard required)', 
    #    default=None)

    parser.add_argument('-o', '--output', dest="output", \
        help='File to write the JSON file. Default graph.json', 
        default="graph.json")    


    args = parser.parse_args()
    if args.smali:
        print "Generating graph from SMALI folder %s" % args.smali
        #files = generate_filelist(folder)
        sm = SmaliJson(args.smali)
        sm.parseSmali()
        sm.generateJson(args.output)
        print "Graph generate in file %s, now you can load it using graph.html" % (args.output)
        return
    elif args.apk:
        print "Not implemented yet"


if __name__ == '__main__':
    main()
