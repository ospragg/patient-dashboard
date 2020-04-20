import pickle
import yaml
import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import textwrap
import os


def render(pathlist):
	
	# load the configuration
	with open("config_enviroment.yaml", "r") as f:
		c_e = yaml.load(f, Loader=yaml.FullLoader)
	
	# get the latest sheets
	filename_sheet_data = "%s/%s.pkl" % (c_e["path_sheet_data"], pathlist[0])
	if os.path.exists(filename_sheet_data):
		with open(filename_sheet_data, "rb") as f:
			sheets = pickle.loads(f.read())
	else:
		return html.H1("Error: sheet '%s' not found" % pathlist[0])
	
	# get the plots we want to make (no annotations)
	plot_sheets = [el for el in sheets if el["metric"] != "annotations"]
	
	# generate the plots
	#p_name = pathlist[0]
	p_name = pathlist[1]
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
	temp_ann_text = [el for el in sheets if el["metric"] == "annotations"][0]["readings"]
	if p_name in temp_ann_text:
		ann_text = temp_ann_text[p_name]
		ann_text = ["<br>".join(textwrap.wrap(el, 12, break_long_words=False)) for el in ann_text]
		ann_yanchor = ["bottom" if i % 2 == 0 else "top" for i in range(len(ann_text))]
		annotations = [{"x":x,"y":1.0,"xref":"x","yref":"paper","text":t,"showarrow":True,"arrowhead":1,"ax":0,"ay":-80,"bordercolor":'black',"align":'left',"valign":'bottom',"yanchor":"top","font":{"size":10}} for x,y,t in zip(ann_x,ann_y,ann_text) if t != ""]
		# https://plotly.com/python/reference/#layout-annotations-items-annotation-align
	else:
		annotations = []
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=len(plots), cols=1,
	                                    shared_xaxes=True,
	                                    shared_yaxes=False,
	                                    vertical_spacing=0.02)
	
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
	                  #height=150 * len(plots),
	                  height=120 * len(plots),
	                  annotations=annotations)
	
	# set up the graph
	graph = html.Div([html.H1("%s" % p_name),
	                 dcc.Graph(figure=fig,
	                 			id='my-figure',
	                 			config={"displayModeBar":False},
	                			responsive=None)])
	
	return graph