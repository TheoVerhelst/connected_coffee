class Buttons extends React.Component {
    constructor(props) {
        super(props);
		this.button_colors = {
            disconnected: "grey lighten-1",
			off: "grey lighten-1",
			heating: "blue lighten-1",
			ready: "light-green lighten-1",
			brewing: "brown lighten-1",
			no_water: "deep-orange lighten-1"
		}
        this.handlePower = this.handlePower.bind(this);
        this.handleOneCup = this.handleCup.bind(this, 1);
        this.handleTwoCups = this.handleCup.bind(this, 2);
	}


    handlePower() {
        this.props.socket.emit(this.props.state === "off" ? "turn_on" : "turn_off");
    }

    handleCup(cups) {
        var command = "brew_" + (cups === 1 ? "one" : "two")
        if (this.props.ordered_cups === cups)
            command = "stop"
        this.props.socket.emit(command);
    }

	render() {
		const classes = "btn-floating btn-large waves-effect waves-light " + this.button_colors[this.props.state] + " command-button";
		var cupButton1, cupButton2;
		if (this.props.state !== "no_water") {
			cupButton1 =
                <button className={classes} onClick={this.handleOneCup}>
    				<i className="material-icons">{this.props.ordered_cups === 1 ? "cancel" : "looks_one"}</i>
    			</button>;
			cupButton2 =
                <button className={classes} onClick={this.handleTwoCups}>
    				<i className="material-icons">{this.props.ordered_cups === 2 ? "cancel" : "looks_two"}</i>
    			</button>;
		} else {
			cupButton1 = null;
			cupButton2 = null;
		}
		return (
			<div className="card-action center-align">
				{cupButton1}
				<button className={classes} onClick={this.handlePower}><i className="material-icons">power_settings_new</i></button>
				{cupButton2}
			</div>
		);
	}
}

class Status extends React.Component {
    constructor(props) {
        super(props);
		this.states_text = {
            disconnected: {
                color: "grey darken-2",
                button_color: "grey lighten-1",
                title: "Not connected",
                text: "Please wait until the connection to the coffee machine is established.",
                icon: "timelapse"
            },
			off: {
				color: "grey darken-2",
				button_color: "grey lighten-1",
				title: "The machine is currently off",
				text: "You can make a coffee, or just turn it on and let it heat up.",
				icon: "power_settings_new"
			},
			heating: {
				color: "blue darken-3",
				button_color: "blue lighten-1",
				title: "The machine is heating up",
				text: "Please wait a little bit, it's not ready yet.",
				icon: "timelapse"
			},
			ready: {
				color: "light-green darken-22",
				button_color: "light-green lighten-1",
				title: "The machine is ready",
				text: "You can brew a coffee or turn it off.",
				icon: "free_breakfast"
			},
			brewing: {
				color: "brown darken-1",
				button_color: "brown lighten-1",
				title: "You coffee is being served",
				text: "Please wait a few seconds for the brewing to finish.",
				icon: "timelapse"
			},
			no_water: {
				color: "deep-orange accent-4",
				button_color: "deep-orange lighten-1",
				title: "The machine has not enough water!",
				text: "Please go ahead and fill the water tank.",
				icon: "error"
			}
		}
    }

	render() {
		const state_text = this.states_text[this.props.state];
        var buttons = null;
        if (this.props.state !== "disconnected") {
            buttons = <Buttons socket={this.props.socket} state={this.props.state} ordered_cups={this.props.ordered_cups}/>
        }
		return (
			<div className={"card " + state_text.color}>
				<div className="card-content white-text">
					<span className="card-title">
						<i className="large material-icons right state-icon">{state_text.icon}</i>
						{state_text.title}
					</span>
					<p>{state_text.text}</p>
				</div>
                {buttons}
			</div>
		);
	}
}

class App extends React.Component {
    constructor(props) {
        super(props);
        this.socket = io.connect('http://0.0.0.0:5000/');
        this.socket.on("update", status => this.setState(status));
        this.state = {
            state: "disconnected",
            led: false,
            ordered_cups: 0
        };
    }

	render() {
		return (
			<div className="App">
				<div className="container">
					<div className="row">
						<h1>
                            <i className={"material-icons left large " + (this.state.led === true ? "red-text" : "")}>wb_sunny</i>
                            Your Coffee Server
                        </h1>
					</div>
                    <div className="row">
                        <Status socket={this.socket} state={this.state.state} ordered_cups={this.state.ordered_cups} />
                    </div>
				</div>
			</div>
		);
	}
}

ReactDOM.render(<App />, document.getElementById('root'));
