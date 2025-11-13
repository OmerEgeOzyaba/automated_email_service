from scrapy.mail import MailSender
from twisted.internet import reactor

class EmailSender:
    def __init__(self, email, psw, recipients = [], cc = []):
        self.email = email
        self.mailer = MailSender(
                mailfrom = email,
                smtphost="smtp.gmail.com",
                smtpport=587,
                smtpuser = email,
                smtppass= psw,
                smtptls=True,
                smtpssl=False
                )
        self.recipients = recipients
        self.cc = cc

    def add_recipient(self, recipient_email):
        self.recipients.append(recipient_email)

    def add_cc(self, cc_email):
        self.cc.append(cc_email)

    def send_email(self, subject_line, body_msg):
        deferred = self.mailer.send(
                to = self.recipients,
                subject = subject_line,
                body = body_msg,
                cc = self.cc
                )

        return deferred


    def send_confirmation(self, result):
        print("Email successfully sent to the recepient")
        print("SUCCESS:", result)

        # Now send confirmation email to yourself
        confirmation = self.mailer.send(
            to=[self.email],  # Send to yourself
            subject="Confirmation: Automated Email Sent Successfully",
            body="Your automated email was sent successfully.",
            cc=[]
        )

        return confirmation  # Return the deferred for chaining

    def confirmation_success(self, result):
        print("Confirmation email sent")
        reactor.stop()

    def failure(self, error):
        print("FAILURE:", error.value)
        reactor.stop()

    def chain_callbacks(self, deferred, send_confirmation, confirmation_success, failure):
        deferred.addCallback(send_confirmation)
        deferred.addCallback(confirmation_success)
        deferred.addErrback(failure)

        reactor.run()


