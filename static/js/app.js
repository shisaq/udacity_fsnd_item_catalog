import Typed from 'typed.js';

// load particles.js
particlesJS.load('particles-js', 'static/js/particles.config.json', function() {
  console.log('callback - particles.js config loaded');
});

var options = {
  strings: ["<i>First</i> sentence.", "&amp; a second sentence."],
  typeSpeed: 40
}

var typed = new Typed(".intro", options);
