import requests
import csv
import os


def refreshLaptops(code):

    # _code = input("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={}&scope={}&response_type=code&redirect_uri={}".format(
    #   '3951948a-22cb-46ee-b218-9c994779ba16', 'files.readwrite.all', 'https://login.microsoftonline.com/common/oauth2/nativeclient') + '\n')

    # # https://login.microsoftonline.com/common/oauth2/nativeclient?code=0.AREAmT13KynyBEe1YloxmIMXeYqUUTnLIu5GshicmUd5uhYRAAk.AQABAAIAAAD--DLA3VO7QrddgJg7WevrH8tyotnm7zsFwhjqkAAmmv3i3ByLvjuM28t8qTfLoTG3OPKWCm73Bo-KmHP34W_6Ra5teYEUG0vzrl66sFMb5X-MdRGfVoY2Az3-9zIZU6jakW3PepR0pd8y9ruuuVQHFOidq7rD458cdKKIYqEbpmhXCUejeRh49-SfwtqhfBcdNjedxKW2L3WffleMsZ_RwG95VUURFytbyQJLZpAsdhIXt4OUDhiD1rAJeFs7HppWi5y35wnv7Qohoekpm1KX4ANM9xRQez3hrBFeWKPptyX4fFckOSEccBhfGSch9SnmLEmBY5C7-n7smNBNyME3CdfAs2mTIXBaxKQCl9aH5gXtvxVPDJQ_0JkMTfdDA9gRH3vUI58vOnverUt3sVZr3PeqcY8CxnnQ8l9e0SdsT_6gNF-MoGtedyxSJl93XhHMp8tpr2TXswBuN1hEQ_dG3Ejy3q7AgtL0tuIWpI2h9Vk8ee2GwvoHw-KK87Ty7lZF-InSAXts02v1RSG9jIUlYCWfdZaQJ0BUyxqKyVZ8GHNflygIqbWOfkNYGeF4LNi02TT9EFEnVmVBqE4iB7L3k8WumJkHfFwXZJAxJnVJimkSUgryk9jAeyd_lKulVZmuvhvn3g3Ev_JgQwFCGvSqJfm64EIpiFY2tB4WT0bjMyAA&session_state=fe187d00-b7dd-4c96-bcf4-469eedde80ca
    data = {'grant_type': 'authorization_code', 'client_id': '3951948a-22cb-46ee-b218-9c994779ba16',
            'redirect_uri': 'https://login.microsoftonline.com/common/oauth2/nativeclient', 'code': code}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    r = requests.post(url, headers=headers, data=data)

    # print(r.json())

    token = r.json()['access_token']
    print(token, '\n')

    # eyJ0eXAiOiJKV1QiLCJub25jZSI6Il9iOWZySEFTM0RRNy1WdzBvbzBmVno2amRmRnA1dlA1M2RBMlNQenEyQUUiLCJhbGciOiJSUzI1NiIsIng1dCI6ImpTMVhvMU9XRGpfNTJ2YndHTmd2UU8yVnpNYyIsImtpZCI6ImpTMVhvMU9XRGpfNTJ2YndHTmd2UU8yVnpNYyJ9
    # token = '.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yYjc3M2Q5OS1mMjI5LTQ3MDQtYjU2Mi01YTMxOTg4MzE3NzkvIiwiaWF0IjoxNjUwOTc2MDE3LCJuYmYiOjE2NTA5NzYwMTcsImV4cCI6MTY1MDk4MDYwMywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkUyWmdZQWo0OGlRa2lIT3poSGZTai9kR1lTcTFXU3YrNVJSSU10Y2V2U2x5cFczYW5CWUEiLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6Ik9uZURyaXZlIFNoYXJlIExpbmsgR2VuZXJhdG9yIiwiYXBwaWQiOiIzOTUxOTQ4YS0yMmNiLTQ2ZWUtYjIxOC05Yzk5NDc3OWJhMTYiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IlJhZHdhbiIsImdpdmVuX25hbWUiOiJZb3VzZWYiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNTYuMjA4LjkxLjI0MSIsIm5hbWUiOiJZb3VzZWYgQWhtZWQgUmFkd2FuIiwib2lkIjoiYzg4ZWI3MDYtNzgxZi00MjdkLWExM2YtMGRjNjNjZWI0Mzc3Iiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTE2MzczOTE2NDMtODkzMTQzNjUtMzEwNzg2MTc3My02OTc4IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAwRUJEMTU0MEQiLCJyaCI6IjAuQVJFQW1UMTNLeW55QkVlMVlsb3htSU1YZVFNQUFBQUFBQUFBd0FBQUFBQUFBQUFSQUFrLiIsInNjcCI6IkZpbGVzLlJlYWRXcml0ZS5BbGwgcHJvZmlsZSBvcGVuaWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJ4NHJxRDBOeURUVkJQXzVlcWMwbF8zZzBUYzVrNEdINEpQcnFFOXM0Wkh3IiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFGIiwidGlkIjoiMmI3NzNkOTktZjIyOS00NzA0LWI1NjItNWEzMTk4ODMxNzc5IiwidW5pcXVlX25hbWUiOiJZby5SYWR3YW5AbnUuZWR1LmVnIiwidXBuIjoiWW8uUmFkd2FuQG51LmVkdS5lZyIsInV0aSI6IjN6Q1hicmIxMjBPdVVSUXIwNWxHQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoiSEE4OEhFU19OVUxUZzVydjJtZjhjeGVwb3g5TS1sV1IzeHNjTkUtWFljZyJ9LCJ4bXNfdGNkdCI6MTQwNDAxNTAzNH0.W4OD2bExG6wVGPvcR4Gr6WZkb_QU3SvXJHfkDMZlDoItahqK1GWXV-DkJOsIV-ARKkrMDT39DLQNUUM6y2iTNiTnnNC5_aAb8tkm7tbPu7ZXlCKX0oe3z_uV_d2mE2TFbgGq_0LGnvbWC6p3_xUflNyVii-e1C0NJKP3A968t6o9kdJUD8cNWCvO3YcysF2sRdUclxLI9XIqDSacjmylVNi-pvOpt9kd5Ov6c7PrpGAlnSUfOFpAguZlfp1kYwgwsTEJiOwb87NWyF808PulhdQDEZpyCsEcdQwut0rFoo85edLSwx_FXiK6_v4CIB7Chojrh7wH8b9qv3nyx5MWPg'
    headers_req = {'Authorization': 'Bearer ' + token}
    # GET /me/drive/root
    # Get item from root directory first then look for remoteitem details and get driveID and ID and use those to reach original file to run children on.
    # 012ICEQRKOYZFPEFVGQZCIYUWNMRJE5RG2
    req_url = 'https://graph.microsoft.com/v1.0//me/drive/items/012ICEQRP5VRNXVZOUSNHKKVOCKITMMDNG'
    res = requests.get(req_url, headers=headers_req)
    # l = input(res.json())
    numberOfFiles = (res.json()['folder']['childCount'])
    skiptoken = ''
    counter = 0
    done = False
    res_list = []
    while True:
        print('new set')
        req_url = 'https://graph.microsoft.com/v1.0/me/drive/items/012ICEQRP5VRNXVZOUSNHKKVOCKITMMDNG/children'
        if skiptoken:
            req_url = skiptoken
        res = requests.get(req_url, headers=headers_req)
        try:
            skiptoken = (res.json()['@odata.nextLink'])
            print(skiptoken)
        except:
            skiptoken = ''
            done = True

        PATH = os.path.dirname(os.path.realpath(__file__))
        for file in res.json()['value']:
            # k = input(str(file))
            counter += 1
            print(counter)
            link = requests.get(
                'https://graph.microsoft.com/v1.0/me/drive/items/' + file['id'], headers=headers_req)
            # print(link.json()['@microsoft.graph.downloadUrl'])
            # sharelink = link.json()['link']['webUrl']
            # downloadlink = create_onedrive_directdownload(sharelink)
            res_list.append(link.json()['@microsoft.graph.downloadUrl'])
            # print(link)
            # outputf.write(link)
            # p = input(link.status_code)

            # print(link.json())
        if done:
            break

    return res_list
