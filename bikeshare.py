import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city would you like to filter by - Chicago, New York, or Washington?\n').lower()  # use lower() to convert user input to lowercase
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Please enter a valid city name.')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month would you like to filter by - January, February, March, April, May, June or All?\n').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Please enter a valid month or "All".')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day of week would you like to filter by - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Please enter a valid day of week or "All".')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month in name
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[df['month'].mode()[0] - 1].title()  # Convert month number to name
    print('The most common month is {}.'.format(popular_month))

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is {}.'.format(popular_day_of_week))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    if 0 <= popular_hour < 12:
        print('The most common start hour is {}am.'.format(popular_hour))
    elif popular_hour == 12:
        print('The most common start hour is {}pm.'.format(popular_hour))
    else:
        print('The most common start hour is {}pm.'.format(popular_hour - 12))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common used start station is {}.'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common used end station is {}.'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['combination stations'] = df['Start Station'] + ' - ' + df['End Station']
    popular_combination_stations = df['combination stations'].mode()[0]
    print('The most frequent combination of start and end station trip is {}.'.format(popular_combination_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # Convert seconds to days, hours, minutes and seconds
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('Total travel time is {} seconds, equivalent to {} days, {} hours, {} minutes and {} seconds.'.format(total_travel_time, d, h, m, s))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time is {:0.2f} seconds.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = pd.DataFrame(df['User Type'].value_counts().reset_index().values, columns=["User Type", "Count"])
    print(user_type_counts)

    # TO DO: Display counts of gender(only available in Chicago and New York City files)
    if city == 'washington':
        print('\nGender information is not available in Washington data.\n')
    else:
        gender_counts = pd.DataFrame(df['Gender'].value_counts().reset_index().values, columns=["Gender", "Count"])
        print()
        print(gender_counts)

    # TO DO: Display earliest, most recent, and most common year of birth (only available in Chicago and New York City files)
    if city == 'washington':
        print('Birth information is not available in Washington data.')
    else:
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        popular_birth_year = int(df['Birth Year'].mode()[0])
        print()
        print('Earliest year of birth is {}. \nMost recent year of birth is {}. \nMost common year of birth is {}.'.format(earliest_birth_year, latest_birth_year, popular_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 rows if the user would like to see the raw data. If the user answers 'yes,' then the script should print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data. The script should continue prompting and printing the next 5 rows at a time until the user chooses 'no,' they do not want any more raw data to be displayed.
    """

    start_row = 0
    while True:
        raw_data = input('\nWould you like to see 5 rows of the raw data? Enter "yes" or "no".\n').lower()
        if raw_data == 'yes':
            print(df.iloc[start_row: start_row + 5])
            start_row = start_row + 5
        elif raw_data not in ['yes', 'no']:
            print('Invalid input. Please enter "yes" or "no".')
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
