import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_name = "world_bank_data.csv"

try:
  if not os.path.exists(file_name):
    raise FileNotFoundError(f"Файл '{file_name}' не знайдено в директорії.")

  # Пропускаємо перші 4 службові рядки, а 5-й робимо заголовком
  df = pd.read_csv(file_name, skiprows=4, low_memory=False)

  # Очищуємо назви стовпчиків від зайвих пробілів
  df.columns = df.columns.str.strip()

  print("Файл успішно завантажено та оброблено!")
except Exception as e:
  print(f"Помилка під час читання файлу: {e}")
  exit()

target_indicator = "Life expectancy at birth, total (years)"

# Фільтруємо за обраним показником
df_indicator = df[df["Indicator Name"] == target_indicator]

if df_indicator.empty:
  print(f"Попередження: Показник '{target_indicator}' не знайдено у файлі.")
  exit()

# Визначаємо список років (усі стовпці, які є числами)
year_columns = [col for col in df.columns if str(col).strip().isdigit()]
years = np.array([int(y) for y in year_columns])

# Беремо період з 2000 по 2022 рік для зручності
mask = (years >= 2000) & (years <= 2022)
filtered_years = years[mask]


# Допоміжна функція для отримання числових даних країни за роками
def get_country_values(c_name):
  res = df_indicator[df_indicator["Country Name"] == c_name]
  if res.empty:
    return None
  return res[year_columns].values.flatten().astype(float)[mask]

print("\nЕТАП 1: Лінійний графік динаміки")
country1 = input(
    "Введіть назву першої країни: "
).strip()
country2 = input(
    "Введіть назву другої країни: "
).strip()

vals1 = get_country_values(country1)
vals2 = get_country_values(country2)

if vals1 is None or vals2 is None:
  print(
      "Помилка: Одну або обидві країни не знайдено у даних. Перевірте написання"
      " (англійською)."
  )
else:
  plt.figure(figsize=(9, 5))
  plt.plot(filtered_years, vals1, label=country1, linewidth=2)
  plt.plot(filtered_years, vals2, label=country2, linewidth=2)
  plt.title(f"Динаміка: {target_indicator}", fontsize=13)
  plt.xlabel("Рік", fontsize=12)
  plt.ylabel("Значення показника", fontsize=12)
  plt.legend()
  plt.grid(True)
  plt.show()

print("\nЕТАП 2: Стовпчаста діаграма")
user_country_bar = input(
    "Введіть назву країни для стовпчастої діаграми: "
).strip()

bar_values = get_country_values(user_country_bar)

if bar_values is None:
  print(f"Помилка: Країну '{user_country_bar}' не знайдено у даних.")
else:
  x = np.arange(len(filtered_years))
  width = 0.5

  plt.figure(figsize=(10, 5))
  plt.bar(x, bar_values, width, label=user_country_bar)
  plt.title(f"Показник за роками для: {user_country_bar}", fontsize=14)
  plt.xlabel("Рік", fontsize=12)
  plt.ylabel("Значення показника", fontsize=12)
  plt.xticks(x, filtered_years, rotation=45)
  plt.legend()
  plt.grid(True, axis="y")
  plt.tight_layout()
  plt.show()

print("\nЕТАП 3: Кругова діаграма порівняння")
pie_country1 = input(
    "Введіть першу країну для кругової діаграми: "
).strip()
pie_country2 = input(
    "Введіть другу країну для кругової діаграми: "
).strip()
print(f"Доступні роки: від {filtered_years[0]} до {filtered_years[-1]}")
user_year_input = input("Введіть рік для порівняння(2000-2022): ").strip()

try:
  user_year = int(user_year_input)
  if user_year not in filtered_years:
    raise ValueError("Введеного року немає в діапазоні спостережень.")

  # Знаходимо індекс року у повному масиві років
  full_year_idx = list(years).index(user_year)

  raw_vals1 = df_indicator[df_indicator["Country Name"] == pie_country1][
      year_columns
  ]
  raw_vals2 = df_indicator[df_indicator["Country Name"] == pie_country2][
      year_columns
  ]

  if raw_vals1.empty or raw_vals2.empty:
    print("Помилка: Одну з обраних країн не знайдено у базі даних.")
  else:
    val1 = float(raw_vals1.values.flatten()[full_year_idx])
    val2 = float(raw_vals2.values.flatten()[full_year_idx])

    pie_data = np.array([val1, val2])
    pie_labels = np.array([pie_country1, pie_country2])


    def pie_format(pct, allvals):
      absolute = np.round(pct / 100 * np.sum(allvals), 2)
      return f"{pct:.1f}%\n({absolute})"


    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        pie_data,
        labels=pie_labels,
        autopct=lambda pct: pie_format(pct, pie_data),
        startangle=140,
    )
    plt.title(
        f"Порівняння ({pie_country1} та {pie_country2}) за {user_year} рік",
        fontsize=14,
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.show()

except ValueError as ve:
  print(f"Помилка вводу: {ve}")
except Exception as e:
  print(f"Сталася помилка при побудові кругової діаграми: {e}")