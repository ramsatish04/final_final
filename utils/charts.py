"""Chart helper functions."""
import pandas as pd
import plotly.express as px
from typing import List, Dict

def expenses_pie(expenses: List[Dict]) -> 'plotly.graph_objs._figure.Figure':
    """Return a pie chart showing paid/unpaid by category."""
    if not expenses:
        return px.pie(title="No expense data yet")
    df = pd.DataFrame(expenses)
    df['status_label'] = df['category'] + ' - ' + df['status']
    return px.pie(
        df, 
        names='status_label', 
        values='amount',
        title='Expenses: Paid vs Unpaid by Category'
    )

def sleep_line(sleep_records: List[Dict]) -> 'plotly.graph_objs._figure.Figure':
    """Return a 7‑day line graph of sleep hours."""
    if not sleep_records:
        return px.line(title="No sleep data yet")
    df = pd.DataFrame(sleep_records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').tail(7)
    return px.line(df, x='date', y='hours', markers=True, title='Sleep Hours (Last 7 Days)')
