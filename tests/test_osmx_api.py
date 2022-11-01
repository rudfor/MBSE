import pytest
import sys
import os
import sim_libs

rel_path = os.path.dirname(__file__)
sys.path.append(os.path.join(rel_path, "..", "..", "release"))

def test_graph():
    graph = sim_libs.map.OsmnxApi()
    assert isinstance(graph, sim_libs.map.OsmnxApi)


@pytest.mark.skip(reason="this only plots no assertion")
def test_plot_graph():
    graph = sim_libs.map.OsmnxApi()
    fig, ax = graph.plot_graph()
    print(f"{fig} - {ax}")


@pytest.mark.parametrize(
    "city_country, network_type, nodes",
    [
        (
                r"Leiden, Netherlands",
                r"drive",
                3124,
        ),
        (
                r"Lyngby, Denmark",
                r"drive",
                9,
        ),
        (
                r"Amager, Denmark",
                r"drive",
                3374,
            r"Leiden, Netherlands",
            r"drive",
            3122,
        ),
        (
            r"Lyngby, Denmark",
            r"drive",
            9,
        ),
        (
            r"Amager, Denmark",
            r"drive",
            3374,
        ),
    ],
)
def test_list_of_nodes(city_country, network_type, nodes):
    graph = sim_libs.map.OsmnxApi(city_country, network_type)
    assert graph.len_nodes()*0.95 <= nodes <= graph.len_nodes()*1.05


@pytest.mark.parametrize(
    "city_country, network_type, nodes, start, end",
    [
        (
                r"Leiden, Netherlands",
                r"drive",
                3122,
                8078549,
                17556263,
        ),
        (
                r"Amager, Denmark",
                r"drive",
                3374,
                1243575961,
                3464076106,
        ),
    ],
)
def test_route(city_country, network_type, nodes, start, end):
    """
    :param city_country:
    :param network_type:
    :param nodes:
    :param start:           # not in use
    :param end:             # not in use
    :return:
    """
    graph = sim_libs.map.OsmnxApi(city_country, network_type)
    start, end, bike_dist = graph.route()
    print(f"{start} - {end} - {graph.route_length_drone(start, end)} ")
    assert graph.route_length_drone(start, end) <= graph.route_length_bike(bike_dist)
