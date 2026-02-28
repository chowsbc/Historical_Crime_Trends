SPECIAL REQUIREMENTS
The main file you will interact with is CrimeDataApp.py. To use this file, you will need the following Python Packages:

1) pandas
2) plotly
3) numpy
4) json

All other packages are in the Python library.


INSTRUCTIONS
1)	Upon starting CrimeDataApp.py, you will be prompted to enter the name of a state that you wish to query. Enter the name
of a state and hit the “Enter” key. State names are not case sensitive.
2) You will be presented with a list of states you have selected and will be prompted to select an additional state or enter "1"
and then hit the "Enter" key to choose the crime type to query.
4)	You will be presented with a numbered list of crime types to choose from. Enter the corrosponding number and hit the "Enter" key.
5)	You will then be prompted to enter a four-digit start year and hit the "Enter" key. The data that CrimeDataApp.py uses goes from
1960 to 2019.
6)	You will be prompted to enter a four-digit end year and hit the "Enter" key.
8)	You will see the following:
     a. The mean, median, standard deviation, minimum, and maximum for total # of crimes of the selected crime type for each year
  	    across the selected time frame for the selected states. This will be displayed in the console.
     b. The mean, median, standard deviation, minimum, and maximum for crime rate of the selected crime type for each year
  	    across the selected time frame for the selected states. This will be displayed in the console.
  	 c. A line chart showing the the total # of crimes of the selected crime type for each year, across the selected time frame.
  	    There will be one line representing each selected state. This will be displayed in your web browser.
  	 d. A line chart showing the the crime rate for the selected crime type for each year, across the selected time frame.
  	    There will be one line representing each selected state. This will be displayed in your web browser.
  	 e. If one of the "all" crime types was selected ("Violent-All" or "Property-All"), you will also see a bar chart showing
  	    the percentage breakdown for the crime subtypes under the the crimetype. This will be displayed in your web browser.



The data for the project was obtained from the following source:


Whitcomb, R., Choi, J. M., & Guan, B. (2021). State Crime CSV File (Version 3.0.0) [Data set]. CORGIS Datasets Project. https://corgis-edu.github.io/corgis/csv/state_crime/
