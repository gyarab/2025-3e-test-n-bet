from apps.strategies.services.base.atomic_strategy import AtomicStrategy


class IndicatorStrategy(AtomicStrategy):
    """
    Class to define Indicator based Strategies that can be used to craft a bigger one's, e.g. SMAStrategy, ..etc.
    Made to distinguish between Indicator based strategies and Prediction Model based ones.
    """

    @classmethod
    def _from_json(cls, json_data: dict) -> "IndicatorStrategy":
        """
        Create an IndicatorStrategy instance from JSON data.

        Expects JSON data structure:
        {
            "name": "Strategy Name"
            "parameters": {
                ...
            }
        }
        """
        name = (
            json_data.get("name", "Unnamed Indicator Strategy").strip().replace(" ", "")
        )

        for subclass in cls.__subclasses__():
            # It needs to evaluate the name without "Strategy" suffix to match the class name, e.g. "SMA" for "SMAStrategy"
            if subclass.__name__ == name or subclass.__name__.replace("Strategy", "") == name:
                return subclass._from_json(json_data.get("parameters", {}))
