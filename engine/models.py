import jsonfield
import os
import requests

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from engine.detect_face import FaceDetector
from engine.find_names import FindName
from engine.image_search import ImageSearch
from engine.social_search import SocialSearch


def get_upload_to_patch(instance, filename):
    return os.path.join('media', filename)


class SearchInfo(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=get_upload_to_patch)

    def __str__(self):
        return self.name or '{} #{}'.format('Search Info', self.pk)


class SearchResult(models.Model):
    search_info = models.ForeignKey(SearchInfo, related_name='search_results', on_delete=models.CASCADE)
    person_name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.person_name


class PosiblePerson(models.Model):
    search_result = models.ForeignKey(SearchResult, related_name='posible_persons', on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, null=True)

    dob = models.DateField(null=True)

    jobs = jsonfield.JSONField(null=True)

    addresses = jsonfield.JSONField(null=True)

    educations = jsonfield.JSONField(null=True)

    ethnicities = jsonfield.JSONField(null=True)

    phones = jsonfield.JSONField(null=True)

    emails = jsonfield.JSONField(null=True)

    names = jsonfield.JSONField(null=True)

    images = jsonfield.JSONField(null=True)

    def __str__(self):
        return self.names[0] if self.names and len(self.names) > 0 else self.pk


def parse_search_result(search_result, person):
    gender = person.gender.display if hasattr(person, 'gender') and person.gender else None
    dob = person.dob.date_range.middle if hasattr(person, 'dob') and person.dob and person.dob.date_range else None
    jobs = [job.display for job in person.jobs or [] if job.display] if hasattr(person, 'jobs') else []
    addresses = [address.display for address in person.addresses or [] if address.display] if hasattr(person, 'addresses') else []
    educations = [education.display for education in person.educations or [] if education.display] if hasattr(person, 'educations') else []
    ethnicities = [ethnicity.display for ethnicity in person.ethnicities or [] if ethnicity.display] if hasattr(person, 'ethnicities') else []
    phones = [phone.display for phone in person.phones or [] if phone.display] if hasattr(person, 'phones') else []
    emails = [email.display for email in person.emails or [] if email.display] if hasattr(person, 'emails') else []
    names = [name.display for name in person.names or [] if name.display] if hasattr(person, 'names') else []
    images = []
    checked = []
    if hasattr(person, 'images'):
        for image in person.images:
            if not image.url or image.url in checked:
                continue

            checked.append(image.url)

            try:
                r = requests.get(image.url)
            except Exception:
                continue

            if 'image' not in r.headers.get('Content-Type', ''):
                continue

            images.append(image.url)

    return PosiblePerson(search_result=search_result, gender=gender, dob=dob, jobs=jobs, addresses=addresses,
                         educations=educations, ethnicities=ethnicities, phones=phones, emails=emails,
                         names=names, images=images)


@receiver(post_save, sender=SearchInfo)
def invitation_post_save(sender, instance, created, **kwargs):
    if created:
        FaceDetector(str(instance.pk), instance.image.url).detect()
        print('Face Detected')
        image_search_results = ImageSearch(str(instance.pk)).search()
        print('Image Searched', image_search_results)
        search_results = []
        for image_url, results in image_search_results.items():
            name = FindName(results).find()
            if not name:
                continue
            search_results.append(SearchResult(search_info=instance, person_name=name))

            if len(search_results) == 50:
                SearchResult.objects.bulk_create(search_results)
                search_results = []

        if len(search_results) > 0:
            SearchResult.objects.bulk_create(search_results)

        print('names founded')

        posible_persons = []
        for search_result in instance.search_results.all():
            first_name, last_name = search_result.person_name.split(' ', 2)
            result = SocialSearch(name=search_result.person_name).search()
            if result and result.person:
                names = result.person.names
                is_exist_name = next((name for name in names if first_name in name.display and last_name in name.display), None)
                if is_exist_name:
                    posible_persons.append(parse_search_result(search_result, result.person))

            for person in result.possible_persons:
                names = person.names
                is_exist_name = next((name for name in names if first_name in name.display and last_name in name.display), None)
                if is_exist_name:
                    posible_persons.append(parse_search_result(search_result, person))

                if len(posible_persons) >= 50:
                    PosiblePerson.objects.bulk_create(posible_persons)
                    posible_persons = []

            if len(posible_persons) > 0:
               PosiblePerson.objects.bulk_create(posible_persons)

        print('social search is done')
