# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AirlineReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    unique_id = scrapy.Field()
    AirlineName = scrapy.Field()
    OverallScore = scrapy.Field()
    Title = scrapy.Field()
    OriginCountry = scrapy.Field()
    DatePub = scrapy.Field()
    Aircraft = scrapy.Field()
    TravelType = scrapy.Field()
    CabinType = scrapy.Field()
    Route = scrapy.Field()
    DateFlown = scrapy.Field()
    SeatComfortRating = scrapy.Field()
    ServiceRating = scrapy.Field()
    FoodRating = scrapy.Field()
    EntertainmentRating = scrapy.Field()
    GroundServiceRating = scrapy.Field()
    WifiRating = scrapy.Field()
    ValueRating = scrapy.Field()
    Recommended = scrapy.Field()
    Review = scrapy.Field()
    TripVerified = scrapy.Field()
    pass