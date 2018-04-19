# Notes for static files of blast

* `code-mirror` is for the functionality of bottom left panel of blast result page.
  * current version: [4.5.0](https://github.com/codemirror/CodeMirror/tree/43e88d47524fc1941fe3b74c13987be23e0feb02)
  * `scripts/codemirror-compressed.js` is compressed version of `codemirror.js` `active-line.js`, and `searchcursor.js` in `scripts/codemirror` through [UglifyJS](https://github.com/mishoo/UglifyJS2).
    * `active-line.js` and `searchcursor.js` are a little modified (make relative paths correct).
    * To generate the `scripts/codemirror-compressed.js`, at this folder
      * `npm install uglify-js@3.3.11 -g`
      * `uglifyjs ./scripts/codemirror/codemirror.js ./scripts/codemirror/active-line.js ./scripts/codemirror/searchcursor.js -o ./scripts/codemirror-compressed.js --compress` (the order of the input file is important)
