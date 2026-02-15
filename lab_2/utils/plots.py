import matplotlib.pyplot as plt
import seaborn as sns

def plot_hypothesis_one(df):
    sns.boxplot(data=df, x='country_grouped', y='amount')
    plt.title('Выручка: США vs другие страны')
    plt.xlabel('Страна')
    plt.ylabel('Выручка')
    plt.show()

def plot_hypothesis_two(df):
    sns.boxplot(data=df, x='rating', y='amount')
    plt.title('Выручка в зависимости от рейтинга')
    plt.xlabel('Рейтинг')
    plt.ylabel('Выручка')
    plt.show()


def plot_hypothesis_three(df):
    df['group'] = 'Другие'
    df.loc[df['length'] < 90, 'group'] = 'Короткие (<90 мин)'
    df.loc[df['length'] > 120, 'group'] = 'Длинные (>120 мин)'

    df_plot = df[df['group'] != 'Другие']

    sns.boxplot(data=df_plot, x='group', y='film_popularity')

    plt.ylabel('Прокаты')
    plt.xlabel('Группа по длине')

    plt.tight_layout()
    plt.show()