from twilio.rest import Client

account_sid = 'AC0aee33b35d39b3feb0d98c2262a955b8'
auth_token = 'b77569c4298ff5c1c83ccec72da08360'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='You violated',
         from_='+14804093877',
         to='+917355714487'
     )

print(message.sid)