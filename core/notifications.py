import uuid

from decouple import config
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

twilio_acct_sid = config("TWILIO_ACC_SID")
twilio_auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone_no = config("TWILIO_NUMBER")
twilio_whatsapp_no = config("TWILIO_WHATSAPP_NO")

from core.models import Room

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

    # Generate a unique identifier for the room
    identifier = str(uuid.uuid4())

    # Create the room in the database
    room = Room(name=room_name, sid=identifier)
    db.session.add(room)
    db.session.commit()

    # Create a new TwiML Voice response
    resp = VoiceResponse()

    # Play the welcome message
    resp.play('https://api.twilio.com/cowbell.mp3')

    # Connect the user to the room
    dial = resp.dial()

    dial.conference(identifier, startConferenceOnEnter=True, endConferenceOnExit=True)

    # Return the room SID
    return identifier


def generate_token(identity, room_sid):
    # Create an access token with the given identity
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Add a grant to the token for joining the room with the given SID
    video_grant = VideoGrant(room=room_sid)
    token.add_grant(video_grant)

    # Add an audio grant to the token
    audio_grant = AudioGrant()
    token.add_grant(audio_grant)

    # Return the token
    return token.to_jwt().decode()