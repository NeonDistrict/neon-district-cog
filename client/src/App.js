import React, { Component } from 'react';
import { BrowserRouter as Router, Link, Route} from 'react-router-dom';

// CSS
import './App.css';

// Images
import cogImg from './images/cog.jpg';

// Pages
import Terminal from './Terminal/Terminal.js';

class App extends Component {
  constructor(props){
    super(props);
  }

  componentDidMount() {
    this.sizeLeftEye();
    this.sizeRightEye();

    var self = this;
    window.$(window).resize(function(){self.sizeLeftEye();self.sizeRightEye();});
  }

  sizeLeftEye() {
    this.top = parseInt(window.innerHeight/1080 * 260);
    this.left = parseInt(window.innerHeight/1080 * 1440);
    this.diameter = parseInt(window.innerHeight/1080 * 77);
    window.$("#left-eye").css("top", this.top + "px");
    window.$("#left-eye").css("left", "calc(100% - " + this.left + "px)");
    window.$("#left-eye").css("height", this.diameter + "px");
    window.$("#left-eye").css("width", this.diameter + "px");
  }

  sizeRightEye() {
    this.top = parseInt(window.innerHeight/1080 * 353);
    this.left = parseInt(window.innerHeight/1080 * 1600);
    this.diameter = parseInt(window.innerHeight/1080 * 77);
    window.$("#right-eye").css("top", this.top + "px");
    window.$("#right-eye").css("left", "calc(100% - " + this.left + "px)");
    window.$("#right-eye").css("height", this.diameter + "px");
    window.$("#right-eye").css("width", this.diameter + "px");
  }

  render() {
    return (
      <Router>
        <div className="App">
          <span id="left-eye" className="eye-dot yellow-glow"></span>
          <span id="right-eye" className="eye-dot yellow-glow"></span>
          <Terminal />
        </div>
      </Router>
    );
  }
}

export default App;
