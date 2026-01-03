
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
data_path = 'data/derived_from_RS_Session_265_AU_1295.csv'
df = pd.read_csv(data_path)

# Initialize Dash app

# Custom CSS for background and style


# Multi-page support with top navigation
app = dash.Dash(__name__, suppress_callback_exceptions=True)

def navbar(active_page):
	return html.Nav([
		html.Div([
			html.H2('Post-Harvest Losses', style={'margin': '0', 'fontWeight': 'bold', 'color': '#1976d2'}),
			html.Div([
				dcc.Link('Dashboard', href='/', className='dash-button' + (' active-nav' if active_page == 'dashboard' else ''), style={'marginRight': '12px'}),
				dcc.Link('Summary', href='/summary', className='dash-button' + (' active-nav' if active_page == 'summary' else ''))
			], style={'display': 'flex', 'alignItems': 'center'}),
		], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '18px 32px'})
	], className='dash-navbar')

def dashboard_layout():
	return html.Div([
		navbar('dashboard'),
		html.Div([
			html.H1('Dashboard', style={'textAlign': 'left', 'marginBottom': '8px'}),
			html.P('Select crop(s) to visualize:', style={'textAlign': 'left', 'marginBottom': '16px'}),
			dcc.Dropdown(
				id='crop-dropdown',
				options=[{'label': crop, 'value': crop} for crop in df['Crops']],
				value=df['Crops'].tolist(),
				multi=True,
				style={'width': '100%', 'maxWidth': '500px', 'marginBottom': '24px'}
			),
			html.Div([
				dcc.Graph(id='loss-plot', style={'height': '350px', 'flex': '1', 'marginRight': '16px'}),
				dcc.Graph(id='change-plot', style={'height': '350px', 'flex': '1'}),
			], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap', 'marginBottom': '24px'}),
			html.Div([
				dcc.Graph(id='pie-plot', style={'height': '350px', 'width': '48%', 'display': 'inline-block', 'marginRight': '16px'}),
				dcc.Graph(id='line-plot', style={'height': '350px', 'width': '48%', 'display': 'inline-block'}),
			], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap', 'marginBottom': '24px'}),
			html.Div(id='summary-table', style={'width': '100%', 'maxWidth': '900px', 'margin': 'auto'}),
		], className='card', style={'maxWidth': '1200px', 'margin': '48px auto', 'padding': '32px'})
	], style={'minHeight': '100vh', 'background': 'transparent'})

def summary_layout():
	return html.Div([
		navbar('summary'),
		html.Div([
			html.H1('Summary', style={'textAlign': 'left', 'marginBottom': '8px'}),
			html.P('Select crop(s) to summarize:', style={'textAlign': 'left', 'marginBottom': '16px'}),
			dcc.Dropdown(
				id='summary-crop-dropdown',
				options=[{'label': crop, 'value': crop} for crop in df['Crops']],
				value=df['Crops'].tolist(),
				multi=True,
				style={'width': '100%', 'maxWidth': '500px', 'marginBottom': '24px'}
			),
			html.Div(id='summary-text', style={'fontSize': '1.2em', 'margin': '32px 0', 'color': '#333'}),
		], className='card', style={'maxWidth': '800px', 'margin': '48px auto', 'padding': '32px'})
	], style={'minHeight': '100vh', 'background': 'transparent'})

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
	if pathname == '/summary':
		return summary_layout()
	return dashboard_layout()



# Interactive callbacks for all plots and table
@app.callback(
	Output('loss-plot', 'figure'),
	Output('change-plot', 'figure'),
	Output('pie-plot', 'figure'),
	Output('line-plot', 'figure'),
	Output('summary-table', 'children'),
	Input('crop-dropdown', 'value')
)
def update_all_plots(selected_crops):
	filtered_df = df[df['Crops'].isin(selected_crops)]
	plot_template = 'plotly_dark'
	# Loss bar plot
	loss_fig = px.bar(
		filtered_df.melt(id_vars='Crops', value_vars=['2020 Loss (%)', '2022 Loss (%)'],
						var_name='Year', value_name='Loss (%)'),
		x='Crops', y='Loss (%)', color='Year', barmode='group',
		title='Loss Percentage by Crop (2020 vs 2022)',
		template=plot_template
	)
	# Change bar plot
	change_fig = px.bar(
		filtered_df, x='Crops', y='Change (%)', color='Crops',
		title='Change in Loss Percentage (2020 to 2022)',
		template=plot_template
	)
	# Pie chart
	pie_fig = px.pie(
		filtered_df, names='Crops', values='2022 Loss (%)',
		title='Share of 2022 Losses by Crop', hole=0.3,
		template=plot_template
	)
	# Line chart
	line_data = filtered_df.melt(id_vars='Crops', value_vars=['2020 Loss (%)', '2022 Loss (%)'],
								 var_name='Year', value_name='Loss (%)')
	line_fig = px.line(
		line_data, x='Year', y='Loss (%)', color='Crops', markers=True,
		title='Loss Trend by Crop (2020 vs 2022)',
		template=plot_template
	)
	# Table
	table = dash.dash_table.DataTable(
		columns=[{"name": i, "id": i} for i in filtered_df.columns],
		data=filtered_df.to_dict('records'),
		style_table={'overflowX': 'auto'},
		style_cell={'textAlign': 'center', 'fontWeight': 'bold'},
		style_header={'fontWeight': 'bold'},
	)
	return loss_fig, change_fig, pie_fig, line_fig, table

# Summary page callback
@app.callback(
	Output('summary-text', 'children'),
	Input('summary-crop-dropdown', 'value')
)
def summarize_crops(selected_crops):
	filtered_df = df[df['Crops'].isin(selected_crops)]
	if filtered_df.empty:
		return "No crops selected. Please select at least one crop to see the summary."
	summary = []
	for _, row in filtered_df.iterrows():
		crop = row['Crops']
		loss_2020 = row['2020 Loss (%)']
		loss_2022 = row['2022 Loss (%)']
		change = row['Change (%)']
		direction = 'increase' if change > 0 else ('decrease' if change < 0 else 'no change')
		summary.append(f"{crop}: Loss in 2020 was {loss_2020}%, in 2022 was {loss_2022}%. This is a {direction} of {abs(change)}%.")
	return html.Div([
		html.P('Summary for selected crops:', style={'fontWeight': 'bold', 'fontSize': '1.1em'}),
		html.Ul([html.Li(s) for s in summary])
	])

if __name__ == '__main__':
	app.run(debug=True)
