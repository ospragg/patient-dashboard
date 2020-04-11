import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

def render(pathlist, pdh):
	
	# get the latest sheets
	sheets = pdh.get_sheets()
	
	# get the plots we want to make (just the first one, no annotations)
	plot_sheets = [el for el in sheets if el["metric"] != "annotations"][0:1]
	
	# generate the plots
	plots = [[] for i in range(len(plot_sheets))]
	for i_sheet, sheet in enumerate(plot_sheets):
		metric = sheet["metric"]
		days = sheet["days"]
		for p_name, p_data in sheet["readings"].items():
			temp_days = [a for a, b in zip(days, p_data) if b != ""]
			temp_data = [a for a in p_data if a != ""]
			plot_link_str = "<a href=\"%s\">%s</a>"
			plot_links = [plot_link_str % (p_name, p_name) for v in p_data]
			ax = plotly.graph_objs.Scatter(name=p_name,
									   x=temp_days,
									   y=temp_data,
									   line = {"width" : 2.0},
									   mode='lines',
									   hoverinfo="text",
									   text=plot_links,
									   opacity=0.5,
									   showlegend=True,
									   )
			plots[i_sheet].append(ax)
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=1, cols=1,
										shared_xaxes=True,
										shared_yaxes=False,)
	
	fig.update_layout(
		hoverlabel=dict(
			bgcolor="white", 
			font_size=16, 
			font_family="Rockwell"
		),
		hovermode='closest'
	)
	
	# add x and y axis labels
	for i_sheet, sheet in enumerate(plot_sheets):
		fig.update_yaxes(title_text=sheet["metric"], row=i_sheet+1, col=1)
	fig.update_xaxes(title_text="Day", row=1, col=1)
	
	# add the axes
	for i_plot in range(len(plots)):
		for i_ax in range(len(plots[i_plot])):
			fig.append_trace(plots[i_plot][i_ax], i_plot+1, 1)
	
	# set up the graph
	graph = html.Div([html.H1("All patients"),
					 dcc.Graph(figure=fig,
								id='my-figure',
								responsive=None)])
	
	return graph


