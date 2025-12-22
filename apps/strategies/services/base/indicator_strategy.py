from apps.strategies.services.base.atomic_strategy import AtomicStrategy


class IndicatorStrategy(AtomicStrategy):
    """
    Class to define Indicator based Strategies that can be used to craft a bigger one's, e.g. SMAStrategy, ..etc.
    Made to distinguish between Indicator based strategies and Prediction Model based ones.
    """
    pass