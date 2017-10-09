import particlesJS from 'particles.js';
import Typed from 'typed.js';

// load particles.js
// https://github.com/VincentGarreau/particles.js/
window.particlesJS.load('particles-js', 'static/js/particles.config.json')

// load typed.js
// https://github.com/mattboldt/typed.js/
var options = {
  strings: [
    "a full stack developer.",
    "a front end developer.",
    "a singer.",
    "a videographer.",
    "a UX designer.",
    "a writer.",
  ],
  typeSpeed: 50,
  loop: true,
  showCursor: false
}

var typed = new Typed(".intro", options);
