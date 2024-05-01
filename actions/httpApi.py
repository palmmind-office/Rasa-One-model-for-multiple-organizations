import requests

# http post services


def http_post(url='', headers={}, data={}):
    print(url, "url")
    try:
        response = requests.post(
            url,
            json=data,
            headers=headers
        )
        responseData = response.json()
        print(responseData, url)
        return responseData
    except Exception as error:
        print("Something has been wrong in dashboard server hai   hh" + str(error))


# http get services
def http_get(url='', headers={}):
    try:
        response = requests.get(
            url,
            headers=headers
        )
        responseData = response.json()
        return responseData
    except Exception as error:
        print("Something has been wrong in dashboard server" + str(error))


# http get facebook users details
def http_get_fb_details(senderid, fb_access_token):
    try:
        url = "https://graph.facebook.com/" + senderid + \
            "?fields=first_name,last_name,profile_pic&access_token="+fb_access_token
        response = requests.get(
            url
        )
        responseData = response.json()
        return responseData
    except Exception as error:
        print("Something has been wrong in facebook user details api" + str(error))
        return None
