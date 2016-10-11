def to_plotly(g,l):
	import plotly.plotly as py
	from plotly.graph_objs import *

	n = g.vcount()
	print('Coords...')
	Xn=[ly[k][0] for k in range(n)]# x-coordinates of nodes
	Yn=[ly[k][1] for k in range(n)]# y-coordinates
	Zn=[ly[k][2] for k in range(n)]# z-coordinates
	Xe=[]
	Ye=[]
	Ze=[]
	for e in edges:
		Xe+=[ly[e[0]][0],ly[e[1]][0], None]# x-coordinates of edge ends
		Ye+=[ly[e[0]][1],ly[e[1]][1], None]
		Ze+=[ly[e[0]][2],ly[e[1]][2], None]

	trace1=Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=Line(color='rgb(125,125,125)', width=1), hoverinfo='none')
	trace2=Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors', marker=Marker(symbol='dot', size=6, color=cols, line=Line(color='rgb(50,50,50)', width=0.5)), text=names, hoverinfo='text')
	axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
	layout = Layout( title="Ashworth et al. 2013", width=1000, height=1000, showlegend=False, scene=Scene( xaxis=XAxis(axis), yaxis=YAxis(axis), zaxis=ZAxis(axis),), margin=Margin( t=100), hovermode='closest', annotations=Annotations([ Annotation( showarrow=False, text="", xref='paper', yref='paper', x=0, y=0.1, xanchor='left', yanchor='bottom', font=Font( size=14)) ]))
	data=Data([trace1, trace2])
	fig=Figure(data=data, layout=layout)
	py.iplot(fig, filename='Ashworth_et_al_2013')

