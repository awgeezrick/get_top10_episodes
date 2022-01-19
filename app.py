# imports
import imdb
import pandas as pd

# creating instance of IMDb
ia = imdb.IMDb()


def get_show_title_and_show_id(show_name):
    print('searching for show on imdb...')
    #show_qry = input('Please enter the name of the TV Series...')
    show = ia.search_movie(show_name)
    show_title = show[0]
    show_id = show[0].movieID

    return show_title, show_id


def get_tv_series_and_episode_data(series_id):
    print('getting series and episode data...')
    # getting information
    tv_series = ia.get_movie(series_id)

    # adding new info set
    ia.update(tv_series, 'episodes')

    return tv_series


def get_season_episode_title_rating_data(series_inf):
    # let's create an empty dictionary
    series_data = []

    # now we go through the main series/episode data and grab the values we want
    # and then update our dictionary with that data
    print('adding season, episode and rating info to dataframe...')

    for season_nr in sorted(series_inf['episodes']):
        for episode_nr in sorted(series_inf['episodes'][season_nr]):
            episode = series_inf['episodes'][season_nr][episode_nr]
            # season = 'S0' + str(season_nr)
            # season_episode = 'E' + str(episode_nr)
            # se = 'S' + str(season_nr) + 'E' + str(episode_nr)
            title = episode.get('title')
            rating = episode.get('rating')
            series_data.append({'Season': season_nr, 'Episode': episode_nr, 'Title': title, 'Rating': rating})

            # now let's make a dataframe from that dictionary
    df_ = pd.DataFrame.from_dict(series_data)

    return df_


def get_top10(df):
    print('getting top 10 episodes...')
    df_top10 = df.sort_values(by='Rating', ascending=False).head(10)
    df_top10.reset_index(drop=True, inplace=True)
    return df_top10


def get_top10_episodes_for_tv_show(tv_show_name_):
    show_title, show_id = get_show_title_and_show_id(tv_show_name_)

    series = get_tv_series_and_episode_data(show_id)

    df_series = get_season_episode_title_rating_data(series)

    df_series_top10 = get_top10(df_series)

    return df_series_top10


# the below value should change to the desired show you are looking for
tv_show_name = 'Brooklyn Nine-Nine'

df_top10_episodes = get_top10_episodes_for_tv_show(tv_show_name)