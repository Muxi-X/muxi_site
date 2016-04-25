var webpack = require('webpack');
var path = require('path');
var OpenBrowserPlugin = require('open-browser-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  entry: path.resolve(__dirname, 'src/js/main.js'),
  output: {
    path: __dirname + '/static',
    publicPath: '../',
    filename: './js/bundle.js'
  },

  module: {
		loaders: [
			{
				test: /(\.jsx|\.js)$/,
				loader: 'babel?presets[]=es2015&presets[]=react',
				exclude: /node_modules/
			},
			{
				test: /(\.scss)$/,
				loader: ExtractTextPlugin.extract(['css-loader', 'sass-loader'])
			},
			{
				test: /\.json$/,
				loader: 'json'
			},
			{
		    test: /\.(jpe?g|png|gif|svg)$/,
      	loader: 'url?limit=8024&name=images/[name].[ext]'
			},
			{
		    test: /\.html$/,
   		  loader: 'url?name=[name].[ext]'
			},
		],
	},
  resolve: {
    extensions: ['', '.js', '.jsx','jpg','png'],
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new OpenBrowserPlugin({ url: 'http://localhost:8080' }),
    new ExtractTextPlugin('css/main.css')
  ],
  devtool: (process.env.NODE_ENV === 'production')?null:'sourceMap'
};