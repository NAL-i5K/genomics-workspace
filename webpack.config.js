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

const blastScripts = path.resolve(__dirname, 'blast/static/blast/scripts');
const blastStyles = path.resolve(__dirname, 'blast/static/blast/css');
const blastScriptConfig = {
  entry: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'),  // Just a fake entry, we only copy files here
  plugins: [
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'), to: blastScripts},
        { from: path.join(nodeModules, '/jquery-hoverintent/jquery.hoverIntent.js'), to: blastScripts},
        { from: path.join(nodeModules, '/jquery-ui-dist/jquery-ui.js'), to: blastScripts},
        { from: path.join(nodeModules, '/datatables-tabletools/js/dataTables.tableTools.js'), to: blastScripts},
        { from: path.join(nodeModules, '/datatables.net-colreorder/js/dataTables.colReorder.js'), to: blastScripts},
        { from: path.join(nodeModules, '/datatables.net-bs/js/dataTables.bootstrap.js'), to: blastScripts},
        { from: path.join(nodeModules, '/chroma-js/chroma.js'), to: blastScripts},
        { from: path.join(nodeModules, '/jquery.dragscrollable/dragscrollable.js'), to: blastScripts},
        { from: path.join(nodeModules, '/backbone/backbone.js'), to: blastScripts},
        { from: path.join(nodeModules, '/bootstrap-switch/dist/js/bootstrap-switch.js'), to: blastScripts},
        { from: path.join(nodeModules, '/bootstrap-switch/dist/css/bootstrap3/bootstrap-switch.css'), to: blastStyles},
        { from: path.join(nodeModules, '/bootstrap-select/dist/css/bootstrap-select.css'), to: blastStyles},
        { from: path.join(nodeModules, '/datatables.net-colreorder-dt/css/colReorder.dataTables.css'), to: blastStyles},
        { from: path.join(nodeModules, '/datatables.net-bs/css/dataTables.bootstrap.css'), to: blastStyles},
        { from: path.join(nodeModules, '/datatables.net-dt/css/jquery.dataTables.css'), to: blastStyles},
    ])
  ]
};

module.exports = [
  appScriptConfig, blastScriptConfig
];
