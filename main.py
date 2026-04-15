import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read new dataset
df = pd.read_csv("AmazonBestsellersAnalysis/BestsellingBooks2025.csv", encoding="cp1252")

print(df.head())
print(df.shape)
print(df.columns)
print(df.describe(include="all"))

# drop duplicates
df.drop_duplicates(inplace=True)

# rename columns to match old dataset logic
df.rename(columns={"Book name": "Title", "reviews count": "Reviews", "price": "Price"}, inplace=True)

# clean Rating: "4.6 out of 5 stars" -> 4.6
df["Rating"] = df["Rating"].astype(str).str.extract(r"(\d+\.\d+|\d+)")[0].astype(float)

# clean Price: "$9.33" -> 9.33
df["Price"] = df["Price"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# extract year from Publishing date
df["Publication Year"] = pd.to_datetime(df["Publishing date"], errors="coerce").dt.year

# keep same old fiction/non-fiction style behavior
df["Genre Group"] = df["Genre"].astype(str).apply(lambda x: "Fiction" if "fiction" in x.lower() else "Non Fiction")

# analyzing author popularity and plotting bar chart of top 10 authors
author_counts = df["Author"].value_counts()
print(author_counts)

plt.figure(figsize=(12, 6))
sns.barplot(x=author_counts.head(10).values, y=author_counts.head(10).index)
plt.title("Top 10 Authors by Bestseller Appearances")
plt.tight_layout()
plt.savefig("AmazonBestsellersAnalysis/visuals/top_authors.png")
plt.close()

# determining average rating per genre and plotting histogram of rating distribution
avg_rating_by_genre = df.groupby("Genre")["Rating"].mean()
print(avg_rating_by_genre)

plt.figure(figsize=(10, 5))
sns.histplot(df["Rating"].dropna(), bins=20, kde=True)
plt.title("Distribution of User Ratings")
plt.tight_layout()
plt.savefig("AmazonBestsellersAnalysis/visuals/rating_distributions.png")
plt.close()

# exporting top selling authors to a CSV file
author_counts.head(10).to_csv("top_authors.csv")

# exporting average rating per genre to a CSV file
avg_rating_by_genre.to_csv("avg_rating_by_genre.csv")

# plotting price vs rating by genre
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Price", y="Rating", hue="Genre")
plt.title("Price vs. Rating by Genre")
plt.tight_layout()
plt.savefig("AmazonBestsellersAnalysis/visuals/price_vs_rating.png")
plt.close()

# plotting fiction vs non-fiction over the years
genre_year = df.groupby(["Publication Year", "Genre Group"]).size().unstack(fill_value=0)
genre_year.plot(kind="bar", figsize=(12, 6))
plt.title("Fiction vs. Non-Fiction Over the Years")
plt.tight_layout()
plt.savefig("AmazonBestsellersAnalysis/visuals/genre_trends.png")
plt.close()