from django.contrib import admin
from .models import User,Word

# Register your models here.

#admin.site.register(Word)
admin.site.register(User)

class WordAdmin(admin.ModelAdmin):
    list_display = ('expression', 'part_of_speech')

admin.site.register(Word,WordAdmin)