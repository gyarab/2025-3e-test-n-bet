class Indicator {
    constructor(name, paremeters) {
        this.name = name;
        this.paremeters = paremeters;
    }

    getParameters() {
        return this.paremeters;
    }

    getName() {
        return this.name;
    }

    getIndicatorData() {
        return {
            name: this.name,
            parameters: this.paremeters
        };
    }
}