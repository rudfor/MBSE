import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import numpy as np

#https://stackoverflow.com/questions/51258029/plotting-multiple-routes-with-osmnx
#https://towardsdatascience.com/find-and-plot-your-optimal-path-using-plotly-and-networkx-in-python-17e75387b873
def plot_path(lat, long, origin_point, destination_point):
    """
    Given a list of latitudes and longitudes, origin
    and destination point, plots a path on a map

    Parameters
    ----------
    lat, long: list of latitudes and longitudes
    origin_point, destination_point: co-ordinates of origin
    and destination
    Returns
    -------
    Nothing. Only shows the map.
    """
    # adding the lines joining the nodes
    fig = go.Figure(go.Scattermapbox(
        name="Path",
        mode="lines",
        lon=long,
        lat=lat,
        marker={'size': 10},
        line=dict(width=4.5, color='blue')))
    # adding source marker
    fig.add_trace(go.Scattermapbox(
        name="Source",
        mode="markers",
        lon=[origin_point[1]],
        lat=[origin_point[0]],
        marker={'size': 12, 'color': "red"}))

    # adding destination marker
    fig.add_trace(go.Scattermapbox(
        name="Destination",
        mode="markers",
        lon=[destination_point[1]],
        lat=[destination_point[0]],
        marker={'size': 12, 'color': 'green'}))

    # getting center for plots:
    lat_center = np.mean(lat)
    long_center = np.mean(long)
    # defining the layout using mapbox_style
    fig.update_layout(mapbox_style="stamen-terrain",
                      mapbox_center_lat=30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox={
                          'center': {'lat': lat_center,
                                     'lon': long_center},
                          'zoom': 13})
    fig.show()


def node_list_to_path(G, node_list):
    """
    Given a list of nodes, return a list of lines that together
    follow the path
    defined by the list of nodes.
    Parameters
    ----------
    G : networkx multidigraph
    route : list
        the route as a list of nodes
    Returns
    -------
    lines : list of lines given as pairs ( (x_start, y_start),
    (x_stop, y_stop) )
    """
    edge_nodes = list(zip(node_list[:-1], node_list[1:]))
    lines = []
    for u, v in edge_nodes:
        # if there are parallel edges, select the shortest in length
        data = min(G.get_edge_data(u, v).values(),
                   key=lambda x: x['length'])
        # if it has a geometry attribute
        if 'geometry' in data:
            # add them to the list of lines to plot
            xs, ys = data['geometry'].xy
            lines.append(list(zip(xs, ys)))
        else:
            # if it doesn't have a geometry attribute,
            # then the edge is a straight line from node to node
            x1 = G.nodes[u]['x']
            y1 = G.nodes[u]['y']
            x2 = G.nodes[v]['x']
            y2 = G.nodes[v]['y']
            line = [(x1, y1), (x2, y2)]
            lines.append(line)
    return lines


#state = ox.gdf_from_place('Georgia, US')
#ox.plot_shape(ox.project_gdf(state))

# Defining the map boundaries
#north, east, south, west = 33.798, -84.378, 33.763, -84.422
north, east, south, west = 55.8279, 12.3406, 55.7995, 12.4209
# Downloading the map as a graph object
G = ox.graph_from_bbox(north, south, east, west, network_type = 'drive')
# Plotting the map graph
#print(list(G.nodes(data=True))[2])
#print(list(G.nodes(data=True))[20])
if True:
    count_nodes = 0
    for node in list(G.nodes(data=True)):
        count_nodes += 1
        print(f"{count_nodes} - {node}")

if False:
    count_edges = 0
    for edge in list(G.edges(data=True)):
        count_edges += 1
        print(f"{count_edges} - {edge}")

#ox.plot_graph(G)

#origin_point = list(G.nodes(data=True))[1]
# Displaying the shape of edge using the geometry
pointA = 5
pointB = 750
origin_point_x = list(G.nodes(data=True))[pointA][1]['x']
origin_point_y = list(G.nodes(data=True))[pointA][1]['y']
origin_point = (origin_point_y, origin_point_x)
destination_point_x = list(G.nodes(data=True))[pointB][1]['x']
destination_point_y = list(G.nodes(data=True))[pointB][1]['y']
destination_point = (destination_point_y, destination_point_x)

print(f"ON to DN : {origin_point} : {destination_point}")

origin_node = ox.nearest_nodes(G, origin_point_x, origin_point_y)
destination_node = ox.nearest_nodes(G, destination_point_x, destination_point_y)

print(f"ON to DN : {origin_node} : {destination_node}")
# Finding the optimal path
route = nx.shortest_path(G, origin_node, destination_node, weight = 'length') #route
print(f"ROUTE: {route}")

# we will store the longitudes and latitudes in following list
long = []
lat = []
for i in route:
     point = G.nodes[i]
     long.append(point['x'])
     lat.append(point['y'])

plot_path(lat, long, origin_point, destination_point)

# getting the list of coordinates from the path
# (which is a list of nodes)
lines = node_list_to_path(G, route)
long2 = []
lat2 = []
for i in range(len(lines)):
    z = list(lines[i])
    l1 = list(list(zip(*z))[0])
    l2 = list(list(zip(*z))[1])
    for j in range(len(l1)):
        long2.append(l1[j])
        lat2.append(l2[j])

print("Length of lat: ", len(lat))
print("Length of lat2: ", len(lat2))

plot_path(lat2, long2, origin_point, destination_point)

# Displaying the 3rd node
#list(G.nodes(data=True))[20]