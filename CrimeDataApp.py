import pandas as pd
import plotly.express as px
import numpy as np
import json


def readcsv():
    ''' Reads state_crime.csv and stores data in dataframe df.

        Parameters
        ----------
        none

        Returns
        -------
        pandas.dataframe
            The dataframe returned from reading state_crime.csv
        '''    

    with open('state_crime.csv', mode='r') as file:
        df = pd.read_csv(file)
        return df
    
def modify_crime_type_string(crime_type_string):
        '''Takes the CrimeType value from total_sum_df and modifies it into a readable crime type to display on the pie chart.

        Parameters
        ----------
        row: 

        Returns
        -------
        string
            The crime type value to display on the pie chart
        '''
        crime_type = crime_type_string['CrimeType'] = crime_type_string['CrimeType'].split('.')[-1]
    
        return crime_type

def generate_type_list():
        '''Genderates a readable list of crime types from the "Headers" list, for the user to choose from"

        Parameters
        ----------
        None 

        Returns
        -------
        Dictionary
            The crime types with corrosponding integers, so that the user can enter an integer to choose a crime type to query.
        '''   

        itemnumber = 1    
        for header in headers:
            if 'Data' in header and 'Population' not in header and 'Rates' not in header:
                item = header.split('.')[-2] + ' - ' + header.split('.')[-1]
                header_list[str(itemnumber)] = item
                headers_filtered[str(itemnumber)] = header
                itemnumber += 1

        return headers_filtered        

def processdata(States, CrimeType, start_year, end_year, type_choice):
    
        '''Finds and displays the mean, median, standard deviation, minimum, and maximum of the total numbers of crimes and the crime rates for the states, crime type, and time frame selected by the user.
        Generates a line graph for the total number of crimes for each selected state across the selected time period for the selected crime type.
        Generates a pie chart for each state breaking down the percentage of each crime subtype of an "all" crime type was selected (eg. Violent-All)"

        Parameters
        ----------
        None 

        Returns
        -------
        None. But creates a line graph of the crime rate of the total number of crimes for selected states, time frames, and crime types, a pie chart breaking down percentags of crime subtypes, and descriptive
        statistics for crime totals and crime rates for each selected state.
        ''' 


        CrimetypeWord = CrimeType.split('.')[-2]
    
        df2 = df.loc[df['State'].isin(states)]

        filtered_df = df2[(df2["Year"] >= int(start_year)) & (df2["Year"] <= int(end_year))]
    
        filtered_total_df = pd.concat([filtered_df['Year'], filtered_df['State'], filtered_df[CrimeType]], axis = 1, ignore_index=True)

        filtered_total_df.columns = ['Year', 'State', 'Total Crime']
    
        for state in states:
            filtered_total_df_state = filtered_total_df[filtered_total_df['State']==state]

            type_choice_title = type_choice.replace('.', ' - ')

            print('\n\nDescriptive Statistics for total crimes in ' + state + ' for ' + start_year + ' to ' + end_year + ': ' + type_choice_title + '\n')
    
            print("Mean: " + str(np.average(filtered_total_df_state[['Total Crime']])))
            print("Median: " + str(np.median(filtered_total_df_state[['Total Crime']])))
            print("Standard Deviation: " + str(np.std(filtered_total_df_state[['Total Crime']])))
            print("Minimum: " + str(np.min(filtered_total_df_state[['Total Crime']])))
            print("Maximum: " + str(np.max(filtered_total_df_state[['Total Crime']])))

        fig = px.line(filtered_total_df, x='Year', y='Total Crime', title='Total crime for ' + start_year + ' - ' + end_year + ': ' + type_choice_title, color = 'State')

        fig.update_yaxes(exponentformat="none")

        fig.show()

        CrimeType_R = CrimeType.replace('Totals','Rates')
    

        filtered_total_df_R = pd.concat([filtered_df['Year'], filtered_df['State'], filtered_df[CrimeType_R]], axis = 1, ignore_index=True)
            
        filtered_total_df_R.columns = ['Year', 'State', 'Crime Rate']
    
        for state in states:
            filtered_total_df_R_state = filtered_total_df_R[filtered_total_df_R['State']==state]
    
            print('\n\nDescriptive Statistics for crimes rates in ' + state + ' for ' + start_year + '-' + end_year + ': ' + type_choice_title + '\n')

            print("Mean: " + str(np.average(filtered_total_df_R_state[['Crime Rate']])))
            print("Median: " + str(np.median(filtered_total_df_R_state[['Crime Rate']])))
            print("Standard Deviation: " + str(np.std(filtered_total_df_R_state[['Crime Rate']])))
            print("Minimum: " + str(np.min(filtered_total_df_R_state[['Crime Rate']])))
            print("Maximum: " + str(np.max(filtered_total_df_R_state[['Crime Rate']])))
    
        fig = px.line(filtered_total_df_R, x='Year', y='Crime Rate', title='Crime Rate for ' + start_year + ' - ' + end_year + ': ' + type_choice_title, color = 'State')

        fig.update_yaxes(exponentformat="none")

        fig.show()

        for state in States:
            if 'All' in CrimeType:
                s_filtered_df = filtered_df[filtered_df["State"] == state]
        
                filtered_sub2_df = s_filtered_df.filter(like=CrimetypeWord)
                filtered_sub3_df = filtered_sub2_df.filter(like='Totals')
                total_sum = np.sum(filtered_sub3_df, axis=0)

                total_sum = total_sum.iloc[1:]
                   
                total_sum_df = total_sum.reset_index()

                total_sum_df.columns = ['CrimeType', 'Total']

                total_sum_df['CrimeType'] = total_sum_df.apply(modify_crime_type_string, axis=1)

                total_sum_df = total_sum_df[total_sum_df['CrimeType'] != 'All']

                fig = px.pie(total_sum_df, values='Total', names='CrimeType', title = CrimetypeWord + ' Crime Subtypes for ' + state)

                fig.show()

if __name__ == "__main__":

    loop = 'n'    

    Continue = 'y'
    
    while True:
        if Continue == 'y':
            firstquery = True
    
            df = readcsv()
      
            state_json = open('statelist.json', 'r')
    
            jsnstates = json.load(state_json)
    
            states = []
    
            dates = []

            if loop  == 'y':
                state = input('\nChoose a state from which to query crime data: ')
            else:
                state = input('Choose a state from which to query crime data: ')

            while True:
                if firstquery == False:
                    state = input('\nChoose a state to add to your query or finish choosing states and choose crime type to query [1]": ')
                    if state == '1':
                        break
                if state == "exit":
                    exit()
                else:
                    if state.lower() in jsnstates and state.capitalize() not in states:
                        states.append(state.capitalize())
                        print('\nStates that will be queried:')
                        for state in states:
                            print(state)
                        firstquery = False
                    else:
                        while True:
                            state = input("\nPlease enter a valid state:")
                            if state.lower() in jsnstates and state.capitalize() not in states:
                                states.append(state.capitalize())
                                print('\nStates that will be queried:')
                                for state in states:
                                    print(state)
                                firstquery = False
                                break
    
            while True:
                headers = df.columns.tolist()
                headers_filtered = {}
                header_list = {}
                df = readcsv()
        
                headers_filtered = generate_type_list()
        
                print('\nCrime Types:')
        
                for key, value in header_list.items():
                    print(f"{key}: {value}")
               
                type_choice_num = input("\nChoose crime type [X]:")
                if type_choice_num.isdigit and type_choice_num in header_list.keys():
                    type_choice = (header_list[type_choice_num]).replace(' - ', '.')
                    for crimetype in headers:
                        if type_choice in crimetype:
                            column_type_choice = headers_filtered[type_choice_num]
                            break
                else:
                    while True:
                        type_choice_num = input("\nPlease choose a number from the list:")
                        if type_choice_num.isdigit and type_choice_num in header_list.keys():
                            type_choice = (header_list[type_choice_num]).replace(' - ', '.')
                            for crimetype in headers:
                                if type_choice in crimetype:
                                    column_type_choice = headers_filtered[type_choice_num]
                                    break
                            break

                while True:
        
                    start_year = input('\nStart Year (XXXX):')
                    if start_year.isdigit and len(start_year) == 4:
                        break
                    else:
                        while True:
                            start_year = input('\nPlease input a four-digit start year:')
                            if start_year.isdigit and len(start_year) == 4:
                                break
                    break
                    
                while True:
                    
                    end_year = input('\nEnd Year (XXXX):')
                    if end_year.isdigit and len(end_year) == 4:
                        break
                    else:
                        while True:
                            end_year = input('\nPlease input a four-digit end year:')
                            if end_year.isdigit and len(end_year) == 4:
                                break
                    break
                
                processdata(states, column_type_choice, start_year, end_year, type_choice)
                
                Continue_input = input('\nStart another query? Y/N')
                Continue = Continue_input.lower()
                if Continue == 'y' or Continue == 'n':
                    if Continue == 'y':
                        start_year = ''
                        end_year = ''
                        loop = 'y'
                    if Continue == 'n':
                        print('\nExiting')
                    break
                else:
                    while True:
                       Continue_input = input('\nPlease select Y if you would like to start another query or N to exit.')
                       Continue = Continue_input.lower()
                       if Continue == 'y' or Continue == 'n':
                            if Continue == 'y':
                               start_year = ''
                               end_year = ''
                               loop = 'y'
                            if Continue == 'n':
                               print('\nExiting')
                            break        
                break
    