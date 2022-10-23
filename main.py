import osmnx as ox
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    ox.plot_graph(ox.graph_from_place('Amager, Denmark'))
    # G = ox.graph_from_place('Amager, Denmark', network_type='walk')
    # basic_stats = ox.basic_stats(G)
    # print(basic_stats['circuity_avg'])
    # extended_stats = ox.extended_stats(G, bc=True)
    # print(extended_stats['betweenness_centrality_avg'])

    # s = pd.Series([1, 2, 3])
    # fig, ax = plt.subplots()
    # s.plot.bar()
    # fig.savefig('my_plot.png')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
