import pandas as pd
from scipy import stats

# todo: сделать подтвержающуюся гипотезу

def hypothesis_one(df: pd.DataFrame) -> dict:
    # думаем что омерекенцы несут больше шекелей чем другие страны
    if 'country' not in df.columns or 'amount' not in df.columns:
        return {'error': "No 'country' or 'amount' column in dataframe"}

    usa = df[df['country'] == 'United States']['amount'].dropna()
    other = df[df['country'] != 'United States']['amount'].dropna()

    if len(usa) < 3 or len(other) < 3:
        return {'error': 'Not enough data for hypothesis_one'}

    sample_usa = usa.sample(min(5000, len(usa)), random_state=42)
    sample_other = other.sample(min(5000, len(other)), random_state=42)

    _, p_usa = stats.shapiro(sample_usa) # тест на нормальность
    _, p_other = stats.shapiro(sample_other) # p_val - вероятность получить такие же или более экстремальные данные, если нулевая гипотеза H0 верна

    if p_usa > 0.05 and p_other > 0.05:
        stat, p_val = stats.ttest_ind(usa, other, equal_var=False)
        test_name = "Welch's t-test" # непрааметрический тест проверящий распределение по группам -
        # у меня омэрэка и дрпугие страны и если p_val мелкий, то группы различны и наоборот
    else:
        stat, p_val = stats.mannwhitneyu(usa, other, alternative='two-sided')
        test_name = "Mann-Whitney U test" # сравнивает срадение значения двух групп

    alpha = 0.05 # порог при котором можно допустить ошибку (тут типа 5 из 100 случаев)
    # h0 - нулевая гипотеза
    if p_val < alpha:
        conclusion = (
            f"Отклоняем H0 (p={p_val:.4f}). Выручка клиентов из США отличается "
            f"(медиана USA=${usa.median():.2f} vs Others=${other.median():.2f})."
        )
    else:
        conclusion = f"Не отклоняем H0 (p={p_val:.4f}). Различий в выручке нет."

    return {'test': test_name, 'p_value': float(p_val), 'conclusion': conclusion, 'p_shapiro_usa': float(p_usa), 'p_shapiro_other': float(p_other)}


def hypothesis_two(df: pd.DataFrame) -> dict:
    # влияние рейтинга на выручку
    if 'rating' not in df.columns or 'amount' not in df.columns:
        return {'error': "No 'rating' or 'amount' column in dataframe"}

    groups = [group['amount'].dropna() for name, group in df.groupby('rating')]
    if any(len(g) < 3 for g in groups):
        return {'error': 'Not enough data in one of the rating groups'}

    normality_flags = []
    for g in groups:
        sample_size = min(500, len(g))
        try:
            _, p = stats.shapiro(g.sample(sample_size, random_state=42))
            normality_flags.append(p > 0.05)
        except Exception as e:
            normality_flags.append(False)

    if all(normality_flags):
        stat, p_val = stats.f_oneway(*groups) # h0 - amount везде одинаковы а h1 - хотя бы где-то разные значения
        test_name = "ANOVA" # anova как раз это и смотрит
    else:
        # крускал все хавает без нормализации
        stat, p_val = stats.kruskal(*groups) # h0 - распределение по группам одинаковые, h1 - одно из распределений отличается
        test_name = "Kruskal-Wallis" # как anova но когда групп больше

    alpha = 0.05
    if p_val < alpha:
        medians = {name: group['amount'].median() for name, group in df.groupby('rating')}
        conclusion = f"Отклоняем H0 (p={p_val:.4f}). Рейтинги влияют на выручку. Медианы: {medians}"
    else:
        conclusion = f"Не отклоняем H0 (p={p_val:.4f}). Рейтинги не влияют."

    return {'test': test_name, 'p_value': float(p_val), 'conclusion': conclusion, 'normality_flags': normality_flags}


def hypothesis_three(df: pd.DataFrame) -> dict:
    # длинные фильмы чаще берут чем короткие
    if 'length' not in df.columns or 'film_popularity' not in df.columns:
        return {'error': "Требуются колонки 'length' и 'rental_count' (сгенерируй через GROUP BY)"}

    short = df[df['length'] < 90]['film_popularity'].dropna()
    long = df[df['length'] > 120]['film_popularity'].dropna()

    if len(short) < 3 or len(long) < 3:
        return {'error': 'Недостаточно данных по группам фильмов'}

    sample_short = short.sample(min(500, len(short)), random_state=42)
    sample_long = long.sample(min(500, len(long)), random_state=42)

    _, p_short = stats.shapiro(sample_short)
    _, p_long = stats.shapiro(sample_long)

    # Выбираем тест
    if p_short > 0.05 and p_long > 0.05:
        stat, p_val = stats.ttest_ind(short, long, equal_var=False)
        test_name = "Welch's t-test"
    else:
        stat, p_val = stats.mannwhitneyu(short, long, alternative='two-sided')
        test_name = "Mann-Whitney U test"

    alpha = 0.05
    if p_val < alpha:
        conclusion = (
            f"Отклоняем H0 (p={p_val:.4f}). Длина фильма влияет на популярность. "
            f"Длинные: {long.median():.1f}, Короткие: {short.median():.1f} прокатов"
        )
    else:
        conclusion = (
            f"Не отклоняем H0 (p={p_val:.4f}). Длина фильма не влияет на популярность. "
            f"Медианы близки: {short.median():.1f}, {long.median():.1f}"
        )

    return {'test': test_name, 'p_value': float(p_val), 'conclusion': conclusion,}