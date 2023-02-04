import requests, json
import random
import os.path

"""
    Use write_json function if you want to store response into .json file:
    write_json(response.json(), 'file_name.json')
"""

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

def download(url, save_path):
    r = requests.get(url, stream=True)
    try:
        filename = str(round(random.random(),6))+url.split('/')[-1].split('?')[0]
    except:
        print("Can't split filename ", url)
    completeName = os.path.join(save_path, filename)  
    with open(completeName, 'bw') as file:
        for chunk in r.iter_content(4096):
            file.write(chunk)
        


def main():
    token=input("Enter your token: ")
    owner=input("Enter owner id: ")
    
    # print available albums
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

    # select album
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
    batches = int(photos_count / 50) + (photos_count % 50 > 0)
    for i in range(batches):
        last = (i+1)*50 if photos_count >= (i+1)*50 else i*50 + photos_count % 50
        print(f"Downloading photos {i*50+1} - {last}...", )
        photos_response = requests.get(f"https://api.vk.com/method/photos.get", params={
                                                                            'owner_id': owner, 
                                                                            'album_id':selected_album_id,
                                                                            'access_token': token, 
                                                                            'photo_sizes': True,
                                                                            'v': 5.89,
                                                                            'offset': 0 + 50*i
                                                                        })

        photos = photos_response.json()
        photos = photos['response']['items']
        for photo in photos:
            sizes = photo['sizes']
            max_size_url = max(sizes, key=get_largest)['url']
            download(max_size_url, save_path)
        print("Done.")

if __name__ == "__main__":
    main()
