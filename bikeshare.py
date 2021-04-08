import time
import pandas as pd
import numpy as np
from datetime import timedelta

CITY_DATA = {'chicago': 'data/chicago.csv',
             'new york city': 'data/new_york_city.csv',
             'washington': 'data/washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city do you want to explore?')
    while True:
        city = input('Type C for Chicago, NYC for New York City or W for '
                     'Washington: ')
        if city.upper() == 'C':
            city = 'chicago'
            break
        elif city.upper() == 'NYC':
            city = 'new york city'
            break
        elif city.upper() == 'W':
            city = 'washington'
            break
        else:
            continue

    # get user input for month (all, january, february, ... , june)
    months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}
    while True:
        month = input('Do you want to see the data for a specific month? y/n ')
        if month == 'y' or month == 'n':
            break
        else:
            print('Please enter y or n')
    if month == 'y':
        while True:
            month = input('For which month do you want to see the data?\n'
                          'Please enter jan, feb, mar, apr, may or jun: ')
            month = months.get(month.lower(), 'none')
            if month != 'none':
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = {'mon': 0, 'tue': 1, 'wed': 2,
            'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
    while True:
        day = input('Do you want to see the data for a specific day? y/n ')
        if day == 'y' or day == 'n':
            break
        else:
            print('Please enter y or n')
    if day == 'y':
        while True:
            day = input('For which day do you want to see the data?\n'
                        'Please enter mon, tue, wed, thu, fri, sat or sun: ')
            day = days.get(day.lower(), 'none')
            if day != 'none':
                break
    print('-'*40)
    # complete names for days and months
    days_c = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
              4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    months_c = {1: 'January', 2: 'February', 3: 'March',
                4: 'April', 5: 'May', 6: 'June'}
    print('\n... calculations will be done for {}... \n'.format(city.title()))
    if month == 'n':
        print('No filter is set for month.')
    else:
        print('Filter for month is set to {}.'.format(months_c.get(month)))
    if day == 'n':
        print('No filter is set for day.')
    else:
        print('Filter for day is set to {}.'.format(days_c.get(day)))
    print('-'*40 + '\n')
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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    if month != 'n':
        df = df[df['month'] == month]
    if day != 'n':
        df = df[df['day'] == day]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    months = {1: 'January', 2: 'February', 3: 'March',
              4: 'April', 5: 'May', 6: 'June'}

    # display the most common month
    # makes only sense if user hasn´t made a previous selection on month
    if month == 'n':
        c_month = df['month'].mode()[0]
        print('Most rentals were registered in {}.'.format(months.get(c_month)))
    else:
        print('... calculated for {}... '.format(months.get(month)))

    # display the most common day of week
    # makes only sense if user hasn´t made a previous selection on day
    if day == 'n':
        c_day = df['day'].mode()[0]
        print('The most frequented weekday was {}.'.format(days.get(c_day)))
    else:
        print('... calculated for {}...'.format(days.get(day)))
    # display the most common start hour
    c_hour = df['hour'].mode()[0]
    print('Most rentals started in the hour between {} and '
          '{} o\'clock.'.format(c_hour, c_hour + 1))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    m_start = df['Start Station'].mode()[0]
    c_start = df['Start Station'][df['Start Station'] == m_start].count()
    print('Most travels start at {}. {} starts were'
          ' registered at this station.'.format(m_start, c_start))
    # display most commonly used end station
    m_end = df['End Station'].mode()[0]
    c_end = df['End Station'][df['End Station'] == m_start].count()
    print('Most travels end at {}. {} ends were registered at this '
          'station.'.format(m_end, c_end))
    # display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'] + ' to ' + df['End Station']
    m_start_to_end = df['start_to_end'].mode()[0]
    c_start_to_end = df['start_to_end'][df['start_to_end']
                                        == m_start_to_end].count()
    print('Most travels were from {}. {} travels of this route were '
          'registered.'.format(m_start_to_end, c_start_to_end))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_t = timedelta(seconds=int(df['Trip Duration'].sum()))
    print('The total traval time was {}.'.format(str(total_t)))
    # display mean travel time
    mean_t = timedelta(seconds=int(df['Trip Duration'].mean()))
    print('The mean traval time was {}.\nThis took {} seconds.' 
          .format(str(mean_t), time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    c_user = df.groupby(['User Type']).count()
    for i, r in c_user.iterrows():
        print('User type {} was registered {} times. \n'.format(i, r[1]))

    # Display counts of gender
    if 'Gender' in df.columns:
        c_gender = df.groupby(['Gender']).count()
        for i, r in c_gender.iterrows():
            print('Gender {} was registered {} times. \n'.format(i, r[1]))
    else:
        print('Gender was in this dataset not available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        m_year = df['Birth Year'].mode()[0]
        print('The earliest registered year of birth was {:.0f}. \n'
              'The most recent registered year of birth was {:.0f}. \n'
              'The most common year of birth was {:.0f}.'
              .format(min_year, max_year, m_year))
    else:
        print('Birth Year was in this dataset not available.\nThis took %s '
              'seconds.' % (time.time() - start_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """ Shows a number of raw data rows based on users wishes.
    Input: Data Frame"""
    while True:
        raw_yn = input('Would you like to see some raw data? y/n: ')
        if raw_yn.lower() == 'n':
            break
        elif raw_yn.lower() == 'y':
            i = 0
            raw_choice_text = 'How many rows would you like to see? '
            while True:
                raw_choice = input(raw_choice_text)
                if raw_choice.lower() == 'stop':
                    break
                else:
                    try:
                        raw_choice = int(raw_choice)
                        print(df.iloc[i:i + int(raw_choice)])
                        i += raw_choice
                        if raw_choice >= len(df):
                            print('These were all available raw data.')
                            break
                        else:
                            raw_choice_text = 'Would you like to see '\
                                'additional rows of raw data? '\
                                'Please enter the number of additional rows '\
                                'you would like to see or enter "stop" if '\
                                'you have seen enough: '
                    except:
                        raw_choice_text = 'Your entry was not "stop" or '\
                            'an integer. Would you like to see additional '\
                            'rows of raw data?' \
                            'Please enter the number of additional rows you '\
                            'would like to see or enter "stop" if you have '\
                            'seen enough: '
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? y/n: ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
