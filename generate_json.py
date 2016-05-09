import os
import random

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

    def parseSmali(self):
        for file in self.files:
            with open(file, 'rt') as fd:
                for line in fd.readlines():
                    line = line.strip()
                    if line.startswith(".class"):
                        name = line.split(' ')[-1]
                        classname = self.addNode(name)

                    if line.startswith("invoke-static") or \
                       line.startswith("invoke-super") or \
                       line.startswith("invoke-direct"):
                        cname, method = self._parseInvoke(line)
                        self.addEdge(classname, cname, method)

    @staticmethod
    def _parseInvoke(line):
        #invoke-super {p0, p1, p2}, Landroid/app/admin/DeviceAdminReceiver;->onDisableRequested(Landroid/content/Context;Landroid/content/Intent;)Ljava/lang/CharSequence;
        #invoke-direct {p0}, Landroid/app/admin/DeviceAdminReceiver;-><init>()V
        #invoke-static {p1, v0, v1}, Lcom/kk/liushiwu/com/zz/c;->a(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;)V
        name = line.split(' ')[-1]
        method = name.split('->')[1].split('(')[0]
        classname = name.split('->')[0][1:-1].replace('/', '.')
        return classname, method


    def addNode(self, name):
        name = name[1:-1].replace('/', '.')
        self.nodes.append({"name": name, "id": "n%d" % self.node_id})
        self.node_id += 1
        return name

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

    def _generate_coords(self):
        rand_x = random.randint(0, 100)
        rand_y = random.randint(0, 100)
        if self.coords.has_key(rand_x):
            if self.coords[rand_x].has_key(rand_y):
                return self._generate_coords
            self.coords[rand_x][rand_y] = True
        else:
            self.coords[rand_x] = dict()
            self.coords[rand_x][rand_y] = True

        return rand_x, rand_y
    def generateJson(self, filename):

        with open(filename, 'wt') as fd:
            fd.write('data = { "nodes": [\n')

            for node in self.nodes:
                x, y = self._generate_coords()
                fd.write('{"borderColor": "#617db4", \n \
                          "color": "#617db4", \n \
                          "id": "%s",  \n \
                          "label": "%s",  \n \
                          "size": 0,  \n \
                          "type": "circle",  \n \
                          "x": %d,  \n \
                          "y": %d },' % (node['id'], node['name'], 
                                         x, y))
            fd.write('], "edges": [')
            
            for edge in self.edges:
                label = ''
                edge['name'] = list(set(edge['name']))
                label = " & ".join(edge['name'])
                
                fd.write('\n \
                        {"id": "%s", \n \
                        "label": "%s", \n \
                        "source": "%s", \n \
                        "target": "%s" },' % (edge['id'], label,
                                                  edge['from'], edge['to']))
            fd.write(']}\n')


def main():
    files = generate_filelist(folder)
    sm = SmaliJson(files)
    sm.parseSmali()
    #sm.showNodes()
    #sm.showEdges()
    sm.generateJson('graph.json')

if __name__ == '__main__':
    main()
