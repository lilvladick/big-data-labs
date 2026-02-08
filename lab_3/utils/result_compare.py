import pandas as pd


def compare_results(results: dict) -> pd.DataFrame:
    comparison_df = pd.DataFrame({
        'Модель': list(results.keys()),
        'Accuracy': [f"{v['accuracy']:.3f}" for v in results.values()],
        'Precision': [f"{v['precision']:.3f}" for v in results.values()],
        'Recall': [f"{v['recall']:.3f}" for v in results.values()],
        'F1-score': [f"{v['f1']:.3f}" for v in results.values()],
        'ROC-AUC': [f"{v['roc_auc']:.3f}" for v in results.values()]
    })

    return comparison_df