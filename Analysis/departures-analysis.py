import pandas as pd
import matplotlib.pyplot as plt

def busiest_day_graph(data, order):
    # Organize data
    data['Day of Week'] = pd.Categorical(data['Day of Week'], categories=order, ordered=True)
    data = data.sort_values('Day of Week')
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.bar(data['Day of Week'], data['Number of Flights'], color='skyblue')
    # Customize axes and title
    plt.title('Number of Flights for Each Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Flights')
    # Add info card above bar
    for index, value in enumerate(data['Number of Flights']):
        plt.text(index, value, str(value), ha='center', va='bottom')
    # Formatting
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def busiest_time_graph(data, order):
    # Organize data
    data['Day of Week'] = pd.Categorical(data['Day of Week'], categories=order, ordered=True)
    data = data.sort_values('Day of Week')
    # Create plot
    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    day = 0
    for i in range(3):
        for j in range(3):
            if(i == 2 and j >= 1):
                break
            # Plot respective day
            day_data = data[data['Day of Week'] == order[day]].sort_values(by = 'Departure Hour')
            axs[i,j].plot(day_data['Departure Hour'], day_data['Number of Flights'])
            # Customize axes and title
            axs[i,j].set_title(order[day], fontweight = 'bold')
            axs[i,j].set_xlabel('Departure Hour')
            axs[i,j].set_ylabel('Number of Flights')
            axs[i,j].set_ylim(0,150)
            axs[i,j].set_xticks(range(0, 25, 3))

            day += 1
    # Delete extra subplots 
    fig.delaxes(axs[2,1])
    fig.delaxes(axs[2,2])
    # Formatting
    plt.tight_layout()
    plt.show()

def popular_routes_graph(data):
    # Create plot
    plt.figure(figsize=(10, 6)) 
    plt.bar(data['Arrival'], data['Number of Flights'], color=['#86e3ce', '#ffc67d', '#d1e7a8', '#fc8c7f', '#cfaedc'])
    # Customize axes and title
    plt.title('Number of Flights by Destination') 
    plt.xlabel('Destination')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    # Add info card above bar
    for index, value in enumerate(data['Number of Flights']):
        plt.text(index, value, str(value), ha='center', va='bottom')
    # Formatting
    plt.tight_layout() 
    plt.show() 



order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df = pd.read_csv('departures.csv')

# Busiest times per day of week
busiest_time = (df.groupby('Day of Week')['Departure Hour'].apply(lambda x: x.value_counts().head(1)).reset_index()).sort_values(by = 'Departure Hour', ascending = False)
busiest_time.columns = ['Day of Week', 'Most Common Departure Hour', 'Number of Flights']
busiest_time = busiest_time.reset_index(drop=True)
print(busiest_time)
flight_counts = df.groupby(['Day of Week', 'Departure Hour']).size().reset_index(name='Number of Flights')
busiest_time_graph(flight_counts, order)

# Busiest days of week
busiest_day = (df.groupby('Day of Week').size().reset_index(name='Number of Flights')).sort_values(by='Number of Flights', ascending=False)
busiest_day = busiest_day.reset_index(drop=True)
print(busiest_day)
busiest_day_graph(busiest_day, order)

# Busiest terminals
busiest_terminal = (df.groupby('Terminal').size().reset_index(name='Number of Flights')).sort_values(by='Number of Flights', ascending=False)
print(busiest_terminal)

# Popular routes
popular_routes = (df.groupby('Arrival').size().reset_index(name='Number of Flights')).sort_values(by='Number of Flights', ascending=False)
print(popular_routes.head(5))
popular_routes_graph(popular_routes.head(5))
