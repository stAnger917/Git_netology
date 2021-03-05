import requests

# path must be in such format
path = "%C%my_folder%file.txt"
token = ""  # put here your token


def ya_uploader(filepath, your_token):
    url_upload = f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={filepath}&overwrite=true"
    header = {"content-type": "application/json",
              'Authorization': your_token}
    response_upload = requests.get(url_upload, headers=header)
    upload_link_status = response_upload.status_code
    if upload_link_status != 200:
        return f"Error! Failed to get upload link. Request returned code {upload_link_status}"
    url_put = response_upload.json()['href']
    res = requests.put(url_put, headers=header)
    result = res.status_code
    if result == 201:
        return 'File successful uploaded'
    else:
        return f"Error! Request returned code {result}"


print(ya_uploader(path, token))
