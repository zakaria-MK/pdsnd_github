import time
import pandas as pd
import datetime 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Handle input error (City)
    while True:
      # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
      city = input('Would you like to see data for Chicago, New York, or Washington?\n')
      
      # Handle input: if user enter wrong input they reenter city name  
      if city.lower() not in CITY_DATA:
        print('\n{} Warning {}'.format('*'*40, '*'*40))
        print('\n     You have entering a wrong city name!! ')
        print('     Please choose between the folowing cities: Chicago, New York, or Washington')
        print('     Please Type out the full city name\n')
        print('*'*40)
        continue
      break

    while True:
      month_day = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
      
      # Handle input: if user enter wrong input they reenter option name  
      if month_day.lower() not in ['month', 'day', 'both', 'none']:
        print('\n{} Warning {}'.format('*'*40, '*'*40))
        print('\n     You have entering a wrong option name!! ')
        print('     Please choose between the folowing option: month, day, both, or none')
        print('     Please Type out the full option name\n')
        print('*'*40)
        continue
      break

    # get user input for month (all, january, february, ... , june)
    if month_day != 'none':
      while True:
        if month_day == 'month' or month_day == 'both':
          month = input('Witch month? January, February, March, April, May or June? Please type out the full month name. \n')
          
          # Handle input: if user enter wrong input they reenter month name
          if month.lower() not in MONTHS:
            print('\n{} Warning {}'.format('*'*40, '*'*40))
            print('\n     You have entering a wrong month name!! ')
            print('     Please choose between the folowing months: January, February, March, April, May or June')
            print('     Please Type out the full month name\n')
            print('*'*40)
            continue
        else:
          month = 'all'
        break
      
      while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        if month_day == 'day' or month_day == 'both':
          day = input('Which day? please type a day Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday \n')
          
          # Handle input: if user enter wrong input they reenter day name
          if day.title() not in DAYS:
            print('\n{} Warning {}'.format('*'*40, '*'*40))
            print('\n       You have entering a wrong day name!! ')
            print('       Please choose between the folowing days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
            print('       Please Type out the full day name\n')
            print('*'*40)
            continue
        else:
          day = 'all'
        break
    
    else: 
      month = day = 'all'
    
    print('*'*40) 
    print('-'*40)
    return city, month, day, month_day


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
    # load data file 
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
      # extract index of month from months list
      month = MONTHS.index(month.lower()) + 1
      # filter data frame by month
      df = df[df['month'] == month]

    if day != 'all':
      # filtre data frame by day 
      df = df[df['day_week'] == day.title()]  
    
    return df

def time_stats(df, option):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
       
    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_count = df[df['month'] == common_month].count()[0]
    print('The most popular month is: {},   Count: {},  Filter: {}'.format(MONTHS[common_month - 1].title(), common_month_count, option))
    
    # display the most common day of week
    common_day = df['day_week'].mode()[0]
    common_day_count = df[df['day_week'] == common_day].count()[0]
    print('The most popular day of week is: {},   Count: {},  Filter: {}'.format(common_day, common_day_count, option))
    
    # display the most common start hour
    start_hour = df['Start Time'].dt.hour
    common_start_hour = start_hour.mode()[0]
    common_start_hour_count = df[start_hour == common_start_hour].count()[0]
    print('The most popular start hour is: {},  Count: {},  Filter: {}'.format(common_start_hour, common_start_hour_count,option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, option):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df[df['Start Station'] == popular_start_station].count()[0]
    print('The most popular start station is:   {} , Count:  {} ,Filter:  {}\n'.format(popular_start_station, popular_start_station_count, option))
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df[df['End Station'] == popular_end_station].count()[0]
    print('The most popular end station is:   {}, Count:  {} , Filter:  {}\n'.format(popular_end_station, popular_end_station_count, option))

    # display most frequent combination of start station and end station trip
    # start_end_station = df.loc[:,['Start Station', 'End Station']].mode()
    df['Start End'] = df['Start Station'].map(str) + ' & ' + df['End Station']
    start_end_station = df['Start End'].value_counts().idxmax()
    start_end_station_count = df[df['Start End'] == start_end_station].count()[0]
    print('The most frequent combination of start station and end station trip:\n\n {}\n\n Count: {},  Filter: {}'.format(start_end_station, start_end_station_count, option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, option):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_ = datetime.timedelta(seconds=int(total_time))
    print('Total travel time: {}, Filter: {}'.format(total_time_, option))
    
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time = datetime.timedelta(seconds=mean_time)
    print('Mean travel time: {}, Filter: {}'.format(mean_time, option))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, option):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df.groupby(['User Type'])['User Type'].count()
    print('User Types count:\n {}\n Filter:  {}\n'.format(user_count, option))
    
    # check if columns "Gender" and "Birth Year" are exist in Dataframe
    if 'Gender' and 'Birth Year' in df.columns:
      next_step = input('\n Would you like to continue to counts of gender: (y/n)  ')
      print('-'*40)
      while next_step != 'n':
        # Display counts of gender
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\nGender count:\n {}\n Filter:  {} \n'.format(gender_count, option))
        next_step = input('\n Would you like to continue to earliest, most recent, and most common year of birth: (y/n)  ')
        print('-'*40)    

        if next_step != 'n':
          # Display earliest, most recent, and most common year of birth and convert it to integer
          earl_year_birth = int(df['Birth Year'].min())
          recent_year_birth = int(df['Birth Year'].max())
          common_year_birth = df['Birth Year'].mode()[0]
          common_year_birth_count = df[df['Birth Year'] == common_year_birth].count()[0]
          print('\n earliest year of birth: {}, Filter:  {} '.format(earl_year_birth, option))
          print('\n most recent year of birth: {},Filter:  {} '.format( recent_year_birth, option))
          print('\n most common year of birth: {}, Count: {} ,Filter:  {} '.format(int(common_year_birth), common_year_birth_count, option))
          
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        break
    else:
      print('*'*60)
      print('\nThe Gender and Birth Year doesn\'t exist for this City.\n')
      print('*'*60)


def show_data_row(df):
  '''Display raw data by 5 rows upon request by user'''
  while True:
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    i = 0
    while view_data.lower() in ['yes', 'y']:
      print(df.iloc[i:i+5])
      i += 5 
      break
    else:
      break

def main():
  while True:
    city, month, day, option = get_filters()
    df = load_data(city, month, day)

    # handle result show by step:
    # if user enter the 'n' responce then the execution of next function is breaking.
    # else if enter the 'y' the program show the next step
    next_step = 'y' # var to ask user to continue or no
    while next_step != 'n':
      time_stats(df, option)
      next_step = input('\n Would you like to continue to Popular stations and trip: (y/n)  ')
      print('-'*40)
      if next_step.lower() == 'y':
        station_stats(df, option)
        next_step = input('\n Would you like to continue Trip duration: (y/n)  ')
        print('-'*40)
        if next_step.lower() == 'y':
          trip_duration_stats(df, option)
          next_step = input('\n Would you like to continue User info: (y/n)  ')
          print('-'*40)
          if next_step.lower() == 'y':
            user_stats(df, option)
            print('-'*40)
            show_data_row(df)
            print('-'*40)
            break
          break
        else:
          break 
      else:
        break

    restart = new_func()
    if restart.lower() != 'yes':
      break

def new_func():
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    return restart


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print('\nInterrupted by user!!!!!!')