import streamlit as st
import folium
from streamlit_folium import st_folium

# Predefined data for provinces, cities, and their connections
province_data = {
    "West Java": {
        "cities": {
            "Bandung": (-6.914744, 107.609810),
            "Cirebon": (-6.737246, 108.552315),
            "Bekasi": (-6.238270, 106.975573),
            "Depok": (-6.402484, 106.794241),
            "Bogor": (-6.595038, 106.816635),
            "Cianjur": (-6.822940, 107.139098),
        },
        "connections": [
            ("Bandung", "Cirebon"),
            ("Bandung", "Bekasi"),
            ("Bekasi", "Depok"),
            ("Depok", "Bogor"),
            ("Bogor", "Cianjur"),
        ],
    },
    "Central Java": {
        "cities": {
            "Semarang": (-6.966667, 110.416664),
            "Surakarta": (-7.574222, 110.828808),
            "Tegal": (-6.868710, 109.141247),
            "Magelang": (-7.470474, 110.217529),
            "Purwokerto": (-7.424460, 109.239639),
            "Cilacap": (-7.720533, 109.015301),
        },
        "connections": [
            ("Semarang", "Surakarta"),
            ("Semarang", "Tegal"),
            ("Surakarta", "Magelang"),
            ("Magelang", "Purwokerto"),
            ("Purwokerto", "Cilacap"),
        ],
    },
    "East Java": {
        "cities": {
            "Surabaya": (-7.257472, 112.752090),
            "Malang": (-7.966620, 112.632629),
            "Madiun": (-7.629838, 111.523850),
            "Kediri": (-7.817550, 112.011780),
            "Blitar": (-8.095905, 112.162762),
            "Banyuwangi": (-8.219233, 114.369141),
        },
        "connections": [
            ("Surabaya", "Malang"),
            ("Surabaya", "Madiun"),
            ("Malang", "Kediri"),
            ("Kediri", "Blitar"),
            ("Blitar", "Banyuwangi"),
        ],
    },
}

# Streamlit app interface
st.title("City Connections in Java Provinces on Map")
st.write("Select a province to view the city connections on an interactive map.")

# Province selection
province = st.selectbox("Choose a Province:", list(province_data.keys()))

# Display map for the selected province
if province:
    data = province_data[province]
    cities = data["cities"]
    connections = data["connections"]

    # Create a map centered at the first city in the province
    first_city_coords = list(cities.values())[0]
    folium_map = folium.Map(location=first_city_coords, zoom_start=8)

    # Add city markers
    for city, coords in cities.items():
        folium.Marker(
            location=coords, popup=city, tooltip=city, icon=folium.Icon(color="blue")
        ).add_to(folium_map)

    # Add lines between connected cities
    for connection in connections:
        city1, city2 = connection
        if city1 in cities and city2 in cities:
            folium.PolyLine(
                locations=[cities[city1], cities[city2]],
                color="green",
                weight=5,
                opacity=0.8,
            ).add_to(folium_map)

    # Embed the map in the Streamlit app
    st_folium(folium_map, width=700, height=500)