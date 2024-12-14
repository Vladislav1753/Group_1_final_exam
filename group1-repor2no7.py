import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import networkx as nx
import random

# Set up custom navigation with links
def navigation(current_page):
    st.markdown(
        f"""
        <style>
        .navigation {{
            background-color: #f2f2f2;
            padding: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .navigation a {{
            text-decoration: none;
            color: #007BFF;
            margin: 0 15px;
            font-weight: bold;
            font-size: 16px;
        }}
        .navigation a:hover {{
            text-decoration: underline;
        }}
        .navigation a.active {{
            color: gray;
            pointer-events: none;
            text-decoration: none;
        }}
        </style>
        <div class="navigation">
            <a href="/?page=map" class="{ 'active' if current_page == 'map' else '' }">City Connections Map</a>
            <a href="/?page=graph" class="{ 'active' if current_page == 'graph' else '' }">Graph Generator</a>
            <a href="/?page=team" class="{ 'active' if current_page == 'team' else '' }">Team Members</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Get the current page from query parameters
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["map"])[0]

# Render navigation with the current page
navigation(current_page=page)

# Page 1: City Connections Map
if page == "map":
    st.title("City Connections in Java Provinces on Map")
    st.write("Select a province to view the city connections on an interactive map.")

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

# Page 2: Graph Generator
elif page == "graph":
    st.title("Graph Generator with Python")
    st.write("Select the number of nodes and edges to generate a random graph.")

    # User input for the number of nodes and edges
    n_nodes = st.number_input("Number of nodes:", min_value=2, max_value=100, value=7, step=1)
    n_edges = st.number_input(
        "Number of edges:", min_value=1, max_value=n_nodes * (n_nodes - 1) // 2, value=6, step=1
    )

    # Button to generate the graph
    if st.button("Generate Graph"):
        # Create a graph
        G = nx.Graph()

        # Add nodes
        for i in range(1, n_nodes + 1):
            G.add_node(i)

        # Add edges
        edges = set()
        while len(edges) < n_edges:
            random_1 = random.randint(1, n_nodes)
            random_2 = random.randint(1, n_nodes)
            if random_1 != random_2:
                edge = tuple(sorted((random_1, random_2)))
                if edge not in edges:
                    edges.add(edge)
                    G.add_edge(*edge)

        # Visualize the graph
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw(
            G, 
            with_labels=True, 
            node_color="green", 
            node_size=1000, 
            font_weight="bold", 
            font_size=15, 
            ax=ax
        )
        st.pyplot(fig)  # Display the graph in Streamlit

# Page 3: Team Members
elif page == "team":
    st.title("Meet Group 1")
    st.write("Here are the amazing people behind this little project:")

    team_members = [
        "Shafira Salsabiila",
        "Vladyslav Baklanov",
        "Nevin Kenneth",
        "Tirza"
    ]

    for member in team_members:
        st.write(f"- {member}")
