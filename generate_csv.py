import pandas as pd
import numpy as np
import random

# Settings
n_rows = 10000
np.random.seed(42)

# 1. Generate User IDs
user_ids = np.arange(1, n_rows + 1)

# 2. Assign Groups (Control vs Test)
groups = np.random.choice(['Control', 'Test'], size=n_rows, p=[0.5, 0.5])

# 3. Assign Devices (Mobile, Desktop, Tablet)
devices = np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=n_rows, p=[0.6, 0.35, 0.05])

# 4. Generate Dates (Over a 30-day period)
dates = pd.date_range(start='2024-01-01', periods=30)
visit_dates = np.random.choice(dates, size=n_rows)

# 5. Simulate Conversions (Test group performs slightly better)
conversions = []
for g in groups:
    if g == 'Control':
        # 10% conversion rate
        conversions.append(1 if np.random.random() < 0.10 else 0)
    else:
        # 12.5% conversion rate (Lift)
        conversions.append(1 if np.random.random() < 0.125 else 0)

# 6. Create DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'date': visit_dates,
    'group': groups,
    'device': devices,
    'converted': conversions
})

# 7. Add some "Real World Messiness" (Duplicates)
df = pd.concat([df, df.sample(50)]) # Add 50 duplicate rows

# Save
df.to_csv('ab_test_data.csv', index=False)
print("✅ ab_test_data.csv generated successfully with 10,000+ rows.")