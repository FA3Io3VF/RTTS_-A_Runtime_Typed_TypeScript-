# RTTS_-A_Runtime_Typed_TypeScript-
A Simply TypeScript RunTime Type Preprocessor


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
