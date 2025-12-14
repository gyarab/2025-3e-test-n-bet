import IndicatorSelector from './indicator_selector.js'

export function initIndicatorSelector(wrapperSelector, indicatorsData) {
    const optionNames = indicatorsData.indicators.map(i => i.name);
    return new IndicatorSelector(wrapperSelector, optionNames, indicatorsData);
}

export function initConditionBuilder(wrapperSelector, indicatorsData) {
    return new initConditionBuilder(wrapperSelector, indicatorsData);
}
