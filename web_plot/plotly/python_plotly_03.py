import plotly.express as px

df = px.data.gapminder()
fig = px.scatter_geo(df, locations="iso_alpha", color="continent", hover_name="country", size="gdpPercap",
               animation_frame="year", projection="natural earth")
        
fig.show()