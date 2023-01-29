import requests, json
import random
import os.path

def write_json(data, filename):
    with open (filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

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
    r_alb = requests.get(f"https://api.vk.com/method/photos.getAlbums", params={
                                                                        'owner_id': owner,
                                                                        'need_system': True,
                                                                        'access_token': token,
                                                                        'v': 5.89
                                                                    })
    write_json(r_alb.json(), 'albums.json')
    
    # print available albums
    r_alb_json = r_alb.json()
    albums = r_alb_json['response']['items']
    for i in range(len(albums)):
        print(f"{i+1}. {albums[i]['title']}, {albums[i]['size']} photos, id: {albums[i]['id']}")

    # preparation steps
    number = int(input("Choose album number to download: "))
    save_path = input("Enter path to download directory (press Enter to use current directory): " or os.getcwd())
    id = int(albums[number-1]['id'])
    for i in range(len(albums)):
        if albums[i]['id'] == id:
            photos_count = albums[i]['size']
    print(f"{photos_count} photos will be downloaded.")
    batches = int(photos_count / 50) + (photos_count % 50 > 0)

    # Downloading photos
    for i in range(batches):
        last = (i+1)*50 if photos_count >= (i+1)*50 else i*50+1 + photos_count % 50
        print(f"Downloading photos {i*50+1} - {last-1}...", )
        r = requests.get(f"https://api.vk.com/method/photos.get", params={
                                                                            'owner_id': owner, 
                                                                            'album_id':id,
                                                                            'access_token': token, 
                                                                            'photo_sizes': True,
                                                                            'v': 5.89,
                                                                            'offset': 0 + 50*i
                                                                        })

        write_json(r.json(), 'photos.json')
        photos = json.load(open('photos.json'))['response']['items']
        for photo in photos:
            sizes = photo['sizes']
            max_size_url = max(sizes, key=get_largest)['url']
            download(max_size_url, save_path)
        print("Done.")

if __name__ == "__main__":
    main()
