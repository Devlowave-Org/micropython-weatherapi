import urequests


class Weatherapi:
    def __init__(self, key: str, city: str):
        self.city = city
        self.key = key

    def get_current_weather_from_api(self, aqi: str = "no") -> dict:
        response = urequests.get(
            url=f"https://api.weatherapi.com/v1/current.json?key={self.key}&q={self.city}&aqi={aqi}").json
        return response["current"]

    def get_forecast_weather_from_api(self, aqi: str = "no", days: int = 1, hour: int = None) -> dict:
        response = urequests.get(url=f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q={self.city}"
                                     f"&aqi={aqi}&days={days}&hour={hour}&lang=fr").json()
        return response["forecast"]["forecastday"]

    def current_weather_option(self, param: str) -> int:
        """current_weather_option() take the parameter of what you want to get such as "temp_c" or "humidity"

        :param param: the value you want to get -> "temp_c", "humidity" : https://www.weatherapi.com/docs/#apis-realtime
        :return: an integer of the option you chose
        """
        current_weather = self.get_current_weather_from_api()
        current_param = current_weather[param]
        return current_param

    def current_condition(self) -> str:
        current_weather = self.get_current_weather_from_api()
        current_condition = current_weather["condition"]["text"]
        return current_condition

    def forecast_for_a_day_option(self, arg: str, day: int = 1) -> dict:
        """forecast_day_option return the forecast for the given day

        :param arg: https://www.weatherapi.com/docs/#apis-realtime
        :param day: day you want the forecast each 14
        :return: an integer according to the option you give : "mintemp_c" -> 7.4

        Example:
        forecast_day_option("avgtemp_c", 3) -> 7.7 in Celsius degree
        forecast_day_option("daily_will_it_snow", 1) -> 0 (it will not snow)
        """
        # Handle day
        if day < 1:
            day = 1

        forecast_weather = self.get_forecast_weather_from_api(days=day)
        return forecast_weather[day - 1]["day"][arg]

    def forecast_for_an_hour_option(self, arg: str, hour: int = 12, day: int = 1):
        """Return the forecast of the given hour and day

        :param arg:
        :param hour:
        :param day:
        :return: integer

        Example:
        I want the temperature in C for tomorrow 1 PM :
        - forecast_for_an_hour_option("temp_c", days=2, hour=13) -> 13 degree Celsius

        List of argument -> https://www.weatherapi.com/docs/#apis-realtime
        """
        forecast_weather = self.get_forecast_weather_from_api(days=day, hour=hour)
        return forecast_weather[day - 1]["hour"][hour - 1][arg]

    def forecast_for_a_day_condition(self, day: int) -> str:
        """forecast_for_a_day_condition() is a function which return the condition of a day
        -> Partly Cloudy or Light Rain ....

        :param day:
        :return: the condition of the day
        """
        forecast_weather = self.get_forecast_weather_from_api(days=day)
        return forecast_weather[day - 1]["day"]["condition"]["text"]

    def forecast_for_an_hour_condition(self, day: int, hour: int) -> str:
        """ same as forecast_for_a_day_condition() but for an hour of a day

        :param day: day between 1 and 14
        :param hour: between 0 and 24
        :return: the forecast condition in string
        """
        forecast_weather = self.get_forecast_weather_from_api(days=day, hour=hour)
        return forecast_weather[day - 1]["day"]["condition"]["text"]

