const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const DisableOutputWebpackPlugin = require('disable-output-webpack-plugin');

const nodeModules = path.resolve(__dirname, 'node_modules');

const appScripts = path.resolve(__dirname, 'app/static/app/scripts');
const appStyles = path.resolve(__dirname, 'app/static/app/css');
const appFonts = path.resolve(__dirname, 'app/static/app/fonts');
const appScriptConfig = {
  entry: path.join(nodeModules, '/jquery/dist/jquery.js'),  // Just a fake entry, we only copy files here
  output: {
    path: __dirname,
    filename: 'bundle.js' // this file will be removed by disable output webpack plugin
  },
  plugins: [
    new DisableOutputWebpackPlugin(),
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/marked/marked.min.js'), to: appScripts},
        { from: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'), to: appScripts},
        { from: path.join(nodeModules, '/jquery/dist/jquery.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/js/bootstrap.js'), to: appScripts},
        { from: path.join(nodeModules, '/underscore/underscore.js'), to: appScripts},
        { from: path.join(nodeModules, '/Respond.js/dest/respond.src.js'), to: appScripts},
        { from: path.join(nodeModules, '/bootstrap/dist/css/bootstrap.css'), to: appStyles},
        { from: path.join(nodeModules, '/bootstrap/dist/css/bootstrap.css.map'), to: appStyles},
        { from: path.join(nodeModules, '/bootstrap/dist/fonts/glyphicons-halflings-regular.eot'), to: appFonts},
        { from: path.join(nodeModules, '/bootstrap/dist/fonts/glyphicons-halflings-regular.svg'), to: appFonts},
        { from: path.join(nodeModules, '/bootstrap/dist/fonts/glyphicons-halflings-regular.ttf'), to: appFonts},
        { from: path.join(nodeModules, '/bootstrap/dist/fonts/glyphicons-halflings-regular.woff'), to: appFonts},
        { from: path.join(nodeModules, '/bootstrap/dist/fonts/glyphicons-halflings-regular.woff2'), to: appFonts},
    ])
  ],
  module: {
    noParse: [/\.js$/] // use noParse to accelerate
  }
};

const blastScripts = path.resolve(__dirname, 'blast/static/blast/scripts');
const blastStyles = path.resolve(__dirname, 'blast/static/blast/css');
const blastImages = path.resolve(__dirname, 'blast/static/blast/css/images');
const blastScriptConfig = {
  entry: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'),  // Just a fake entry, we only copy files here
  output: {
    path: __dirname,
    filename: 'bundle.js' // this file will be removed by disable output webpack plugin
  },
  plugins: [
    new DisableOutputWebpackPlugin(),
    new CopyWebpackPlugin([
        { from: path.join(nodeModules, '/d3/d3.js'), to: blastScripts},
        { from: path.join(nodeModules, '/codemirror/lib/codemirror.js'), to: blastScripts},
        { from: path.join(nodeModules, '/codemirror/addon/search/searchcursor.js'), to: blastScripts},
        { from: path.join(nodeModules, '/codemirror/addon/selection/active-line.js'), to: blastScripts},
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
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_444444_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_777620_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_cc0000_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_555555_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_777777_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-dist/images/ui-icons_ffffff_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_diagonals-thick_18_b81900_40x40.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_diagonals-thick_20_666666_40x40.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_highlight-soft_75_ffe45c_1x100.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_highlight-soft_100_eeeeee_1x100.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_gloss-wave_35_f6a828_500x100.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_glass_65_ffffff_1x400.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_glass_100_fdf5ce_1x400.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-bg_glass_100_f6f6f6_1x400.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-icons_222222_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-icons_228ef1_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-icons_ef8c08_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-icons_ffd27a_256x240.png'), to: blastImages},
        { from: path.join(nodeModules, '/jquery-ui-themes/themes/ui-lightness/images/ui-icons_ffffff_256x240.png'), to: blastImages},
    ])
  ],
  module: {
    noParse: [/\.js$/] //use noParse to accelerate
  }
};

const hmmerScripts = path.resolve(__dirname, 'hmmer/static/hmmer/scripts');
const hmmerScriptConfig = {
  entry: path.join(nodeModules, '/jquery-validation/dist/jquery.validate.js'),  // Just a fake entry, we only copy files here
  output: {
    path: __dirname,
    filename: 'bundle.js' // this file will be removed by disable output webpack plugin
  },
  plugins: [
    new DisableOutputWebpackPlugin(),
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
