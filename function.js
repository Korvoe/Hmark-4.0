
 				should.not.exist(err);
 				should.exist(tree);
 				tree.children.should.have.length(1);
 				tree.children[0].should.have.property('name', 'foo');
 				tree.children[0].should.have.property('value', 'bar');
 				tree.children[0].comments.should.have.length(0);
 				done();
 			