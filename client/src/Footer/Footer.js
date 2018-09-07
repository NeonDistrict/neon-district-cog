import React, { Component } from 'react';

import './Footer.css';
import nd_logo_white from '../images/nd-logo.png';
import icon_twitter from '../images/icon-twitter.png';
import icon_discord from '../images/icon-discord.png';
import icon_reddit from '../images/icon-reddit.png';

const latest_date = new Date().getFullYear();

class Footer extends Component {
	constructor(props){
		super(props);
	}

	render() {
		return (
			<div id="footerContainer">
				<footer id="footer">
					<div className="right-menu">
						<a href="https://twitter.com/neondistrictRPG" target="_blank"><img id="twitter" src={icon_twitter} /></a>
						<a href="https://discord.gg/3AbutcS" target="_blank"><img id="discord" src={icon_discord} /></a>
						<a href="https://www.reddit.com/r/PineappleArcade/" target="_blank"><img id="reddit" src={icon_reddit} /></a>
						<a href="https://neondistrict.io" target="_blank"><img id="logo" src={nd_logo_white} /></a>
					</div>
				</footer>
			</div>
		);
	}

	/*
	render() {
		return (
			<div id="footerContainer">
				<footer id="footer">
					<div className="left-menu">
						<p id="copyright">NEON DISTRICT &reg; <br /> &copy; {latest_date} BLOCKADE GAMES, LLC</p>
					</div>

					<div className="right-menu">
						<a href="https://discord.gg/3AbutcS" target="_blank"><img id="discord" src={icon_discord} /></a>
						<a href="https://www.reddit.com/r/PineappleArcade/" target="_blank"><img id="reddit" src={icon_reddit} /></a>
						<a href="https://neondistrict.io" target="_blank"><img id="logo" src={nd_logo_white} /></a>
					</div>
				</footer>
			</div>
		);
	}
	*/
}

export default Footer;
