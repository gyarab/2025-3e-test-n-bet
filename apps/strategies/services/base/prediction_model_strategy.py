from apps.strategies.services.base.atomic_strategy import AtomicStrategy


class PredictionModelStrategy(AtomicStrategy):
    """
    Class to define Prediction Model based Strategies that can be used to craft a bigger one's, e.g. ARIMAStrategy, ..etc.
    Made to distinguish between Indicator based strategies and Prediction Model based ones.
    """
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'PredictionModelStrategy':
        """
        Create an PredictionModelStrategy instance from JSON data.

        Get json data structure:
        {
            "name": "Strategy Name"
            "parameters": {
                ...
            }
        }
        """
        name = json_data.get("name", "Unnamed Prediction Strategy").strip().replace(" ", "")
        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass._from_json(json_data.get("parameters", {}))