from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing.')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing_id=listing_id,
                          listing=listing,
                          name=name,
                          email=email,
                          phone=phone,
                          message=message,
                          user_id=user_id,
                          realtor_email=realtor_email)

        contact.save()

        send_mail(
            'Property Listing Inquiry',
            'An enquiry has been made for '+listing+' by '+name+'. Sign in for more details',
            'nikhil6raga@gmail.com',
            [realtor_email, 'ragasai.nikhil2017@vitstudent.ac.in'],
            fail_silently=False
        )

        messages.success(request, 'Your inquiry has been submitted. Realtor will get back to you soon.')
        return redirect('/listings/'+listing_id)
