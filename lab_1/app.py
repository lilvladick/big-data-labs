import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Настройка стиля
sns.set_theme(style="whitegrid")


# Загрузка данных
@st.cache_data
def load_data():
    df = pd.read_csv('utils/data/optimized_sakila.csv')
    return df


df = load_data()


# Функция для получения числовых столбцов без айди
def get_numeric_columns(df):
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
    meaningful_numeric = [
        col for col in numeric_columns
        if not col.lower().endswith("_id") and col.lower() != "id"
    ]
    return meaningful_numeric


# Основной интерфейс
st.set_page_config(layout="wide", page_title="Sakila Data Analysis")

# Создание навигации
page = st.sidebar.radio("Выберите страницу", ["Одномерный анализ", "Многомерный анализ"])

if page == "Одномерный анализ":
    st.title("📊 Одномерный анализ данных")

    # Получение списка числовых столбцов
    numeric_cols = get_numeric_columns(df)

    # Выбор столбца
    selected_column = st.selectbox(
        "Выберите столбец для анализа:",
        options=numeric_cols,
        help="Выберите числовой столбец для анализа распределения"
    )

    if selected_column:
        st.subheader(f"Анализ столбца: {selected_column}")

        # Статистика
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Основная статистика")
            stats_df = df[selected_column].describe()
            st.dataframe(stats_df)

            # Дополнительная информация
            st.markdown("### ℹ️ Дополнительная информация")
            st.write(f"**Количество значений:** {df[selected_column].count()}")
            st.write(f"**Количество пропусков:** {df[selected_column].isnull().sum()}")
            st.write(f"**Уникальных значений:** {df[selected_column].nunique()}")

            # Статистика по квантилям
            st.markdown("### 📊 Квантили")
            quantiles = df[selected_column].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
            st.dataframe(quantiles)

        with col2:
            # Гистограмма
            st.markdown("### 📊 Гистограмма распределения")

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(
                data=df,
                x=selected_column,
                bins=30,
                kde=True,
                ax=ax,
                color='skyblue',
                edgecolor='black'
            )
            ax.set_xlabel(selected_column, fontsize=12, fontweight='bold')
            ax.set_ylabel('Частота', fontsize=12, fontweight='bold')
            ax.set_title(f'Распределение {selected_column}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

            # Box plot
            st.markdown("### 📦 Box Plot")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            sns.boxplot(data=df, x=selected_column, ax=ax2, color='lightgreen')
            ax2.set_xlabel(selected_column, fontsize=12, fontweight='bold')
            ax2.set_title('Box Plot распределения', fontsize=14, fontweight='bold')
            st.pyplot(fig2)

        # Анализ выбросов
        st.markdown("### ⚠️ Анализ выбросов")
        Q1 = df[selected_column].quantile(0.25)
        Q3 = df[selected_column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[selected_column] < lower_bound) | (df[selected_column] > upper_bound)]

        col3, col4 = st.columns(2)

        with col3:
            st.write(f"**Нижняя граница (Q1 - 1.5*IQR):** {lower_bound:.2f}")
            st.write(f"**Верхняя граница (Q3 + 1.5*IQR):** {upper_bound:.2f}")

        with col4:
            st.write(f"**Количество выбросов:** {len(outliers)}")
            st.write(f"**Процент выбросов:** {(len(outliers) / len(df) * 100):.2f}%")

        # Отображение выбросов
        if len(outliers) > 0:
            with st.expander("Показать выбросы"):
                st.dataframe(outliers[[selected_column]].head(20))

elif page == "Многомерный анализ":
    st.title("📈 Многомерный анализ данных")

    st.markdown("""
    ### 📖 Описание графиков

    На этой странице представлены 5 различных графиков, показывающих взаимосвязи между различными признаками в наборе данных.
    """)

    # График 1: Корреляционная матрица
    st.subheader("1️⃣ Корреляционная матрица Пирсона")
    st.markdown("""
    **Что показывает:** Матрица корреляций показывает силу линейной связи между числовыми признаками.
    - **1 или -1:** Сильная положительная/отрицательная корреляция
    - **0:** Отсутствие линейной связи
    - **Цвета:** Теплые цвета (красный) - положительная корреляция, холодные (синий) - отрицательная
    """)

    meaningful_numeric = get_numeric_columns(df)
    corr_df = df[meaningful_numeric].corr()

    fig1, ax1 = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr_df,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax1,
        square=True,
        cbar_kws={"label": "Коэффициент корреляции"}
    )
    ax1.set_title("Корреляционная матрица Пирсона", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    st.pyplot(fig1)

    # График 2: Парные графики
    st.subheader("2️⃣ Парные графики распределений")
    st.markdown("""
    **Что показывает:** Визуализация попарных отношений между выбранными признаками.
    - **Диагональ:** Распределение каждого признака (плотность)
    - **Нижний треугольник:** Диаграммы рассеяния, показывающие зависимости между парами признаков
    - **Форма облака:** Прямоугольное облако = отсутствие связи, наклонное = наличие зависимости
    """)

    features_columns = ["amount", "replacement_cost"]

    fig2, ax2 = plt.subplots(figsize=(10, 8))
    pairplot = sns.pairplot(
        df[features_columns],
        diag_kind="kde",
        corner=True,
        plot_kws={'alpha': 0.6},
        diag_kws={'fill': True}
    )
    pairplot.fig.suptitle("Парные графики распределений", y=1.02, fontsize=16, fontweight='bold')
    st.pyplot(pairplot.fig)

    # График 3: Совместный график
    st.subheader("3️⃣ Совместный график (amount vs replacement_cost)")
    st.markdown("""
    **Что показывает:** Взаимосвязь между суммой платежа и стоимостью замены.
    - **Гексагональная сетка:** Показывает плотность точек
    - **Цвета:** Чем темнее/насыщеннее цвет, тем больше точек в данной области
    - **Отсутствие наклона:** Слабая или отсутствующая корреляция между признаками
    """)

    fig3, ax3 = plt.subplots(figsize=(10, 8))
    jointplot = sns.jointplot(
        data=df,
        x="amount",
        y="replacement_cost",
        kind="hex",
        height=8,
        ratio=4,
        marginal_kws={'fill': True}
    )
    jointplot.ax_joint.set_xlabel('Сумма платежа ($)', fontsize=12, fontweight='bold')
    jointplot.ax_joint.set_ylabel('Стоимость замены ($)', fontsize=12, fontweight='bold')
    jointplot.fig.suptitle('Совместное распределение', y=1.02, fontsize=16, fontweight='bold')
    st.pyplot(jointplot.fig)

    # График 4: Группированная столбчатая диаграмма
    st.subheader("4️⃣ Средний доход по жанрам с разбивкой по рейтингу")
    st.markdown("""
    **Что показывает:** Сравнение среднего дохода для разных жанров фильмов с учетом возрастного рейтинга.
    - **Ось X:** Жанры фильмов
    - **Ось Y:** Средний доход в долларах
    - **Цвета:** Разные возрастные рейтинги (MPAA)
    - **Высота столбцов:** Средний доход для конкретного жанра и рейтинга
    """)

    pivot_data = df.groupby(['category', 'rating'])['amount'].mean().reset_index()

    fig4, ax4 = plt.subplots(figsize=(16, 8))
    sns.barplot(
        data=pivot_data,
        x='category',
        y='amount',
        hue='rating',
        palette='Set2',
        ax=ax4
    )
    ax4.set_title('Средний доход по жанрам фильмов с разбивкой по возрастному рейтингу',
                  fontsize=14, fontweight='bold', pad=20)
    ax4.set_xlabel('Жанр фильма', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Средний доход ($)', fontsize=12, fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend(title='Рейтинг MPAA', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig4)

    # График 5: Диаграмма рассеяния с множественными параметрами
    st.subheader("5️⃣ Зависимость длительности фильма и стоимости замены")
    st.markdown("""
    **Что показывает:** Многомерная визуализация с 4 параметрами одновременно.
    - **Ось X:** Длительность фильма (минуты)
    - **Ось Y:** Стоимость замены ($)
    - **Цвета:** Жанр фильма (категория)
    - **Размер точек:** Доход от проката (чем больше точка, тем выше доход)
    - **Прозрачность:** Помогает видеть перекрытия точек
    """)

    top_categories = df['category'].value_counts().nlargest(5).index
    filtered_df = df[df['category'].isin(top_categories)]

    fig5, ax5 = plt.subplots(figsize=(14, 10))
    scatter = sns.scatterplot(
        data=filtered_df,
        x='length',
        y='replacement_cost',
        hue='category',
        size='amount',
        sizes=(40, 200),
        alpha=0.6,
        palette='tab10',
        ax=ax5
    )
    ax5.set_title('Зависимость длительности фильма и стоимости замены с разбивкой по жанру',
                  fontsize=14, fontweight='bold', pad=20)
    ax5.set_xlabel('Длительность фильма (минуты)', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Стоимость замены ($)', fontsize=12, fontweight='bold')
    ax5.legend(title='Жанр', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax5.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig5)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Информация")
st.sidebar.markdown(f"**Всего записей:** {len(df)}")
st.sidebar.markdown(f"**Числовых столбцов:** {len(get_numeric_columns(df))}")