
 	if (!this.files.length) 
 		callback && callback(null, false);
 		return;
 	
 
 	var contents = this.toString(),
 		len = this.files.length,
 		errors = [],
 		completed = 0;
 
 	for (var i = 0; i < len; i++) 
 		fs.writeFile(this.files[i], contents, 'utf8', function(err) 
 			err && errors.push(err);
 			completed++;
 			if (completed === len) 
 				callback && callback(errors.length ? errors : null, true);
 			
 		);
 	
 