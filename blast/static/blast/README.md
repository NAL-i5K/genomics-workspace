# Notes for static files of blast

* `code-mirror` is for the functionality of bottom left panel of blast result page.
  * current version: `4.0.3`
  * `scripts/codemirror-compressed.js` is compressed version of `codemirror.js` `active-line.js`, and `searchcursor.js` in `scripts/codemirror` through [UglifyJS](https://github.com/mishoo/UglifyJS2).
    * `active-line.js` and `searchcursor.js` are a little modified (make relative paths correct).
    * To generate the `scripts/codemirror-compressed.js`, at this folder
      * `npm install uglify-js@3.3.11 -g`
      * `uglifyjs ./scripts/codemirror/codemirror.js ./scripts/codemirror/active-line.js ./scripts/codemirror/searchcursor.js -o ./scripts/codemirror-compressed.js --compress` (the order of the imput file is important)
