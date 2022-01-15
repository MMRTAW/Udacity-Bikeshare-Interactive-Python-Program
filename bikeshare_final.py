import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


#Defining Global Variables


list_city=('chicago','new york city','washington')
list_date_check=('day','month','none','both')
list_month=('january', 'february', 'march', 'april', 'may', 'june')
list_week_day=('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')

sentence_city=('Please Select a city from Chicago, New York City or Washington\n')
sentence_date_check=('Do you want to filter by day, month, both or not at all? If not at all please type "none"\n')
sentence_month=('Please Select a month from January, February, March, April, May or June\n')
sentence_week_day=('Please Select a day from Saturay, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday\n')


#Defining the user input constraints for each of our input values
def input_constraints(entry, entry_list, sentence):
    while True:
        entry=input(sentence).lower()
        try:
            entry in entry_list
        except:
            print('You have entered an incorrect value here, please try again')
            continue
        if entry not in entry_list:
            print('You have entered an incorrect value here, please try again')
            continue
        else:
            return entry
        break



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    city=''
    date_check=''
    month=''
    week_day=''
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input_constraints(city, list_city, sentence_city)
    
    # Check the required date filter
    date_check=input_constraints(date_check, list_date_check, sentence_date_check)
    
    if date_check=='none':
        month='all'
        week_day='all'
     
    # get user input for month (all, january, february, ... , june)        
    elif date_check=='month':
        month=input_constraints(month, list_month, sentence_month)
        week_day='all'
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif date_check=='day':
        week_day=input_constraints(week_day, list_week_day, sentence_week_day)
        month='all'
    
     # get user input for both month & day of week
    else:
         month=input_constraints(month, list_month, sentence_month)
         week_day=input_constraints(week_day, list_week_day, sentence_week_day)
     
        
    print('-'*40)
    return city, month, week_day


def load_data(city, month, week_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = list_month.index(month)+1
        # filter by month to create the new dataframe
        df = df[(df.month==month)]

    # filter by day of week if applicable
    if week_day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df.week_day==week_day.title())]
    
    return df


def time_stats(week_day,month,df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common start hour
    popular_hour = (df['hour'].value_counts().idxmax(), df['hour'].value_counts().max())
    print('Most popular hour: {0[0]},  Count:{0[1]}'.format(popular_hour))
    
    # display the most common day of week    
    if month != 'all' and week_day == 'all':
        popular_week_day= (df['week_day'].value_counts().idxmax(), df['week_day'].value_counts().max())
        print('Most popular week day in the given month is: {0[0]},  Count:{0[1]}'.format(popular_week_day))

    # display the most common month    
    elif month == 'all' and week_day != 'all':
        popular_month= (df['month'].value_counts().idxmax(), df['month'].value_counts().max())
        print('Most popular month for the given week day is: {0[0]},  Count:{0[1]}'.format(popular_month))
        
    # display the most month and weekday
    elif month == 'all' and week_day == 'all':
        popular_month= (df['month'].value_counts().idxmax(), df['month'].value_counts().max())
        print('Most popular month is: {0[0]},  Count:{0[1]}'.format(popular_month))
        popular_week_day= (df['week_day'].value_counts().idxmax(), df['week_day'].value_counts().max())
        print('Most popular week day is: {0[0]},  Count:{0[1]}'.format(popular_week_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = (df['Start Station'].value_counts().idxmax(), df['Start Station'].value_counts().max())
    print('Most popular starting station is: {0[0]},  Count:{0[1]}'.format(popular_start_station))
    
    # display most commonly used end station
    popular_start_station = (df['End Station'].value_counts().idxmax(), df['End Station'].value_counts().max())
    print('Most popular ending station is: {0[0]},  Count:{0[1]}'.format(popular_start_station))
    
    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " - " +df['End Station']
    popular_trip = (df['Trip'].value_counts().idxmax(), df['Trip'].value_counts().max())
    print('Most popular trip is: {0[0]},  Count:{0[1]}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_trip_duration= pd.to_timedelta(sum(df['Trip Duration']), unit='s')    
    print('Total trip duration: {}'.format(tot_trip_duration))

    # display mean travel time
    avg_trip_duration= pd.to_timedelta(df['Trip Duration'].mean(), unit='s')    
    print('Average trip duration: {}'.format(avg_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
      
    
        # Display counts of user types
    user_type=df['User Type'].value_counts()
    print('User Types:\n'+user_type.to_string()+'\n')
    
    if "Gender" in df.columns and "Birth Year" in df.columns:
    # Display counts of gender
        gender=df['Gender'].value_counts()
        print('Gender:\n'+gender.to_string()+'\n')

    # Display earliest, most recent, and most common year of birth
        df1=df.dropna()
        common_year = (int(df1['Birth Year'].value_counts().idxmax()), df1['Birth Year'].value_counts().max())
        print('Birth Dates:\nMost common birth year is: {0[0]},  Count:{0[1]}'.format(common_year))

        earliest_year = int(df1['Birth Year'].min())
        print('Earliest birth year is: {}'.format(earliest_year))
    
        latest_year = int(df1['Birth Year'].max())
        print('Most recent birth year is: {}'.format(latest_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()


def main():
    while True:
        city, month, week_day = get_filters()
        df = load_data(city, month, week_day)

        time_stats(week_day,month,df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
