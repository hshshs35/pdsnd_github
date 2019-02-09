import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_filter, month_filter, day_filter = None, None, None
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city_filter = input('Would you like to see data for Chicago, New York, or Washington?\n').lower().strip()
            if city_filter in ('chicago', 'new york', 'washington'):
                break
            else:
                raise ValueError
        except:
            print('Invalid input, please give a valid filter')

    while True:
        try:
            time_filter = input('Would you like to filter the data by month, day, both, '
                                'or not at all? Type "none" for no time filter?\n').lower()
            if time_filter in ('month','day','both','none'):
                break
            else:
                raise ValueError
        except:
            print('Invalid input, please give a valid filter')

    if time_filter in ('month', 'both'):
        while True:
            try:
                month_filter = input('Which month? January, February, March, April, May or June?\n').lower()
                if month_filter in ('january', 'february', 'march', 'april', 'may', 'june'):
                    break
                else:
                    raise ValueError
            except:
                print('Invalid input, please give a valid filter')

    if time_filter in ('both', 'day'):
        while True:
            try:
                day_filter = int(input('Which day? Please type your response as an integer (e.g.,0=Mpnday)\n'))
                if 0 <= day_filter < 7:
                    break
                else:
                    raise ValueError
            except:
                print('Invalid input, please give a valid filter')

    print('-'*40)
    return city_filter, month_filter, day_filter


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
    if city == 'new york':
        city = city.replace(' ', '_') + '_city'

    filename = city + '.csv'

    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    if month:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day:
        df = df[df['weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\nMost common month\n: {}'.format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print('\nMost common day of week\n: {}'.format(df['weekday'].mode()[0]))

    # TO DO: display the most common start hour
    print('\nMost common start hour\n: {}'.format(df['Start Time'].mode()[0]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost commonly used start start station:\n {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('\nMost commonly used end station:\n {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('\nMost frequent combination of start station and station:\n {}'.format(
        (df['Start Station'] + ' and ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('\nTotal Travel Time')
    print(df['Trip Duration'])


    # TO DO: display mean travel time
    print('\nMean Travel Time')
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nCounts of each user type')
    print(df.groupby('User Type')['User Type'].count())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender')
        print(df.groupby('Gender')['Gender'].count())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth')
        print(df['Birth Year'].min())
        print('\nLatest year of birth')
        print(df['Birth Year'].max())
        print('\nMost Common Year of birth')
        print(df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    idx = 0
    while True:
        display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display.lower() == 'no':
            break
        else:
            raw_data = df[idx:idx+5].to_json(orient='records')
            raw_data_list = json.loads(raw_data)
            for data in raw_data_list:
                print(data)
        idx += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

