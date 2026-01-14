import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score
from sklearn.utils import resample

df = pd.read_csv(r"C:\Users\erick\Downloads\ProyectoMineríaDeDatos\datasetINE_preparado.csv")
df['alta_participacion'] = np.where(df['total_lista'] > 0.75 * df['total_padron'], 1, 0)
df['tamano_padron'] = df['total_padron'].apply(lambda x: 0 if x < 10 else (1 if x < 20 else 2))
df = df[df['total_padron'] > 0]

X = df[['clave municipio', 'tamano_padron']]
y = df['alta_participacion']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

df_train = pd.concat([X_train, y_train], axis=1)
clase_mayor = df_train[df_train.alta_participacion == 1]
clase_minor = df_train[df_train.alta_participacion == 0]

clase_mayor_downsampled = resample(
    clase_mayor,
    replace=False,
    n_samples=len(clase_minor),
    random_state=42
)

df_balanced = pd.concat([clase_mayor_downsampled, clase_minor])
X_res = df_balanced[['clave municipio', 'tamano_padron']]
y_res = df_balanced['alta_participacion']

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_res, y_res)

y_pred = model.predict(X_test)

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
print(f"Precisión balanceada: {balanced_accuracy_score(y_test, y_pred):.2f}")
