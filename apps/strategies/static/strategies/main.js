import ConditionBuilder from './strategy_builder/condition_builder.js';

export function initConditionBuilder(wrapperSelector, indicatorsData) {
    return new ConditionBuilder(wrapperSelector, indicatorsData);
}
