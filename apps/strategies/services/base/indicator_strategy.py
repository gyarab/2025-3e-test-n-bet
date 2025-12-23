from apps.strategies.services.base.atomic_strategy import AtomicStrategy


class IndicatorStrategy(AtomicStrategy):
    """
    Class to define Indicator based Strategies that can be used to craft a bigger one's, e.g. SMAStrategy, ..etc.
    Made to distinguish between Indicator based strategies and Prediction Model based ones.
    """
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'IndicatorStrategy':
        """
        Create an IndicatorStrategy instance from JSON data.

        Get json data structure:
        {
            "name": "Strategy Name"
            "parameters": {
                ...
            }
        }
        """
        name = json_data.get("name", "Unnamed Indicator Strategy").strip().replace(" ", "")
        print("IndicatorStrategy name from json:", name)
        for subclass in cls.__subclasses__():
            print("Checking subclass:", subclass.__name__)
            if subclass.__name__ == name:
                return subclass._from_json(json_data.get("parameters", {}))