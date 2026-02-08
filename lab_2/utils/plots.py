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
