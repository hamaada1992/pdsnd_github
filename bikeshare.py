import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (int/str) month - number of the month to filter by, or "all" to apply no month filter
        (int/str) day - number of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Type "exit" at any time to quit.')

    city_mapping = {'1': 'chicago', '2': 'new york city', '3': 'washington'}
    while True:
        city = input("Enter city (1: Chicago, 2: New York City, 3: Washington): ").strip().lower()
        if city in city_mapping:
            city = city_mapping[city]
            break
        elif city == 'exit':
            return city, None, None
        else:
            print("Invalid input. Please enter a valid number for city (1, 2, or 3).")

    month_mapping = {'0': 'all', '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
    while True:
        month = input("Enter month (0: All, 1: January, 2: February, 3: March, 4: April, 5: May, 6: June): ").strip()
        if month in month_mapping:
            month = month_mapping[month]
            break
        elif month == 'exit':
            return city, month, None
        else:
            print("Invalid input. Please enter a valid number for month (0 to 6).")

    day_mapping = {'0': 'all', '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7}
    while True:
        day = input("Enter day of week (0: All, 1: Monday, 2: Tuesday, 3: Wednesday, 4: Thursday, 5: Friday, 6: Saturday, 7: Sunday): ").strip()
        if day in day_mapping:
            day = day_mapping[day]
            break
        elif day == 'exit':
            return city, month, day
        else:
            print("Invalid input. Please enter a valid number for day of week (0 to 7).")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (int/str) month - number of the month to filter by, or "all" to apply no month filter
        (int/str) day - number of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek + 1  # Monday=1, ..., Sunday=7
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {most_common_day}")

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print(f"Most common trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time}")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

   #  Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of user types:\n{user_types}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of gender:\n{gender_counts}")
    else:
        print("Gender data not available for Washington.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest year of birth: {earliest_birth_year}")
        print(f"Most recent year of birth: {most_recent_birth_year}")
        print(f"Most common year of birth: {most_common_birth_year}")
    else:
        print("Birth year data not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request by the user."""
    row_index = 0
    while True:
        user_input = input("Would you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if user_input == 'yes':
            print(df.iloc[row_index:row_index+5])
            row_index += 5
        elif user_input == 'no':
            break
        elif user_input == 'exit':
            return

def main():
    while True:
        city, month, day = get_filters()
        if city == 'exit' or month == 'exit' or day == 'exit':
            print('Exiting program. Goodbye!')
            break

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            print('Exiting program. Goodbye!')
            break

if __name__ == "__main__":
    main()
