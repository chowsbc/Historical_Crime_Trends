import pandas as pd
import plotly.express as px
import numpy as np
import json


def readcsv():
    with open('state_crime.csv', mode='r') as file:
        df = pd.read_csv(file)
        return df
    
def row_operation(row):

    crime_type = row['CrimeType'] = row['CrimeType'].split('.')[-1]
    
    return crime_type

def generate_type_list():
    itemnumber = 1    
    for header in headers:
        if 'Data' in header and 'Population' not in header:
            item = header.split('.')[-2] + ' - ' + header.split('.')[-1]
            header_list[str(itemnumber)] = item
            headers_filtered[str(itemnumber)] = header
            itemnumber += 1

    return headers_filtered        

def processdata(States, CrimeType, start_year, end_year):

    CrimetypeWord = CrimeType.split('.')[-2]
    
    df2 = df.loc[df['State'].isin(States)]
    filtered_df = df2[(df2["Year"] >= int(start_year)) & (df2["Year"] <= int(end_year))]

    filtered_total_df = pd.concat([filtered_df['Year'], filtered_df['State'], filtered_df[CrimeType]], axis = 1, ignore_index=True)

    filtered_total_df.columns = ['Year', 'State', 'Total Crime']

    print('Total Violent Crime Descriptives \n \n')
    print(filtered_total_df[['Total Crime']].describe())

    fig = px.line(filtered_total_df, x='Year', y='Total Crime', title='Total Violent Crime over Time', color = 'State')

    fig.update_yaxes(exponentformat="none")

    fig.show()

    CrimeType_R = 'Data.Rates.Violent.All'

    filtered_total_df_R = pd.concat([filtered_df['Year'], filtered_df['State'], filtered_df[CrimeType_R]], axis = 1, ignore_index=True)

    filtered_total_df_R.columns = ['Year', 'State', 'Crime Rate']

    print('\n \n \n Crime Rate Descriptives \n \n')
    print(filtered_total_df_R[['Crime Rate']].describe())

    fig = px.line(filtered_total_df_R, x='Year', y='Crime Rate', title='Violent Crime rate over Time', color = 'State')

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

            total_sum_df['CrimeType'] = total_sum_df.apply(row_operation, axis=1)

            total_sum_df = total_sum_df[total_sum_df['CrimeType'] != 'All']

            fig = px.pie(total_sum_df, values='Total', names='CrimeType', title='Crime Subtypes for '+ state)

            fig.show()

if __name__ == "__main__":
    
    Continue = 'y'
    
    while True:
        if Continue == 'y':
            firstquery = True
    
            df = readcsv()
      
            state_json = open('statelist.json', 'r')
    
            jsnstates = json.load(state_json)
    
            states = []
    
            dates = []

            state = input('\nChoose a state from which to query crime data: ')

            while True:
                if firstquery == False:
                    state = input('Choose a state to add to your query, "choose crime type [1]": ')
                    if state == '1':
                        break
                if state == "exit":
                    exit()
                else:
                    if state.lower() in jsnstates and state.capitalize() not in states:
                        states.append(state.capitalize())
                        print('states to query:')
                        for state in states:
                            print(state)
                        firstquery = False
                    else:
                        while True:
                            state = input("Please enter a valid state:")
                            if state.lower() in jsnstates and state.capitalize() not in states:
                                states.append(state.capitalize())
                                print('states to query:')
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
        
                print('Crime Types:')
        
                for key, value in header_list.items():
                    print(f"{key}: {value}")
               
                type_choice_num = input("Choose crime type [X]:")
                if type_choice_num.isdigit and type_choice_num in header_list.keys():
                    type_choice = (header_list[type_choice_num]).replace(' - ', '.')
                    for crimetype in headers:
                        if type_choice in crimetype:
                            column_type_choice = headers_filtered[type_choice_num]
                            break
                else:
                    while True:
                        type_choice_num = input("Please choose a number from the list:")
                        if type_choice_num.isdigit and type_choice_num in header_list.keys():
                            type_choice = (header_list[type_choice_num]).replace(' - ', '.')
                            for crimetype in headers:
                                if type_choice in crimetype:
                                    column_type_choice = headers_filtered[type_choice_num]
                                    break
                            break

                while True:
        
                    start_year = input('Start Year (XXXX):')
                    if start_year.isdigit and len(start_year) == 4:
                        break
                    else:
                        while True:
                            start_year = input('Please input a four-digit start year:')
                            if start_year.isdigit and len(start_year) == 4:
                                break
                    break
                    
                while True:
                    
                    end_year = input('End Year (XXXX):')
                    if end_year.isdigit and len(end_year) == 4:
                        break
                    else:
                        while True:
                            end_year = input('Please input a four-digit end year:')
                            if end_year.isdigit and len(end_year) == 4:
                                break
                    break
                
                processdata(states, column_type_choice, start_year, end_year)
                
                Continue_input = input('Start another query? Y/N')
                Continue = Continue_input.lower()
                if Continue == 'y' or Continue == 'n':
                    if Continue == 'y':
                        start_year = ''
                        end_year = ''
                    if Continue == 'n':
                        print('Exiting')
                    break
                else:
                    while True:
                       Continue_input = input('Please select Y if you would like to start another query or N to exit.')
                       Continue = Continue_input.lower()
                       if Continue == 'y' or Continue == 'n':
                            if Continue == 'y':
                               start_year = ''
                               end_year = ''
                            if Continue == 'n':
                               print('Exiting')
                            break        
                break
    