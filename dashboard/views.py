from django.shortcuts import render, HttpResponse
from .models import *
import pandas as pd
import numpy as np
import random


def cosine_sim(x, y):
    return np.dot(x.T, y) / (np.linalg.norm(x) * np.linalg.norm(y))


def similar(x, data, top):
    dic = {}
    for index, row in data.iterrows():
        dic[index] = cosine_sim(x, row.values.reshape(-1, 1))
    dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    return dict(zip(list(dic.keys())[:top], list(dic.values())[:top]))


def similar_item(x, data, top):
    var = similar(x, data, top)
    for i in var.keys():
        print(df.iloc[i]['Mood'], "\t\t", df.iloc[i]['Title'], "\t\t", df.iloc[i]['Artist'])


def similar_item_mood_genre(x, data, top):
    var = similar(x, data, top)
    return var.keys()


def index(request):
    return render(request, 'index.html', {})


def dashboard(request):
    habits = Habits.objects.all()

    context = {
        'habits' : habits,
    }

    return render(request, 'Dash.html', context)


def recommend(request):
    context = {}
    if request.method == 'POST':
        # print(True)
        habits = Habits.objects.all()

        collected_data = {}
        for i in habits:
            id = request.POST.get(i)
            habit = request.POST.get(str(i.id))
            if habit == 'True':
                collected_data[i.name] = True

            else:
                collected_data[i.name] = False
            print(habit)

        mood = request.POST.get('mood')         # mood data  >>>>>>>>>>>>>
        print(mood, '\t', type(mood))


        ## First_time_playing songs        
        file = Files.objects.all()

        df = pd.read_csv(file[0].file.path)  ##path to music_with_genre_path
        temp_df = pd.read_csv(file[1].file.path)  ##path_to_temp_df
        songs_list_with_mood = dict(zip(df[df['Mood'] == mood].index.values,
                                        df['Title'][df["Mood"] == mood]))  # list of songs with particular mood
        songs = dict(zip(df['Mood'].index.values, df["Title"]))  ##List of songs

        sampling = random.choices(list(songs_list_with_mood), k=8)

        for i in sampling:
            print(songs_list_with_mood[i])

        ##after second time

        played_not_played_from_displayed_songs = dict(zip(sampling, [False for i in range(len(sampling))]))

        song = -1
        for i in played_not_played_from_displayed_songs:
            if songs_list_with_mood[i]:
                song = i

        x = temp_df.iloc[song].values.reshape(-1, 1)

        suggested_song = similar_item_mood_genre(x, temp_df, top=10)
        for i in suggested_song:
            print(songs[i])

        ###Second time se
        suggested_song = similar_item_mood_genre(x, temp_df, top=10)
        played_not_played_from_displayed_songs = dict(zip(suggested_song, [False for i in range(len(suggested_song))]))

        song = -1
        for i in played_not_played_from_displayed_songs:
            if songs_list_with_mood[i]:
                song = i

        x = temp_df.iloc[song].values.reshape(-1, 1)
        suggested_song = similar_item_mood_genre(x, temp_df, top=10)
        recommened_songs = []
        for i in suggested_song:
        
            recommened_songs.append(songs[i])

        print('\n\n recommened_songs : ', recommened_songs)
        


        context = {
            'recommened_songs' : recommened_songs,
        }



        # print('ID: ',i, id)
    return render(request, 'Dash.html', context)
