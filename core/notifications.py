import uuid

from decouple import config
from twilio.jwt.access_token import AccessToken
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.jwt.access_token.grants import ChatGrant, VideoGrant, VoiceGrant

twilio_acct_sid = config("TWILIO_ACC_SID")
twilio_auth_token = config("TWILIO_AUTH_TOKEN")
twilio_phone_no = config("TWILIO_NUMBER")
twilio_whatsapp_no = config("TWILIO_WHATSAPP_NO")
twilio_api_key = config("TWILIO_API_KEY")

from core.database import db
from core.models import Room

client = Client(twilio_acct_sid, twilio_auth_token)



def sendNotification(recipent_no, msg):

    client.messages.create(
        to = recipent_no,
        from_ = twilio_phone_no,
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



def create_room(room_name, vlp_id):

    # Generate a unique identifier for the room
    identifier = str(uuid.uuid4())

    # Create the room in the database
    room = Room(name=room_name, sid=identifier, vlp_id=vlp_id)
    db.session.add(room)
    db.session.commit()

    # Create a new TwiML Voice response
    resp = VoiceResponse()

    # Play the welcome message
    music = resp.play('https://api.twilio.com/cowbell.mp3')

    # Connect the user to the room
    dial = resp.dial()

    dial.conference(identifier, startConferenceOnEnter=True, endConferenceOnExit=True)

    # Return the room SID
    return identifier, music



def generate_token(room, room_sid, identity):
    # Create an access token with the given identity
    token = AccessToken(twilio_acct_sid, twilio_api_key, twilio_auth_token, identity=identity)

    # Add a grant to the token for joining the room with the given SID
    video_grant = VideoGrant(room=room)
    token.add_grant(video_grant)

    # Add an audio grant to the token
    # audio_grant = AudioGrant(room=room_sid)
    # token.add_grant(audio_grant)

    chat_grant = ChatGrant(service_sid=room_sid)

    # Return the token
    return token.to_jwt()