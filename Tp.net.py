import igraph as ig
import pickle as pk
import os,sys,string,re

def to_ply(g,l,f):
	# header
	f.write('''ply
format ascii 1.0
comment author: J Ashworth
comment object: network
element vertex %s
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element edge %s
property int vertex1
property int vertex2
property uchar red
property uchar green
property uchar blue
end_header\n''' %(g.vcount(), g.ecount()))
	# vertices
	for i in range(g.vcount()):
		f.write('%f %f %f %i %i %i\n' %(l[i][0], l[i][1], l[i][2], g.vs[i]['color'][0], g.vs[i]['color'][1], g.vs[i]['color'][2]))
	# edges
	for e in g.es:
		f.write('%i %i 125 125 125\n' %(e.tuple[0], e.tuple[1]))

def to_json(g,l,f):
	# edges
	f.write('"edges":[\n')
	for e in g.es:
		f.write('{"source":"%i", "target":"%i",' %(e.tuple[0], e.tuple[1]))
		f.write(','.join( ['"%s":"%s"' %(n,str(e[n])) for n in e.attribute_names()] ))
		f.write('},\n')
	f.write('],\n')
	# vertices
	f.write('"nodes":{\n')
	for i in range(g.vcount()):
		f.write('"%i":{"location":[%f, %f, %f], "color":"#%s", "label":"%s", "group":"%s"}\n' %(i, l[i][0], l[i][1], l[i][2], ''.join( ['%02x' %(int(c)) for c in g.vs[i]['color']]), g.vs[i]['label'], g.vs[i]['group'] ))
	f.write('}\n')


# BEGIN proc code
nf = 'Tp.nodes'
ef = 'Tp.edges'

# read and 0-index nodes
nodes = {}
geneids = []
labels = []
groupnames = []
ind = 0
for l in open(nf):
	w = l.strip().split()
	print(w)
	geneid = w[0]
	if len(w) < 6: group = ''
	else: group = w[5]
	nodes[geneid] = ind
	geneids.append(geneid)
	labels.append('%s: %s' %(geneid,group))
	groupnames.append(group)
	ind = ind+1

colorkey = {
	"" : (0.3,0,3,0.3),
	"Dawn" : (1,0.7,0),
	"Dusk" : (0,0.2,0.8),
	"Exponential" : (0,1,0),
	"Stationary" : (0.5,0.3,0.1),
	"Dawn" : (1,0.7,0),
	'Dawn_Exponential' : (0.7,1,0),
	'Dawn_Stationary' : (0.7,0.5,0.3),
	'Dusk_Exponential' : (0,0.5,0.5),
	'Dusk_Stationary' :(0.2,0.2,0.7),
}

# read edges
edges = []
edgeweights = []
for l in open(ef):
	w = l.strip().split()
	edges.append( (nodes[w[0]], nodes[w[1]]) )
	edgeweights.append( float(w[2]) )

# create graph object
print('creating igraph...')
g = ig.Graph(edges,directed=False)
g.es["weight"] = edgeweights
g.es['color'] = "#888888"

# add vertex attributes
for i in range(g.vcount()):
	g.vs[i]["geneid"] = geneids[i]
	g.vs[i]["label"] = labels[i]
	g.vs[i]["group"] = groupnames[i]
	g.vs[i]["color"] = [ j*255 for j in colorkey[groupnames[i]] ]

pk.dump(g, open('graph.p','wb'))

print('Layout...(creating graph layout--slow)')
ly=g.layout('kk3d')
#ly=g.layout('fr3d')

pk.dump(ly, open('layout.p','wb'))

to_ply(g,ly,open('nw.ply','w'))
to_json(g,ly,open('nw.json','w'))

#to_plotly(g,ly) # function is elsewhere
