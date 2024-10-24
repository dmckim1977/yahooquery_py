# yahooquery_py

Very simple wrapper around yahooquery

Version: `v.0.2.0`

## Installation

```python
pip install git+https://github.com/dmckim1977/yahooquery_py.git@{version}
```

Via requirements

```text
yahooquery_py @ git+https://github.com/dmckim1977/yahooquery_py.git@{version}
```

Examples:

```python
import yahooquery_py

c = daily_close("ES", "2024-10-01")
print(type(c), c)

# output
>>><class 'float'> 5759.75
```
# TODO add polygon examples
