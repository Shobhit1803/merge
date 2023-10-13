from django.contrib import admin
from .models import Post, User, Category, Tag, Comment
import csv
from django.http import HttpResponse


# Register your models here.





class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("author", "category", "title", "text", "published_date")
    list_filter = ("author", "category", "title", "published_date")
    search_fields = ["title"]
    autocomplete_fields = ['category', 'author']
    filter_horizontal = ['tag']
    actions = ["export_as_csv"]

@admin.register(Tag)
class Tag(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    actions = ["export_as_csv"]

@admin.register(Category)
class Category(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    actions = ["export_as_csv"]

@admin.register(Comment)
class Comment(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("post", "user", "email", "text", "published_date")
    list_filter = ("post", "user", "email", "published_date")
    search_fields = ["user", "email"]
    actions = ["export_as_csv"]

@admin.register(User)
class User(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("username", "email", "phone_number")
    list_filter = ("username", "email", "phone_number")
    search_fields = ["username"]
    actions = ["export_as_csv"]