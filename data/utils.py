import json
import glob
import pandas as pd
import os


def aggregate_data(file_list):
    """
    aggregate data from several json files
    :param file_list:
    :return:
    """
    data = {}
    for f in file_list:
        with open(f, "r") as f:
            data.update(json.load(f))

    return data


def make_tables(data, path_to_csv=None):
    """
    make tables form the aggregated data
    :param data:
    :return:
    """
    meta = {}
    written_reviews = {}
    star_reviews = {}
    key_words = {}
    for trail_id, trail_data in data.items():
        meta[trail_id] = trail_data["meta"]
        written_reviews[trail_id] = trail_data["reviews"]["written"]
        star_reviews[trail_id] = trail_data["reviews"]["ratings"]
        key_words[trail_id] = trail_data["reviews"]["key_words"]

    written_reviews = pd.DataFrame(
        [written_reviews.keys(), written_reviews.values()]
    ).transpose()
    written_reviews.columns = ["trail_id", "reviews"]
    star_reviews = pd.DataFrame(
        [star_reviews.keys(), star_reviews.values()]
    ).transpose()
    star_reviews.columns = ["trail_id", "rating"]
    key_words = pd.DataFrame([key_words.keys(), key_words.values()]).transpose()
    key_words.columns = ["trail_id", "key_words"]
    meta = pd.DataFrame.from_dict(meta).transpose().reset_index()
    meta.columns = ["trail_id", "description", "length_elev_type", "tags", "coords"]
    if path_to_csv:
        written_reviews.to_csv(os.path.join(path_to_csv, "written_reviews.csv"))
        star_reviews.to_csv(os.path.join(path_to_csv, "star_reviews.csv"))
        key_words.to_csv(os.path.join(path_to_csv, "key_words.csv"))
        meta.to_csv(os.path.join(path_to_csv, "meta_reviews.csv"))

    return written_reviews, star_reviews, key_words, meta


def plot_data(written_reviews, star_reviews, key_words):
    import seaborn as sns

    sns.set_theme()
    import matplotlib.pyplot as plt

    num_reviews = [["Written Reviews", len(j)] for j in written_reviews["reviews"]]
    num_stars = [["Star Reviews", len(j)] for j in star_reviews["rating"]]
    num_kws = [["Key Words", len(j)] for j in key_words["key_words"]]
    df = pd.DataFrame(num_reviews + num_stars + num_kws, columns=[" ", "count"])
    ax = sns.boxplot(x=" ", y="count", data=df)
    plt.show()
    return ax


if __name__ == "__main__":
    file_list = glob.glob(r"/blah/GimmeAllTheTrails/data\*.json")
    data = aggregate_data(file_list)
    csv_dir = r"/blah/GimmeAllTheTrails/data/csv"
    written_reviews, star_reviews, key_words, meta = make_tables(
        data, path_to_csv=csv_dir
    )
    plot_data(written_reviews, star_reviews, key_words)
    print(data)
