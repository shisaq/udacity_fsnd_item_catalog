var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');
var MinifyPlugin = require("babel-minify-webpack-plugin");

module.exports = {
  context: path.join(__dirname, "static"),
  devtool: debug ? "inline-sourcemap" : false,
  entry: "./js/app.js",
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: ['env']
        }
      }
    ]
  },
  output: {
    path: __dirname + "/static/js/",
    filename: "app.min.js"
  },
  plugins: debug ? [] : [
    new MinifyPlugin(),
  ],
};
