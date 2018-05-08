const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const nodeModules = path.resolve(__dirname, 'node_modules');

const appScripts = path.resolve(__dirname, 'app/static/app/scripts');
const appStyles = path.resolve(__dirname, 'app/static/app/content');
const appScriptConfig = {
  entry: path.join(nodeModules, '/jquery/dist/jquery.js'),  // Just a fake entry, we only copy files here
  plugins: [
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/jquery/dist/jquery.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/js/bootstrap.js'), to: appScripts},
        { from: path.join(nodeModules, '/underscore/underscore.js'), to: appScripts},
        { from: path.join(nodeModules, '/Respond.js/dest/respond.src.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/css/bootstrap.css'), to: appStyles},
    ])
  ]
};

module.exports = [
  appScriptConfig,
];
