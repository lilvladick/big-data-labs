from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, \
    classification_report
from sklearn.neighbors import KNeighborsClassifier


def train_models(x_train, y_train, x_test, y_test, target_1: str, target_2: str) -> dict:
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'KNN (k=5)': KNeighborsClassifier(n_neighbors=5)
    }
    results = {}

    for name, model in models.items():
        print(f"модель: {name} \n")

        if 'KNN' in name:
            model.fit(x_train, y_train)  # KNN требует нормализованные данные
            y_pred = model.predict(x_test)
            y_proba = model.predict_proba(x_test)[:, 1]
        else:
            model.fit(x_train, y_train)  # Лог. регрессия работает и без нормализации
            y_pred = model.predict(x_test)
            y_proba = model.predict_proba(x_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc = roc_auc_score(y_test, y_proba)
        cm = confusion_matrix(y_test, y_pred)

        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'roc_auc': roc,
            'confusion_matrix': cm,
            'y_proba': y_proba
        }

        print(f"Accuracy: {acc:.3f}")
        print(f"Precision: {prec:.3f}")
        print(f"Recall: {rec:.3f}")
        print(f"F1-score: {f1:.3f}")
        print(f"ROC-AUC: {roc:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=[target_1, target_2]))

        plt.figure(figsize=(4, 3.5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=[target_1, target_2],
                    yticklabels=[target_1, target_2])
        plt.title(f'Confusion Matrix: {name}')
        plt.ylabel('Истинный класс')
        plt.xlabel('Предсказанный класс')
        plt.tight_layout()
        plt.show()

    return results
