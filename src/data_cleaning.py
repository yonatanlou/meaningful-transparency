import re

import numpy as np
import pandas as pd

from constants import DATA_DIR

# Text processing constants
TEXT_COL = "Text"
URL_RE = re.compile(r"(https?://\S+?)(?=\s|$)", flags=re.IGNORECASE)
URL_EXTERNAL = re.compile(r"(https://t.co/.*\s via)", flags=re.IGNORECASE)
MENTION_RE = re.compile(r"(^|\s)@\w+")
HASHTAG_RE = re.compile(r"(^|\s)#\w+")
SPACE_RE = re.compile(r"\s+")
VIA_RE = re.compile(r"\bvia\b", flags=re.IGNORECASE)

# Filtering parameters
MIN_CLEAN_TEXT_LENGTH = 10
MAX_MENTIONS_IN_TEXT = 1
MAX_NO_TEXT_RATIO = 0.85


def strip_urls(s: str) -> str:
    """Remove URLs from text."""
    return URL_RE.sub(" ", s)


def strip_mentions(s: str) -> str:
    """Remove @mentions from text."""
    return MENTION_RE.sub(" ", s)


def number_of_mentions(s: str) -> int:
    """Count @mentions in text."""
    return len(MENTION_RE.findall(s))


def strip_hashtags(s: str) -> str:
    """Remove #hashtags from text."""
    return HASHTAG_RE.sub(" ", s)


def normalize_space(s: str) -> str:
    """Normalize whitespace."""
    return SPACE_RE.sub(" ", s).strip()


def core_text(s: str) -> str:
    """Extract core text by removing URLs, mentions, and hashtags."""
    s = strip_urls(s)
    s = strip_mentions(s)
    s = strip_hashtags(s)
    return normalize_space(s)


def count_hashtags(s: str) -> int:
    """Count hashtags in text."""
    return len(HASHTAG_RE.findall(s))


def count_words(s: str) -> int:
    """Count words in text."""
    s = normalize_space(s)
    return 0 if not s else len(s.split())


def url_via_flags(s: str) -> tuple[bool, bool]:
    """Return (non_twitter_url, twitter_url) flags.

    non_twitter_url => there is a URL and a 'via' occurs AFTER a URL
    twitter_url     => there is a URL and there is NO 'via' after any URL
    """
    if not s:
        return (False, False)
    has_url = False
    via_after_any_url = False

    for m in URL_RE.finditer(s):
        has_url = True

    if URL_EXTERNAL.findall(s):
        via_after_any_url = True

    if not has_url:
        return (False, False)
    if via_after_any_url:
        return (True, False)
    else:
        return (False, True)


def add_filter_flags(df: pd.DataFrame, text_col: str = TEXT_COL) -> pd.DataFrame:
    """Add filtering flags to the dataframe."""
    out = df.copy()
    txt = out[text_col].fillna("").astype(str)

    # Precompute helpers
    txt_no_urls = txt.map(strip_urls).map(normalize_space)
    txt_core = txt.map(core_text)
    total_tokens = txt.map(count_words)
    core_tokens = txt_core.map(count_words)
    hashtag_counts = txt.map(count_hashtags)

    # Add flags and counts
    out["n_words"] = total_tokens
    out["n_words_no_urls_mentions_hashtags"] = core_tokens.astype(int)
    out["extracted_urls"] = txt.map(lambda s: URL_RE.findall(s))
    out["flag_link_only"] = txt_no_urls.str.len().eq(0) | core_tokens.le(2)
    out["flag_starts_with_mention"] = txt.str.match(r"^\s*@\w+")
    out["n_mentions_in_text"] = txt.map(number_of_mentions)
    out["n_hashtags_in_text"] = hashtag_counts
    out["n_urls_in_text"] = txt.map(lambda s: len(URL_RE.findall(s)))
    out["no_text_ratio"] = (
        out["n_mentions_in_text"] + out["n_hashtags_in_text"] + out["n_urls_in_text"]
    ) / (
        core_tokens
        + out["n_mentions_in_text"]
        + out["n_hashtags_in_text"]
        + out["n_urls_in_text"]
    )
    out["flag_empty_after_cleanup"] = txt_core.str.len().eq(0)

    # URL flags
    non_twitter, twitter = zip(*txt.map(url_via_flags))
    out["flag_non_twitter_url"] = np.array(non_twitter, dtype=bool)
    out["flag_twitter_url"] = np.array(twitter, dtype=bool)

    # Add core text for inspection
    out["Text_core"] = txt_core
    return out


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all filtering rules to the dataframe."""
    # Apply filtering rules
    len_ok = df["n_words_no_urls_mentions_hashtags"] > MIN_CLEAN_TEXT_LENGTH
    not_url_only = ~df["flag_link_only"]
    not_empty_after = ~df["flag_empty_after_cleanup"]
    mentions_ok = df["n_mentions_in_text"] <= MAX_MENTIONS_IN_TEXT
    noise_ratio_ok = df["no_text_ratio"] <= MAX_NO_TEXT_RATIO
    no_non_twitter_url = ~df["flag_non_twitter_url"]
    no_twitter_url = ~df["flag_twitter_url"]

    # Combine all rules
    row_is_valid = (
        len_ok
        & not_url_only
        & not_empty_after
        & mentions_ok
        & noise_ratio_ok
        & no_non_twitter_url
        & no_twitter_url
    )

    # Apply filter
    filtered = df.loc[row_is_valid].copy()

    return filtered


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """Load and clean the Twitter dataset."""
    # Load data
    df = pd.read_csv(csv_path)

    # Convert date and add year
    df["CreateDate"] = pd.to_datetime(df["CreateDate"], errors="coerce")
    df["Year"] = df["CreateDate"].dt.year

    print(f"Loaded {len(df)} rows from {csv_path}")

    # Add filter flags
    df_flags = add_filter_flags(df, TEXT_COL)

    # Apply filters
    filtered = apply_filters(df_flags)

    print(f"After filtering: {len(filtered)} rows ({len(df) - len(filtered)} removed)")
    print("Bias distribution after filtering:")
    print(filtered["Biased"].value_counts(dropna=False))

    return filtered


def split_train_test(
    df: pd.DataFrame, train_years: list, test_years: list
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into train and test sets by year."""
    train_data = df[df["Year"].isin(train_years)].copy()
    test_data = df[df["Year"].isin(test_years)].copy()

    print(f"\nTrain set: {len(train_data)} rows (years: {train_years})")
    print("Train bias distribution:")
    print(train_data["Biased"].value_counts(dropna=False))

    print(f"\nTest set: {len(test_data)} rows (years: {test_years})")
    print("Test bias distribution:")
    print(test_data["Biased"].value_counts(dropna=False))

    return train_data, test_data


def main():
    """Main function to clean data and create train/test splits."""
    # Paths
    input_csv = DATA_DIR / "GoldStandard2024.csv"
    output_dir = DATA_DIR / "train_test_datasets"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Load and clean data
    cleaned_data = load_and_clean_data(str(input_csv))

    # Split by years: train (2019-2021), test (2022-2023)
    train_years = [2019, 2020]
    test_years = [2021, 2022, 2023]

    train_data, test_data = split_train_test(cleaned_data, train_years, test_years)

    # Save datasets
    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"

    train_data.to_csv(train_path, index=False)
    test_data.to_csv(test_path, index=False)

    print(f"\nSaved train data to: {train_path}")
    print(f"Saved test data to: {test_path}")

    # Display year distribution
    print("\nYear distribution by dataset:")
    year_dist = (
        cleaned_data.groupby("Year")["Biased"].value_counts().reset_index(name="count")
    )
    year_dist = (
        year_dist.pivot(index="Year", columns="Biased", values="count")
        .fillna(0)
        .astype(int)
    )
    year_dist.columns = ["Not antisemitic", "Antisemitic"]
    print(year_dist)


if __name__ == "__main__":
    main()
