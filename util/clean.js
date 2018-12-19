const fs = require('fs');
const path = require('path');

const deleteFolderRecursive = function(path) {
  fs.readdirSync(path).forEach(function(file, index){
    let curPath = path + "/" + file;
    if (fs.lstatSync(curPath).isDirectory()) { // recurse
      deleteFolderRecursive(curPath);
    } else { // delete file
      fs.unlinkSync(curPath);
    }
  });
  fs.rmdirSync(path);
};

const projectRootPath = path.resolve(__dirname, '..');
const gitIgnorePath = path.resolve(projectRootPath, '.gitignore');

let files = fs.readFileSync(gitIgnorePath)
              .toString()
              .split('\n')
              .filter(function(data){
                if (
                  data !== '' &&
                  !data.startsWith('#') &&
                  !data.startsWith('*') &&
                  !data.startsWith('.')
                ) {
                    if (
                      data.startsWith('/app/static') ||
                      data.startsWith('/blast/static') ||
                      data.startsWith('/clustal/static') ||
                      data.startsWith('/hmmer/static')
                    )
                      return true;
                }
              });

for (let f of files) {
  f = path.resolve(projectRootPath, '.' + f);
  if (fs.existsSync(f)) {
    if (fs.lstatSync(f).isDirectory()) {
      deleteFolderRecursive(f);
    } else {
      fs.unlinkSync(f);
    }
  } 
}