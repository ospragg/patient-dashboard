import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

def render(pathlist, pdh):
	
	pdh.load_data()
	
	plots = [[] for i in range(len(pdh.sheets[0:1]))]
	for i_sheet, sheet in enumerate(pdh.sheets[0:1]):
		metric = sheet["metric"]
		days = sheet["days"]
		for p_name, p_data in sheet["readings"].items():
			temp_days = [a for a, b in zip(days, p_data) if b != ""]
			temp_data = [a for a in p_data if a != ""]
			ax = plotly.graph_objs.Scatter(name=p_name,
		                               x=temp_days,
		                               y=temp_data,
		                               line = {"width" : 2.0},
		                               mode='lines',
		                               hoverinfo="text",
		                               text=["<a href=\"%s\">%s</a>" % (p_name, p_name) for v in p_data],
		                               opacity=0.5,
		                               showlegend=True,
		                               textposition="middle center")
			plots[i_sheet].append(ax)
	
	# set up the figure
	fig = plotly.subplots.make_subplots(rows=len(plots), cols=1,
	                                    shared_xaxes=True,
	                                    shared_yaxes=False,)
	
	for i_sheet, sheet in enumerate(pdh.sheets[0:1]):
		fig.update_yaxes(title_text=sheet["metric"], row=i_sheet+1, col=1)
	
	fig.update_xaxes(title_text="Day", row=i_sheet+1, col=1)
	
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


