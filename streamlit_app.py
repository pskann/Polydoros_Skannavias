import streamlit as st
import requests

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 4em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True )

# Title in  the center
st.markdown('<h1 class="centered-title">First Assignment</h1>', unsafe_allow_html=True)

# First Row: 3 Widgets in a row
col1, spacer1, col2, spacer2, col3 = st.columns([3, 1, 3, 1, 3])

with col1:
    with st.container():

        st.title("Welcome")

        # Bring api from AWS
        api_url = "https://4v19ka1q3g.execute-api.eu-north-1.amazonaws.com/default/Welcome"

        # Button to trigger the serverless function
        if st.button("Press this button"):

            response = requests.get(api_url)

            # Bring the message from the lambda function
            if response.status_code == 200:

                st.write(response.json())

            else:
                st.error("Failed to get a response from Lambda.")

        st.write("This widget is a serveless function. With the click of the button the user gets a text that is written in an Lambda function in AWS.")       

with col2:
    with st.container():

        # API Gateway URL for the Lambda function
        api_url = "https://ytkwqq74f2.execute-api.eu-north-1.amazonaws.com/default/Distance"  # Replace with your actual API Gateway URL

        st.title("City Distance Calculator")

        # City options
        cities = ["Limassol", "Nicosia", "Larnaca", "Paphos"]

        # Dropdown menus for selecting cities
        city1 = st.selectbox("Select the first city:", cities)
        city2 = st.selectbox("Select the second city:", cities)

        # Button to calculate distance
        if st.button("Calculate Distance"):
            # Make a request to the Lambda function
            payload = {
                "city1": city1,
                "city2": city2
            }
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                # Parse and display the result
                result = response.json()
                st.write(f"The distance between {result['city1']} and {result['city2']} is {result['distance_km']} km.")
            else:
                st.error("Failed to calculate the distance. Please try again.")


        st.write("This widget is a serveless and interactive function, where the user can add two numbers. The addition is done in the AWS Lambda Console    ")       


with col3:
    with st.container():

        st.title("Weather Information")

        # Input for location
        location = st.text_input("Enter a location to see the current weather")

        # OpenWeatherMap API key
        api_key = "e1d1151f153c6f12e0d4c5800d29b5d5"

        # How to get weather data from openweathemap
        def get_weather(city, api_key):
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
        
            response = requests.get(complete_url)
            return response.json()

        # Button to show the weather
        if st.button("Show Weather"):
            
            weather_data = get_weather(location, api_key)
            
            # Check if the response is valid
            if weather_data.get("cod") == 200:
                main = weather_data["main"]
                weather_desc = weather_data["weather"][0]["description"]
                temperature = main["temp"]
                
                # Display the weather information
                st.write(f"### Weather in {location.capitalize()}:")
                st.write(f"**Temperature:** {temperature} °C")
            else:
                st.error(f"City not found. Please enter a valid city name.")

        st.write("This an interactive widget. The user inserts a location and by clicking the button it gives the current weather in that location.")       
 
# Second Row: 3 Widgets in a row
col4, spacer4, col5, spacer5, col6 = st.columns([3.5, 1, 3, 1, 3])

with col4:
    with st.container():

        st.title("Currency Converter")
        
        # API Gateway URL for the Lambda function
        api_url = "https://2pj3udf4dc.execute-api.eu-north-1.amazonaws.com/prod/Currency"

        # Input field for the amount in EUR
        amount_eur = st.number_input("Enter amount in EUR:", min_value=0.0, value=1.0)

        if st.button("Convert to USD"):
            # Make a request to the Lambda function through API Gateway
            response = requests.post(api_url, json={"amount": amount_eur})

            # How the convertion is done
            if response.status_code == 200:
                result = response.json()
                exchange_rate = result["exchange_rate"]
                converted_amount = result["converted_amount_usd"]
                st.write(f"**Exchange Rate**: 1 EUR = {exchange_rate} USD")
                st.write(f"**Converted Amount**: {amount_eur} EUR = {converted_amount} USD")
            else:
                st.error("Failed to fetch conversion rate.")

with col5:
    with st.container():

        st.title("Top 10 Highest Rated TV Series")
        
        # TMDb API key
        api_key = "bff01f6c1b2ca5e1a46def81c524f195"

        # How to get the top-rated TV series from TMDb
        def get_top_rated_tv_series(api_key):
            url = f"https://api.themoviedb.org/3/tv/top_rated?api_key={api_key}&language=en-US&page=1"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the top 10 highest-rated TV series
                top_tv_series = [
                    {
                        "title": show["name"],
                        "rating": show["vote_average"]
                    }
                    for show in data["results"][:10]
                ]
                return top_tv_series
            else:
                st.error("Failed to bring TV series data.")

        # Button to show the top 10 rated TV series
        if st.button("When you press this button it will show the Top 10 Highest Rated Tv Seires"):
            top_tv_series = get_top_rated_tv_series(api_key)

            # Show in order
            for i, series in enumerate(top_tv_series, start=1):
                    st.write(f"**{i}. {series['title']}**")
                    st.write(f"    Rating: {series['rating']}")
                    st.write("---")

with col6:
    with st.container():

        st.title("Google Stock Market")

        # Alpha Vantage api key
        api_key = "ZD8F4JXAAQID7KQ2"

    # How to get stock data from Alpha Vantage for Google
    def get_stock_data(symbol, api_key):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
        response = requests.get(url)
        return response.json()

    symbol = "GOOGL"

    # Button to show the stock data for Google
    if st.button("By pressing this button you will see the current stock market data of Google"):

        # How to get the stock data using Alpha Vantage API
        stock_data = get_stock_data(symbol, api_key)
        
        if "Time Series (5min)" in stock_data:

            # Extract the latest stock data
            time_series = stock_data["Time Series (5min)"]
            latest_time = next(iter(time_series))  # Get the most recent timestamp
            latest_data = time_series[latest_time]

            st.write(f"**The Stock for Google now is**: {latest_data['1. open']}")
        else:
            st.error("Error fetching stock data. Please try again later.")
