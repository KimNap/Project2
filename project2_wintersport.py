#!/usr/bin/env python
# coding: utf-8

text = 'blablabla'
st.text(text)

# In[ ]:


# Import package
import requests
import pandas as pd
import streamlit as st


# In[2]:


# Assign URL to variable: url
url = 'https://opendata.cbs.nl/ODataApi/odata/37282/TypedDataSet'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Decode the JSON data into a dictionary: json_data
json_data = r.json()

# Print each key-value pair in json_data
#for k in json_data.keys():
 #   print(k + ': ', json_data[k])
    
# Maak dataframe
df = pd.DataFrame.from_dict(json_data['value'], orient='columns', dtype=None, columns=None)


# In[3]:


#Laat alle kolommen zien van de dataframe
pd.set_option("display.max_columns", None)
df.head()


# In[4]:


#Vervang alle NaN values met 0
df_na = df.fillna(0)
df_na.head()


# In[5]:


sum_column1 = df_na['k_0Tot6Jaar_4']+ df_na['k_0Tot6Jaar_14']
df_na['0Tot6'] = sum_column1
sum_column2 = df_na['k_6Tot15Jaar_5']+ df_na['k_6Tot13Jaar_15']
df_na['6Tot15'] = sum_column2
sum_column3 = df_na['k_15Tot19Jaar_6']+ df_na['k_13Tot18Jaar_16']
df_na['15Tot19'] = sum_column3
sum_column4 = df_na['k_19Tot25Jaar_7']+ df_na['k_18Tot25Jaar_17']
df_na['19Tot25'] = sum_column4
sum_column5 = df_na['k_25Tot30Jaar_8']+ df_na['k_25Tot35Jaar_18']
df_na['25Tot30'] = sum_column5
sum_column6 = df_na['k_30Tot40Jaar_9']+ df_na['k_35Tot45Jaar_19']
df_na['30Tot40'] = sum_column6
sum_column7 = df_na['k_40Tot50Jaar_10']+ df_na['k_45Tot55Jaar_20']
df_na['40Tot50'] = sum_column7
sum_column8 = df_na['k_50Tot65Jaar_11']+ df_na['k_55Tot65Jaar_21']
df_na['50Tot65'] = sum_column8
sum_column9 = df_na['k_65Tot75Jaar_12']+ df_na['k_65Tot75Jaar_22']
df_na['65Tot75'] = sum_column9
sum_column10 = df_na['k_75JaarOfOuder_13']+ df_na['k_75JaarOfOuder_23']
df_na['75Ouder'] = sum_column10


# In[6]:


df_na.head()


# In[7]:


df.describe()


# In[8]:


# Tabel vervormen

df_na.set_index(['Perioden'], drop=True, append=False, inplace=False, verify_integrity=False)
df_na['Perioden'] = df_na['Perioden'].str.replace('X001','')
df_na.drop('ID', axis = 1, inplace=True)
df_na.head()


# In[9]:


import plotly.express as px
import plotly.graph_objects as go


# In[10]:


fig = px.line(df_na, x="Perioden", y="TotaalLangeWintersportvakanties_1", title='')
fig.update_xaxes(rangeslider_visible=True)
fig.show()
st.write(fig)


# In[11]:


fig = px.histogram(df_na, x='Perioden', y=['Mannen_2', 'Vrouwen_3'],
              title='Aantal mannen en vrouwen op wintersport per jaartal',
              labels={'Mannen_2': 'Man', 'Vrouwen_3': 'Vrouw', 'variable': 'Geslacht', 'value': 'Aantal', 'Perioden': 'Jaartal'})
fig.update_layout(title_x=0.5)
fig.update_xaxes(tickangle=40)
dropdown_buttons=[{'label': 'Man & Vrouw', 'method': 'update',
                  'args':[{'visible': [True, True]},
                         {'title': 'Barchart aantal mannen en vrouwen op wintersport per jaartal'}]},
                  {'label': 'Man', 'method': 'update',
                  'args':[{'visible': [True, False]},
                         {'title': 'Barchart aantal mannen op wintersport per jaartal'}]},
                 {'label': 'Vrouw', 'method': 'update',
                  'args':[{'visible': [False, True]},
                         {'title': 'Barchart aantal vrouwen op wintersport per jaartal'}]}]
fig.update_layout({'updatemenus':[{'type': "dropdown",
                                  'x':1.3,
                                  'y':0.5,
                                  'showactive': True,
                                  'active': 0,
                                  'buttons': dropdown_buttons}]})
fig.update_yaxes(title_text='Aantal')
fig.update_layout(barmode='group')
fig.show()
st.write(fig)


# In[12]:


fig = px.bar(df_na, x='Perioden', y=['0Tot6', '6Tot15', '15Tot19', '19Tot25', '25Tot30', '30Tot40', '40Tot50', '50Tot65', '65Tot75', '75Ouder'],
              title='Leeftijdsgroepen per jaartal',
              labels={'variable': 'Leeftijdcategoriën', 'value': 'Aantal', 'Perioden': 'Jaartal'})
fig.update_layout(title_x=0.5)
fig.update_xaxes(tickangle=40)
dropdown_buttons=[{'label': 'Alle leeftijden', 'method': 'update',
                  'args':[{'visible': [True, True, True, True, True, True, True, True, True, True]},
                         {'title': '1'}]},
                  {'label': '0 Tot 6 Jaar', 'method': 'update',
                  'args':[{'visible': [True, False, False, False, False, False, False, False, False, False]},
                         {'title': '2'}]},
                  {'label': '6 Tot 15 Jaar', 'method': 'update',
                  'args':[{'visible': [False, True, False, False, False, False, False, False, False, False]},
                         {'title': '3'}]},
                  {'label': '15 Tot 19 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, True, False, False, False, False, False, False, False]},
                         {'title': '4'}]},
                  {'label': '19 Tot 25 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, True, False, False, False, False, False, False]},
                         {'title': '5'}]},
                  {'label': '25 Tot 30 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, True, False, False, False, False, False]},
                         {'title': '6'}]},
                  {'label': '30 Tot 40 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, False, True, False, False, False, False]},
                         {'title': '7'}]},
                  {'label': '40 Tot 50 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, False, False, True, False, False, False]},
                         {'title': '8'}]},
                  {'label': '50 Tot 65 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, False, False, False, True, False, False]},
                         {'title': '9'}]},
                  {'label': '65 Tot 75 Jaar', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, False, False, False, False, True, False]},
                         {'title': '10'}]},
                 {'label': '75 jaar +', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, False, False, False, False, False, True]},
                         {'title': '11'}]}]
fig.update_layout({'updatemenus':[{'type': "dropdown",
                                  'x':1.3,
                                  'y':1.1,
                                  'showactive': True,
                                  'active': 0,
                                  'buttons': dropdown_buttons}]})
fig.update_yaxes(title_text='Aantal')
fig.update_layout(barmode='stack')
fig.show()
st.write(fig)


# In[13]:


sum_regio1 = df_na['GroningenPV_55']+ df_na['FrieslandPV_56']+ df_na['DrenthePV_57']
df_na['Noord'] = sum_regio1
sum_regio2 = df_na['OverijsselPV_58']+ df_na['GelderlandPV_60']+ df_na['FlevolandPV_59']
df_na['Oost'] = sum_column2
sum_regio3 = df_na['LimburgPV_66']+ df_na['NoordBrabantPV_65']
df_na['Zuid'] = sum_column3
sum_regio4 = df_na['ZeelandPV_64']+ df_na['ZuidHollandPV_63']+ df_na['NoordHollandPV_62']+ df_na['UtrechtPV_61']
df_na['West'] = sum_column4
df_na.head()


# In[14]:


fig = px.line(df_na, x='Perioden', y=['Noord', 'Oost', 'Zuid', 'West'],
              title='Vakantiegangers per regio',
              labels={'variable': 'Regios', 'value': 'Aantal', 'Perioden': 'Jaartal'})
my_buttons = [{'label': 'Alle Regios', 'method': 'update',
                  'args':[{'visible': [True, True, True, True]},
                         {'title': '10'}]},
              {'label': 'Regio Noord', 'method': 'update',
                  'args':[{'visible': [True, False, False, False]},
                         {'title': '10'}]},
             {'label': 'Regio Oost', 'method': 'update',
                  'args':[{'visible': [False, True, False, False]},
                         {'title': '10'}]},
             {'label': 'Regio Zuid', 'method': 'update',
                  'args':[{'visible': [False, False, True, False]},
                         {'title': '10'}]},
             {'label': 'Regio West', 'method': 'update',
                  'args':[{'visible': [False, False, False, True]},
                         {'title': '10'}]}]
fig.update_layout(title_x=0.5)
fig.update_layout({'updatemenus':[{'type': "buttons",
                  'direction': 'down',
                  'x': 1.2, 'y': 0.5,
                  'showactive': True,
                  'active': 0,
                  'buttons': my_buttons}]})
fig.update_xaxes(rangeslider_visible=True)
fig.update_xaxes(tickangle=40)
fig.show()


# In[16]:


fig = px.line(df_na, x='Perioden', y='TotaalGemUitgavenPerVakantieganger_129',
              title='Leeftijdsgroepen per jaartal',
              labels={'variable': 'Leeftijdcategoriën', 'value': 'Aantal', 'Perioden': 'Jaartal'})
fig.update_layout(title_x=0.5)
fig.update_xaxes(tickangle=40)

fig.show()
st.write(fig)


# In[ ]:




