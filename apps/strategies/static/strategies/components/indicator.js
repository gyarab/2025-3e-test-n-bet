class Indicator {
    constructor(name, params) {
        this.name = name;
        this.parameters = new Set();

        params.forEach(item => {
            this.parameters.add({
                max: item.max,
                min: item.min,
                default: item.default,
                name: item.name,
                value: item.default
            });
        });
    }

    getNamesOfParameters() {
        paramNames = this.parameters.map(param => param.name??null);
    }

    getName() {
        return this.name.replace("_", " ");
    }

    getParameters() {
        return this.parameters;
    }

    getIndicatorData() {
        const parametersObj = {};
        this.parameters.forEach(param => {
            parametersObj[param.name] = param.value;
        });

        return {
            name: this.name,
            parameters: parametersObj
        };
    }

    setValue(paramName, value) {
        const param = this.parameters.find(p => p.name === paramName);
        if (param) {
            param.value = value;
        }
    }

    getValue(paramName) {
        const param = this.parameters.find(p => p.name === paramName);
        return param ? param.value : null;
    }
}

export default Indicator;