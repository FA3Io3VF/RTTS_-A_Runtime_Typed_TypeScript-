# RTTS A Runtime Typed TypeScript Compiler

A Simply TypeScript Compiler with Superpower (without Node) :D



**This Software is Beta Version**


From this:

```
function addNumbers(a: number, b: number): number {
    return a + b;
}

const result = addNumbers(1, "2");
console.log(result);
```

to this:

```
function addNumbers(a, b) {
    if (typeof a !== "number") {
        throw new TypeError("Type 'string' is not assignable to type 'number'");
    }
    if (typeof b !== "number") {
        throw new TypeError("Type 'string' is not assignable to type 'number'");
    }
    return a + b;
}

const result = addNumbers(1, "2");
if (typeof result !== "number") {
    throw new TypeError("Type 'string' is not assignable to type 'number'.");
}
console.log(result);
```

Or with Decoration:

```
let x = 10; // @type number
let y = "hello"; // @type string
let z = true; // @type boolean
```


"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
