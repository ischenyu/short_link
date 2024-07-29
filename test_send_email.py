import resend

resend.api_key = 're_TRqawMh1_5wLdr6z8L5f777nk9t9yr7aN'

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["abb1234aabb@gmail.com"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

r = resend.Emails.send(params)

print(r)
