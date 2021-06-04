from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from home.models import Contact
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about_us(request):
    return render(request, 'about.html')


def contact_us(request):

    # The value of method is 'post' in the form tag of html file.
    if request.method == "POST":

        # store the values of form in variables.
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email_id")
        phone = request.POST.get("phone_no.")
        desc = request.POST.get("description")

        # set conditions for input form fields are mandatory or optional.
        if (fname != "" and lname != "" and email != "" and phone != ""):
            
            # store data of models in a funtion variable and save.
            contact_us = Contact(fname=fname, lname=lname, email=email, phone=phone, description=desc, date=datetime.today())
            contact_us.save()

            # create an alert message for form submition.
            messages.success(request, "Details submit successfully")
            
        else:    
            
            messages.warning(request, "Fieds are empty")
    
    return render(request, 'contact.html')


def analyze(request):
    # store the value of input text to variable.
    text = request.GET.get('text', 'default')
    print("------------------------", text)
    
    # store the input of checkboxes in variables.
    inp1 = request.GET.get('removepunc', 'off')    # Remove Punctuations
    inp2 = request.GET.get('fullcaps', 'off')    # Uppercase
    inp3 = request.GET.get('removeline', 'off')    # Newline remover
    inp4 = request.GET.get('removespace', 'off')    # Remove extra space
    inp5 = request.GET.get('charcount', 'off')    # Character count

    # create conditions for checkbox if one or more than one checkboxes are 'on'.
    if inp1 == 'on':
        analyzed = ""
        punctuations = '''\\~!@#$%^&*()_+-=[]{};':",./<>?|'''
        for i in text:
            if i not in punctuations:
                analyzed = analyzed + i
        params = {'purpose':'Remove Punctuations', 'analyzed_text':analyzed, 'text':text}
        text = analyzed
    
    if inp2 == 'on':
        analyzed = text.upper()
        params = {'purpose':'Change to uppercase', 'analyzed_text':analyzed, 'text':text}
        text = analyzed

    if inp3 == 'on':
        analyzed = ''' 
        '''
        for i in text:
            if i != "\n" and i != "\r":
                analyzed = analyzed + i

        params = {'purpose':'Remove new lines', 'analyzed_text':analyzed, 'text':text}
        text = analyzed

    if inp4 == 'on':
        analyzed = ""
        for i in range(len(text)):
            if text[i] == " " and text[i+1] == " ":
                pass
            else:
                analyzed = analyzed + text[i]
            
        params = {'purpose':'Remove extra space', 'analyzed_text':analyzed, 'text':text}
        text = analyzed

    if inp5 == 'on':
        analyzed = len(text)
            
        params = {'purpose':'Character count', 'analyzed_text':analyzed, 'text':text}
        text = analyzed

    # create conditions for checkbox if user not choose any checkbox.
    if (inp1 != 'on' and inp2 != 'on' and inp3 != 'on' and inp4 != 'on' and inp5 != 'on'):
        messages.warning(request, 'Please select any one or more checkbox.')
        return render(request, 'home.html')

    # rendering the html file with template variable
    return render(request, 'analyzed.html', params)
