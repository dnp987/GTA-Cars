//step 1) require the modules we need
var
http = require('http'),//helps with http methods
path = require('path'),//helps with file paths
fs = require('fs');//helps with file system tasks
 
//a helper function to handle HTTP requests
function requestHandler(req, res) {
	var
	content = '',
	fileName = path.basename(req.url),//the file that was requested
	localFolder = __dirname + '/';//where our public files are located
	process.chdir("../html");
	localFolder = process.cwd();
	 
	//NOTE: __dirname returns the root folder that
	//this javascript file is in.
 
	if(fileName === 'test1.html'){//if index.html was requested...
		content = localFolder + "/" + fileName;//setup the file name to be returned

		//reads the file referenced by 'content'
		//and then calls the anonymous function we pass in
		fs.readFile(content,function(err,contents){
			//if the fileRead was successful...
			if(!err){
				//send the contents of index.html
				//and then close the request
				res.end(contents);
			} else {
				//otherwise, let us inspect the eror
				//in the console
				console.dir(err);
			};
		});
	} else {
		//if the file was not found, set a 404 header...
		res.writeHead(404, {'Content-Type': 'text/html'});
		//send a custom 'file not found' message
		//and then close the request
		res.end('<h1>Sorry, the page you are looking for cannot be found.</h1>');
	};
};
 
//step 2) create the server
http.createServer(requestHandler)
 
//step 3) listen for an HTTP request on port 3000
.listen(3000);
 console.log('Connected to port 3000');