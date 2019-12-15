import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US Bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city (chicago, new york city, washington) " + \
                     "would you want analysis for? ").strip().lower()
        if city in ['chicago', 'new york city', 'washington']:
            print(f'\nOkay! You want analysis for {city.title()}.\n')
            break
        else:
            print(f'\nYou entered {city}, and that\'s not right.')
            continue

    # get user input for month (all, january, february, ... , june)
    input_message = (f"\nAvailable months are: {MONTHS}. \n" + \
                     "Enter which month you want analysis on or 'all' " + \
                     "for analysis on all months. ")
    while True:
        month = input(input_message).strip().lower()
        if month in MONTHS or month.lower() == 'all':
            filter = "all months" if month.lower() == "all" else month.title()
            print(f'\nOkay! You want analysis for {filter}.\n')
            break
        else:
            print(f'\nYou entered {month}, and that\'s not right.')
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    input_message = (f"\nAvailable days are: {DAYS}. \n" + \
                     "Enter which day you want analysis on or 'all' " \
                      "for analysis on all days. ")
    while True:
        day = input(input_message).strip().lower()
        if day in DAYS or day.lower() == 'all':
            filter = "all days" if day.lower() == "all" else day.title()
            print(f'\nOkay! You want analysis for {filter}.\n')
            break
        else:
            print(f'\nYou entered {day}, and that\'s not right.')
            continue


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month_int = df['month'].value_counts().idxmax()
    most_common_month = MONTHS[most_common_month_int - 1]
    print(f"\n{most_common_month.title()} is the most common month.")


    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print(f"\n{most_common_day_of_week} is the most common day of week.")


    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print(f"\n{most_common_start_hour} is the most common start hour.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].value_counts().idxmax()
    print(f"\n{most_used_start_station} is the most commonly used start station.")

    # display most commonly used end station
    most_used_end_station = df['End Station'].value_counts().idxmax()
    print(f"\n{most_used_end_station} is the most commonly used end station.")


    # display most frequent combination of start station and end station trip

    most_frequent_combination = df.groupby(
        ['Start Station', 'End Station']
    ).size().idxmax()
    print("\n" + most_frequent_combination[0] + " and " + \
          most_frequent_combination[1] + " are the most frequent combination" \
          + " of start station and end station trip.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_seconds = df['Trip Duration'].sum()
    formatted_total_travel = str(datetime.timedelta(
        seconds=int(total_travel_seconds)
    ))
    print(f"\n{formatted_total_travel} was the total travel time")

    # display mean travel time
    mean_travel_duration_seconds = df['Trip Duration'].mean()
    formatted_mean_travel_duration = str(datetime.timedelta(
        seconds=int(mean_travel_duration_seconds)
    ))
    print("\n{} was the mean travel time".format(formatted_mean_travel_duration))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = dict(df['User Type'].value_counts())
    print("\nBelow are the details of user types count:")
    for user_type, count in user_type_count.items():
        print(user_type + ": " + str(count))

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender_details(df)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        user_birth_year_details(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_gender_details(df):
    """Breakdown of gender types of bikeshare users."""

    # Get the gender types in a dict
    gender_counts = dict(df['Gender'].value_counts())
    print("\nBelow are the details on gender counts:")
    # Loop through the gender details
    for gender, count in gender_counts.items():
        print(gender + ": " + str(count))


def user_birth_year_details(df):
    """Display earliest, most recent, and most common year of birth"""

    # Fetch 'Birth Year'
    birth_year = df['Birth Year']

    print()

    # the most common birth year
    most_common_birth_year = int(birth_year.value_counts().idxmax())
    print(most_common_birth_year, "is the most common birth year.")

    # the most recent birth year
    most_recent_birth_year = int(birth_year.max())
    print(most_recent_birth_year, "is the most recent birth year.")

    # the most earliest birth year
    earliest_birth_year = int(birth_year.min())
    print(earliest_birth_year, "is the most earliest birth year.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
