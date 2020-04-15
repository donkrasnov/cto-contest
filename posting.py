import requests


def main():
    # Токены доступа
    # Нужно указать персональные токены доступа
    # И ID страницы в контакте, на стене которой необходимо сделать публикацю.
    # Сейчас токены намеренно испорчены.
    newVkToken = 'c6793f38f309ecb854a3e178e93438a5b05a533d02cfe008f1dfb6d580071a5bb498764247e61'
    myUserId = '4985385'
    newFbToken = 'EAAJF89iagS8BAE3Q2S7tfgMj7WZBtUnQN4aSRyRBR7YzflzFhJ5MwYr7MPBByrgv6kAJKAie0l9IjsfAZAIyzTjSPm3EEI98agHZBDLZAFETNNEvU6ngvyPUUYngskD6YQi1JgJDRfA4kf5aHLwgzDlXczyYofZBDeaeBXM3CmVWbQ88UbJNKWHVIEZD'

    # Выбор простого поста или поста с картинкой
    chooseCase = int(input('Введите 1, если публикация содержит только текст.\nВведите 2, если текст и фото.\nВвод: '))

    # Обработка случая простого поста
    if chooseCase == 1:
        print('Введите текст поста здесь:')
        myPost = input()

        # Запрос на публикацию поста в VK
        requestToPost = 'https://api.vk.com/method/wall.post?owner_id=' + myUserId + \
                        '&message=' + myPost + \
                        '&access_token=' + newVkToken + \
                        '&v=5.103'

        responseToPost = requests.get(requestToPost)
        print('Ответ от сервера VK: ')
        print(responseToPost.json())

        # Запрос на публикацию поста в Facebook
        # 'https://graph.facebook.com/{group_id}}/feed' -- нужно заменить параметр group_id на группу, в которой нужно создать пост
        requestToFbPost = 'https://graph.facebook.com/105260741152680/feed'
        dataForRequestToFbPost = {'message': myPost,
                                  'access_token': newFbToken}
        responseFromFbPost = requests.post(requestToFbPost, data=dataForRequestToFbPost)
        print('Ответ от сервера Facebook: ')
        print(responseFromFbPost.json())

        if 'error' not in responseToPost.json() and \
                'response' in responseToPost.json() and \
                responseToPost.status_code == 200:
            print('\nПост успешно опубликован в VK! ✅')
        else:
            print('\nВозникли ошибки! Пост не был опубликован в VK. ❌')

        if 'error' not in responseFromFbPost.json() and \
                'id' in responseFromFbPost.json() and \
                responseFromFbPost.status_code == 200:
            print('\nПост успешно опубликован в Facebook! ✅')
        else:
            print('\nВозникли ошибки! Пост не был опубликован в Facebook. ❌')

    # Обработка случая поста с картинкой
    elif chooseCase == 2:
        print('Введите текст поста здесь:')
        myPost = input()

        print("Укажите имя изображения для загрузки:")
        picForDownload = input()

        # Блок обработки загрузки фотографий на сервер VK
        requestToGetPhotoServer = 'https://api.vk.com/method/photos.getWallUploadServer?' + \
                                  '&access_token=' + \
                                  newVkToken + \
                                  '&v=5.103'

        responseToGetPhotoServer = requests.get(requestToGetPhotoServer)

        # print(responseToGetPhotoServer.json())

        with open(picForDownload, 'rb') as picture:
            requestToLoadPicture = requests.post(responseToGetPhotoServer.json()['response']['upload_url'],
                                                 files={'photo': picture})
        # print(requestToLoadPicture.json())

        requestToSavePhoto = 'https://api.vk.com/method/photos.saveWallPhoto?user_id=' + \
                             myUserId + \
                             '&server=' + str(requestToLoadPicture.json()['server']) + \
                             '&photo=' + requestToLoadPicture.json()['photo'] + \
                             '&hash=' + requestToLoadPicture.json()['hash'] + \
                             '&access_token=' + newVkToken + \
                             '&v=5.103'

        responseToSavePhoto = requests.get(requestToSavePhoto)

        # print(responseToSavePhoto.json())

        argForAttach = 'photo' + str(responseToSavePhoto.json()['response'][0]['owner_id']) + \
                       '_' + str(responseToSavePhoto.json()['response'][0]['id'])

        # print(argForAttach)

        # Запрос для публикации поста с фотографией в VK
        requestToPostPhoto = 'https://api.vk.com/method/wall.post?owner_id=' + myUserId + \
                             '&message=' + myPost + \
                             '&attachments=' + argForAttach + \
                             '&access_token=' + newVkToken + \
                             '&v=5.103'

        responseToPostWithPhoto = requests.get(requestToPostPhoto)
        print('Ответ от сервера VK: ')
        print(responseToPostWithPhoto.json())

        # Запрос для публикации поста с фотографией в Facebook
        # 'https://graph.facebook.com/{group_id}}/photos' -- нужно заменить параметр group_id на группу, в которой нужно создать пост
        requestToFbPostWithPhoto = 'https://graph.facebook.com/105260741152680/photos'
        dataForRequestToFbPostWithPhoto = {'message': myPost,
                                           'access_token': newFbToken,
                                           'url': responseToSavePhoto.json()['response'][0]['sizes'][9]['url']}

        responseFromFbPostWithPhoto = requests.post(requestToFbPostWithPhoto, data=dataForRequestToFbPostWithPhoto)
        print('Ответ от сервера Facebook: ')
        print(responseFromFbPostWithPhoto.json())

        if 'error' not in responseToPostWithPhoto.json() \
                and 'response' in responseToPostWithPhoto.json() \
                and responseToPostWithPhoto.status_code == 200:
            print('\nПост успешно опубликован в VK! ✅')
        else:
            print('\nВозникли ошибки! Пост не был опубликован в VK. ❌')

        if 'error' not in responseFromFbPostWithPhoto.json() and \
                'id' in responseFromFbPostWithPhoto.json() and \
                responseFromFbPostWithPhoto.status_code == 200:
            print('\nПост успешно опубликован в Facebook! ✅')
        else:
            print('\nВозникли ошибки! Пост не был опубликован в Facebook. ❌')
    else:
        print('\nВведено некорректное значение. ❌')


if __name__ == '__main__':
    main()
