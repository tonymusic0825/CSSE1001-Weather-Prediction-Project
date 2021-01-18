"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = ""
__email__ = ""

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
class Event(object):
    """Creats an event according to user's input"""
    def __init__(self, name, outdoors, cover_avaliable, time):
        """
        Parameters:
            name (str): The name of the event
            outdoors (bool): Represents whether the event is indoors or outdoors
            cover_avaliable (bool): Shows if the event has any cover avaliable
            time (int): Closest hour to the starting time of event
        """
        self._name = name
        self._outdoors = outdoors
        self._cover_avaliable = cover_avaliable
        self._time = time

    def get_name(self):
        """(str) Returns name of event """
        return self._name

    def get_time(self):
        """(int) Returns the closest hour to the starting time of event"""
        return self._time

    def get_outdoors(self):
        """(bool) Returns True if the event is outdoors"""
        return self._outdoors

    def get_cover_available(self):
        """(bool) Returns True of there are covers avaliable at the event"""
        return self._cover_avaliable

    def __str__(self):
        """Outputs a human readable representation of a event instance"""
        return f"Event({self._name} @ {self._time}, {self._outdoors}, {self._cover_avaliable})"


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""
    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        temperature_factor = 0
        humidity_factor = 0
        humidity = self._prediction_model.humidity()
        event_time = self._event.get_time()
        event_outdoors = self._event.get_outdoors()

        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()

        if humidity > 70:
            humidity_factor = humidity / 20

        if high_temperature > 0:
            high_temperature += humidity_factor
        elif high_temperature < 0:
            high_temperature -= humidity_factor

        if low_temperature > 0:
            low_temperature += humidity_factor
        elif low_temperature < 0:
            low_temperature -= humidity_factor

        if (event_time >= 6 and event_time <= 19 and event_outdoors and high_temperature >= 30) or high_temperature >= 45:
            temperature_factor = (high_temperature / -5) + 6

            if temperature_factor < 0:
                if self._event.get_cover_available():
                    temperature_factor += 1
                if self._prediction_model.wind_speed() > 3 and self._prediction_model.wind_speed() < 10:
                    temperature_factor += 1
                if self._prediction_model.cloud_cover() > 4:
                    temperature_factor += 1

        elif (self._event.get_time() >= 0 and self._event.get_time() <= 5) or (self._event.get_time() >= 20 and self._event.get_time() <= 23) \
             and low_temperature < 5 and high_temperature < 45:

             temperature_factor = (low_temperature / 5) - 1.1

        elif low_temperature > 15 and high_temperature < 30:
            temperature_factor = (high_temperature - low_temperature) / 5

        else:
            temperature_factor = 0

        return temperature_factor

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        chance_of_rain = self._prediction_model.chance_of_rain()

        if self._prediction_model.chance_of_rain() < 20:
            rain_factor = (chance_of_rain / -5) + 4
        elif self._prediction_model.chance_of_rain() > 50:
            rain_factor = (chance_of_rain / -20) + 1
        else:
            rain_factor = 0

        if self._event.get_outdoors() and self._event.get_cover_available() and self._prediction_model.wind_speed() < 5:
            rain_factor += 1

        if rain_factor < 2 and self._prediction_model.wind_speed() > 15:
            rain_factor += (self._prediction_model.wind_speed() / -15)

        if rain_factor < -9:
            rain_factor = -9

        return rain_factor

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        advisability = self._temperature_factor() + self._rain_factor()

        if advisability < -5:
            advisability = -5
        elif advisability > 5:
            advisability = 5

        return advisability

class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """
        Parameters:
            None
        """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        name = input("What is the name of the event? ")
        outdoors = input("Is the event outdoors? ")
        outdoors = outdoors.lower()
        cover_avaliable = input("Is there covered shelter? ")
        cover_avaliable = cover_avaliable.lower()
        time = int(input("What time is the event? "))

        if outdoors == "y" or outdoors == "yes":
            outdoors = True
        else:
            outdoors = False

        if cover_avaliable == "y" or cover_avaliable == "yes":
            cover_avaliable = True
        else:
            cover_avaliable = False

        event = Event(name, outdoors, cover_avaliable, time)
        self._event = event

        return self._event

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        print("  2) Simple prediction.")
        print("  3) Sophisticated prediction.")
        model_choice = int(input("> "))
        # Error handling can be added to this method.
        if model_choice == 1 :
            self._prediction_model = YesterdaysWeather(weather_data)
        elif model_choice == 2:
            number_days = int(input("Enter how many days of data you wish to use for making the prediction: "))
            self._prediction_model = SimplePrediction(weather_data, number_days)
        elif model_choice == 3:
            number_days = int(input("Enter how many days of data you wish to use for making the prediction: "))
            self._prediction_model = SophisticatedPrediction(weather_data, number_days)

        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # The following print statement is an example of printing out the
        # class name of an object, which you may use for making the
        # advisability output more meaningful.
        print("Based on", type(self._prediction_model).__name__, "model, the advisability of holding",\
         self._event.get_name(), "is", impact)

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """

        another_check = input("Would you like to check again? ")
        another_check = another_check.lower()
        if another_check == 'y' or another_check == 'yes':
            return True
        elif another_check == 'n' or another_check == 'no':
            return False

def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()



if __name__ == "__main__":
    main()
