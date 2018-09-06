import React, { Component } from 'react';
import return_wav from '../sounds/return.wav';
import success_wav from '../sounds/success.wav';
import error_short_wav from '../sounds/error_short.wav';
import './Terminal.css';

class Terminal extends Component {
	constructor(props){
		super(props);
		this.$terminal = null;
		this.sounds = {
			'blarp' : new Audio(return_wav),
			'bleep' : new Audio(success_wav),
			'bloop' : new Audio(error_short_wav)
		};

		window.queryTerminal = this.queryTerminal;
	}

	componentWillMount() {}

	componentWillUnmount() {}

	componentDidMount() {
		this.resizeTerminal();

		var self = this;
		window.$(window).resize(function(){self.resizeTerminal();});
	}

	resizeTerminal() {
		this.height = parseInt(window.innerHeight/1080 * 540);
		this.width  = parseInt(window.innerHeight/1080 * 926);
		this.constructTerminal();
		window.$(".small-terminal").css("left", "calc(100% - " + this.width + "px)");
	}

	constructTerminal() {
		// Reset terminal
		if (this.$terminal && this.$terminal.hasOwnProperty('destroy')) {
			this.$terminal.destroy();
		}

		var self = this;
		this.$terminal = window.$('#terminal').terminal(function(command) {
			self.handleCommand.call(this, command, self);
		}, {
			greetings: '<< COG 1347-1 :: *CONFIDENTIAL* FOR INTERNAL USE ONLY >>\n',
			name: 'cog',
			height: this.height,
			width: this.width,
			prompt: '$ ',
			exit: false
		});
	}


	queryTerminal = async (line) => {
		const command = line.split(' ')[0];
		const input = line.split(' ').slice(1).join(' ').toString();

		//let url = (window.location.href.includes("localhost")) ? "http://127.0.0.1" : window.location.protocol + '//' + window.location.hostname;
		const response = await fetch(window.location.href + "get?msg=" + line, {'method': 'get'});

		const status = response.status;
		if (status !== 200) {
			return '-cog: Lost connection to COG 1347-1'
		}

		const text = await response.text();
		return "[[b;lightblue;]" + text + "]";
	}

	handleCommand(command, env) {
		if (command === '') {
			return;
		}

		//env.sounds.bleep.play();
		var res = env.queryTerminal.call(env, command);
		this.echo(res);
		env.sounds.blarp.play();
	}

	render() {
		return (
			<div>
				<div id="terminal" className="small-terminal"></div>
			</div>
		);
	}
}

export default Terminal;
