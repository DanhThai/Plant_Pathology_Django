from django.contrib import admin

from UserProfile.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(PredictHistory)
