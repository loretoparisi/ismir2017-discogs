#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas
import matplotlib.pyplot as plt

import pprint
import pickle

from config import *


# Functions for selecting data

def select_genre(data, genre):
    """Return all releases annotated with the specified genre"""
    return data[data['genres'].apply(lambda x: genre in x)]


def select_style(data, style):
    """Return all releases annotated with the specified style"""
    return data[data['styles'].apply(lambda x: style in x)]


def select_only_genre(data, genre):
    """Return all releases annotated solely with the specified genre"""
    return data[data['genres'].apply(lambda x: len(x) == 1 and genre in x)]


def select_only_style(data, style):
    """Return all releases annotated solely with the specified style"""
    return data[data['styles'].apply(lambda x: len(x) == 1 and style in x)]


def select_label(data, label):
    """Return all releases from the specified label"""
    return data[data['labels'].apply(lambda x: label in x)]


def select_artistname(data, artist):
    """Return all releases by the specified artist"""
    return data[data['artists'].apply(lambda x: artist in [a['name'] for a in x])]


def select_artistid(data, artistid):
    """Return all releases by the specified artistid"""
    return data[data['artists'].apply(lambda x: artistid in [a['id'] for a in x])]


def select_masterid(data, masterid):
    """Return all releases associated to the specified masterid"""
    return data[data['master_id'] == masterid]


def select_year(data, year):
    """Return all releases from the specified year"""
    return data[data['released'] == year]


def select_country(data, country):
    """Return all releases from the specified country"""
    return data[data['country'] == country]


def select_format(data, format):
    """Return all releases for the specified format"""
    return data[data['formats'].apply(lambda x: format in x)]


def select_tracks(data, tracks_number):
    """Return all releases with the specified number of tracks"""
    return data[data['tracks_number'] == tracks_number]


def select_unofficial(data):
    """Return all releases annotated as unofficial"""
    return data[data['unofficial'] == True]


def select_compilation(data):
    """Return all releases annotated as compilations"""
    return data[data['compilation'] == True]


def select_mixed(data):
    """Return all releases annotated as mixed"""
    return data[data['mixed'] == True]


def select_notmixed(data):
    """Return all releases not annotated as mixed"""
    return data[data['mixed'] == False]



def select(data, genre=None, style=None, format=None, year=None, country=None, tracks=None):
    """
    Return all releases from the specified genre, style, format, year, country,
    and number of tracks
    """
    selected = data
    if style:
        selected = select_style(selected, style)
        if not len(selected):
            return selected
    if genre:
        selected = select_genre(selected, genre)
        if not len(selected):
            return selected
    if format:
        selected = select_format(selected, format)
        if not len(selected):
            return selected
    if year:
        selected = select_year(selected, year)
        if not len(selected):
            return selected
    if country:
        selected = select_country(selected, country)
        if not len(selected):
            return selected
    if tracks:
        selected = select_tracks(selected, tracks)

    return selected


# Functions for unique artists analysis (TODO)
# Each unique artist is associated with a list of ids for all artist items in
# which he/she participated (TODO: get this data from the artist dump)

def select_artistids(data, artistids):
    """Return all releases matching the specified list of artistid"""
    return data[data['artists'].apply(lambda x: len(set(artistids) & set([a['id'] for a in x])) > 0)]


# Functions to gather vocabulary of genres/styles/formats/countries in data


def find_genres(data):
    """Find out all genres present in data"""
    genres = set()
    for gg in data['genres']:
        for g in gg:
            genres.add(g)
    return sorted(list(genres))


def find_styles(data):
    """Find out all styles present in data"""
    styles = set()
    for ss in data['styles']:
        for s in ss:
            styles.add(s)
    return sorted(list(styles))


def find_formats(data):
    """Find out all formats present in data"""
    formats = set()
    for ff in data['formats']:
        for f in ff:
            formats.add(f)
    return sorted(list(formats))

def find_countries(data):
    """Find out all countries present in data"""
    releases = data[pandas.notnull(data['country'])]
    countries = set()
    for c in releases['country']:
        countries.add(c)
    return sorted(list(countries))


def find_artists(data):
    """Find out all artists present in data"""
    artists = set()
    for aa in data['artists']:
        for a in aa:
            artists.add(a)
    return artists


# Functions for duration analysis


def find_durations(data):
    """Find out all track durations in data"""
    releases = data[pandas.notnull(data['tracks_duration_list'])]
    if not len(releases):
        return None
    return [d for dd in releases['tracks_duration_list'].tolist() for d in dd]


# Functions for per-year analysis


def releases_per_year(data, start_year, end_year, format=None, genre=None, style=None, country=None):
    """
    Count the number of releases from 'start_year' to 'end_year'
    from the specified format, genre, style and country
    """
    years = range(start_year, end_year+1)
    number_releases = [len(select(data, year=year, genre=genre, style=style, format=format, country=country)) for year in years]
    return years, number_releases


def artists_per_year(data, start_year, end_year, format=None, genre=None, style=None, country=None):
    """
    Count the number of artists from 'start_year' to 'end_year'
    from the specified format, genre, style and country
    """
    years = range(start_year, end_year+1)
    number_releases = [len(select(data, year=year, genre=genre, style=style, format=format, country=country)) for year in years]
    return years, number_releases
    years = range(start_year, end_year+1)
    number_artists = []
    for year in years:
        releases = select(data, year=year, genre=genre, style=style, format=format, country=country)
        artists = set()
        for aa in releases['artists']:
            for a in aa:
                artists.add(a)
        number_artists.append(len(artists))
    return years, number_artists


def tracks_per_year(data, start_year, end_year, format=None, genre=None, style=None, country=None):
    """
    Count the number of tracks from 'start_year' to 'end_year'
    from the specified format, genre, style and country
    """
    years = range(start_year, end_year+1)
    number_releases = [len(select(data, year=year, genre=genre, style=style, format=format, country=country)) for year in years]
    return years, number_releases
    years = range(start_year, end_year+1)
    number_tracks = []
    for year in years:
        releases = select(data, year=year, genre=genre, style=style, format=format, country=country)
        try:
            number_tracks.append(releases['tracks_number'].sum())
        except:
            print len(releases)
    return years, number_tracks


# Functions for data statistics/coverage

def releases_stats(data):
    """
    Compute statistics for a dataset
    - present genres, styles, formats and countries and their total number
    - total number of releases, tracks, and artists
    - percentage of releases annotated by duration, and their total duration
    - total number of unofficial releases and tracks
    - total number of releases and tracks from compilations
    - total number of mixed releases and tracks
    """
    stats = {}

    stats['all_genres'] = find_genres(data)
    stats['all_styles'] = find_styles(data)
    stats['all_formats'] = find_formats(data)
    stats['all_countries'] = find_countries(data)

    stats['total_genres'] = len(stats['all_genres'])
    stats['total_styles'] = len(stats['all_styles'])
    stats['total_formats'] = len(stats['all_formats'])
    stats['total_countries'] = len(stats['all_countries'])

    stats['total_releases'] = len(data)
    stats['total_tracks'] = data['tracks_number'].sum()
    stats['total_artists'] = len(find_artists(data))

    stats['releases_annotated_by_duration (%)'] = 100. * data['tracks_duration'].count() / len(data)
    stats['total_duration_days'] = data['tracks_duration'].sum() / 60. / 24.
    stats['total_duration_years'] = 0.00273973 * stats['total_duration_days']

    unofficial = select_unofficial(data)
    stats['total_releases_unofficial'] = len(unofficial)
    stats['total_tracks_unofficial'] = unofficial['tracks_number'].sum()
    # stats['total_artists_unofficial'] = len(find_artists(unofficial))

    compilation = select_compilation(data)
    stats['total_releases_compilation'] = len(compilation)
    stats['total_tracks_compilatioñn'] = compilation['tracks_number'].sum()

    mixed = select_mixed(data)
    stats['total_releases_mixed'] = len(mixed)
    stats['total_tracks_mixed'] = mixed['tracks_number'].sum()

    return stats


def releases_coverage(data, data_stats=None):
    """
    Compute coverage for a dataset (percentages of releases, tracks and
    artists) in terms of genres, styles, countries and formats
    """
    if data_stats is None:
        data_stats = releases_stats(data)

    # TODO add coverage in terms of labels
    stats = {
        'coverage_genres': {
             'releases (%)': {},
             'tracks (%)': {},
             'artists (%)': {},
        },
        'coverage_styles': {
             'releases (%)': {},
             'tracks (%)': {},
             'artists (%)': {},
        },
        'coverage_countries': {
             'releases (%)': {},
             'tracks (%)': {},
             'artists (%)': {},
        },
        'coverage_formats': {
             'releases (%)': {},
             'tracks (%)': {},
             'artists (%)': {},
        },
    }

    # TODO re-factor all ugly code below

    for g in data_stats['all_genres']:
        releases = select_genre(data, g)
        stats['coverage_genres']['releases (%)'][g] = 100. * len(releases)/len(data)
        stats['coverage_genres']['tracks (%)'][g] = 100. * releases['tracks_number'].sum() / data_stats['total_tracks']
        stats['coverage_genres']['artists (%)'][g] = 100. * len(find_artists(releases)) / data_stats['total_artists']

    for s in data_stats['all_styles']:
        releases = select_style(data, s)
        stats['coverage_styles']['releases (%)'][s] = 100. * len(releases)/len(data)
        stats['coverage_styles']['tracks (%)'][s] = 100. * releases['tracks_number'].sum() / data_stats['total_tracks']
        stats['coverage_styles']['artists (%)'][s] = 100. * len(find_artists(releases)) / data_stats['total_artists']

    for c in data_stats['all_countries']:
        releases = select_country(data, c)
        stats['coverage_countries']['releases (%)'][c] = 100. * len(releases)/len(data)
        stats['coverage_countries']['tracks (%)'][c] = 100. * releases['tracks_number'].sum() / data_stats['total_tracks']
        stats['coverage_countries']['artists (%)'][c] = 100. * len(find_artists(releases)) / data_stats['total_artists']

    for f in data_stats['all_formats']:
        releases = select_format(data, f)
        stats['coverage_formats']['releases (%)'][f] = 100. * len(releases)/len(data)
        stats['coverage_formats']['tracks (%)'][f] = 100. * releases['tracks_number'].sum() / data_stats['total_tracks']
        stats['coverage_formats']['artists (%)'][f] = 100. * len(find_artists(releases)) / data_stats['total_artists']

    for type_key in ["coverage_genres", "coverage_styles", "coverage_countries", "coverage_formats"]:

        stats_tmp = [[v for k, v in stats[type_key]['releases (%)'].items()],
                     [v for k, v in stats[type_key]['tracks (%)'].items()],
                     [v for k, v in stats[type_key]['artists (%)'].items()]]

        columns = stats[type_key]['releases (%)'].keys()
        index = ['releases (%)', 'tracks (%)', 'artists (%)']
        df = pandas.DataFrame(stats_tmp, columns=columns, index=index)
        df = df.sort_values(by='releases (%)', axis=1, ascending=False)
        stats[type_key] = df

    return stats


def visualize_releases_coverage(coverage_df, type="genre", show_top=15):
    """
    Visualize coverage for a dataset in terms of genres, styles, countries, and
    formats given a DataFrame with coverage statistics

    - type: genre, style, country, format
    - show_top: number of top categories to show
    """
    if type == "genre":
        title = 'Genre'
    elif type == "style":
        title = 'Style'
    elif type == "country":
        title = 'Country'
    elif type == "format":
        title = 'Format'
    else:
        print("Wrong 'type' value (expected 'genre' or 'style'): %s" % type)
        return
    title += ' coverage in terms of number of releases, tracks and artists'

    coverage_df = coverage_df[list(coverage_df)[:15]]

    coverage_df.plot(kind='barh', color=prepare_colors(len(list(coverage_df))))
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    # plt.ylim([0, 100])
    if PLOT_TITLES:
        plt.title(title)

    plt.show()
    return



def coverage_countries_evolution(data,
                                 countries=['US', 'UK', 'Germany', 'Brazil'],
                                 genre=None, style=None, type='releases',
                                 title=None,
                                 start_year=START_YEAR, end_year=END_YEAR):
    """
    Visualize coverage for a dataset in terms countries by year
    - start_year and end_year define the time interval to consider
    - countries is a list of countries to plot
    - genre and style: only consider releases from those genres and styles
    - type='releases': compute coverage in terms of releases
    - type='tracks': compute coverage in terms of tracks
    - title: plot title to show
    """

    if type == 'releases':
        compute = releases_per_year
    elif type == 'tracks':
        compute = tracks_per_year

    if not title:
        title = "Number of " + type + " across years by country"
        if genre:
            title = title + " (%s)" % genre
        if style:
            title = title + " (%s)" % style

    stats = {}
    for c in countries:
        years, counts = compute(data, start_year, end_year, genre=genre, style=style, country=c)
        stats[c] = counts
        stats.setdefault('years', years)

    for c, color in zip(countries, prepare_colors(len(countries))):
        stats[c] = [float('nan') if x == 0 else x for x in stats[c]]
        plt.plot(stats['years'], stats[c], label=c, color=color)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    if PLOT_TITLES:
        plt.title(title)
    plt.show()

    return stats


# Functions for track duration analysis

def visualize_track_duration_per_genre(data, type="genre", title=None, genres=None, skip_genres=None):
    """
    Visualize tracks durations per genre (style)
    - type:
        - "genre" using all tracks annotated by any genre
        - "style" using all tracks annotated by any style
        - "genre_only" using only tracks annotated by a single genre
        - "style_only" using only tracks annotated by a single style
    - skip_genres: list of genres (or styles) to exclude from analysis
    - title: plot title to show
    """

    if type == "genre":
        select_func = select_genre
        if not title:
            title = "Boxplot of track durations (sec.) per genre"

    elif type == "genre_only":
        select_func = select_only_genre
        if not title:
            title = "Boxplot of track durations (sec.) per genre (exclusive)"

    elif type == "style":
        select_func = select_style
        if not title:
            title = "Boxplot of track durations (sec.) per style"

    elif type == "style_only":
        select_func = select_only_style
        if not title:
            title = "Boxplot of track durations (sec.) per style (exclusive)"

    else:
        print "Wrong type:", type
        return

    stats = {}
    tracks_number = {}
    sorted_genres = []
    for g in genres:
        if skip_genres:
            if not skip_genres in g:
                continue
        releases = select_func(data, g)
        durations = find_durations(releases)
        if durations is None:
            continue
        stats[g] = durations
        #stats[g] = (releases['tracks_duration'] / releases['tracks_number']).dropna().values.tolist()
        tracks_number[g] = releases['tracks_number'].sum()
        sorted_genres.append((np.median(stats[g]), np.percentile(stats[g], 95) - np.percentile(stats[g], 5), g))
        #sorted_genres.append((np.median(stats[g]), scipy.stats.iqr(stats[g]), g))

    result = [(g, m, irq) for m, irq, g in sorted(sorted_genres)]

    sorted_genres = [g for g, m, irq in result]
    values = [stats[g] for g in sorted_genres]

    if type == "genre" or type == "genre_only":
        # 400 genre rows fit well into vertical size of 80 (0.2 row per 1 unit of size)
        plt.figure(figsize=(7, len(sorted_genres)*0.2))
        labels = ["%s (%d)" % (g, tracks_number[g]) for g in sorted_genres]
        plt.xlim([0, 25])

    elif type == "style" or type == "style_only":
        plt.figure(figsize=(7, len(sorted_genres)*0.2))
        labels = ["%s - %s (%d)" % (g[0], g[1], tracks_number[g]) for g in sorted_genres]
        plt.xlim([0, 40])

    plt.boxplot(values, vert=False, labels=labels, whis=[5, 95])
    if PLOT_TITLES:
        plt.title(title)
    plt.gca().xaxis.grid(True)
    plt.show()
    return result


# Load the dataset from pandas dump
data = pandas.read_hdf(dump_pandas)

# Dataset statistics
data_stats = releases_coverage(data)
pprint.pprint(data_stats)

# Dataset coverage
#visualize_releases_coverage(data_stats['coverage_genres'], type="genre")
#visualize_releases_coverage(data_stats['coverage_styles'], type="style")
#visualize_releases_coverage(data_stats['coverage_countries'], type="country")
#visualize_releases_coverage(data_stats['coverage_formats'], type="format")

# Evolution of recording industry in different countries
countries = ["US", "UK", "Germany", "Brazil", "Japan", "Russia", "India"]
data_stats['coverage_countries_evolution'] = coverage_countries_evolution(data, countries, start_year=1950)

pickle.dump(data_stats, open(results_stats, 'wb'))


# Per-genre (per-style) track duration analysis
data_notmixed = select_notmixed(data)
data_duration_per_genre = visualize_track_duration_per_genre(data_notmixed, type="genre", genres=data_stats['all_genres'])
data_duration_per_genre_only = visualize_track_duration_per_genre(data_notmixed, type="genre_only", genres=data_stats['all_genres'])
data_duration_per_style = visualize_track_duration_per_genre(data_notmixed, type="style")

# Not enough data for analysis on tracks annotated by a single style
#data_duration_per_style_only = visualize_track_duration_per_genre(data, type="style_only")


# Group style analysis by parent genres
data_duration_per_style_genres = {}
#data_duration_per_style_genres_exclusive = {}

for g in data_stats['all_genres']:
    releases = select_genre(data_notmixed, g)
    data_duration_per_style_genres[g] = visualize_track_duration_per_genre(releases,
                                                                           type="style",
                                                                           title="Boxplot of track durations (sec.) per style (%s genre)" % g,
                                                                           genre_filter=g)
    #data_duration_per_style_genres_exclusive[g] = visualize_track_duration_per_genre(releases,
    #                                                                       type="style_only",
    #                                                                       title="Boxplot of track durations (sec.) per style (%s genre) (exclusive)" % g,
    #                                                                       genre_filter=g)