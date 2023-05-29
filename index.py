from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
from datetime import datetime, date
from flask import Flask, redirect, render_template

server = Flask(__name__)
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], server=server, url_base_pathname='/dash/')
app.title = 'Placements 2022-2023'

@server.route('/')
def index():
    return redirect('/dash/')

@server.route('/code/<int:id>')
def show_code(id):
    obj = json.load(open('res.json', 'r'))
    codeObj = list(filter(lambda x: x['id'] == id, obj))[0]
    degreeTypes = ['BTech', 'Dual','MTech', 'MPP', 'Mphil', 'MSc', 'Dual MTech+MSc', 'MS', 'Phd']
    departmentTypes = ['Aerospace Engineering', 'Applied Geophysics', 'Applied Statistics and Informatics', 'Biosciences & Bioengineering',
                       'Center for Nano research', 'Centre for digital health', 'Centre for policy studies', 'Centre for urban science and engineering',
                       'Centre of studies in resources engineering', 'Chemical Engineering', 'Chemistry', 'Civil Engineering', 'Climate Studies',
                       'Computer Science and Engineering', 'Earth Sciences', 'Economics','Educational Technology','Electrical Engineering',
                       'Energy Science and Engineering', 'Engineering Physics', 'Environmental Science and Engineering', 'Geo Informatics',
                       'Humanities and Social Sciences', 'Industrial Engineering', 'Machine Learning', 'Mathematics', 'Mechanical Engineering',
                       'Metallurgical and Materials Engineering', 'Physics', 'Reliability Engineering Department', 'School of Management', 'Systems & Controls',
                       'Technology and Development']
    elgcr = codeObj['depts']
    elgResult= ''
    for i in range(len(departmentTypes)):
        booler=False
        tempRes = ''
        for j in range(len(degreeTypes)):
            if elgcr[i][j] == True:
                booler=True
                tempRes += degreeTypes[j] + ', '
        tempRes+= '</p>'
        if booler:
            elgResult += '<p>'+departmentTypes[i] + ': ' + tempRes

    salary=''
    for i in codeObj['compDet']:
        salary += '<p>' +  i['program'] + ' ' + str(i['gross'])+' '+ str(i['ctc'])+' '+ i['cat']+ '</p>'

    selProc =''
    for i in codeObj['selection']:
        selProc += '<p>' +  i['process'] + ' ' + i['duration']+'</p>'

    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{}</title>
</head>
<body>
<center><h1>{}</h1></center>
<hr class="solid">
<h2>Job Details</h2>
<div>{}</div>
<hr class="solid">

<h4>Place of Posting - {}</h4>
<h4>Accomodation Details - {}</h4>
<h4>Bond Applicable - {}</h4>
<hr class="solid">

<h2>Eligibility Criteria</h2>
<div>{}</div>
<hr class="solid">

<h2>Compensation Details</h2>
<h4>Currency - {}</h4>
<h3>Salary [Programme Gross CTC Category]</h3>
<div>{}</div>
<hr class="solid">

<h2>Selection Process</h2>
<div>{}</div>

</body>
</html>""".format(codeObj['title']+'-'+codeObj['company']['name'], codeObj['title']+'-'+codeObj['company']['name'],
                  codeObj['jobDetails'], codeObj['postingLoc'], codeObj['AccoDet'], codeObj['bondApp'], elgResult, codeObj['currType'],
                  salary, selProc)


app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [html.A(
                dbc.Row([
                    dbc.Col(dbc.NavbarBrand("Placements 2022-2023 by exodus", className="ms-2")),
                ],
                    align="center",
                    className="g-0",
                ),
                href="https://campus.placements.iitb.ac.in/",
                style={"textDecoration": "none"},
            )
            ]
        ),
        color="dark",
        dark=True,
    ),
    html.Br(),
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(dbc.Col(
                                html.H3('Range of dates', style={'text-align':'center'})
                            )),
                            dbc.Row(dbc.Col(
                                html.Div(dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2022, 8, 5),
        max_date_allowed=date(2023, 5, 30),
        start_date=date(2022, 9, 8),
        initial_visible_month=date(2022, 9, 5),
        end_date=date(2022, 9, 30)
    ), style=dict(display='flex', justifyContent='center'))
                            )),

                            dbc.Row(dbc.Col(
                                html.H3('Select Category', style={'text-align':'center'})
                            )),
                            dcc.Dropdown(
                                options=[
                                    {
                                        'label': 'Consulting', 'value': 1
                                    },
                                    {'label': 'Education', 'value': 2},
                                    {'label': 'Engineering & Technology', 'value': 3},
                                    {'label': 'Finance', 'value': 4},
                                    {'label': 'IT/Software', 'value': 5},
                                    {'label': 'Other', 'value': 6},
                                    {'label': 'Public Sector Undertaking', 'value': 7},
                                    {'label': 'Research & Development', 'value': 8},
                                    {'label': 'Services', 'value': 9},
                                ], value=1, id='category-dropdown', multi=True
                            ),
                            html.Br(),
                            dbc.Row([dbc.Col(
                                html.H4('Minimum gross(in L)', style={'text-align':'center'})
                            ), dbc.Col(dcc.Input(id='gross-min-input', type='number', value=0, min=0, max=99),),
                                dbc.Col(
                                html.H4('Maximum gross(in L)', style={'text-align':'center'})
                            ), dbc.Col(dcc.Input(id='gross-max-input', type='number', value=100, min=1, max=100),),
                            ]),



                        ])
                    ])
                ])
            ]),

            html.Br(),


            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H2('Result', style={'text-align':'center'}, id='title-res'),),
                        dbc.CardBody([dbc.Container([], style={'height': '700px', 'overflowY': 'scroll', 'align-items':'center'}, id='player-info-card')
                        ])
                    ])
                ])
            ]),
        ]
    )
])

@app.callback(
    [Output('player-info-card', 'children'),
     Output('title-res', 'children')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('gross-min-input', 'value'),
     Input('gross-max-input', 'value')]
)
def update_output(start_date, end_date, val, g_min, g_max):
    data = json.load(open('res.json', 'r'))
    lis = []

    if(type(val) == int):
        val = [val]


    for i in data:
        if datetime.strptime(i.get('opensAt')[:10], '%Y-%m-%d') >= datetime.strptime(start_date, '%Y-%m-%d') and datetime.strptime(i.get('opensAt')[:10], '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d') and i.get('company').get('sectorId') in val and i['compDet'][0].get('gross') >= g_min*100000 and i['compDet'][0].get('gross') <= g_max*100000:
            lis.append([i['compDet'][0].get('gross'), i.get('id'), i.get('opensAt'), i.get('closesAt'), i.get('title'), i.get('company').get('name')])
            try:
                lis[-1] = lis[-1] + [i.get('slot').get('day')]
            except:
                pass
    res = []

    for i in lis:
        bodylis=[]
        try:
            bodylis = [html.H4('Day: '+i[6])]
        except:
            pass
        res.append(dbc.Card([
            dbc.CardHeader(dcc.Link(html.H5(i[4]), href='/code/{}'.format(i[1]), target='_blank')),
            dbc.CardBody(bodylis+[
                html.H5('Opens at: ' + i[2][:10]+' Closes at: ' + i[3][:10]),

            ]),
            dbc.CardFooter(html.H5(i[5]))
        ], style={'width': '100%', 'align': 'center'}))
        res.append(html.Br())
    return res, 'Result: ({} found)'.format(str(len(res)))

server.run()