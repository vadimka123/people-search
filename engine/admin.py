from django.contrib import admin
from django.utils.html import format_html

from engine.models import SearchInfo, SearchResult


class SearchResultInlineAdmin(admin.TabularInline):
    model = SearchResult
    fields = ('person_name', 'names', 'gender', 'dob', 'addresses', 'phones', 'emails', 'jobs', 'educations',
              'ethnicities', 'images',)
    readonly_fields = fields
    can_delete = False

    def names(self, obj):
        names = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.names:
                continue
            names += posible_person.names
        return '\n'.join(sorted(list(set(names))))
    names.short_description = 'Possible Names'

    def gender(self, obj):
        genders = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.gender or posible_person.gender in genders:
                continue
            genders.append(posible_person.gender)
        return '\n'.join(sorted(genders))
    gender.short_description = 'Possible Genders'

    def dob(self, obj):
        dobs = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.dob or posible_person.dob in dobs:
                continue
            dobs.append(posible_person.dob)
        return '\n'.join([dob.strftime('%m %d %Y') for dob in sorted(dobs)])
    dob.short_description = "Possible DOB's"

    def addresses(self, obj):
        addresses = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.addresses:
                continue
            addresses += posible_person.addresses
        return '\n'.join(sorted(list(set(addresses))))
    addresses.short_description = 'Possible Addresses'

    def phones(self, obj):
        phones = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.phones:
                continue
            phones += posible_person.phones
        return '\n'.join(sorted(list(set(phones))))
    phones.short_description = 'Possible Phones'

    def emails(self, obj):
        emails = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.emails:
                continue
            emails += posible_person.emails
        return '\n'.join(sorted(list(set(emails))))
    emails.short_description = 'Possible Emails'

    def jobs(self, obj):
        jobs = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.jobs:
                continue
            jobs += posible_person.jobs
        return '\n'.join(sorted(list(set(jobs))))
    jobs.short_description = 'Possible Jobs'

    def educations(self, obj):
        educations = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.educations:
                continue
            educations += posible_person.educations
        return '\n'.join(sorted(list(set(educations))))
    educations.short_description = 'Possible Educations'

    def ethnicities(self, obj):
        ethnicities = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.ethnicities:
                continue
            ethnicities += posible_person.ethnicities
        return '\n'.join(sorted(list(set(ethnicities))))
    ethnicities.short_description = 'Possible Ethnicities'

    def images(self, obj):
        images = []
        for posible_person in obj.posible_persons.all():
            if not posible_person.images:
                continue
            images += posible_person.images
        images = list(set(images))
        return format_html(''.join(['<img src="{}" width="100px" height="100px" />'.format(image) for image in images]))
    images.short_description = 'Images'
    images.allow_tags = True

    def has_add_permission(self, request):
        return False


class SearchInfoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (SearchResultInlineAdmin,)

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.pk:
            self.readonly_fields = ('name',)
            self.exclude = ("image",)
        form = super(SearchInfoAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(SearchInfo, SearchInfoAdmin)
