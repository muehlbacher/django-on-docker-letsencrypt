import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        imagename = request.POST.get('imagename')
        image_file = request.FILES["image_file"]
        file_name = image_file.name
        file_extension = os.path.splitext(file_name)[1]
        print("content type:" + image_file.content_type)
        fs = FileSystemStorage()
        filename = fs.save(imagename + file_extension, image_file )
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")
