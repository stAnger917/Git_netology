import requests
import dpath.util as dp
from datetime import datetime
import logging

"""
How to use

Greetings! First you should to do - paste your yandex token from da https://yandex.ru/dev/disk/poligon/
into variable yandex_token. VK_token - is common, just use it, no need to change.
Then - just run the function vk_profile_photo_backup()

I split the execution flow of the application on states for convenience.
For logging I use logging module into the file logs.txt. Before running program - be sure that file exists.
"""

# Put your yndex token here
yandex_token = ''
vk_token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"

logging.basicConfig(filename='logs.txt', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


def vk_profile_photo_backup():
    stater = True
    while stater:
        logging.info('Execution started')
        vk_user_profile_name = input("Enter a correct VK user`s profile name: ")
        # vk_user_profile_name = 'begemot_korovin'
        logging.info(f'User entered VK profile name: {vk_user_profile_name} ')

        # State_1: getting VK user profile ID by the vk_user_profile_name

        logging.info('Getting VK user profile ID by the vk_user_profile_name')
        url_vk = f"https://api.vk.com/method/users.get?user_ids={vk_user_profile_name}&v=5.130&access_token={vk_token}"
        response_vk_user_id = requests.get(url_vk)

        if response_vk_user_id.status_code != 200:
            print(f'Error! Failed to get VK users ID!')
            logging.error(f'Error! Failed to get VK users ID! Request status: {response_vk_user_id.status_code}')
            logging.info('Execution finished')
            break

        null_result = []
        response_vk_user_id_json = (response_vk_user_id.json().get('response'))
        if response_vk_user_id_json == null_result:
            print(f'Error! There is no such VK user!')
            logging.error(f'Error! Failed to find such user with profile name: {vk_user_profile_name}')
            logging.info('Execution finished')
            break

        vk_user_id = 0
        for item in response_vk_user_id_json:
            vk_user_id = item.get('id')
        logging.info(f'Completed! VK users id: {vk_user_id}')

        # State_2: getting all users photo from da profile album

        logging.info('Getting all users photo from the profile album')
        url_get_photo = f"https://api.vk.com/method/photos.get?owner_id={vk_user_id}&v=5.130&access_token={vk_token}" \
                        f"&album_id=profile&extended=1&photo_sizes=1"
        response_vk_get_vk_photo = requests.get(url_get_photo)

        if response_vk_get_vk_photo.status_code != 200:
            print(f'Error! Failed to get VK users photos!')
            logging.error(f'Error! Failed to get VK users photos! Request status: '
                          f'{response_vk_get_vk_photo.status_code}')
            logging.info('Execution finished')
            break

        logging.info('Completed! Data received!')

        # State_3: formatting needed photo list to upload

        logging.info('Forming a list of files to upload')

        sizes_list = dp.values(response_vk_get_vk_photo.json(), "//**/sizes")
        likes_list = dp.values(response_vk_get_vk_photo.json(), "//**/likes/count")
        date_list = dp.values(response_vk_get_vk_photo.json(), "//**/date")
        if len(sizes_list) == 0:
            print('Warning! There is no images in the profile album!')
            logging.warning('There is no images in the profile album!')
            logging.info('Execution finished')
            break

        vk_photo_links = []
        vk_photo_filenames = []
        type_list = []

        for i in range(len(likes_list)):
            if likes_list[i] not in vk_photo_filenames:
                vk_photo_filenames.append(likes_list[i])
        else:
            date_list[i] = (datetime.utcfromtimestamp(date_list[i]).strftime('%Y-%m-%d_%H:%M:%S'))
            vk_photo_filenames.append(f'{likes_list[i]}_{date_list[i]}')

        # last elem - is the largest by size - so - we take him

        for photo in sizes_list:
            vk_photo_links.append(photo[-1]['url'])
            type_list.append((photo[-1]['type']))
        logging.info('Completed! List of files for uploading formatted')

        # State_4: creating new folder on the Ya.disk
        logging.info(f'Using entered Yandex token: {yandex_token}')

        logging.info('Creating new folder ont the Yndex.disk')
        disk_folder_name = str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        url_create_disk_folder = f"https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{disk_folder_name}"
        ya_header = {"content-type": "application/json",
                     'Authorization': yandex_token}
        response_create_disk_folder = requests.put(url_create_disk_folder, headers=ya_header)
        if response_create_disk_folder.status_code != 201:
            print(f"Error! Failed to create upload folder. Request returned code "
                  f"{response_create_disk_folder.status_code}")
            logging.error(f'Error! Failed to create upload folder. Request returned code '
                          f'{response_create_disk_folder.status_code}')
            logging.info('Execution finished')
            break
        else:
            logging.info(f'Completed! Created new folder: {disk_folder_name}')
            pass

        logging.info('Uploading images in the created folder')
        # State_5: uploading photos to da created folder
        upload_counter = 0
        # Getting number of uploading images from the user
        logging.info('Getting from the user number of uploading images')
        need_2_upload = 0
        while True:
            try:
                need_2_upload = int(
                    input(f'How many images need to upload? Available for uploading: {len(vk_photo_links)} '))
                if need_2_upload not in range(1, len(vk_photo_links) + 1):
                    print('Wrong input, try again!')
                    logging.warning(f'Users wrong input of number of uploading images: {need_2_upload}')
                else:
                    break
            except ValueError:
                print('Wrong input, try again!')
                logging.warning(f'Users wrong input of number of uploading images')
                continue

        for j in range(need_2_upload):
            logging.info(f'Getting image content: {vk_photo_filenames[j]}')
            image = requests.get(vk_photo_links[j])
            logging.info(f'Completed! Image content received')
            logging.info(f'Getting upload link from the Yndex.disk')
            url_upload_img = f"https://cloud-api.yandex.net/v1/disk/resources/" \
                             f"upload?path=disk%3A%2F{disk_folder_name}/" \
                             f"{vk_photo_filenames[j]}&overwrite=false "
            response_get_upload_link = requests.get(url_upload_img, headers=ya_header)
            if response_get_upload_link.status_code != 200:
                print(f"Error! Failed to get upload link. Request returned code {response_get_upload_link.status_code}")
                logging.error(f"Error! Failed to get upload link. Request returned code "
                              f"{response_get_upload_link.status_code}")
                logging.info('Execution finished')
                break
            else:
                logging.info(f'Completed! Upload link for {vk_photo_filenames[j]} received')
                pass
            logging.info(f'Uploading image {vk_photo_filenames[j]}')
            url_put_img = response_get_upload_link.json()['href']
            response_upload_img = requests.put(url_put_img, image.content)
            print(response_upload_img.status_code)
            if response_upload_img.status_code == 201:
                print(f'File {vk_photo_filenames[j]} was successfully uploaded! PUT request status: '
                      f'{response_upload_img.status_code}')
                upload_counter += 1
                logging.info(f'Completed! {vk_photo_filenames[j]} uploaded!')
            else:
                print(f'Error! Failed to upload image! PUT request status: {response_upload_img.status_code}')
                logging.error(f'Error! Failed to upload image! PUT request status: {response_upload_img.status_code}')
                logging.info(f'Uploading next image!')

        print(f'{upload_counter} of {len(vk_photo_links)} images was successfully uploaded!')
        logging.info(f'{upload_counter} of {len(vk_photo_links)} images was successfully uploaded!')
        if upload_counter > 0:
            res_json = {}
            for k in range(upload_counter):
                item = [{
                    'filename': vk_photo_filenames[k],
                    'size': type_list[k]
                    }]
                res_json[k] = item
            print(res_json)
        stater = False
        logging.info('Execution finished')


vk_profile_photo_backup()
