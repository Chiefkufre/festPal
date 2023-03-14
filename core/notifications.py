
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


from decouple import config



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