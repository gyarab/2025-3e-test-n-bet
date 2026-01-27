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

    // Create Indicator instance from JSON data
    static fromJSON(data) {
        const name = data.name;
        const parameters= data.parameters;
        const paramsArray = Object.entries(parameters).map(([key, value]) => ({
            name: key,
            value: value,
        }));
        return new Indicator(name, paramsArray);
    }

    // Get names of all parameters
    getNamesOfParameters() {
        return this.parameters.map(param => param.name??null);
    }

    // Get serialized name of the indicator
    getName() {
        return this.name.replaceAll("_", " ");
    }

    // Get all parameters
    getParameters() {
        return this.parameters;
    }

    // Get indicator data in serializable format
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

    // Set value of a specific parameter
    setValue(paramName, value) {
        const param = this.parameters.find(p => p.name === paramName);
        if (param) {
            param.value = value;
        }
    }

    // Get value of a specific parameter
    getValue(paramName) {
        const param = this.parameters.find(p => p.name === paramName);
        return param ? param.value : null;
    }
}

export default Indicator;