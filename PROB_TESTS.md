# Probabilistic Programming Test Suite for ALGOL 26

## Test 1: Basic Bernoulli Sampling

```
begin
  var d := prob { x: bernoulli(0.6); x; };
  var s := sample(d);
  println("Sample from Bernoulli(0.6): ", s)
end
```

Expected: prints either `true` or `false` with roughly 60% true.

## Test 2: Normal Distribution

```
begin
  var d := prob { x: normal(0.0, 1.0); x; };
  var s := sample(d);
  println("Sample from Normal(0,1): ", s)
end
```

Expected: prints a floating point number.

## Test 3: Uniform Distribution

```
begin
  var d := prob { x: uniform(1, 6); x; };
  var s := sample(d);
  println("Sample from Uniform(1,6): ", s)
end
```

Expected: prints integer between 1 and 5.

## Test 4: Multiple Samples and Loop

```
proc countHeads(n: int) => int =
  if n <= 0 then
    0
  else
    var d := prob { x: bernoulli(0.5); x; };
    var s := sample(d);
    (if s then 1 else 0) + countHeads(n - 1);

begin
  var heads := countHeads(10);
  println("Number of heads in 10 flips: ", heads)
end
```

Expected: prints a number between 0 and 10.

## Test 5: Using Given (Conditional) - NOT YET IMPLEMENTED

```
begin
  var d := prob { x: normal(0, 1); x; };
  var conditioned := d given (x > 0);
  var s := sample(conditioned);
  println("Conditioned sample: ", s)
end
```

Expected: NotImplementedError.

---

All tests except Test 5 should pass. The interpreter implements:
- `bernoulli(p)`, `normal(mean, std)`, `uniform(a,b)`
- `prob { ... }` as an expression returning a distribution
- `sample(d)` to draw a sample
- Binding inside prob blocks with `identifier: dist_expr;`
- Effect tracking at type level (not enforced at runtime yet)
