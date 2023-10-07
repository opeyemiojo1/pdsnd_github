#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    The get_filters function asks a user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        (str) filter_data - requests how user would want to filter the data by? both, month or day
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
   
    
    while True:
        try:
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            city = input('Would you like to see data for Chicago, New York City or Washington? \n').lower()
            city == CITY_DATA[city]
            break
        except:
            print('This is an invalid input, please enter a valid city name from the options available.')
    
    print()
    # get user input on how the data should be filtered? by both month and day, month only and day only
    filter_data = input('Would you like to filter the data by month, day, or both? \n').lower()
    while filter_data != 'month' and filter_data != 'day' and filter_data != 'both':
        print('This is an invalid input. Please enter a valid input from the available options.\n')
        filter_data = input('Would you like to filter the data by month, day, or both? \n').lower()
            
    print()
    # get user input for month (all, January, February, March, April, May or June)
    month = input('Which month would you love to filter the data by? - all, January, February, March, April, May, or June.\n').lower()
    while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
        print('This is an invalid input. Please enter a valid month from the options available.\n')
        month = input('Which month would you love to filter the data by? - all, January, February, March, April, May, or June.\n').lower()
        
        
    print()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day would you love to filter the data by? - all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n' ).lower()
    while day != 'monday' and day != 'tuesday' and 'day' != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
        print('This is an invalid input. Please enter a valid day from the options available.\n')
        day = input('Which day would you love to filter the data by? - all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n').lower()
        
        
    print('-'*40)
    return city, month, day, filter_data


def load_data(city, month, day, filter_data):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        (str) filter_data - requests how user would want to filter the data by? both, month or day
    Returns:
        df - Pandas DataFrame containing city data filtered by both month and day, month only, or day only
    """
    
    # load data file into a dataframe
    df1 = pd.read_csv(CITY_DATA[city])
        
    # eliminate row NaN values from the data
    df = df1.dropna(axis=0)
        
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    # extract month name and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    # filter by both month and day if applicable
    if filter_data == 'both':
        # filter by both month and day of week to create the new dataframe
        df = df[df['month'] == month.title()]
        df = df[df['day_of_week'] == day.title()]
        
    # filter by month if applicable
    elif filter_data == 'month':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
            
    # filter by day of week if applicable
    elif filter_data == 'day':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df

    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'month' in df:
        print('The most common day of the week is: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common month
    if 'day_of_week' in df:
        print('The most common month is: {}'.format(df['month'].mode()[0]))

    # display the most common hour
    if 'month' and 'day_of_week' in df:
        print('The most common hour is: {}'.format(df['Start Time'].dt.hour.mode()[0]))
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most popular start station is: {}\n'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most popular end station is: {}\n'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of Start and End station is:...\n', df.groupby(['Start Station','End Station'])['Start Station'].count().index.max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is... \n', df['Trip Duration'].sum())

    # display mean travel time
    print('The average travel time is...\n', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    
    """Displays statistics on bikeshare users."""
        
    print('\nCalculating User Stats...\n')
    start_time = time.time()
            
    # Display counts of user types
    print('The counts of user types are given below...\n',df['User Type'].value_counts())
    
    print()
    # Display counts of gender
    if 'Gender' in df:
        print('The counts of gender are given below...\n',df['Gender'].value_counts())
    else:
        print('There is no gender data to display for Washington')
    
    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is: ', df['Birth Year'].min())
        print()
        print('The most recent year of birth is: ', df['Birth Year'].max())
        print()
        print('The most common year of birth is: ', df['Birth Year'].mode()[0])
        
    else:
        print('There is no Birth Year data to display for Washington')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        

def show_data(df1):
    """ Displays individual data based on user's choice"""
    
    # request from users if they would like to view the raw data
    show_data = input('Would you like to view the individual data? Indicate by typing yes or no.\n').lower()
    
    if show_data != 'no':
        i = 0
        while i <= len(df1):
            print(df1.loc[i],'\n\n', df1.loc[i+1],'\n\n', df1.loc[i+2],'\n\n', df1.loc[i+3], '\n\n' ,df1.loc[i+4])
            show = input('\nWould you love to see 5 more rows of the data? Type "yes" or "no"\n\n ').lower()
            if show == 'yes':
                i += 5
            else:
                break
    else:
        print('Thanks for your time!')


def main():
    while True:
        city, month, day, filter_data = get_filters()
        df = load_data(city, month, day, filter_data)
        df1 = pd.read_csv(CITY_DATA[city])
        
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df1)
        
        # code to restart the project
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

            
if __name__ == "__main__":
	main() 


# In[ ]:





# In[ ]:





# In[ ]:




