import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from utils.st_helpers import centered_caption
from utils.stats_helpers import get_best_poly, get_worst_poly


def visualize_chain_plotly(coords: np.ndarray, names: np.ndarray):
    x = coords[:, 0]
    y = coords[:, 1]
    colors = ['#E41A1C' if name == 'H' else '#377EB8' for name in names]

    fig = go.Figure(data=go.Scatter(x=x, y=y,
                                    mode="markers+lines",
                                    line=dict(color='rgba(255, 255, 255, 0.5)', width=2)))

    # visible = False turns off "locked" zooming
    fig.update_xaxes(visible=False)
    fig.update_yaxes(scaleanchor="x",
                     scaleratio=1,
                     visible=False)

    fig.update_layout(dragmode='pan',
                      margin=dict(l=0, r=0, t=0, b=0))

    fig.update_traces(marker=dict(color=colors, size=15),
                      hoverinfo='none')

    return fig


def graph_energies(energy_stats: list):
    energies = np.array(energy_stats) # Convert to numpy array for efficiency

    x = np.arange(energies.shape[0])

    min_e = energies[:, 0]
    q1_e = energies[:, 1]
    med_e = energies[:, 2]
    q3_e = energies[:, 3]
    max_e = energies[:, 4]

    fig = go.Figure()

    # Min Boundary
    fig.add_trace(go.Scatter(x=x, y=min_e,
                             mode='lines',
                             line=dict(color='rgba(220, 238, 243, 0.1)', width=0),
                             name='Min',
                             showlegend=False))

    # Max Boundary + Fill
    fig.add_trace(go.Scatter(x=x, y=max_e,
                             mode='lines',
                             line=dict(color='rgba(220, 238, 243, 0.1)', width=0),
                             fill='tonexty',
                             name='Range',
                             showlegend=True))

    # Q1
    fig.add_trace(go.Scatter(x=x, y=q1_e,
                             mode='lines',
                             line=dict(color='rgba(0, 92, 171, 0.3)', width=0),
                             name='Q1',
                             showlegend=False))

    # Q3 + Fill
    fig.add_trace(go.Scatter(x=x, y=q3_e,
                             mode='lines',
                             line=dict(color='rgba(0, 92, 171, 0.3)', width=0),
                             fill='tonexty',
                             name='IQR',
                             showlegend=True))

    # Median
    fig.add_trace(go.Scatter(x=x, y=med_e,
                             mode='lines',
                             line=dict(color='rgba(0, 45, 106, 1)', width=3),
                             name='Median'))

    fig.update_layout(dragmode='pan',
                      margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(itemclick=False, itemdoubleclick=False),
                      xaxis_title = 'Generation',
                      yaxis_title = 'Score')

    fig.update_yaxes(scaleanchor=None, # Kill "janky" zooming
                     scaleratio=None,
                     rangemode='tozero',
                     fixedrange=True)

    return fig

def plot_energies(container: DeltaGenerator = st):
    energy_graph_fig = graph_energies(st.session_state['energy_statistics'])
    container.plotly_chart(energy_graph_fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch')


def graph_deaths(deaths: dict):
    # Get all ages
    ages = list(deaths.keys())
    # Sort ages
    ages.sort()
    death_counts = [deaths[age] for age in ages]


    fig = go.Figure(go.Bar(x=ages, y=death_counts))

    # If no one has died, last age = 50 (default)
    last_age = ages[-1] if ages else 50

    # If no-one has died, set max count to 10
    max_count = max(death_counts, default=10)

    fig.update_xaxes(range=[-0.5, last_age])
    fig.update_yaxes(range=[-0.1, math.log10(max_count)], # default range
                     fixedrange=True, # no scrolling below 0
                     type='log',
                     dtick=1) # ticks every 10^1

    fig.update_layout(dragmode='pan',
                      xaxis_title='Polymer Age',
                      yaxis_title='Count')

    return fig

def plot_deaths(deaths: dict, key_suffix: str, container: DeltaGenerator = st):
    fig = graph_deaths(deaths)
    container.plotly_chart(fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch',
                           key=f"deaths_{key_suffix}")

def graph_selection_differential(sd: list):
    x = np.arange(1, len(sd) + 1)

    fig = go.Figure(go.Scatter(x=x, y=sd))

    fig.update_yaxes(fixedrange=True)

    fig.update_layout(dragmode='pan',
                      xaxis_title='Generations',
                      yaxis_title='Selection Differential')

    return fig

def plot_selection_differential(sd: list, key_suffix: str, container: DeltaGenerator = st):
    fig = graph_selection_differential(sd)

    container.plotly_chart(fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch', key=f'selection_diff{key_suffix}')

def graph_pop_scores(scores: list):
    fig = go.Figure(data=[go.Histogram(x=scores)])

    fig.update_yaxes(fixedrange=True)

    fig.update_layout(dragmode='pan',
                      xaxis_title='Scores',
                      yaxis_title='Count',
                      margin=dict(l=0, r=0, t=0, b=0))

    return fig

def plot_pop_scores(scores: list, key_suffix: str, container: DeltaGenerator = st):
    fig = graph_pop_scores(scores)

    container.plotly_chart(fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch', key=f'pop_scores{key_suffix}')

# Graph the current generation's best polymer
def plot_cur_best(key_suffix: str, container: DeltaGenerator = st, container_caption: DeltaGenerator = st):
    best_poly = get_best_poly(st.session_state['population'])

    fig = visualize_chain_plotly(best_poly.coords.copy(), best_poly.names.copy())
    centered_caption(f"Best Polymer in Generation {st.session_state['current_generation']}: Score = {best_poly.energy}", container_caption)
    container.plotly_chart(fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch',
                           key=f'current_best_plot{key_suffix}')

# Graph the current generation's worst polymer
def plot_cur_worst(key_suffix: str, container: DeltaGenerator = st, container_caption: DeltaGenerator = st):
    worst_poly = get_worst_poly(st.session_state['population'])

    fig = visualize_chain_plotly(worst_poly.coords.copy(), worst_poly.names.copy())
    centered_caption(f"Worst Polymer in Generation {st.session_state['current_generation']}: Score = {worst_poly.energy}", container_caption)
    container.plotly_chart(fig,
                           config={"scrollZoom": True, 'displayModeBar': False},
                           width='stretch',
                           key=f'current_worst_plot{key_suffix}')

def plot_polymer(coords: np.ndarray, names: np.ndarray, key: str, container: DeltaGenerator = st):
    fig = visualize_chain_plotly(coords, names)

    container.plotly_chart(fig,
                    config={"scrollZoom": True, 'displayModeBar': False},
                    width='stretch', key=key)