import time
import pandas as pd
import numpy as np
import calendar #used to capture the day of the week
import datetime as dt #used to work with statistics containing dates (hour, day and months

# Dictionary containing the data source file for each option available to the users
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def greeting():
    """
    Asks for the users name to greet him/her.

    Returns:
        (str) name - name inputed by the user
    """
    name = input('Hi! What\'s your name? \n')
    if name == '':
        print('\nYou\'re probably in a hurry. Not a problem. I\'ll call you USER.')
        name = 'User'
    return name

def get_filters(name, repeat):
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        (str) name - User's name to personalize the interativity
        (boo) repeat - flag to tell if it's the first time being run. Used to select proper communication with user.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    #Lists containing the valid values to entered by the user
    valid_cities = ['chicago','new york city','washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_days   = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    if not repeat:
        print('\nHello, {}! Let\'s explore some US bikeshare data!'.format(name.title()))
    else:
        print('\nOkay, {}! Here we go again!'.format(name.title()))
        
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    boo_ok = False
    msg = 'Inform the city desired. Use these exact values'
    while not boo_ok:
        city = input('\n' + msg + '\n' + str(valid_cities) + ':\n')
        if city.lower() in valid_cities:
            boo_ok = True
            print('\nOk! Let\'s check it out about {}.'.format(city.title()))
        else:
            msg = '!!Wrong entry!!\n {}, make sure to use one of these options below (in between single quotes)'.format(name.title())

    # TO DO: get user input for month (all, january, february, ... , june)
    boo_ok = False
    msg = '\nIs there a desired month to filter the data by? Use these exact values to inform'
    while not boo_ok:
        month = input('\n' + msg + '\n \'None\' for All or ' + str(valid_months) + ':\n')
        if month.lower() == 'none' or month.lower() in valid_months:
            boo_ok = True
            print('Got it! {} it is.'.format(month.title()))
        else:
            msg = '!!Wrong entry!!\n {}, make sure to use one of these options below (in between single quotes)'.format(name.title())

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    boo_ok = False
    msg = '\nNow, what about day of the week? Is there any one to filter the data by? Use these exact values to inform'
    while not boo_ok:
        day = input('\n' + msg + '\n \'None\' for All or ' + str(valid_days) + ':\n')
        if day.lower() == 'none' or day.lower() in valid_days:
            boo_ok = True
            print('Got it! {} it is.'.format(day.title()))
        else:
            msg = '!!Wrong entry!!\n {}, make sure to use one of these options below (in between single quotes)'.format(name.title())


    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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

    # extract month, hour and day of week from Start Time to create new columns
    df['start_month'] = df['Start Time'].dt.month
    df['start_hour'] = df['Start Time'].dt.hour
    df['start_day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df.loc[ df['start_month'] == month ]

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        df = df.loc[ df['start_day_of_week'] == day.title() ]
        print(df)
    
    boo_ok = False
    while not boo_ok:
        see_data = input('Would you like to see the raw data (5 lines only)?\n')
        if see_data.lower() == 'yes':
            print(df.head(5))
            break
        elif see_data.lower() == 'no':
            print('Wrong entry!! Please, use \'Yes\' or \'No\'.')
        else:
            break
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    that_month = df['start_month'].mode()[0]
    that_month_occurrences = df['start_month'].value_counts()[that_month]
    print(' - Most common Month..........: {} ( {} occurrences )'.format(calendar.month_name[that_month],that_month_occurrences))

    # TO DO: display the most common day of week
    that_day = df['start_day_of_week'].mode()[0]
    that_day_occurrences = df['start_day_of_week'].value_counts()[that_day]
    print(' - Most common Day of the Week: {} ( {} occurrences )'.format(that_day, that_day_occurrences))

    # TO DO: display the most common start hour
    h1 = df['start_hour'].mode()[0]             #The most common hour in 24h format
    h2 = dt.datetime.strptime(str(h1), '%H')    #The most common hour in 12h format
    that_hour_occurrences = df['start_hour'].value_counts()[h1]
    print(' - Most common Start Hour.....: {} ({}) ( {} occurrences )'.format(h1, h2.strftime('%I %p'),that_hour_occurrences))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    that_init_station = df['Start Station'].mode()[0]
    occurrences_init_station = df['Start Station'].value_counts()[that_init_station]
    print(' - Most commonly used Start Station.......................: {} ( {} occurrences )'.format(that_init_station, occurrences_init_station))

    # TO DO: display most commonly used end station
    that_end_station = df['End Station'].mode()[0]
    occurrences_end_station = df['End Station'].value_counts()[that_end_station]
    print(' - Most commonly used End Station.........................: {} ( {} occurrences )'.format(that_end_station, occurrences_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Itinerary'] = df['Start Station'] + ' - ' + df['End Station']
    that_itinerary = df['Itinerary'].mode()[0]
    occurrences_that_itinerary = df['Itinerary'].value_counts()[that_itinerary]
    print(' - Most common itinerary (Start and End Stations combined): {} ( {} occurrences )'.format(that_itinerary, occurrences_that_itinerary))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print(' - Total Travels......: {}'.format(df['Trip Duration'].count()))
    print(' - Total Travel Time..: {} seconds'.format(df['Trip Duration'].sum()))
 
    # TO DO: display mean travel time
    print(' - Average Travel Time: {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df.fillna('Not Informed')

    # TO DO: Display counts of gender
    try:
        print(' - Counts of Genders.............: {}'.format(df['Gender'].count()))
    except:
        print('For this file, there\'s no column GENDER. Moving forward to the next stats.')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print(' - The youngest user was born on.: {}'.format(int(df['Birth Year'].max())))
        print(' - The wisest user was born on...: {}'.format(int(df['Birth Year'].min())))
        print(' - Most of the users were born on: {}'.format(int(df['Birth Year'].mode()[0])))
    except:
        print('For this file, there\'s no column BIRTH YEAR. Moving forward to the next stats.\n')

    # TO DO: Display counts of user types
    print(' - Counts of Users Types:\n{}'.format(df.groupby(['User Type'], axis=0)['Start Time'].count()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    name = greeting() #User's name
    repeat = False #Flag to check for first time run
    while True:
        city, month, day = get_filters(name, repeat)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\n{}, would you like to restart? Enter yes or no.\n'.format(name.title()))
        if restart.lower() != 'yes':
            break
        else:
            repeat = True


if __name__ == "__main__":
	main()
