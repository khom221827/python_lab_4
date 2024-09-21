import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

age_labels = ["до 18", "18-45", "45-70", "старше 70"]

class EmployeeAnalyzer:
    def __init__(self, csv_filename):
        try:
            self.data = pd.read_csv(csv_filename)
            print("Ok: Файл CSV успішно завантажено.")
        except FileNotFoundError:
            print("Помилка: Файл CSV не знайдено.")
            exit(1)
        except Exception as e:
            print(f"Помилка: {e}. Неможливо відкрити файл CSV.")
            exit(1)

    def calculate_age(self, birth_date):
        birth_date = datetime.strptime(birth_date, '%Y.%m.%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def add_age_column(self):
        self.data['Вік'] = self.data['Дата народження'].apply(self.calculate_age)

    def plot_gender_distribution(self):
        gender_counts = self.data['Стать'].value_counts()

        sns.set_style("whitegrid")
        plt.figure(figsize=(8, 6))
        sns.barplot(x=gender_counts.index, y=gender_counts.values, palette="pastel")
        plt.title("Розподіл співробітників за статтю")
        plt.xlabel("Стать")
        plt.ylabel("Кількість")
        plt.show()

    def plot_age_category_distribution(self):
        bins = [0, 18, 45, 70, 80]

        self.data['Вікова категорія'] = pd.cut(self.data['Вік'], bins=bins, labels=age_labels)

        age_category_counts = self.data['Вікова категорія'].value_counts()

        plt.figure(figsize=(8, 6))
        sns.barplot(x=age_category_counts.index, y=age_category_counts.values, palette="pastel")
        plt.title("Розподіл співробітників за віковими категоріями")
        plt.xlabel("Вікова категорія")
        plt.ylabel("Кількість")
        plt.show()

    def plot_gender_age_distribution(self):
        gender_age_counts = self.data.groupby(['Вікова категорія', 'Стать']).size().unstack(fill_value=0)

        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        colors = ['#ff9999', '#66b3ff']

        for i, age_category in enumerate(age_labels):
            ax = axes[i // 2, i % 2]
            ax.pie(gender_age_counts.loc[age_category], labels=gender_age_counts.columns, colors=colors,
                   autopct='%1.1f%%', startangle=140, pctdistance=0.85, textprops={'fontsize': 12})
            ax.set_title(f"Вікова категорія: {age_category}", fontsize=14)

        plt.tight_layout()
        plt.show()

def main():
    analyzer = EmployeeAnalyzer('employees.csv')
    analyzer.add_age_column()
    analyzer.plot_gender_distribution()
    analyzer.plot_age_category_distribution()
    analyzer.plot_gender_age_distribution()

if __name__ == "__main__":
    main()
