import React from 'react';
import './Buttons.css';

export default class Buttons extends React.Component {
    constructor(props) {
        super(props);
		this.button_colors = {
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
