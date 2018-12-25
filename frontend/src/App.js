import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import openSocket from 'socket.io-client';
import './App.css';
import Status from './Status';

class App extends Component {
    constructor(props) {
        super(props);
        this.socket = openSocket('http://192.168.0.7:5000/');
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

export default App;
