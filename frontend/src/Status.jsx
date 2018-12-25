import React from 'react';
import './Status.css';
import Buttons from './Buttons';

export default class Status extends React.Component {
    constructor(props) {
        super(props);
		this.states_text = {
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
		const state_text = this.states_text[this.props.state_ll];
		return (
			<div className={"card " + state_text.color}>
				<div className="card-content white-text">
					<span className="card-title">
						<i className="large material-icons right state-icon">{state_text.icon}</i>
						{state_text.title}
					</span>
					<p>{state_text.text}</p>
				</div>
				<Buttons socket={this.props.socket} state_ll={this.props.state_ll} ordered_cups={this.props.ordered_cups}/>
			</div>
		);
	}
}
