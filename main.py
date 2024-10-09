import requests
import base64
import time
import aiohttp

catalog_id = ''

art_apikey = ''
gpt_apikey = ''

def yandex_art_request(prompt, seed, attempts=5):
    prompt = {
        "modelUri": f"art://{catalog_id}/yandex-art/latest",
        "generationOptions": {
        "seed": seed,
        "aspectRatio": {
            "widthRatio": "1",
            "heightRatio": "1"
        }
        },
        "messages": [
            {
                "weight": "1",
                "text": prompt
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {art_apikey}"
    }

    create_request = requests.post('https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync', headers=headers, json=prompt)

    print('Генерация запущена')

    try:
        return create_request.json()['error']

    except:
        pass

    attempt = 0

    while attempt < attempts:
        attempt += 1
        print(f'Попытка: {attempt}')
        done_request = requests.get(f'https://llm.api.cloud.yandex.net:443/operations/{create_request.json()["id"]}', headers=headers)
        if done_request.json()['done'] == True:
            with open('yandexart_' + create_request.json()['id'] + '.jpeg', 'wb') as file:
                file.write(base64.b64decode(done_request.json()['response']['image']))

            break

        time.sleep(5)

    return 'yandexart_' + create_request.json()['id'] + '.jpeg'

def yandex_gpt_request(prompt):
    prompt = {
        "modelUri": f"gpt://{catalog_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {gpt_apikey}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    return response.json()['result']['alternatives'][0]['message']['text']

async def yandex_gpt_async_request(prompt):
    prompt = {
        "modelUri": f"gpt://{catalog_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {gpt_apikey}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=prompt, headers=headers) as response:
            json = await response.json()
            return json['result']['alternatives'][0]['message']['text']
