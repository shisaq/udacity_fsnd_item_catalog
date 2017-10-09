# Udacity FSND Catalog App

## How to Run It

1. Follow the instructions to install virtual environment in vagrant(from Udacity):

 [Vagrant VM Installation](https://www.udacity.com/wiki/ud088/vagrant)

2. Run Vagrant VM and head to the `/vagrant` path:

 `vagrant up`

 `vagrant ssh`

 `cd /vagrant`

3. In the local invironment of the same path, wownload this repo:

 `cd path/to/vagrant`

 `git clone https://github.com/shisaq/udacity_fsnd_item_catalog`

4. In Vagrant VM, go to the repo and initiate the database:

 `cd udacity_fsnd_item_catalog`

 `python initial_data.py`

5. In Vagrant VM, run the server:

 `python application.py`

6. Head to your browser and type the url to open this app:

 `localhost:8000`

## Technique Stacks

* Python & Flask
* HTML
* CSS
* JavaScript
* Oauth2.0

## Sources Used

* [Typed.js](https://github.com/mattboldt/typed.js/)
* [particles.js](https://github.com/VincentGarreau/particles.js/)
* jQuery
* [Google Oauth Login](https://developers.google.com/identity/protocols/OAuth2)
* [Facebook Oauth Login](https://developers.facebook.com/docs/facebook-login/web)
* [Color Reference](http://nipponcolors.com/)
* [Webpack](https://webpack.js.org/)

## Special Announcement

The client ID and Secrets of Google and Facebook Oauth Login I used is for personal
use and just for this project. Any other use by other people is not allowed and not
related to me.

## License

MIT
