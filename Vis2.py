import pandas as pd
import altair as alt

data= pd.read_csv("https://drive.google.com/uc?id=1EeOaVTQOPq86Ukf7e-tx6Q-BX90hwSho")
data

peer_schools = alt.Chart(data).mark_line(strokeWidth = 1).encode(
    x = alt.X('FiscalYear:O'),
    y = 'TuitionAndFees:Q',
    color = alt.Color('Institution:N', scale = alt.Scale(scheme = 'tableau10')),
    tooltip = ['Institution', 'FiscalYear', 'TuitionAndFees']
).transform_filter(
    alt.FieldOneOfPredicate(field = 'Institution', oneOf = ['CU Boulder', 'Michigan St', 'Ohio St', 'Penn St', 'Iowa St'])
)

points = alt.Chart(data).mark_point(size = 30, filled = False).encode(
    x = alt.X('FiscalYear:O'),
    y = 'TuitionAndFees:Q',
    color = alt.Color('Institution:N', scale = alt.Scale(scheme = 'tableau10')),
    tooltip = ['Institution', 'FiscalYear', 'TuitionAndFees']
).transform_filter(
    alt.FieldOneOfPredicate(field = 'Institution', oneOf = ['CU Boulder', 'Michigan St', 'Ohio St', 'Penn St', 'Iowa St'])
)

peer_schools + points


filtered_data = data[
    (data['Institution'].isin(['CU Boulder', 'Michigan St', 'Ohio St', 'Penn St', 'Iowa St'])) &
    (data['FiscalYear'].isin([1997, 2002, 2007, 2012, 2017, 2022]))
]

line_graph = alt.Chart(filtered_data).mark_line(strokeWidth=3).encode(
    x = alt.X('FiscalYear:O', axis=alt.Axis(labelAngle=0)),
    y = alt.Y('Rank:Q', scale=alt.Scale(reverse=True)),
    color = alt.Color('Institution:N', legend=None),
).properties(
    width = 300,
    height = 500
)

text_data = filtered_data[filtered_data['FiscalYear'] == 2022]

text = alt.Chart(text_data).mark_text(
    align = 'left',
    dx = 5,
    fontSize = 16
).encode(
    x = 'FiscalYear:O',
    y = 'Rank:Q',
    text = 'Institution:N',
    color = alt.Color('Institution:N', legend=None)
)


line_graph + text

boston_url = "https://gist.githubusercontent.com/evanpeck/7b801bc5b5259d38cbf0d8de286e7769/raw/e886b870cfdebe6ba2d73ed939717d4c33b37689/boston_neighborhood.json"


boston_geojson_data = alt.Data(url=boston_url, format=alt.DataFormat(property="features", type="json"))

boston_choropleth = alt.Chart(boston_geojson_data).mark_geoshape(
    stroke = 'white'
).encode(
    alt.Color('properties.tot_pop_18plus:Q'),
    alt.Tooltip(['properties.blockgr2020_ctr_neighb_name:N'], title='Neighborhood')
).properties(
    width = 500,
    height = 400
).project(
    type='identity',
    reflectY=True
)

boston_choropleth


custom_choropleth = alt.Chart(boston_geojson_data).mark_geoshape(
    stroke = 'white'
).encode(
    alt.Color('properties.tot_pop_18plus:Q',
              scale = alt.Scale(scheme = 'blueorange'),
              bin = alt.Bin(maxbins = 5),
              legend = alt.Legend(orient = 'bottom', direction = 'horizontal'),
              title = '18+ Population'),
    alt.Tooltip(['properties.blockgr2020_ctr_neighb_name:N'], title = 'Neighborhood')
).properties(
    width = 500,
    height = 400
).project(
    type = 'identity',
    reflectY = True
)

custom_choropleth


selected_institutions = ['CU Boulder', 'Michigan St', 'Ohio St', 'Penn St', 'Iowa St']

# Custom color scale for institutions with adjusted lighter shades
custom_colors = {
    'CU Boulder': '#CFB87C',  # CU Boulder Shade
    'Michigan St': '#2E8B57', # Lighter shade for Michigan State
    'Ohio St': '#8B0000',     # Darker shade for Ohio State
    'Penn St': '#3C6EAA',     # Lighter shade for Penn State
    'Iowa St': '#E63946'      # Lighter shade for Iowa State
}

peer_schools = alt.Chart(data).mark_line(strokeWidth=1.5).encode(
    x=alt.X(
        'FiscalYear:O',
        axis=alt.Axis(
            title="Academic Fiscal Year",
            labelExpr="datum.label % 5 === 0 ? datum.label : ''",  
            labelAngle=0 
        )
    ),
    y=alt.Y(
        'TuitionAndFees:Q',
        axis=alt.Axis(
            title="Annual Tuition and Fees (USD)",
            labelAngle=180
        )
    ),
    color=alt.Color(
        'Institution:N',
        scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values())),
        legend=None
    ),
    tooltip=['Institution', 'FiscalYear', 'TuitionAndFees']
).transform_filter(
    alt.FieldOneOfPredicate(field='Institution', oneOf=selected_institutions)
)

# Add hollow circles for points
points = alt.Chart(data).mark_point(size=30, filled=False).encode(
    x='FiscalYear:O',
    y='TuitionAndFees:Q',
    color=alt.Color(
        'Institution:N',
        scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values())),
        legend=None
    ),
    tooltip=['Institution', 'FiscalYear', 'TuitionAndFees']
).transform_filter(
    alt.FieldOneOfPredicate(field='Institution', oneOf=selected_institutions)
)

# Filter data for the last Fiscal Year
max_year = data['FiscalYear'].max()
text_data = data[
    (data['Institution'].isin(selected_institutions)) &
    (data['FiscalYear'] == max_year)
]

text_general = alt.Chart(text_data[text_data['Institution'] != 'CU Boulder']).mark_text(
    align='left',
    dx=15,
    dy=-3,
    fontSize=12
).encode(
    x='FiscalYear:O',
    y='TuitionAndFees:Q',
    text=alt.Text('Institution:N'),
    color=alt.Color(
        'Institution:N',
        scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values()))
    )
)

cu_boulder_text = alt.Chart(text_data[text_data['Institution'] == 'CU Boulder']).mark_text(
    align='left',
    dx=15,
    dy=-8,  
    fontSize=12
).encode(
    x='FiscalYear:O',
    y='TuitionAndFees:Q',
    text=alt.Text('Institution:N'),
    color=alt.Color(
        'Institution:N',
        scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values()))
    )
)

final_chart = (peer_schools + points + text_general + cu_boulder_text).properties(
    title="Comparison of Tuition and Fees Among Peer Institutions"
)

final_chart