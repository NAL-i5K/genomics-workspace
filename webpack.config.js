const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const nodeModules = path.resolve(__dirname, 'node_modules');

const appScripts = path.resolve(__dirname, 'app/static/app/scripts');
const appStyles = path.resolve(__dirname, 'app/static/app/css');
const appScriptConfig = {
  entry: path.join(nodeModules, '/jquery/dist/jquery.js'),  // Just a fake entry, we only copy files here
  plugins: [
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/marked/marked.min.js'), to: appScripts},
        { from: path.join(nodeModules, '/jquery/dist/jquery.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/js/bootstrap.js'), to: appScripts},
        { from: path.join(nodeModules, '/underscore/underscore.js'), to: appScripts},
        { from: path.join(nodeModules, '/Respond.js/dest/respond.src.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/css/bootstrap.css'), to: appStyles},
    ])
  ],
  module: {
    noParse: [/\.js$/] //use noParse to accelerate
  }
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
  ],
  module: {
    noParse: [/\.js$/] //use noParse to accelerate
  }
};

const hmmerScripts = path.resolve(__dirname, 'hmmer/static/hmmer/scripts');
const hmmerScriptConfig = {
  entry: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'),  // Just a fake entry, we only copy files here
  plugins: [
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'), to: hmmerScripts},
        { from: path.join(nodeModules, '/jquery-hoverintent/jquery.hoverIntent.js'), to: hmmerScripts},
    ])
  ],
  module: {
    noParse: [/\.js$/] //use noParse to accelerate
  }
};

const clustalScripts = path.resolve(__dirname, 'clustal/static/clustal/scripts');
const clustalScriptConfig = {
  entry: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'),  // Just a fake entry, we only copy files here
  plugins: [
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'), to: clustalScripts},
        { from: path.join(nodeModules, '/jquery-hoverintent/jquery.hoverIntent.js'), to: clustalScripts},
    ])
  ],
  module: {
    noParse: [/\.js$/] //use noParse to accelerate
  }
};

module.exports = [
  appScriptConfig, blastScriptConfig, hmmerScriptConfig, clustalScriptConfig,
];
