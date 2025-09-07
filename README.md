# 🚇 Urban Mobility Analysis in Barcelona
Urban mobility analysis in Barcelona using open data from TMB, Renfe, and Bicing.
Explores transportation patterns with geospatial visualizations, detects behaviors of stations through clustering (KMeans/DBSCAN), and builds a predictive model for bike demand. Includes reproducible notebooks, data processing scripts, and a Streamlit dashboard (in progress).

# Project overview
This project aims to understand and model mobility patterns in Barcelona by integrating multiple transport modes:  
- Public transport (TMB metro/bus, Renfe trains)  
- Shared mobility (Bicing)  
- Contextual factors (traffic counts, weather)  

The goals are to:  
1. Explore and visualize mobility flows.  
2. Segment stations and areas using clustering.  
3. Build a predictive model for bike demand.  
4. Provide an interactive dashboard for insights.

# Tech stack
- Python: pandas, numpy, geopandas, scikit-learn, statsmodels  
- isualization: matplotlib, plotly, folium/keplergl  
- Machine Learning: KMeans, DBSCAN, SARIMAX, LightGBM/XGBoost  
- Dashboard: Streamlit

# Data sources
- TMB Developers (GTFS)(https://developer.tmb.cat/) – metro and bus schedules  
- Renfe Datos Abiertos(https://data.renfe.com/pages/home/) – train positions and timetables  
- Bicing (GBFS)(https://opendata-ajuntament.barcelona.cat/data/en/dataset/estacions-bicing) – bike station availability  
- Open Data BCN (https://opendata-ajuntament.barcelona.cat/en) – bus stops, bike lanes, traffic counts  
- AEMET OpenData (https://opendata.aemet.es/) – weather conditions

# Project status
Work in progress

# License
This project is released under the MIT License.  
