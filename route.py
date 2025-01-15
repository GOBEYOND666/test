import networkx as nx
import matplotlib.pyplot as plt
import random


# 1. 创建一个随机网络拓扑
def create_random_topology(num_nodes, num_edges):
    """
    创建一个随机网络拓扑。

    参数:
        num_nodes: 节点数量。
        num_edges: 边数量。

    返回:
        G: 网络图对象。
    """
    G = nx.gnm_random_graph(num_nodes, num_edges)
    return G


# 2. 模拟匿名路由
def apply_anonymous_routing(G, hide_ratio):
    """
    模拟匿名路由，随机隐藏部分节点和边。

    参数:
        G: 原始网络图对象。
        hide_ratio: 隐藏节点和边的比例（0 到 1 之间）。

    返回:
        G_anonymous: 匿名路由后的网络图对象。
        hidden_nodes: 被隐藏的节点列表。
        hidden_edges: 被隐藏的边列表。
    """
    G_anonymous = G.copy()

    # 随机隐藏节点
    nodes_to_hide = random.sample(list(G.nodes), int(hide_ratio * G.number_of_nodes()))
    hidden_nodes = nodes_to_hide.copy()
    G_anonymous.remove_nodes_from(nodes_to_hide)

    # 随机隐藏边
    edges_to_hide = random.sample(list(G.edges), int(hide_ratio * G.number_of_edges()))
    hidden_edges = edges_to_hide.copy()
    G_anonymous.remove_edges_from(edges_to_hide)

    return G_anonymous, hidden_nodes, hidden_edges


# 3. 标记匿名路由
def mark_anonymous_routes(G, hidden_nodes, hidden_edges):
    """
    标记匿名路由中被隐藏的节点和边。

    参数:
        G: 原始网络图对象。
        hidden_nodes: 被隐藏的节点列表。
        hidden_edges: 被隐藏的边列表。

    返回:
        G_marked: 标记后的网络图对象。
    """
    G_marked = G.copy()

    # 标记被隐藏的节点
    for node in hidden_nodes:
        G_marked.nodes[node]['hidden'] = True

    # 标记被隐藏的边
    for edge in hidden_edges:
        G_marked.edges[edge]['hidden'] = True

    return G_marked


# 4. 还原拓扑网络
def restore_topology(G_anonymous, hidden_nodes, hidden_edges):
    """
    还原拓扑网络，添加被隐藏的节点和边。

    参数:
        G_anonymous: 匿名路由后的网络图对象。
        hidden_nodes: 被隐藏的节点列表。
        hidden_edges: 被隐藏的边列表。

    返回:
        G_restored: 还原后的网络图对象。
    """
    G_restored = G_anonymous.copy()

    # 添加被隐藏的节点
    G_restored.add_nodes_from(hidden_nodes)

    # 添加被隐藏的边
    G_restored.add_edges_from(hidden_edges)

    return G_restored


# 5. 绘制拓扑图
def draw_topology(G, title, hidden_nodes=None, hidden_edges=None):
    """
    绘制网络拓扑图。

    参数:
        G: 网络图对象。
        title: 图的标题。
        hidden_nodes: 被隐藏的节点列表。
        hidden_edges: 被隐藏的边列表。
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # 使用弹簧布局算法

    # 绘制节点
    node_colors = []
    for node in G.nodes:
        if hidden_nodes and node in hidden_nodes:
            node_colors.append('red')  # 被隐藏的节点用红色标记
        else:
            node_colors.append('lightblue')
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

    # 绘制边
    edge_colors = []
    for edge in G.edges:
        if hidden_edges and edge in hidden_edges:
            edge_colors.append('red')  # 被隐藏的边用红色标记
        else:
            edge_colors.append('gray')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)

    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title(title)
    plt.show()


# 6. 主程序
if __name__ == "__main__":
    # 创建随机拓扑
    num_nodes = 20
    num_edges = 30
    G = create_random_topology(num_nodes, num_edges)

    # 绘制原始拓扑图
    draw_topology(G, "Original Topology")

    # 模拟匿名路由
    hide_ratio = 0.3  # 隐藏 30% 的节点和边
    G_anonymous, hidden_nodes, hidden_edges = apply_anonymous_routing(G, hide_ratio)

    # 绘制匿名路由后的拓扑图
    draw_topology(G_anonymous, f"Topology After Anonymous Routing (Hide Ratio: {hide_ratio})")

    # 标记匿名路由
    G_marked = mark_anonymous_routes(G, hidden_nodes, hidden_edges)

    # 绘制标记后的拓扑图
    draw_topology(G_marked, "Topology with Marked Anonymous Routes", hidden_nodes, hidden_edges)

    # 还原拓扑网络
    G_restored = restore_topology(G_anonymous, hidden_nodes, hidden_edges)

    # 绘制还原后的拓扑图
    draw_topology(G_restored, "Restored Topology")