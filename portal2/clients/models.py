from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


#Business model. Basis is a design studio, who has clients, and users.
	#Fairly simple, should just need a title, a date joined, and then Clients and Users can foreignkey to it. 
class Business(models.Model):
	title = models.CharField(max_length=255)
	dob = models.DateField(default=timezone.now().date())

	def __unicode__(self):
		return self.title

	def admin_url(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


#Clients model. A client may have many websites. 
	#Needs title, date joined, possibly it's own email and contact number. Needs a foreignkey to businesses.
class Client(models.Model):
	title = models.CharField(max_length=255)
	dob = models.DateField(default=timezone.now().date())

	def __unicode__(self):
		return self.title

	def admin_url(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


#User model. Users are associated with a client, and are able to create tickets.
	#Needs to be able to log in, log out, change and reset passwords. Needs to have a foreignkey to businesses. Needs title, email address, passwords, and all the standard user stuff...
class CustomUser(User):
	client = models.ForeignKey('Client')


#Website model. A website has hostings, and may have tickets associated with it. 
	#Needs title, url, dob, foreignkey to which client owns it, and probably which business owns it.
class Website(models.Model):
	client = models.ForeignKey('Client')
	title = models.CharField(max_length=254)
	url = models.URLField()
	dob = models.DateField(verbose_name="Date of birth")

	def __unicode__(self):
		return self.title

	def admin_url(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


#Hosting model. Hosting costs money, and will have to be renewed over time. 
	#Needs to be associated with a website, a client, and a business. Needs a cost and a renewal date. The renewal date tells us when the client/business must pay up. 
class Hosting(models.Model):
	website = models.ForeignKey('Website')
	client = models.ForeignKey('Client')
	cost = models.DecimalField(max_digits=7, decimal_places=2)
	renewal_date = models.DateField()	

	def renewal_date_order(self):
		return []

	renewal_date_order.admin_order_field = 'client'
	def __unicode__(self):
		return self.client.title

	class Meta: 
		verbose_name_plural ="Hosting"

	
	def renewal_date_passed(self):
		if datetime.datetime.now().day > self.renewal_date.day:
			return "Renewal date passed"
		else:
			return ""

	def admin_url(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

#Ticket model. Users describe what they want us to do, and how urgently we need to do it. 
	#Needs to be foreignkey associated with a website, user, business and client, though we should be able to get those from the User who submits the form. Needs a dob, title, and text box.
class Ticket(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	client = models.ForeignKey('Client')
	website = models.ForeignKey('Website')
	title = models.CharField(max_length=255, null = True)
	ticket = models.TextField()
	urgent = models.BooleanField(default=False)
	dob = models.DateTimeField(default=timezone.now())

	def __unicode__(self):
		return self.title