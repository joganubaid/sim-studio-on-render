import plotly.graph_objects as go
import numpy as np

# Create figure
fig = go.Figure()

# Define positions for components in a cleaner architecture layout
positions = {
    'Users': (2, 9),
    'simstudio': (2, 7),
    'realtime-server': (0.5, 5),
    'simstudio-db': (3.5, 5),
    'simstudio-disk': (2, 5),
    'OpenAI': (0.5, 2),
    'Anthropic': (1.5, 2),
    'Google AI': (2.5, 2),
    'DeepSeek': (3.5, 2),
    'Env Vars': (4.5, 7),
    'Health Check': (4.5, 5)
}

# Define component colors and shapes
components = {
    'Users': {'color': '#1FB8CD', 'size': 25, 'symbol': 'circle', 'type': 'External'},
    'simstudio': {'color': '#FFC185', 'size': 30, 'symbol': 'square', 'type': 'Web Service'},
    'realtime-server': {'color': '#ECEBD5', 'size': 25, 'symbol': 'square', 'type': 'Private Svc'},
    'simstudio-db': {'color': '#5D878F', 'size': 25, 'symbol': 'diamond', 'type': 'Database'},
    'simstudio-disk': {'color': '#D2BA4C', 'size': 20, 'symbol': 'hexagon', 'type': 'Storage'},
    'OpenAI': {'color': '#B4413C', 'size': 15, 'symbol': 'circle', 'type': 'AI API'},
    'Anthropic': {'color': '#964325', 'size': 15, 'symbol': 'circle', 'type': 'AI API'},
    'Google AI': {'color': '#944454', 'size': 15, 'symbol': 'circle', 'type': 'AI API'},
    'DeepSeek': {'color': '#13343B', 'size': 15, 'symbol': 'circle', 'type': 'AI API'},
    'Env Vars': {'color': '#DB4545', 'size': 20, 'symbol': 'triangle-up', 'type': 'Config'},
    'Health Check': {'color': '#1FB8CD', 'size': 20, 'symbol': 'star', 'type': 'Monitor'}
}

# Define connections with directions
connections = [
    ('Users', 'simstudio'),
    ('simstudio', 'realtime-server'),
    ('simstudio', 'simstudio-db'),
    ('realtime-server', 'simstudio-db'),
    ('simstudio', 'simstudio-disk'),
    ('simstudio', 'OpenAI'),
    ('simstudio', 'Anthropic'), 
    ('simstudio', 'Google AI'),
    ('simstudio', 'DeepSeek'),
    ('Env Vars', 'simstudio'),
    ('Env Vars', 'realtime-server'),
    ('Health Check', 'simstudio'),
    ('Health Check', 'realtime-server')
]

# Add connection lines with arrows
for from_comp, to_comp in connections:
    from_pos = positions[from_comp]
    to_pos = positions[to_comp]
    
    # Calculate arrow direction
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    
    fig.add_trace(go.Scatter(
        x=[from_pos[0], to_pos[0]],
        y=[from_pos[1], to_pos[1]],
        mode='lines',
        line=dict(color='#666666', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrowhead
    arrow_x = to_pos[0] - 0.1 * (dx / (dx**2 + dy**2)**0.5) if dx**2 + dy**2 > 0 else to_pos[0]
    arrow_y = to_pos[1] - 0.1 * (dy / (dx**2 + dy**2)**0.5) if dx**2 + dy**2 > 0 else to_pos[1]
    
    fig.add_trace(go.Scatter(
        x=[arrow_x],
        y=[arrow_y],
        mode='markers',
        marker=dict(
            symbol='triangle-up',
            size=8,
            color='#666666',
            angle=np.arctan2(dy, dx) * 180 / np.pi
        ),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add component nodes
legend_added = set()
for comp_name, pos in positions.items():
    comp_info = components[comp_name]
    show_legend = comp_info['type'] not in legend_added
    if show_legend:
        legend_added.add(comp_info['type'])
    
    fig.add_trace(go.Scatter(
        x=[pos[0]], 
        y=[pos[1]],
        mode='markers+text',
        marker=dict(
            symbol=comp_info['symbol'],
            size=comp_info['size'],
            color=comp_info['color'],
            line=dict(width=2, color='white')
        ),
        text=[comp_name],
        textposition="middle center",
        textfont=dict(size=9, color='black'),
        name=comp_info['type'],
        showlegend=show_legend,
        hovertemplate=f"<b>{comp_name}</b><extra></extra>"
    ))

# Update layout
fig.update_layout(
    title="Sim Studio Architecture",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 5.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[1, 10]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save the chart
fig.write_image("sim_studio_architecture.png")