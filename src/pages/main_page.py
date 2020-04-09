import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

def render(pathlist, pdh):
	
	#print(pdh.datetimes)
	#print(pdh.readings)
	
	# set up the axes
	axes = []
	for p_name, p_data in pdh.readings.items():
		ax = plotly.graph_objs.Scatter(name=p_name,
		                               x=pdh.datetimes,
		                               y=p_data,
		                               line = {"width" : 1.5},
		                               mode='lines',
		                               hoverinfo="text",
		                               text=["<a href=\"%s\">Patient %s</a>" % (p_name, p_name) for v in p_data])
		axes.append(ax)
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=1, cols=1,
	                                    shared_xaxes=True,
	                                    shared_yaxes=False,)
	
	title = plotly.graph_objs.layout.Title(text="All patients")
	fig.update_layout(title=title)
	
	# add the axes to the figure
	for ax in axes:
		fig.append_trace(ax, 1, 1)
	
	# set up the graph
	graph = html.Div([dcc.Graph(figure=fig,
	                 id='my-figure',
	                 responsive=True)])
	
	return graph


