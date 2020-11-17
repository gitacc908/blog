from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150, unique=True, blank=True)
	body = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('detail', kwargs={'slug':self.slug})

	class Meta:
		ordering = ['-timestamp']

class Tag(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True, blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Tag, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('tag_detail', kwargs={'slug':self.slug})

	class Meta:
		ordering = ['title']