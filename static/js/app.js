import particlesJS from 'particles.js';
import Typed from 'typed.js';

// load particles.js
// https://github.com/VincentGarreau/particles.js/
window.particlesJS.load('particles-js', 'static/js/particles.config.json')

// load typed.js
// https://github.com/mattboldt/typed.js/
var options = {
  strings: ["<i>First</i> sentence.", "&amp; a second sentence."],
  typeSpeed: 40
}

var typed = new Typed(".intro", options);
