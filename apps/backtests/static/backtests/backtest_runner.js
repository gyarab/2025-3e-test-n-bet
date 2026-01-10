export default class BacktestRunner {
    constructor(selector, backtestData) {
        this.wrapper = document.querySelector(selector);

        this.backtestData = backtestData;
        
        this.lastBacktestData = null;
        this.lastUsedParams = null;
    }

    _getCsrfToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }

    run({circleImgSelector, 
        saveBtnSelector, 
        backtestResults, 
        selectedStrategySelector,
        initialBalanceSelector,
        tokenSelector,
        timeframeSelector,
        candleAmountSelector}) {
        
        this.disableSaveButton(saveBtnSelector);

        // Reset previous results
        backtestResults.reset();

        this.startLoadingAnimation(circleImgSelector);

        // Get selected strategy and parameters
        const selectedStrategy = document.querySelector(selectedStrategySelector);

        if (selectedStrategy) {
            const strategy_id = selectedStrategy.id.split('-').pop();
            const initial_balance = document.getElementById(initialBalanceSelector).value || 1000;
            const token = document.getElementById(tokenSelector).value;
            const timeframe = document.getElementById(timeframeSelector).value;
            const candle_amount = document.getElementById(candleAmountSelector).value || 500;
            
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
                backtestResults.buildUI(data.result);

                this.enableSaveButton(saveBtnSelector);
            })
            .catch(error => {
                console.error("Error running backtest:", error);
                alert("An error occurred while running the backtest.");
            })
            .finally(() => {
                this.stopLoadingAnimation(circleImgSelector);
            });
        } else {
            alert('Please select a strategy before starting the backtest.');
            this.stopLoadingAnimation(circleImgSelector);
        }
    };

    save(saveBtnSelector) {
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
                this.disableSaveButton(saveBtnSelector);
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

    startLoadingAnimation(circleImgSelector) {
        const circleImg = document.getElementById(circleImgSelector);
        if (circleImg) {
            circleImg.classList.remove('hidden');
        }
    }

    stopLoadingAnimation(circleImgSelector) {
        const circleImg = document.getElementById(circleImgSelector);
        if (circleImg) {
            circleImg.classList.add('hidden');
        }
    }

    disableSaveButton(saveBtnSelector) {
        const saveBtn = document.getElementById(saveBtnSelector);
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    enableSaveButton(saveBtnSelector) {
        const saveBtn = document.getElementById(saveBtnSelector);
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    }

    prepare(saveBtnSelector) {
        this.lastBacktestData = null;
        this.lastUsedParams = null;
        this.disableSaveButton(saveBtnSelector);
    }
}