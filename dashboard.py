import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


data = pd.read_csv('cleaned_data_visit.csv', encoding='ISO-8859-1')

data['visit_created_on'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(data['visit_created_on'], 'D')

# Sidebar filters
logo_url = 'logo.svg'  
st.sidebar.image(logo_url, use_column_width=True)

year = st.sidebar.selectbox("Year", options=["All"] + [2023, 2024])
quarter = st.sidebar.selectbox("Quarter", options=["All", "Q1", "Q2", "Q3", "Q4"])
month = st.sidebar.selectbox("Month", options=["All"] + [f"{pd.to_datetime(month, format='%m').strftime('%b')}" for month in range(1, 13)])
visit_type = st.sidebar.selectbox("Visit Type", options=["All"] + data['visit_type'].unique().tolist())


filtered_data = data.copy()
if year != "All":
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.year == int(year)]
if quarter != "All":
    quarters = {"Q1": [1, 2, 3], "Q2": [4, 5, 6], "Q3": [7, 8, 9], "Q4": [10, 11, 12]}
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.month.isin(quarters[quarter])]
if month != "All":
    month_num = pd.to_datetime(month, format='%b').month
    filtered_data = filtered_data[filtered_data['visit_created_on'].dt.month == month_num]
if visit_type != "All":
    filtered_data = filtered_data[filtered_data['visit_type'] == visit_type]

    

# Calculate total visits, average day visits, and average night visits
total_visits = filtered_data.shape[0]
average_day_visits = filtered_data[filtered_data['DayOrNight'] == 'Day'].shape[0] / 12  # Average per month
average_night_visits = filtered_data[filtered_data['DayOrNight'] == 'Night'].shape[0] / 12  # Average per month
average_visits = total_visits / filtered_data['visit_created_on'].dt.to_period('M').nunique()  # Average visits per month

filtered_data['visit_month'] = filtered_data['visit_created_on'].dt.to_period('M')
visits_by_month = filtered_data['visit_month'].value_counts().sort_index()
max_month = visits_by_month.idxmax()
max_month_visits = visits_by_month.max()
max_month_str = max_month.strftime('%b %Y')

st.markdown("""
    <h1 style='text-align: center; color: white;'>SERVICE PROVIDER VISITS DASHBOARD</h1>
    """, unsafe_allow_html=True)
start_date = filtered_data['visit_created_on'].min().strftime('%Y-%m-%d')
end_date = filtered_data['visit_created_on'].max().strftime('%Y-%m-%d')

st.markdown("<br>", unsafe_allow_html=True)  

# Row 0: Start and End Dates
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(f"""
    <div style='height: 70px; background-color: #262730; color: white; text-align: center; padding: 10px; margin: 0 auto;'>
        <strong>Start Date:</strong><br>{start_date}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='height: 70px; background-color: #262730; color: white; text-align: center; padding: 10px; margin: 0 auto;'>
        <strong>End Date:</strong><br>{end_date}
    </div>
    """, unsafe_allow_html=True)
    
    
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Adjust height as needed


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Total Visits</h6>
                <h2 style="margin: 0;">{total_visits}</h2>
            </div>
        </div>
        """.format(total_visits=total_visits), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Average Day Visits</h6>
                <h2 style="margin: 0;">{:.2f}</h2>
            </div>
        </div>
        """.format(average_day_visits), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Average Night Visits</h6>
                <h2 style="margin: 0;">{:.2f}</h2>
            </div>
        </div>
        """.format(average_night_visits), unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Average Visits</h6>
                <h2 style="margin: 0;">{:.2f}</h2>
            </div>
        </div>
        """.format(average_visits), unsafe_allow_html=True)

st.markdown("""
    <div style="background-color: #008040; color: white; padding: 15px; text-align: center; border-radius: 5px; margin-top: 20px;">
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
            <h6 style="margin: 0;">Month with Highest Visits</h6>
            <h2 style="margin: 0;">{max_month_str} ({max_month_visits} visits)</h2>
        </div>
    </div>
    """.format(max_month_str=max_month_str, max_month_visits=max_month_visits), unsafe_allow_html=True)

# Row 3: Graphs Side by Side with Equal Height and Spacing
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)  

    visits_by_month.index = visits_by_month.index.strftime('%b %Y')  

    fig, ax = plt.subplots(figsize=(10, 6))  
    bars = ax.bar(visits_by_month.index, visits_by_month.values, color='#008040')  
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Number of Visits", color='white')
    ax.set_title("Visits by Months of the Year", color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    st.pyplot(fig)

with col2:
    st.markdown("<div style='height: 90px;'></div>", unsafe_allow_html=True)  

    monthly_change = visits_by_month.pct_change() * 100  

    # Plot combined bar and line chart
    fig, ax1 = plt.subplots(figsize=(10, 6))  

    # Bar chart for visits
    color_bar = '#008040'
    ax1.set_xlabel('Month', color='white')
    ax1.set_ylabel('Number of Visits', color=color_bar)
    bars = ax1.bar(visits_by_month.index.astype(str), visits_by_month.values, color=color_bar, alpha=0.7, label='Number of Visits')
    ax1.tick_params(axis='y', labelcolor=color_bar)

    # Line chart for rate of change
    ax2 = ax1.twinx()  
    color_line = '#FF4500'
    ax2.set_ylabel('Rate of Change (%)', color=color_line)  
    line = ax2.plot(visits_by_month.index.astype(str), monthly_change, color=color_line, marker='o', linestyle='-', linewidth=2, label='Rate of Change')
    ax2.tick_params(axis='y', labelcolor=color_line)

    ax1.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()  # adjust layout to fit both y-axes
    plt.title('Monthly Visits and Rate of Change', color='white')

    fig.autofmt_xdate()

    fig.patch.set_facecolor('#0E1117')
    ax1.set_facecolor('#0E1117')
    ax2.set_facecolor('#0E1117')
    ax1.tick_params(axis='x', rotation=45, colors='white')
    ax2.tick_params(axis='x', colors='white')

    # Display plot
    st.pyplot(fig)
    
    
# Calculate day and night visits
day_visits = filtered_data[filtered_data['DayOrNight'] == 'Day'].shape[0]
night_visits = filtered_data[filtered_data['DayOrNight'] == 'Night'].shape[0]

# Plot Seasonal Visits using Plotly for interactivity
fig_seasonal_visits = go.Figure(data=[go.Pie(
    labels=["Day", "Night"],
    values=[day_visits, night_visits],
    hole=0.3,
    textinfo='none',  
    hoverinfo='label+percent',  
    marker=dict(colors=['#008040', '#FF4500']),
)])

fig_seasonal_visits.update_layout(
    title_text="Seasonal Visits",
    title_font_color="white",
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color="white",
    annotations=[dict(
        text="Visits",
        x=0.5,
        y=0.5,
        font_size=20,
        showarrow=False,

    )],
        height=270,
        width=500  

)

# Row 4: Graphs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.plotly_chart(fig_seasonal_visits, use_container_width=True)

with col3:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Total Visits by Day</h6>
                <h2 style="margin: 0;">{}</h2>
            </div>
        </div>
        """.format(day_visits), unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div style="background-color: #FF4500; color: white; padding: 15px; text-align: center; border-radius: 5px;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box;">
                <h6 style="margin: 0;">Total Visits by Night</h6>
                <h2 style="margin: 0;">{}</h2>
            </div>
        </div>
        """.format(night_visits), unsafe_allow_html=True)
    
# Row 5: Top 10 Attending Doctor Specializations Chart
col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

with col1:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  

with col2:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  

with col3:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  

with col4:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  

# Create the horizontal bar chart for Top 10 Attending Doctor Specializations
top_specializations = filtered_data['attending_doctor_specialisation'].value_counts().head(10)
fig_specializations = go.Figure()

fig_specializations.add_trace(go.Bar(
    y=top_specializations.index,
    x=top_specializations.values,
    orientation='h',
    marker=dict(color='#008040'),
    text=top_specializations.values,
    textposition='none',  
    hoverinfo='x+text'  
))

fig_specializations.update_layout(
    title="Top 10 Attending Doctor Specializations",
    xaxis_title="Number of Visits",
    yaxis_title="Doctor Specialization",
    plot_bgcolor='#0E1117',
    paper_bgcolor='#0E1117',
    font=dict(color='white'),
    xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
    yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
    margin=dict(l=0, r=0, t=30, b=50)
)


st.plotly_chart(fig_specializations, use_container_width=True)
    
# Data
visits_by_type = filtered_data['visit_type'].value_counts()

# Create dropdown for visit types
visit_type_options = ['All'] + visits_by_type.index.tolist()

# Row 5: Dropdown and Pie Chart
st.markdown("<br>", unsafe_allow_html=True)  # Add space between rows
col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_visit_type = st.selectbox('Select Visit Type', visit_type_options, key='visit_type_dropdown')

# Filter data based on selected visit type
if selected_visit_type != 'All':
    filtered_visits = visits_by_type.copy()
    for visit_type in visits_by_type.index:
        if visit_type != selected_visit_type:
            filtered_visits[visit_type] = 0

    labels = filtered_visits.index
    values = filtered_visits.values
    colors = ['#d3d3d3' if visit_type != selected_visit_type else color for visit_type, color in zip(visits_by_type.index, ['#008040', '#FF4500', '#a2d9ff', '#f5b7b1'])]
else:
    labels = visits_by_type.index
    values = visits_by_type.values
    colors = ['#008040', '#FF4500', '#a2d9ff', '#f5b7b1']

# Plotly Pie Chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.3,
    marker=dict(colors=colors),
    textinfo='none',
    hoverinfo='label+percent'
)])

fig.update_layout(
    title="Visits by Visit Type",
    title_font_color='white',
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font=dict(color='white'),
    width=800,  
    height=600, 
)

col_chart, col_labels = st.columns([3, 1])

with col_chart:
    st.plotly_chart(fig, use_container_width=True)



st.markdown("""
    <style>
    .chart-container {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .chart-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
