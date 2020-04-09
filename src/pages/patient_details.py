import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

def render(pathlist, pdh):
	
	# error if patient doesn't exist
	if pathlist[0] not in pdh.readings.keys():
		return html.Div([ html.H3("Patient ID not recognised") ])
	
	axes = []
	p_name = pathlist[0]
	p_data = pdh.readings[p_name]
	ax = plotly.graph_objs.Scatter(name=p_name,
	                               x=pdh.datetimes,
	                               y=p_data,
	                               line = {"width" : 1.5},
	                               mode='lines')
	axes.append(ax)
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=1, cols=1,
	                                    shared_xaxes=True,
	                                    shared_yaxes=False,)
	
	title = plotly.graph_objs.layout.Title(text="Patient: %s" % pathlist[0])
	fig.update_layout(title=title)
	
	# add the axes to the figure
	for ax in axes:
		fig.append_trace(ax, 1, 1)
	
	# set up the graph
	graph = html.Div([dcc.Graph(figure=fig,
	                 id='my-figure',
	                 responsive=True)])
	
	return graph