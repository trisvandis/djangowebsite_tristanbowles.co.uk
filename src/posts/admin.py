from django.contrib import admin
from .models import Post  #imports Post class from posts.models as they share the same directory, can just reference '.models'


class PostAdmin(admin.ModelAdmin):
  list_display = ["__str__", "updated", "timestamp"]
  list_filter = ["updated", "timestamp"]
  search_fields = ["title", "content"]
  
  class Meta:
    model = Post


admin.site.register(Post, PostAdmin)
