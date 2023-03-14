
from decouple import config
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse


twilio_acct_sid = config("TWILIO_ACC_SID")
twilio_auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone_no = config("TWILIO_NUMBER")
twilio_whatsapp_no = config("TWILIO_WHATSAPP_NO")



client = Client(twilio_acct_sid, twilio_auth_token)



def sendNotification(recipent_no, msg):

    client.messages.create(
        to = recipent_no,
        from_ = twilio_whatsapp_no,
        body = msg
    )


def sendSMS(recipent_no, msg):

    response = MessagingResponse()

    response.message("{}".format(msg))
    
    # Send the response message to the reciepent phone number

    client.messages.create(
        to= recipent_node,
        from_ = twilio_phone_no,
        body= str(response)
    )



def create_room(room_name):
    
    room_sid = 'your_twilio_room_sid'

    response = VoiceResponse()

    dial = response.dial()

    dial.conference(room_sid)

    room = Room(name=f"Virtual Listening Party {identifier}", sid=room_sid)

    db.session.add(room)
    db.session.commit()



def generate_token(room):
    token = AccessToken(account_sid, auth_token, identity=user.id)
    video_grant = VideoGrant(room=room.sid)
    token.add