from django.contrib import admin
from .models import AboutUs,Contact,Feedback,DonorBlogPost,Payment
admin.site.register(DonorBlogPost)
admin.site.register(Contact)
admin.site.register(Feedback)
admin.site.register(AboutUs)
admin.site.register(Payment)
# Register your models here.
