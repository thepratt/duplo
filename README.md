# duplo

Under development, not production ready.

Goals of duplo:

- Make functional programming more approachable, making use of the concepts that help with delivering value, without overloading newcomers.
- Make code safer - or at least the developer safer in writing code.
- Enhance developer understanding for how functions can fail, and what's required to run them - what may be referred to as Results/Eithers, and Reader Monads.
- Readers can grab dependencies through a late-bound IoC container.

### Results

Using plain Results:

```python
Success(1)
Error(BusinessError())
```

TOOD: comparitive example, chaining, collect/sequence
