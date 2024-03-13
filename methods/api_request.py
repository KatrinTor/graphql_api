import json
from json import JSONDecodeError

import allure
from allure_commons.types import AttachmentType
from curlify import to_curl
from requests import sessions


def api_request(url, method='POST', **kwargs):
    base_urls = {
        "gql": 'https://countries.trevorblades.com/'
    }
    if url == "gql":
        new_url = base_urls["gql"]
    else:
        new_url = base_urls["rest"] + url

    with allure.step(f"{method.upper()}{new_url}"):
        with sessions.Session() as session:
            response = session.request(
                method=method,
                url=new_url,
                verify=False,
                **kwargs)
            try:
                message = (to_curl(response.request)).replace(r'\n', '\n')
                allure.attach(
                    body=message.encode("utf-8"),
                    name="Curl",
                    attachment_type=AttachmentType.TEXT,
                    extension='txt'
                )
            except UnicodeDecodeError:
                allure.attach(
                    body='Невозможно декодировать запрос, отправляющий файл',
                    name="Curl",
                    attachment_type=AttachmentType.TEXT,
                    extension='txt'
                )
            if not response.content:
                allure.attach(
                    body='empty response',
                    name='Empty Response',
                    attachment_type=AttachmentType.TEXT,
                    extension='txt')
            else:
                try:
                    allure.attach(
                        body=json.dumps(response.json(),
                                        ensure_ascii=False,
                                        indent=4).encode("utf-8"),
                        name="Response Json",
                        attachment_type=AttachmentType.JSON,
                        extension='json'
                    )
                except JSONDecodeError:
                    allure.attach(
                        body=response.text,
                        name="Response Text",
                        attachment_type=AttachmentType.TEXT,
                        extension='txt'
                    )
    return response
