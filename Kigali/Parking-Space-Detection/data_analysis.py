import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
from datetime import datetime, timedelta


def get_connection():
    return sqlite3.connect('integrated_system.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


def get_historical_data(days=30):
    """Retrieve historical parking data from the database."""
    conn = get_connection()

    query = '''
    SELECT 
        date as Date,
        COALESCE(avg_empty_spots, 0) as Empty_Spots,
        COALESCE(avg_filled_spots, 0) as Filled_Spots,
        COALESCE(avg_efficiency, 0) as Parking_Efficiency,
        peak_hours as Peak_Hours,
        COALESCE(total_revenue, 0) as Revenue,
        COALESCE(total_vehicles, 0) as Vehicles
    FROM daily_summaries
    WHERE date >= date('now', ?)
    ORDER BY date
    '''

    df = pd.read_sql_query(query, conn, params=(f'-{days} days',))

    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Empty_Spots'] = df['Empty_Spots'].astype(float).round(0)
        df['Filled_Spots'] = df['Filled_Spots'].astype(float).round(0)
        df['Parking_Efficiency'] = df['Parking_Efficiency'].astype(float)
        df['Revenue'] = df['Revenue'].astype(float).round(2)
        df['Vehicles'] = df['Vehicles'].astype(int)

    conn.close()
    return df


def get_todays_data():
    """Retrieve today's parking data from the database."""
    conn = get_connection()
    query = '''
    SELECT 
        timestamp,
        COALESCE(empty_spots, 0) as empty_spots,
        COALESCE(filled_spots, 0) as filled_spots,
        COALESCE(efficiency, 0) as efficiency,
        COALESCE(revenue, 0) as revenue
    FROM parking_analytics
    WHERE date(timestamp) = date('now')
    ORDER BY timestamp
    '''
    df = pd.read_sql_query(query, conn, parse_dates=['timestamp'])
    conn.close()
    return df


def render_data_analysis():
    """Render the comprehensive data analysis dashboard."""
    st.title("📊 Parking Data Analysis")

    # Get historical data
    df = get_historical_data()

    if df.empty:
        st.warning("No historical data available. Please analyze some parking images first.")
        return

    # Create dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Real-time Metrics",
        "🚗 Parking Occupancy",
        "💰 Revenue Analysis",
        "📊 Advanced Analytics"
    ])

    with tab1:
        render_realtime_metrics(df)

    with tab2:
        render_parking_occupancy(df)

    with tab3:
        render_revenue_analysis(df)

    with tab4:
        render_advanced_analytics(df)


def render_realtime_metrics(df):
    st.header("Real-time Parking Metrics")

    # Current metrics
    today_data = get_todays_data()
    if not today_data.empty:
        latest_data = today_data.iloc[-1]
        col1, col2, col3 = st.columns(3)
        with col1:
            current_empty = latest_data['empty_spots']
            previous_empty = today_data.iloc[-2]['empty_spots'] if len(today_data) > 1 else current_empty
            st.metric(
                label="Empty Spots",
                value=f"{current_empty:,.0f}",
                delta=f"{current_empty - previous_empty:,.0f}"
            )

        with col2:
            current_filled = latest_data['filled_spots']
            previous_filled = today_data.iloc[-2]['filled_spots'] if len(today_data) > 1 else current_filled
            st.metric(
                label="Filled Spots",
                value=f"{current_filled:,.0f}",
                delta=f"{current_filled - previous_filled:,.0f}"
            )

        with col3:
            current_efficiency = latest_data['efficiency']
            previous_efficiency = today_data.iloc[-2]['efficiency'] if len(today_data) > 1 else current_efficiency
            st.metric(
                label="Parking Efficiency",
                value=f"{current_efficiency:.1%}",
                delta=f"{(current_efficiency - previous_efficiency):.1%}"
            )

        # Real-time trend chart
        st.subheader("Today's Parking Trends")
        fig_today = px.line(today_data, x='timestamp', y=['empty_spots', 'filled_spots'],
                            title="Today's Parking Occupancy")
        fig_today.update_layout(xaxis_title="Time", yaxis_title="Number of Spots")
        st.plotly_chart(fig_today, use_container_width=True)
    else:
        st.warning("No data available for today yet.")


def render_parking_occupancy(df):
    st.header("Parking Occupancy Analysis")

    # Occupancy trend
    fig_occupancy = px.bar(
        df,
        x='Date',
        y=['Empty_Spots', 'Filled_Spots'],
        title='Parking Occupancy Trend',
        barmode='stack'
    )
    fig_occupancy.update_layout(xaxis_title="Date", yaxis_title="Number of Spots")
    st.plotly_chart(fig_occupancy, use_container_width=True)

    # Efficiency trend
    fig_efficiency = px.line(
        df,
        x='Date',
        y='Parking_Efficiency',
        title='Parking Efficiency Over Time'
    )
    fig_efficiency.update_layout(xaxis_title="Date", yaxis_title="Efficiency")
    fig_efficiency.update_traces(y=df['Parking_Efficiency'].apply(lambda x: x * 100))  # Convert to percentage
    st.plotly_chart(fig_efficiency, use_container_width=True)

    # Vehicle count trend
    fig_vehicles = px.bar(
        df,
        x='Date',
        y='Vehicles',
        title='Daily Vehicle Count'
    )
    fig_vehicles.update_layout(xaxis_title="Date", yaxis_title="Number of Vehicles")
    st.plotly_chart(fig_vehicles, use_container_width=True)


def render_revenue_analysis(df):
    st.header("Revenue Analysis")

    # Daily revenue trend
    fig_revenue = px.line(
        df,
        x='Date',
        y='Revenue',
        title='Daily Parking Revenue'
    )
    fig_revenue.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)")
    st.plotly_chart(fig_revenue, use_container_width=True)

    # Revenue by peak hours
    fig_peak_hours = px.bar(
        df,
        x='Date',
        y='Revenue',
        color='Peak_Hours',
        title='Revenue by Peak Hours'
    )
    fig_peak_hours.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)")
    st.plotly_chart(fig_peak_hours, use_container_width=True)

    # Revenue metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_revenue = df['Revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        avg_daily_revenue = df['Revenue'].mean()
        st.metric("Average Daily Revenue", f"${avg_daily_revenue:,.2f}")
    with col3:
        revenue_trend = df['Revenue'].pct_change().mean()
        st.metric("Revenue Trend", f"{revenue_trend:.1%}")


def render_advanced_analytics(df):
    st.header("Advanced Analytics")

    # Correlation analysis
    correlation = df[['Empty_Spots', 'Filled_Spots', 'Parking_Efficiency', 'Revenue']].corr()
    fig_corr = px.imshow(correlation,
                         title='Correlation Matrix',
                         color_continuous_scale='RdBu')
    st.plotly_chart(fig_corr, use_container_width=True)

    # Weekly patterns
    df['WeekDay'] = df['Date'].dt.day_name()
    weekly_stats = df.groupby('WeekDay')['Parking_Efficiency'].mean().reset_index()
    fig_weekly = px.bar(weekly_stats,
                        x='WeekDay',
                        y='Parking_Efficiency',
                        title='Average Parking Efficiency by Day of Week')
    fig_weekly.update_layout(xaxis_title="Day of Week", yaxis_title="Average Efficiency")
    fig_weekly.update_traces(y=weekly_stats['Parking_Efficiency'].apply(lambda x: x * 100))  # Convert to percentage
    st.plotly_chart(fig_weekly, use_container_width=True)

    def populate_sample_data():
        """Populate the database with sample data for testing."""
        conn = get_connection()
        c = conn.cursor()

        # Sample data for daily_summaries
        sample_data = [
            (datetime.now().date() - timedelta(days=i),
             50 - i, 100 + i, 0.66 + (i * 0.01),
             1000 + (i * 100), f"{12 + i}:00-{13 + i}:00", 300 + (i * 10))
            for i in range(30)
        ]

        c.executemany('''
            INSERT OR REPLACE INTO daily_summaries 
            (date, avg_empty_spots, avg_filled_spots, avg_efficiency, total_revenue, peak_hours, total_vehicles)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)

        # Sample data for parking_analytics (today's data)
        today_data = [
            (datetime.now().replace(hour=h, minute=0, second=0, microsecond=0),
             50 - h, 100 + h, 0.66 + (h * 0.01), 100 + (h * 10))
            for h in range(24)
        ]

        c.executemany('''
            INSERT OR REPLACE INTO parking_analytics 
            (timestamp, empty_spots, filled_spots, efficiency, revenue)
            VALUES (?, ?, ?, ?, ?)
        ''', today_data)

        conn.commit()
        conn.close()

    # Add this to your main function or Streamlit app
    if st.button("Populate Sample Data"):
        populate_sample_data()
        st.success("Sample data has been populated in the database.")
