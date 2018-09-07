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

		this.sounds.blarp.volume = 0.3;
		this.sounds.bleep.volume = 0.3;
		this.sounds.bloop.volume = 0.3;

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

		var today = new Date();
		var date = '2XXX-'+(today.getMonth()+1)+'-'+today.getDate();
		var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
		var date_and_time = date + " " + time;

		let welcome = "<< Neon District Help Desk is Online >>\n\nCOG 1347-1 version 2.4.2148 (gcc version 7.96 200)\nMUR 132118 (GOG MUR 5.5.2393) " + date_and_time + "\nBIOS-provided neon RAM map:\nBIOS-mur132118: 00000000000000000 - 000000000009fc00 (usable)\nBIOS-mur132118: 0000000000009fc00 - 00000000000a0000 (reserved)\nBIOS-mur132118: 00000000000ce0000 - 0000000000100000 (reserved)\nBIOS-mur132118: 00000000000100000 - 000000003fff8000 (usable)\nBIOS-mur132118: 0000000003fff0000 - 0000000040000000 (ACPI data)\nBIOS-mur132118: 0000000003fff8000 - 0000000040000000 (ACPI NVS)\nBIOS-mur132118: 000000000fff00000 - 0000000100000000 (reserved)\nInitializing CPU#0\nDentry cache hasssssssssssssssssssssssssssh\nRamfs: mounted with oooooooooooooooooooooooooopjuhuihrfp8943hh\nERROR\nCPU : MURMURMURMURMURMURMURMURMURMUR\n     SYSTEM_ERROR\n     Total number of system errors : 5\n     Manual correction needed.";

		var self = this;
		this.$terminal = window.$('#terminal').terminal(function(command) {
			self.handleCommand.call(this, command, self);
		}, {
			greetings: welcome,//'<< COG 1347-1 :: *CONFIDENTIAL* FOR INTERNAL USE ONLY >>\n',
			name: 'cog',
			height: this.height,
			width: this.width,
			prompt: '$ ',
			exit: false
		});
	}

	queryTerminal = async (line, term) => {

		// Loading
		term.set_prompt("[[b;yellow;]Computing Response.\n]");

		let url = (window.location.href.includes("localhost")) ? "http://127.0.0.1" : window.location.protocol + '//' + window.location.hostname;
		const response = await fetch(url + "/cakechat_api/v1/actions/get_response", {
			'method': 'post',
			'headers': {
				'Accept' : 'application/json',
				'Content-Type' : 'application/json'
			},
			'body': JSON.stringify({
				'context' : [line]
			})
		});

		const status = response.status;
		if (status !== 200) {
			return '-cog: Lost connection to COG 1347-1'
		}

		const json = await response.json();
		let text = json.response;
		let emotion = (json.hasOwnProperty('emotion') ? json.emotion : 'neutral');
		let activity = (json.hasOwnProperty('activity') ? json.activity : 'none');

		// Show response
		term.echo("[[b;green;]Loaded Response.]")
			.set_prompt("$ ");

		window.$('.eye-dot').removeClass('yellow-glow red-glow green-glow blue-glow orange-glow violet-glow');
		if (emotion == 'neutral') {
			window.$('.eye-dot').addClass('yellow-glow');
		} else if (emotion == 'anger') {
			window.$('.eye-dot').addClass('red-glow');
		} else if (emotion == 'joy') {			
			window.$('.eye-dot').addClass('green-glow');
		} else if (emotion == 'sadness') {
			window.$('.eye-dot').addClass('blue-glow');
		} else if (emotion == 'fear') {
			window.$('.eye-dot').addClass('orange-glow');
		}

		if (activity == 'raw') {
			// Raw HTML
			term.echo(text, {'raw':true});
		} else {
			// Default
			term.echo("[[b;lightblue;]" + text + "]");
		}

		// Return sound
		this.sounds.blarp.play();
	}

	handleCommand(command, env) {
		if (command === '') {
			return;
		}

		env.queryTerminal.call(env, command, this);
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
