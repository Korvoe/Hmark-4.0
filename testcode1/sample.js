	var name = node.name,
		value = node.value,
		children = node.children,
		comments = node.comments || [];

    var i = f();

	var newContext = {
		_remove: function(name, index) {
			index = Math.max(index || 0, 0);
			if (!this[name]) {
				return this;
			}

			var node = this[name];
			if (Array.isArray(this[name])) {
				if (this[name][index]) {
					node = this[name][index];
					this[name].splice(index, 1);
					if (this[name].length === 1) {
						this[name] = this[name][0];
					}
					file.emit('removed', node);
				}
			} else {
				node = this[name];
				delete this[name];
				file.emit('removed', node);
			}

			return this;
		},

		_add: function(name, value, children, comments, options) {
			if (blacklistedNames[name]) {
				throw new Error('The name "' + name + '" is reserved');
			}

			options = options || {};

			var node = createConfItem(file, newContext, {
				name: name,
				value: value,
				children: children,
				comments: comments,
				isVerbatim: !!options.isVerbatim
			});
			file.emit('added', node);
			return this;
		},

		_addVerbatimBlock: function(name, value, comments) {
			return this._add(name, value, null, comments, {
				isVerbatim: true
			});
		},

		_getString: function(depth) {
			depth = depth || +!this._root;
			var prefix = new Array(depth).join(file.tab),
				buffer = '',
				i;

			if (this._comments.length) {
				for (i = 0; i < this._comments.length; i++) {
					buffer += '#' + this._comments[i] + '\n';
				}
			}

			buffer += prefix + (!this._root ? this._name : '');

			if (this._isVerbatim) {
				buffer += ' {' + (this._value || '') + '}';
			} else if (this._value) {
				buffer += ' ' + this._value;
			}

			var properties = Object.keys(this)
				.filter(function(key) {
					return typeof(newContext[key]) !== 'function';
				})
				.map(function(key) {
					return newContext[key];
				});

			if (properties.length) {
				if (!this._root) {
					buffer += ' {\n';
				}
				for (i = 0; i < properties.length; i++) {
					var prop = properties[i];
					if (Array.isArray(prop)) {
						for (var j = 0; j < prop.length; j++) {
							buffer += prop[j]._getString(depth + 1);
						}
					} else {
						buffer += prop._getString(depth + 1);
					}
				}
				if (!this._root) {
					buffer += prefix + '}\n';
				}
			} else if (!this._root) {
				if (!this._isVerbatim) {
					buffer += ';';
				}
				buffer += '\n';
			}

			return buffer;
		},

		toString: function() {
			return this._getString(0);
		}
	};

	Object.defineProperty(newContext, '_value', {
		enumerable: false,
		get: function() {
			return value;
		},
		set: function(newValue) {
			newValue = newValue.toString();
			if (value === newValue) {
				return;
			}

			var oldValue = value;
			value = newValue;
			file.emit('changed', newContext, oldValue);
		}
	});

	Object.defineProperty(newContext, '_isVerbatim', {
		enumerable: false,
		value: node.isVerbatim,
		writable: false
	});

	Object.defineProperty(newContext, '_name', {
		enumerable: false,
		value: name,
		writable: false
	});

	Object.defineProperty(newContext, '_comments', {
		enumerable: false,
		value: comments,
		writable: false
	});

	if (context[name]) {
		//already exists, create an array or append it to the new one
		if (!Array.isArray(context[name])) {
			context[name] = [ context[name] ];
		}

		context[name].push(newContext);
	} else {
		context[name] = newContext;
	}

	if (children) {
		for (var i = 0; i < children.length; i++) {
			createConfItem(file, newContext, children[i]);
		}
	}

	return newContext;

