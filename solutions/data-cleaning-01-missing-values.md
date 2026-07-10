# Soluzione: missing values

```python
from pathlib import Path

import pandas as pd

from memory_ai.data_cleaning import clean_memory_records, missing_summary

raw = pd.read_csv(Path("datasets/synthetic/memory_events_raw.csv"))
print(missing_summary(raw))

result = clean_memory_records(raw)
print(result.data)
print(result.report)
```

La soluzione completa eseguibile e' anche in:

- `examples/data_cleaning_missing_values.py`
- `notebooks/data-cleaning-01-missing-values.ipynb`
