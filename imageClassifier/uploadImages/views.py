import json
import boto3
import secrets
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView
from uploadImages.forms import ImageForm
from django.conf import settings
from uploadImages.models import Image
# Create your views here.
def FormView(request):
    if request.method == 'POST':
    
        form = ImageForm(request.POST,request.FILES)
    
        if form.is_valid():
        
            image = request.FILES
            file = image.__getitem__('image')
            prefix='photos/'
            key = secrets.token_urlsafe(8) 
            Key = prefix + key +'.png'
            s3_client = boto3.client('s3')
            #subimos imagen al s3 
            s3_client.put_object(
                
                    Bucket=settings.PHOTO_BUCKET,
                    Key= Key,
                    Body=file,
                    ContentType='image/png',
                )
            #generamos la presigned url
            
            url = s3_client.generate_presigned_url(
                
                    'get_object',
                    Params={'Bucket':settings.PHOTO_BUCKET,'Key':Key})
                    
            #Image rekognition
            
            rek = boto3.client('rekognition')
            
            response = rek.detect_labels(
                
                    Image={
                        
                        'S3Object':{
                            'Bucket':settings.PHOTO_BUCKET,
                            'Name':Key,
                        }
                    })
            
            labels = [label for label in response['Labels']]
            user = request.session.__getitem__('nickname')
            slug = user + '-'+ key
            
            
            
            #guardamos metadata de la imagen en la base de datos
            image= Image.objects.create(
                
                user = user,
                key = key,
                labels=json.dumps(labels),
                slug = slug)
            
            
            image.save()
            
            return redirect(reverse('imageview', kwargs={'slug':slug}))
            
    else:
        
        form = ImageForm()
        
    return render(request,'uploadImages/upload.html',{'form':form})
    

class ImageDetailView(DetailView):
    
    model = Image
    template_name = 'uploadImages/image.html'
    
    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        
        s3_client = boto3.client('s3')
        
        url = s3_client.generate_presigned_url(
                
                    'get_object',
                    Params={'Bucket':settings.PHOTO_BUCKET,'Key':'photos/' + self.object.key +'.png'  })
        
        context['url'] = url
        
        context['labels'] = json.loads(self.object.labels)
            
        return context
        
    