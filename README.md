# yahooquery_py

Very simple wrapper around yahooquery

## Installation

```python
pip install git + https://github.com/dmckim1977/yahooquery_py.git@v0.1.1
```

Via requirements

```text
yahooquery_py @ git+https://github.com/dmckim1977/yahooquery_py.git@v0.1.1
```

Examples:

```python
import yahooquery_py

c = daily_close("ES", "2024-10-01")
print(type(c), c)

# output
>>><class 'float'> 5759.75
```

