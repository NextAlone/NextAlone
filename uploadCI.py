import json
import os
import requests

apiAddress = "http://127.0.0.1:8081/"
urlPrefix = apiAddress + "bot" + os.getenv("TELEGRAM_TOKEN")


def findString(sourceStr, targetStr):
    if str(sourceStr).find(str(targetStr)) == -1:
        return False
    else:
        return True


def genFileDirectory(path):
    files_walk = os.walk(path)
    target = {}
    for root, dirs, file_name_dic in files_walk:
        for fileName in file_name_dic:
            if findString(fileName, "arm64"):
                target["document"] = (fileName, open(path + "/" + fileName, "rb"))

    return target


def sendMetadataDesc():
    parma = {
        "chat_id": -0,
        "text": os.environ["COMMIT_MESSAGE"],
    }
    response = requests.post(urlPrefix + "/sendMessage", params=parma)

    # print(response.json())
    return response.json()["result"]["message_id"]


def sendAPKs(path):
    # startMessageParma = {
    #     "chat_id": -1001500637449,
    #     "text": "==== ====",
    # }
    # startMessageResponse = requests.post(urlPrefix + "/sendMessage", params=startMessageParma)

    file = genFileDirectory("./apks")

    parma = {
        "chat_id": -1001500637449,
        "caption": os.environ["COMMIT_MESSAGE"].split("\n")[0],
    }

    print(parma)

    r = requests.post(urlPrefix + "/sendDocument", params=parma, files=file)


def sendMetadata(changesID, startID):
    parma = {
        "chat_id": -0,
        "text": str(os.getenv("VERSION_NAME"))
        + ","
        + str(os.getenv("VERSION_CODE"))
        + ","
        + str(startID)
        + ","
        + str(changesID)
        + ",false",
    }
    response = requests.get(urlPrefix + "/sendMessage", params=parma)


if __name__ == "__main__":
    # changesID = sendMetadataDesc()
    startID = sendAPKs("./apks")
    # sendMetadata(changesID, startID)
