import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import seaborn as sns


data_file = "data/satis_verisi.xlsx"
if not os.path.exists(data_file):
    os.makedirs("data", exist_ok=True)
    tarihler = pd.date_range(start="2023-01-01", end="2024-12-31")
    np.random.seed(42)
    satis = np.random.poisson(lam=20, size=len(tarihler)) + np.sin(np.linspace(0, 30, len(tarihler))) * 5
    df = pd.DataFrame({"Tarih": tarihler, "Satış": np.round(satis).astype(int)})
    df.to_excel(data_file, index=False)
else:
    df = pd.read_excel(data_file)


df["Tarih"] = pd.to_datetime(df["Tarih"])
df.set_index("Tarih", inplace=True)
df["7G_Hareketli"] = df["Satış"].rolling(window=7).mean()
df["30G_Hareketli"] = df["Satış"].rolling(window=30).mean()
aylik = df["Satış"].resample("ME").sum()



sns.set_theme(style="darkgrid")  
  # veya listedeki herhangi biri
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle(" Satış Verisi Gelişmiş Zaman Serisi Analizi", fontsize=16, fontweight='bold')

# Grafik 1: Günlük ve hareketli ortalama
axes[0, 0].plot(df.index, df["Satış"], label="Günlük Satış", alpha=0.4)
axes[0, 0].plot(df.index, df["7G_Hareketli"], label="7 Günlük Ortalama", color="blue")
axes[0, 0].plot(df.index, df["30G_Hareketli"], label="30 Günlük Ortalama", color="red", linestyle="--")
axes[0, 0].set_title("Günlük Satış ve Hareketli Ortalamalar")
axes[0, 0].legend()
axes[0, 0].grid(True)

#  Grafik 2: Aylık toplamlar
axes[0, 1].bar(aylik.index.strftime("%Y-%m"), aylik.values, color="teal")
axes[0, 1].set_title("Aylık Toplam Satışlar")
axes[0, 1].tick_params(axis='x', rotation=45)

#  Grafik 3: Yıl içi trend
df["Ay"] = df.index.month
df["Yıl"] = df.index.year
pivot = df.pivot_table(index="Ay", columns="Yıl", values="Satış", aggfunc="mean")
pivot.plot(ax=axes[1, 0], marker="o")
axes[1, 0].set_title("Yıllara Göre Aylık Ortalama Satışlar")
axes[1, 0].set_xticks(range(1, 13))
axes[1, 0].set_xticklabels(["Ocak", "Şub", "Mart", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"], rotation=45)

#  Grafik 4: Boxplot (Dağılım Analizi)
df.boxplot(column="Satış", by="Ay", ax=axes[1, 1])
axes[1, 1].set_title("Aylara Göre Satış Dağılımı")
axes[1, 1].set_xlabel("Ay")
axes[1, 1].set_ylabel("Satış")
axes[1, 1].set_xticklabels(["Ocak", "Şub", "Mart", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"], rotation=45)
fig.subplots_adjust(hspace=0.4, wspace=0.3)

#  Kayıt
os.makedirs("grafikler", exist_ok=True)
plt.savefig("grafikler/tum_rapor.png", dpi=300)
plt.show()
