# Soluzione: duplicati, tipi e outlier

```python
from pathlib import Path

import pandas as pd

from memory_ai.data_quality import clean_memory_quality_issues, duplicate_memory_mask

raw = pd.read_csv(Path("datasets/synthetic/memory_events_quality_issues.csv"))

duplicate_mask = duplicate_memory_mask(raw)
print(raw.loc[duplicate_mask])

result = clean_memory_quality_issues(raw)
print(result.data)
print(result.report)
```

Risultato atteso:

- vengono rimossi 2 duplicati;
- `"high"` viene segnalato con `importance_was_invalid_type`;
- `1.70` viene portato a `1.0`;
- `-0.20` viene portato a `0.0`;
- il report registra tutte le decisioni.

La soluzione completa eseguibile e' anche in:

- `examples/duplicates_types_outliers.py`
- `notebooks/duplicates-types-outliers.ipynb`
