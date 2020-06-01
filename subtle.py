#!/usr/bin/python3.6
import requests
from bs4 import BeautifulSoup
import os
import sys


subtle_link = {}   # Dict. for holding movie names and links


def downsub(moviename=input("\n\t\tEnter movie name:  "), lang=None):
    
    try:
        moviename.strip()
        mainURL = "https://opensubtitles.co"
        searchurl = "https://opensubtitles.co/search?q=" + \
            moviename.replace(" ", "+")

        r = requests.get(searchurl).text
        soup = BeautifulSoup(r, 'html5lib')
        scratch_link = soup.find_all("a", class_="list-group-item")

        name_Count = 0
        print()
        for moviename in scratch_link[:-5]:
            name_Count += 1
            # print(moviename)

            imdb = moviename.find(
                'div', attrs={'class': 'col-xs-2 col-md-2 text-center'}).text.replace(" ", "").replace("\n", " ")

            print(
                f"\t\t[ {str(name_Count)} ]  {imdb}  {moviename['href'].split('/')[-1]}")

            # adding values to "subtle_link" Dictionary
            subtle_link[name_Count] = moviename['href']

        if len(subtle_link) != 0:
            try:
                Uesrs_Choice = int(input("\nEnter your choice : "))
                # Uesrs_Choice = int(1)
                if Uesrs_Choice < len(subtle_link):
                    MV_name = subtle_link[Uesrs_Choice].split('/')[-1]
                    r2 = requests.get(subtle_link[Uesrs_Choice]).text
                    sub2 = BeautifulSoup(r2, 'html5lib')
                    links = sub2.find('ul', class_="list-group").a['href']
                    r3 = requests.get(links).text
                    sub3 = BeautifulSoup(r3, 'html5lib')
                    half_Link = sub3.find('a', class_="btn btn-danger")['href']
                    full_Link = mainURL + half_Link
                    # Downloading Content
                    generateDown = requests.get(full_Link)
                    with open(f"{MV_name}.srt", 'wb') as file:
                        file.write(generateDown.content)
                        print("\n" + MV_name +
                              " Downloaded in > " + os.getcwd() + "  \n")

                else:
                    print(f"\n\t\tInvalid Choice....Try Agian....\n")

            except Exception as e:
                # print(e)
                pass
        else:
            print("\n\t\t Zero search results!!! \n")

    except Exception as e:
        print(f"\n{e}")


downsub()
