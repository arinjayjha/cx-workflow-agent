# workflow_graph.py
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import time

# ⚙️ Create and style the CX Agent Flow Graph
def show_cx_flow(active_stage=None):
    """
    Draws a 3-node agent flow diagram.
    Highlights the 'active_stage' in bright cyan during animation.
    """

    # Define workflow
    G = nx.DiGraph()
    agents = ["Customer Support", "Technical Expert", "QA Reviewer"]
    G.add_nodes_from(agents)
    G.add_edges_from([
        ("Customer Support", "Technical Expert"),
        ("Technical Expert", "QA Reviewer")
    ])

    # Layout (horizontal)
    pos = {
        "Customer Support": (0, 0),
        "Technical Expert": (1, 0),
        "QA Reviewer": (2, 0)
    }

    # Define colors for all agents
    base_color = "#0078ff"   # blue
    active_color = "#00ffff" # cyan glow
    colors = [
        active_color if a == active_stage else base_color for a in agents
    ]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#000000")

    # Draw edges
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        arrows=True, arrowstyle='-|>',
        arrowsize=25, edge_color="white", width=2
    )

    # Draw nodes with glow effect
    nx.draw_networkx_nodes(
        G, pos,
        node_color=colors,
        node_size=6000,
        alpha=0.95
    )

    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        labels={n: n for n in G.nodes()},
        font_size=12,
        font_color="white",
        font_weight="bold"
    )

    plt.axis("off")
    plt.margins(x=0.15)
    plt.title("🔄 CX Workflow Agent Flow", color="white", fontsize=13, pad=20)

    st.pyplot(fig)


# 🚀 Animated Flow (called from streamlit_app)
def animate_cx_flow():
    """
    Sequentially lights up the CX workflow: Support → Tech → QA
    """
    st.subheader("🧩 Agent Flow Visualization")

    steps = ["Customer Support", "Technical Expert", "QA Reviewer"]
    graph_placeholder = st.empty()

    for step in steps:
        graph_placeholder.empty()
        with graph_placeholder.container():
            show_cx_flow(active_stage=step)
        st.markdown(
            f"<p style='text-align:center; color:cyan;'>🟢 Active: <b>{step}</b></p>",
            unsafe_allow_html=True
        )
        time.sleep(1.2)

    graph_placeholder.empty()
    with graph_placeholder.container():
        show_cx_flow(active_stage=None)
    st.markdown(
        "<p style='text-align:center; color:limegreen;'>✅ Workflow Complete!</p>",
        unsafe_allow_html=True
    )
