from email.policy import default
from enum import unique
import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PropertyPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = 'For Sale', _("For Sale")
        FOR_RENT = 'For Rent', _("For Rent")
        AUCTION = 'Auction', _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(User, verbose_name=_("Agent, Seller or Buyer"),
                             related_name="agent_buyer", on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(verbose_name=_("Property Reference Code"), max_length=255, unique=True, blank=True)
    description = models.TextField(verbose_name=_("Description"),
                                   default="Deffault description....Update me please....")
    country = CountryField(verbose_name=_("Country"), default="IN", blank_label="(Select Country)")
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Mumbai")
    postal_code = models.CharField(verbose_name=_("Postal Code"), max_length=100, default="0000")
    street_address = models.CharField(verbose_name=_("Street Address"), max_length=200, default="Please Update Street")
    property_number = models.IntegerField(verbose_name=_("Property Number"), validators=[
                                          MinValueValidator(1)], default=111)
    price = models.DecimalField(verbose_name=_("Property Price"), max_digits=10, decimal_places=2, default=0.0)
    tax = models.DecimalField(verbose_name=_("Property Tax"), max_digits=8,
                              decimal_places=2, default=0.15, help_text="15% Property Tax")
    plot_area = models.DecimalField(verbose_name=_("Plot Area in Sqr.Meters"),
                                    max_digits=10, decimal_places=2, default=0.0)
    total_floors = models.IntegerField(verbose_name=_("Number of Floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Number of Bedrooms"), default=0)
    bathrooms = models.IntegerField(verbose_name=_("Number of Bathrooms"), default=0)
    advert_type = models.CharField(verbose_name=_("Advert Typer"), max_length=50,
                                   choices=AdvertType.choices, default=AdvertType.FOR_SALE)
    property_type = models.CharField(verbose_name=_("Property Type"), max_length=50,
                                     choices=PropertyType.choices, default=PropertyType.OTHER)
    cover_photo = models.ImageField(verbose_name=_("Cover Photo"),
                                    default="sample_images/house_sample.jpg", null=True, blank=True)
    photo1 = models.ImageField(default="interior_sample.jpg", null=True, blank=True)
    photo2 = models.ImageField(default="interior_sample.jpg", null=True, blank=True)
    photo3 = models.ImageField(default="interior_sample.jpg", null=True, blank=True)
    photo4 = models.ImageField(default="interior_sample.jpg", null=True, blank=True)
    published_status = models.BooleanField(verbose_name=_("Published Status"), default=False)
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address of Viewers"), max_length=250)
    property = models.ForeignKey(Property, related_name="property_views", on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"Total views on -{self.property.title} is {self.property.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Property"
        verbose_name_plural = "Total Property Views"
