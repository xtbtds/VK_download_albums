import requests, json
import random
import os.path
import os

def write_json(data, filename):
    with open (filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

def create_folder(profile_data):
    folder_name = "_".join(profile_data)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)
    print("Directory {} is created.".format(folder_name))
    return folder_name

def download(url_date_dict, save_path):
    r = requests.get(url_date_dict['url'], stream=True)
    try:
        filename = str(round(random.randint(10,99),3)) + url_date_dict['url'].split('/')[-1].split('?')[0] 
    except:
        print("Can't split filename ", url_date_dict['url'])
    completeName = os.path.join(save_path, filename)  
    with open(completeName, 'bw') as file:
        for chunk in r.iter_content(4096):
            file.write(chunk)
    os.utime(completeName, (url_date_dict['date'], url_date_dict['date']))

def get_photos(photos_count, owner_id, album_id, token):
    batches = int(photos_count / 50) + (photos_count % 50 > 0)
    all_photos_and_dates = []
    for i in range(batches):
        last = (i+1)*50 if photos_count >= (i+1)*50 else i*50 + photos_count % 50
        print(f"Receiving photos {i*50+1} - {last}...", )
        photos_response = requests.get(f"https://api.vk.com/method/photos.get", params={
                                                                            'owner_id': owner_id, 
                                                                            'album_id':album_id,
                                                                            'access_token': token, 
                                                                            'photo_sizes': True,
                                                                            'v': 5.89,
                                                                            'offset': 0 + 50*i
                                                                        })
        photos = photos_response.json()
        photos = photos['response']['items']
        for photo in photos:
            sizes = photo['sizes']
            date = photo['date']
            max_size_url = max(sizes, key=get_largest)['url']
            all_photos_and_dates.append({"url": max_size_url, "date": date})
    return all_photos_and_dates


def available_albums(owner, token):
    albums_response = requests.get(f"https://api.vk.com/method/photos.getAlbums", params={
                                                                        'owner_id': owner,
                                                                        'need_system': True,
                                                                        'access_token': token,
                                                                        'v': 5.89
                                                                    })
    albums = albums_response.json()
    albums = albums['response']['items']
    for i in range(len(albums)):
        print(f"{i+1}. {albums[i]['title']}, {albums[i]['size']} photos, id: {albums[i]['id']}")
    return albums
