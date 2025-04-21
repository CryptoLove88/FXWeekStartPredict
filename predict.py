import pandas as pd

# Load the data from the CSV file
def load_data(file_path):
    data = pd.read_csv(file_path, sep='\t')
    data['<DATETIME>'] = pd.to_datetime(data['<DATE>'] + ' ' + data['<TIME>'])
    return data

# Extract Monday data and determine the starting open price and trend
def get_starting_open_and_trend(data):
    monday_data = data[data['<DATETIME>'].dt.weekday == 0]
    if monday_data.empty:
        return None, None, None

    # Get the first available open price for Monday
    start_open = monday_data['<OPEN>'].iloc[0]
    start_time = monday_data['<DATETIME>'].iloc[0]

    # Check if there is at least one more data point to determine the trend
    if len(monday_data) > 1:
        next_open = monday_data['<OPEN>'].iloc[1]
        trend = 'up' if next_open > start_open else 'down'
    else:
        trend = None

    return start_time, start_open, trend

# Main function
def main():
    file_path = '/Volumes/Resource/GBPUSD_H1_202310020000_202504211600.csv'
    data = load_data(file_path)

    # Group data by weeks starting from Monday
    monday_dates = data[data['<DATETIME>'].dt.weekday == 0]['<DATETIME>'].dt.date.unique()

    for monday_date in monday_dates:
        week_data = data[(data['<DATETIME>'].dt.date >= monday_date) & 
                         (data['<DATETIME>'].dt.date < monday_date + pd.Timedelta(days=7))]

        start_time, start_open, trend = get_starting_open_and_trend(week_data)

        if start_time and start_open and trend:
            print(f"Start Time: {start_time}, Start Open: {start_open}, Trend: {trend}")
        else:
            print(f"No valid data for Monday starting {monday_date}.")

if __name__ == "__main__":
    main()