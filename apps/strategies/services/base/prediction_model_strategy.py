from apps.strategies.services.base.atomic_strategy import AtomicStrategy


class PredictionModelStrategy(AtomicStrategy):
    """
    Class to define Prediction Model based Strategies that can be used to craft a bigger one's, e.g. ARIMAStrategy, ..etc.
    Made to distinguish between Indicator based strategies and Prediction Model based ones.
    """
    pass