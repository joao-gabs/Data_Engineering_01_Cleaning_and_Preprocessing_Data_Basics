import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dirty_cafe_sales.csv"

df_cafe = pd.read_csv(DATA_PATH)
print(df_cafe)
