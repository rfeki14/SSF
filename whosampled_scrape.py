import requests
from bs4 import BeautifulSoup
from typing import Optional


def get_samples(song_name: str) -> Optional[list]:
    """
    Get a list of samples used in a song by scraping the whosampled website.

    :param song_name: The name of the song to find samples for.
    :return: A list of samples used in the song, or None if no samples were found.
    """
    # Search for the song on whosampled
    search_url = f"https://www.whosampled.com/search/songs/{song_name}/"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first search result
    search_results = soup.find_all("article", class_="search-result")
    if not search_results:
        return None
    search_result = search_results[0]

    # Get the song URL from the search result
    song_url = search_result.find("a")["href"]

    # Scrape the song page for samples
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the sample entries
    sample_entries = soup.find_all("div", class_="sample-entry")
    samples = []
    for sample_entry in sample_entries:
        # Get the sample name and artist
        sample_name = sample_entry.find("h3", class_="title").text.strip()
        sample_artist = sample_entry.find("span", class_="artist").text.strip()

        # Add the sample to the list
        samples.append({
            "title": sample_name,
            "artist": sample_artist
        })

    return samples

def who_sampled(song):
    # Get the samples used in the song
    samples = get_samples(song['name'])
    if samples is None:
        print("No samples found for this song.")
    else:
        print("Samples used in this song:")
        for sample in samples:
            print(f"{sample['title']} by {sample['artist']}")
