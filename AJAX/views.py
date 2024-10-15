import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import ContactForm
from django.http import JsonResponse
from django.shortcuts import render
import threading

def contact(request):
    form = ContactForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            # Get all url files
            files = request.FILES.getlist("files")
            files_paths = get_paths_to_files_stored_in_memory(files)
            # Send email in background
            threading_emails = threading.Thread(
                target=send_email,
                args=(
                    "Nuevo aviso",  # subject
                    ["mi@correo.com"],  # to
                    "contact_email.txt",  # template_txt
                    "contact_email.html",  # template_html
                    {  # data
                        "name": form.cleaned_data.get("name"),
                        "email": form.cleaned_data.get("email"),
                        "message": form.cleaned_data.get("message"),
                    },
                    files_paths,  # attachments
                ),
            )

            threading_emails.start()
            # Response
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "ko", "errors": form.errors})
    return render(request, "public/contact.html", {"form": form})





def send_email(
    subject="Nuevo aviso",
    to=[],
    template_txt="",
    template_html="",
    data={},
    attachments=[],
):
    """Send email"""
    msg = EmailMultiAlternatives(
        subject,
        render_to_string(template_txt, data),
        settings.DEFAULT_FROM_EMAIL,
        to,
    )
    msg.attach_alternative(render_to_string(template_html, data), "text/html")
    for attachment in attachments:
        msg.attach_file(attachment)
    msg.send()


def get_paths_to_files_stored_in_memory(files):
    """Get paths to files stored in memory"""

    def get_url_from_memory_file(file):
        path = default_storage.save("tmp/" + str(file), ContentFile(file.read()))
        return os.path.join(settings.MEDIA_ROOT, path)

    return list(map(get_url_from_memory_file, files))


