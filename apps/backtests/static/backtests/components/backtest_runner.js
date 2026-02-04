import BacktestResults from "./backtest_results.js";
import StrategySelector from "./strategy_selector.js";

export default class BacktestRunner {
    constructor(root, strategiesData) {
        this.wrapper = root;
        
        this.lastBacktestData = null;
        this.lastUsedParams = null;
        
        this.strategiesData = strategiesData;

        this.init();
    }

    _getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    }

    init() {
        this.cacheElements();

        this.initBacktestResults();
        this.initStrategySelector();

        this.setupRunButton();
        this.setupSaveButton();

        this.handleSelectedStrategy();
        this.prepare();
    }

    cacheElements() {
        this.saveBtn = this.wrapper.querySelector('.save-backtest-btn');
        this.runBtn = this.wrapper.querySelector('.start-backtest-btn');;

        this.initialBalanceInput = this.wrapper.querySelector('.initial-balance-input');
        this.tokenSelect = this.wrapper.querySelector('.token-select');
        this.timeframeSelect = this.wrapper.querySelector('.timeframe-select');
        this.candleAmountInput = this.wrapper.querySelector('.candle-amount-input');
        this.circleImg = this.wrapper.querySelector('.loading-circle');

        if (!this.saveBtn || !this.runBtn) {
            throw new Error("BacktestRunner: Missing required elements in the DOM");
        }
    }

    setupSaveButton() {
        this.saveBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            try {   
                await this.save();
            } catch (error) {
                console.error("Error saving backtest:", error);
            }
        });
    }

    setupRunButton() {
        this.runBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            try {
                await this.run();
            } catch (error) {
                console.error("Error running backtest:", error);
            }
        });
    }

    initBacktestResults() {
        const backtestsResultRoot = this.wrapper.querySelector('.backtest-results');

        if (!backtestsResultRoot) {
            throw new Error("BacktestRunner: Backtest results wrapper not found");
        }

        this.backtestResults = new BacktestResults(backtestsResultRoot);
    }

    initStrategySelector() {
        const strategySelectorRoot = this.wrapper.querySelector('.strategy-selector');
        const descriptionWrapper = this.wrapper.querySelector('.strategy-description-wrapper');

        if (!strategySelectorRoot) {
            throw new Error("BacktestRunner: Strategy selector wrapper not found");
        }

        if (!descriptionWrapper) {
            throw new Error("BacktestRunner: Strategy description wrapper not found");
        }

        this.strategySelector = new StrategySelector(strategySelectorRoot, descriptionWrapper, this.strategiesData);
    }

    handleSelectedStrategy() {
        this.wrapper.addEventListener('strategySelected', () => {
            if (this.strategySelector.getSelectedStrategy()) {
                this.runBtn.classList.remove("bg-gray-400", "cursor-not-allowed");
                this.runBtn.classList.add("bg-teal-600", "hover:bg-teal-700");
                this.runBtn.disabled = false;
            } else {
                this.runBtn.classList.remove("bg-teal-600", "hover:bg-teal-700");
                this.runBtn.classList.add("bg-gray-400", "cursor-not-allowed");
                this.runBtn.disabled = true;
            }
        });
    }

    run() {    
        this.disableSaveButton();

        // Reset previous results
        this.backtestResults.reset();

        this.startLoadingAnimation();

        const selectedStrategy = this.strategySelector.getSelectedStrategy();

        if (selectedStrategy) {
            const strategy_id = selectedStrategy.id;
            const initial_balance = this.initialBalanceInput.value || 1000;
            const token = this.tokenSelect.value;
            const timeframe = this.timeframeSelect.value;
            const candle_amount = this.candleAmountInput.value || 500;
            
            // Store params for saving later
            this.lastUsedParams = {
                strategy_id: strategy_id,
                initial_capital: initial_balance,
                asset_id: token,
                timeframe: timeframe,  
                candle_amount: candle_amount
            };
            
            // Run backtest via API
            fetch("/api/backtests/run/", { 
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this._getCsrfToken(),
                    "Accept": "application/json"
                },
                body: JSON.stringify({
                    strategy_id,
                    initial_balance,
                    token,
                    timeframe,
                    candle_amount
                })
            })
            .then(res => {
                if (res.status === 401) {
                    window.location.href = '/login';
                    return;
                }   
                return res.json();
            })
            .then(data => {
                this.lastBacktestData = data.result;

                // Display results 
                this.backtestResults.buildUI(data.result);

                this.enableSaveButton();
            })
            .catch(error => {
                console.error("Error running backtest:", error);
                alert("An error occurred while running the backtest.");
            })
            .finally(() => {
                this.stopLoadingAnimation();
            });
        } else {
            alert('Please select a strategy before starting the backtest.');
            this.stopLoadingAnimation();
        }
    };

    save() {
        if (!this.lastBacktestData || !this.lastUsedParams) return;

        const payload = {
            strategy_id: this.lastUsedParams.strategy_id,
            asset_id: this.lastUsedParams.asset_id,
            initial_capital: this.lastUsedParams.initial_capital,
            position_size: this.lastUsedParams.position_size,
            start_date: this.lastBacktestData.start_date || new Date().toISOString().split('T')[0], 
            end_date: this.lastBacktestData.end_date || new Date().toISOString().split('T')[0],
            result: this.lastBacktestData
        };

        // Save backtest via API
        fetch("/api/backtests/save/", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this._getCsrfToken()
            },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                alert("Backtest saved successfully!");
                this.disableSaveButton();
            } else {
                alert("Error saving Backtest");
                console.error("Error saving backtest:", data.message);
            }
        })
        .catch(err => {
            console.error(err);
            alert("Network error trying to save.");
        });
    };

    startLoadingAnimation() {
        this.circleImg?.classList.remove('hidden');
    }

    stopLoadingAnimation() {
        this.circleImg?.classList.add('hidden');
    }

    disableSaveButton() {
        this.saveBtn.disabled = true;
        this.saveBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }

    enableSaveButton() {
        this.saveBtn.disabled = false;
        this.saveBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    prepare() {
        this.lastBacktestData = null;
        this.lastUsedParams = null;
        this.disableSaveButton();
    }

    
}