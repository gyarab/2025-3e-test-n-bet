class Indicator {
    constructor(name, params) {
        this.name = name;

        this.parameters = params.map(item => ({
            max: item.max || null,
            min: item.min || null,
            default: item.default || null,
            name: item.name,
            value: item.value ?? item.default,
        }));
    }

    static fromJSON(data) {
        const name = data.name;
        const parameters= data.parameters;
        const paramArray = Object.entries(parameters).map(([key, value]) => ({
            name: key,
            value: value,
        }));
        return new Indicator(name, paramsArray);
    }

    getNamesOfParameters() {
        return this.parameters.map(param => param.name??null);
    }

    getName() {
        return this.name.replaceAll("_", " ");
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