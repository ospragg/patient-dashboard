import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

def render(pathlist, pdh):
	
	# get the latest sheets
	sheets = pdh.get_sheets()
	
	# get the plots we want to make (no annotations)
	plot_sheets = [el for el in sheets if el["metric"] != "annotations"]
	
	# generate the plots
	p_name = pathlist[0]
	plots = [[] for i in range(len(plot_sheets))]
	for i_sheet, sheet in enumerate(plot_sheets):
		metric = sheet["metric"]
		days = sheet["days"]
		if p_name in sheet["readings"]:
			p_data = sheet["readings"][p_name]
			temp_days = [a for a, b in zip(days, p_data) if b != ""]
			temp_data = [a for a in p_data if a != ""]
			ax = plotly.graph_objs.Scatter(name=p_name,
		                               x=temp_days,
		                               y=temp_data,
		                               line = {"width" : 1.0},
		                               #mode='lines',
									   mode="lines+markers",
		                               opacity=0.8,
		                               showlegend=False,
		                               textposition="middle center")
			plots[i_sheet].append(ax)
	
	# set up the annotations
	ann_x = plot_sheets[0]["days"]
	temp_y = [el for el in plot_sheets[0]["readings"][p_name] if el != ""]
	ann_y = [max(temp_y) if len(temp_y) > 0 else 0.0 for el in ann_x]
	ann_text = [el for el in sheets if el["metric"] == "annotations"][0]["readings"][p_name]
	annotations = [{"x":x,"y":y,"xref":"x","yref":"y","text":t,"showarrow":True,"arrowhead":7,"ax":0,"ay":-20} for x,y,t in zip(ann_x,ann_y,ann_text) if t != ""]
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=len(plots), cols=1,
	                                    shared_xaxes=True,
	                                    shared_yaxes=False)
	
	# add x and y axis labels
	for i_sheet, sheet in enumerate(plot_sheets):
		fig.update_yaxes(title_text=sheet["metric"], 
		                 row=i_sheet+1, col=1)
	fig.update_xaxes(title_text="Day", row=len(plots), col=1, rangemode='tozero')
	
	# add the axes
	for i_plot in range(len(plots)):
		for i_ax in range(len(plots[i_plot])):
			fig.append_trace(plots[i_plot][i_ax], i_plot+1, 1)
	
	# set the plot height
	fig.update_layout(autosize=True,
	                  height=150 * len(plots),
	                  annotations=annotations)
	
	# set up the graph
	graph = html.Div([html.H1("%s" % pathlist[0]),
	                 dcc.Graph(figure=fig,
	                 			id='my-figure',
	                			responsive=None)])
	
	return graph