from tqdm import tqdm
import requests
from os import listdir
from os.path import isfile, join

def DownloadFolders():
    url = 'https://newlms.magtu.ru/mod/folder/download_folder.php?id=1584707'
    response = requests.get(url, stream=True)
    with open(f"test.zip",'wb') as handle:
        for data in tqdm(response.iter_content(chunk_size=1024), unit="kB"):
            handle.write(data)

if __name__ == '__main__':
    DownloadFolders()
