# RTTS A Runtime Typed TypeScript Compiler

A Simply TypeScript Compiler with Superpower (without Node) :D



**This Software is Beta Version**


From this:

```typescript
function addNumbers(a: number, b: number): number {
    return a + b;
}

const result = addNumbers(1, "2");
console.log(result);
```

to this:

```javascript
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

```javascript
let x = 10; // @type number
let y = "hello"; // @type string
let z = true; // @type boolean
```

LICENSE:

A Simply TypeScript compiler with RunTime Type Check Copyright (C) 2023 Fabio F.G. Buono

This program is free software: you can redistribute it and/or modify it under the terms of the 
GNU Affero General Public License as published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. 
If not, see https://www.gnu.org/licenses/

