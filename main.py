import requests, json
import random
import os.path
from multiprocessing import Pool
import functools
from utils import create_folder, download, get_photos, available_albums

def main():
    token=input("Enter your token: ")
    owner=input("Enter owner id: ")
    
    # select album
    albums = available_albums(owner, token)
    number = int(input("Choose album number to download: "))
    selected_album_id = int(albums[number-1]['id'])
    album_name = albums[number-1]['title']
    photos_count = [x for x in albums if x['id'] == selected_album_id][0]['size']
    print(f"{photos_count} photos will be downloaded.")

    # create folder to store photos
    profile_info_response = requests.get(f"https://api.vk.com/method/account.getProfileInfo", params={
                                                                        'owner_id': owner,
                                                                        'access_token': token,
                                                                        'v': 5.89
                                                                    })
    profile_info = profile_info_response.json()                                                             
    first_name = profile_info['response']['first_name']
    last_name = profile_info['response']['last_name']
    save_path = create_folder((first_name, last_name, album_name))

    # Downloading photos
    photos_urls = get_photos(photos_count, owner, selected_album_id, token)
    print("Download started.")
    p = Pool()
    p.map(functools.partial(download, save_path=save_path), photos_urls)
    p.close()
    p.join()
    print(f"{photos_count} photos were downloaded.")


if __name__ == "__main__":
    main()
