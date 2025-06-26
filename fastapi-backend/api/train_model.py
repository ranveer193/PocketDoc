import pandas as pd, joblib, numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from xgboost import XGBClassifier
from .features import SYMPTOMS

ROOT   = Path(__file__).resolve().parents[2]
DATA   = ROOT / "dataset" / "Dataset.csv"          # <= replace with real CSV
OUTDIR = ROOT / "models"
OUTDIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
X  = df[SYMPTOMS]
y  = df["prognosis"]

enc  = LabelEncoder().fit(y)
yenc = enc.transform(y)

xgb  = XGBClassifier(
    objective="multi:softprob",
    eval_metric="mlogloss",
    num_class=len(enc.classes_),
    n_estimators=600,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
)
param = {
    "max_depth":        [3,4,5,6],
    "min_child_weight": [1,2,3],
    "gamma":            [0,0.1,0.2],
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = RandomizedSearchCV(
    xgb, param, n_iter=12, cv=cv, scoring="accuracy",
    n_jobs=-1, random_state=42
).fit(X, yenc)

model = search.best_estimator_
print("✅ CV accuracy ≈", round(search.best_score_,3))

joblib.dump(model, OUTDIR / "model.joblib")
joblib.dump(enc,   OUTDIR / "label_encoder.joblib")
np.save(OUTDIR / "feat_imp.npy", model.feature_importances_)
print("✅ Saved artefacts in /models")
