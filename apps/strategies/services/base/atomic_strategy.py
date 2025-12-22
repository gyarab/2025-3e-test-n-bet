from apps.strategies.services.base.base_strategy import BaseStrategy


class AtomicStrategy(BaseStrategy):
    """
    Class to define AtomicStrategies that can be used to craft a bigger one's, e.g. SMAStrategy, ARIMAStrategy, ..etc.
    Atomic Strategies are the building blocks for more complex strategies (called strategy conditions).
    Atomic Strategies contain either one indicator or one prediction model, but not more.
    """
    pass