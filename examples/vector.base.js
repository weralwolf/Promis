var Vector = function (x, y, z) {
    // Vector data fields
    this.x = 0.;
    this.y = 0.;
    this.z = 0.;
    this.dim = 0;
        
    // Vector methods
    this.toString = function() {
        _representation = '{';
        switch (this.dim) {
            case 0: break;
            case 1: _representation += str(this.x); break;
            case 2: _representation += str(this.x) + ', ' + str(this.y); break;
            case 3: _representation += str(this.x) + ', ' + str(this.y) + ', ' + str(this.z); break;
        };
        return _representation + '}';
    };

    this.abs = function() {
            return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
    };
    
    // Vector construction
    if (typeof x === 'undefined') {
        this.x = x;
    } else {
        return;
    };
    this.dim = 1;
    if (typeof y === 'undefined') {
        this.y = y;
    } else {
        return;
    };
    this.dim = 2;
    if (typeof z === 'undefined') {
        this.z = z;
    } else {
        return;
    };
    this.dim = 3;
};

k = new Vector(1, 1, 1);

// addint new method to Vector class
Vector.prototype.add = function(vector) {
  this.x += vector.x;
  this.y += vector.y;
  this.z += vector.z;
  return this;  
};

// k vector already has `add` function, cause it added with prototype property

l = new Vector(2, 3, 4);

// l twice added to k vector
k.add(l).add(l);
