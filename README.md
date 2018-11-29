# python_examples
File with simple examples of most common use cases for:
- unittest
- pytypes
- pydantic
- typing
- enum
- cython
- importing structure (TODO: Add in Bens solution)

# Python File Checklist
- test using *unittest TestCase*
- file is typechecked using *pytypes @typechecked*
- *pydantic BaseModel* when using *json*
- *pydantic @validator* used when validation on top of type checking is required
- Use *Enum* when the type would be an invalid Union like  *Union['left', 'right', 'center']*

# NOTES:
Running python in optimized mode disables @typechecked
```
python -O
```
You can run the **unittest** using
```
python examples/simple.py --unittest
```
Having this flag allows the python file to be called by other processes without running the unittest every time.
