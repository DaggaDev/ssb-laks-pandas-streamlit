# Post spørring og få Pandas dataframe i retur
# benytter biblioteket pyjstat for JSON-stat
# Viser data som Streamlit DataFrame


from pyjstat import pyjstat
import requests
import streamlit as st

st.write("Streamlit app som henter fryst og fersk laks siste 53 uker og viser data i en dataFrame")

numWeeks=st.slider("Antall uker", min_value=2, max_value=53, value=10)

# Eksport av laks
POST_URL = 'https://data.ssb.no/api/v0/no/table/03024'

# API spørring, kan tas fra Konsoll  - fryst og fersk laks siste x uker (bestemmes av bruker)
payload = {"query": [
			{"code": "VareGrupper2", "selection": {"filter": "item", "values": ["01", "02"] } },
			{"code": "ContentsCode", "selection": {"filter": "item", "values": ["Vekt", "Kilopris"] } },
			{"code": "Tid", "selection": {"filter": "top", "values": [numWeeks] } }
		],
		"response": {"format": "json-stat2"}
		}

resultat = requests.post(POST_URL, json = payload)
# Resultat gir bare http statuskode - 200 hvis OK. Body ligger i resultat.text

dataset = pyjstat.Dataset.read(resultat.text)
df = dataset.write('dataframe')

st.dataframe(df)

