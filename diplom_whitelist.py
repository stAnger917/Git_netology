import requests
import dpath.util as dp
from datetime import datetime
import logging

"""
Greetings! 
For logging I use logging module into the file logs.txt. Before running program - be sure that file exists.
"""

logging.basicConfig(filename='logs.txt', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


def get_yandex_token():
    yandex_token = input("Plz, input your Yandex token here: ")
    return yandex_token


def get_vk_token():
    # vk_token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
    vk_token = input("Plz, input your VK token here: ")
    return vk_token


def get_vk_user_name():
    vk_user_profile_name = input("Enter a correct VK user`s profile name: ")
    return vk_user_profile_name


def get_vk_user_id(token, profile_name):
    logging.info('Getting VK user profile ID by the vk_user_profile_name')
    url_vk = f"https://api.vk.com/method/users.get?user_ids={profile_name}&v=5.130&access_token={token}"
    response_vk_user_id = requests.get(url_vk)

    if response_vk_user_id.status_code != 200:
        logging.error(f'Error! Failed to get VK users ID! Request status: {response_vk_user_id.status_code}')
        return 'Error! Failed to get VK users ID!'

    null_result = []
    response_vk_user_id_json = (response_vk_user_id.json().get('response'))

    if response_vk_user_id_json == null_result or response_vk_user_id_json is None:
        logging.error(f'Error! Failed to find such user with profile name: {profile_name}')
        logging.info('Execution finished')
        return 'Error! There is no such VK user!'

    vk_user_id = 0
    for item in response_vk_user_id_json:
        vk_user_id = item.get('id')
    logging.info(f'Completed! VK users id: {vk_user_id}')
    return vk_user_id


def get_all_photo(token, user_id):
    logging.info('Getting all users photo from the profile album')
    url_get_photo = f"https://api.vk.com/method/photos.get?owner_id={user_id}&v=5.130&access_token={token}" \
                    f"&album_id=profile&extended=1&photo_sizes=1"
    response_vk_get_vk_photo = requests.get(url_get_photo)

    if response_vk_get_vk_photo.status_code != 200:
        logging.error(f'Error! Failed to get VK users photos! Request status: '
                      f'{response_vk_get_vk_photo.status_code}')
        logging.info('Execution finished')
        return 'Error! Failed to get VK users photos!'

    logging.info('Completed! Data received!')
    return response_vk_get_vk_photo.json()


def create_upload_links_list(photo_json):
    logging.info('Forming a list of links to upload')

    sizes_list = dp.values(photo_json, "//**/sizes")
    if len(sizes_list) == 0:
        logging.warning('There is no images in the profile album!')
        logging.info('Execution finished')
        return 'Warning! There is no images in the profile album!'

    vk_photo_links = []

    # last elem - is the largest by size - so - we take him

    for photo in sizes_list:
        vk_photo_links.append(photo[-1]['url'])
    logging.info('Completed! List of links for uploading formatted')
    return vk_photo_links


def create_filename_list(photo_json):
    logging.info('Forming a list of filenames to upload')

    sizes_list = dp.values(photo_json, "//**/sizes")
    likes_list = dp.values(photo_json, "//**/likes/count")
    date_list = dp.values(photo_json, "//**/date")
    if len(sizes_list) == 0:
        logging.warning('There is no images in the profile album!')
        logging.info('Execution finished')
        return 'Warning! There is no images in the profile album!'

    vk_photo_filenames = []

    for i in range(len(likes_list)):
        if likes_list[i] not in vk_photo_filenames:
            vk_photo_filenames.append(likes_list[i])
    else:
        date_list[i] = (datetime.utcfromtimestamp(date_list[i]).strftime('%Y-%m-%d_%H:%M:%S'))
        vk_photo_filenames.append(f'{likes_list[i]}_{date_list[i]}')

    logging.info('Completed! List of filenames for uploading formatted')
    return vk_photo_filenames


def create_file_type_list(photo_json):
    logging.info('Forming a list of filetypes to upload')

    sizes_list = dp.values(photo_json, "//**/sizes")
    if len(sizes_list) == 0:
        logging.warning('There is no images in the profile album!')
        logging.info('Execution finished')
        return 'Warning! There is no images in the profile album!'

    types_list = []

    for photo in sizes_list:
        types_list.append((photo[-1]['type']))

    logging.info('Completed! List of filetypes for uploading formatted')
    return types_list


def create_new_folder(token):
    logging.info('Creating new folder ont the Yndex.disk')
    disk_folder_name = str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    url_create_disk_folder = f"https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{disk_folder_name}"
    ya_header = {"content-type": "application/json",
                 'Authorization': token}
    response_create_disk_folder = requests.put(url_create_disk_folder, headers=ya_header)
    if response_create_disk_folder.status_code != 201:
        logging.error(f'Error! Failed to create upload folder. Request returned code '
                      f'{response_create_disk_folder.status_code}')
        logging.info('Execution finished')
        return "Error! Failed to create upload folder!"
    else:
        logging.info(f'Completed! Created new folder: {disk_folder_name}')
        return disk_folder_name


def get_upload_photo_num(links_list):
    need_2_upload = 0
    while True:
        try:
            need_2_upload = int(
                input(f'How many images need to upload? Available for uploading: {len(links_list)} '))
            if need_2_upload not in range(1, len(links_list) + 1):
                print('Wrong input, try again!')
                logging.warning(f'Users wrong input of number of uploading images: {need_2_upload}')
            else:
                break
        except ValueError:
            print('Wrong input, try again!')
            logging.warning(f'Users wrong input of number of uploading images')
            continue
    return need_2_upload


def upload_photo(upload_num, filenames_list, folder_name, links_list, token):
    upload_counter = 0

    ya_header = {"content-type": "application/json",
                 'Authorization': token}

    for j in range(upload_num):
        logging.info(f'Getting image content: {filenames_list[j]}')
        image = requests.get(links_list[j])
        logging.info(f'Completed! Image content received')
        logging.info(f'Getting upload link from the Yndex.disk')
        url_upload_img = f"https://cloud-api.yandex.net/v1/disk/resources/" \
                         f"upload?path=disk%3A%2F{folder_name}/" \
                         f"{filenames_list[j]}&overwrite=false "
        response_get_upload_link = requests.get(url_upload_img, headers=ya_header)
        if response_get_upload_link.status_code != 200:
            print(f"Error! Failed to get upload link. Request returned code {response_get_upload_link.status_code}")
            logging.error(f"Error! Failed to get upload link. Request returned code "
                          f"{response_get_upload_link.status_code}")
            logging.info('Execution finished')
            break
        else:
            logging.info(f'Completed! Upload link for image {filenames_list[j]} received')
            pass
        logging.info(f'Uploading image {filenames_list[j]}')
        url_put_img = response_get_upload_link.json()['href']
        response_upload_img = requests.put(url_put_img, image.content)
        if response_upload_img.status_code == 201:
            print(f'File {filenames_list[j]} was successfully uploaded! PUT request status: '
                  f'{response_upload_img.status_code}')
            upload_counter += 1
            logging.info(f'Completed! {filenames_list[j]} uploaded!')
        else:
            print(f'Error! Failed to upload image! PUT request status: {response_upload_img.status_code}')
            logging.error(f'Error! Failed to upload image! PUT request status: {response_upload_img.status_code}')
            logging.info(f'Uploading next image!')

    print(f'{upload_counter} of {len(links_list)} images was successfully uploaded!')
    return upload_counter


def create_data_for_json_result_file(counter, filenames, types):
    if counter > 0:
        res_json = {}
        for k in range(counter):
            item = [{
                'filename': filenames[k],
                'size': types[k]
            }]
            res_json[k] = item
        return res_json


def create_json_result_file(data):
    import json
    with open('json_result.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


logging.info('Execution started')

YA_TOKEN = get_yandex_token()
VK_TOKEN = get_vk_token()
VK_USER_ID = get_vk_user_id(VK_TOKEN, get_vk_user_name())

while True:
    if VK_USER_ID == 'Error! Failed to get VK users ID!':
        print('Error! Failed to get VK users ID!')
        break
    elif VK_USER_ID == 'Error! There is no such VK user!':
        print('Error! There is no such VK user!')
        break
    else:
        if get_all_photo(VK_TOKEN, VK_USER_ID) == 'Error! Failed to get VK users photos!':
            print('Error! Failed to get VK users photos!')
            break
        else:
            all_photo_json = get_all_photo(VK_TOKEN, VK_USER_ID)
            link_list = create_upload_links_list(all_photo_json)
            if link_list == 'Warning! There is no images in the profile album!':
                print('Warning! There is no images in the profile album!')
                break
            else:
                filename_list = create_filename_list(all_photo_json)
                type_list = create_file_type_list(all_photo_json)
                ya_folder_name = create_new_folder(YA_TOKEN)
                if ya_folder_name == "Error! Failed to create upload folder!":
                    print("Error! Failed to create upload folder!")
                    break
                else:
                    uploads_number = get_upload_photo_num(link_list)
                    upload_result = upload_photo(uploads_number, filename_list, ya_folder_name, link_list, YA_TOKEN)
                    create_json_result_file(create_data_for_json_result_file(upload_result, filename_list, type_list))
                    logging.info('Execution finished')
                    break
