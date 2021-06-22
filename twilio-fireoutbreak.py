from twilio.rest import Client
def fireoutbreak():
    account_sid = 'ACcf81279b0973c435ecbdfb66c2b5822d'
    auth_token = '85a808f12bf7d3e88dfeda72dcc2ef4d'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='화재 발생,위치는 정왕동 한국산업기술대학교 e동',
        from_='13476868137',
        to='821085904378'
    )
    print(message.sid)

fireoutbreak()
