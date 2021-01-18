"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = "Youngsu Choi"
__email__ = "tonymusic0825@gmail.com"

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()

class SimplePrediction(WeatherPrediction):
    """Simple prediction model, based on the weather of multiple days."""
    def __init__(self, weather_data, number_days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            number_days (int): Numbers of days being used to predict weather

        Pre-condition:
            weather_data.size() > 0
        """
        if number_days > 28:
            self._number_days = 28
        else:
            self._number_days = number_days
        super().__init__(weather_data)
        self._past_weather_list = self._weather_data.get_data(self._number_days)

    def get_number_days(self):
        """(int) The number of days being used to predict weather"""
        return self._number_days

    def get_average(self, weather_list, information):
        """
        Parameters:
            weather_list (list<instance>): Collection of weather data instances.
            information (str): Specification of which information is needed.

        Return:
            int: The average value of the specified information in the parameter
        """
        average = 0

        if information == "humidity":
            for weather in weather_list:
                average += weather.get_humidity()

        elif information == "cloud_cover":
            for weather in weather_list:
                average += weather.get_cloud_cover()

        elif information == "wind_speed":
            for weather in weather_list:
                average += weather.get_average_wind_speed()

        average = round(average / self._number_days)

        return average

    def get_temperature(self, weather_list, information):
        """
        Parameters:
            weather_list (list<instance>): Collection of weather data instances.
            information (str): Specification of which information is needed.

        Return:
            list<int>: A sorted list of temperature values in respective to the required information in parameter
        """
        temperature_list = []

        if information == "high_temperature":
            for weather in self._past_weather_list:
                temperature_list.append(weather.get_high_temperature())

        elif information == "low_temperature":
            for weather in self._past_weather_list:
                temperature_list.append(weather.get_low_temperature())

        temperature_list = sorted(temperature_list)
        return temperature_list

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        average_rainfall = 0

        for weather in self._past_weather_list:
            average_rainfall += weather.get_rainfall()

        average_rainfall = round((average_rainfall/self._number_days) * 9)

        if average_rainfall > 100:
            average_rainfall = 100

        return average_rainfall

    def high_temperature(self):
        """(int) The highest temperature in the past days."""
        high_temperature_list = self.get_temperature(self._past_weather_list, "high_temperature")
        highest_temperature = high_temperature_list[-1]
        return highest_temperature

    def low_temperature(self):
        """(int) The lowest temperature the past days."""
        low_temperature_list = self.get_temperature(self._past_weather_list, "low_temperature")
        lowest_temperature = low_temperature_list[0]
        return lowest_temperature

    def humidity(self):
        """(int) Expected humidity."""
        return self.get_average(self._past_weather_list, "humidity")

    def cloud_cover(self):
        """(int) Expected amount of average cloud cover."""
        return self.get_average(self._past_weather_list, "cloud_cover")

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self.get_average(self._past_weather_list, "wind_speed")

class SophisticatedPrediction(WeatherPrediction):
    """Sophisticated prediction model, based on the weather of multiple days."""
    def __init__(self, weather_data, number_days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            number_days (int): Numbers of days being used to predict weather

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        if number_days > 28:
            self._number_days = 28
        else:
            self._number_days = number_days

        self._past_weather_list = self._weather_data.get_data(self._number_days)

        air_pressure = 0
        for weather in self._past_weather_list:
            air_pressure += weather.get_air_pressure()
        self._air_pressure = air_pressure / self._number_days

    def get_number_days(self):
        """(int) The number of days being used to predict weather"""
        return self._number_days

    def get_average(self, weather_list, information):
        """
        Parameters:
            weather_list (list<instance>): Collection of weather data instances.
            information (str): Specification of which information is needed.

        Return:
            int: The average value of the specified information in the parameter
        """
        average = 0

        if information == "rainfall":
            for weather in weather_list:
                average += weather.get_rainfall()

        elif information == "high_temperature":
            for weather in weather_list:
                average += weather.get_high_temperature()

        elif information == "low_temperature":
            for weather in weather_list:
                average += weather.get_low_temperature()

        elif information == "humidity":
            for weather in weather_list:
                average += weather.get_humidity()

        elif information == "cloud_cover":
            for weather in weather_list:
                average += weather.get_cloud_cover()

        elif information == "wind_speed":
            for weather in weather_list:
                average += weather.get_average_wind_speed()

        average = average / self._number_days
        return average

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        rainfall = self.get_average(self._past_weather_list, "rainfall")

        if self._past_weather_list[-1].get_air_pressure() < self._air_pressure:
            rainfall = rainfall * 10
        else:
            rainfall = rainfall * 7

        if 'E' in self._past_weather_list[-1].get_wind_direction():
            rainfall = round(rainfall * 1.2)
        else:
            rainfall = round(rainfall)

        if rainfall > 100:
            rainfall = 100

        return rainfall

    def high_temperature(self):
        """(float) Expected high temperature."""
        high_temperature = self.get_average(self._past_weather_list, "high_temperature")

        if self._past_weather_list[-1].get_air_pressure() > self._air_pressure:
            high_temperature += 2

        return high_temperature

    def low_temperature(self):
        """(float) Expected low temperature."""
        low_temperature = self.get_average(self._past_weather_list, "low_temperature")

        if self._past_weather_list[-1].get_air_pressure() < self._air_pressure:
            low_temperature -= 2

        return low_temperature

    def humidity(self):
        """(int) Expected humidity."""
        humidity = self.get_average(self._past_weather_list, "humidity")

        if self._past_weather_list[-1].get_air_pressure() < self._air_pressure:
            humidity = round(humidity + 15)
        elif self._past_weather_list[-1].get_air_pressure() > self._air_pressure:
            humidity = round(humidity - 15)
        else:
            humidity = round(humidity)

        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0

        return humidity

    def cloud_cover(self):
        """(int) Expected amount of average cloud cover."""
        cloud_cover = self.get_average(self._past_weather_list, "cloud_cover")

        if self._past_weather_list[-1].get_air_pressure() < self._air_pressure:
            cloud_cover = round(cloud_cover + 2)
        else:
            cloud_cover = round(cloud_cover)

        if cloud_cover > 9:
            cloud_cover = 9

        return cloud_cover

    def wind_speed(self):
        """(int) Expected average wind speed."""
        wind_speed = self.get_average(self._past_weather_list, "wind_speed")

        if self._past_weather_list[-1].get_maximum_wind_speed() > 4 * wind_speed:
            wind_speed = round(wind_speed * 1.2)
        else:
            wind_speed = round(wind_speed)

        return wind_speed

# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
