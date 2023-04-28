# Import library
import scrapy
import re
import datetime
import csv
import uuid
from AirlineReviews.items import AirlineReviewsItem

# Create Spider class
class AirlineReviewCrawler(scrapy.Spider):
    # Name of spider
    name = 'AirlineReviewCrawler'
    allowed_domains = ['airlinequality.com']

    def start_requests(self):
        with open('/Users/joelljungstrom/PycharmProjects/AirlineReviewOverview/AirlineReviewCounts/AirlineReviewCounts/spiders/AirlineReviewCounts.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                slug = row['Slug']
                reviews = int(row['Reviews'])
                airline = row['AirlineName']

                url = f'https://www.airlinequality.com/airline-reviews/{slug}/page/1/?sortby=post_date%3ADesc&pagesize=100'
                yield scrapy.Request(url=url, callback=self.parse, meta={'airline': airline})

    # Parses the website
    def parse(self, response):
        reviews = response.xpath('//article[@itemprop="review"]')
        for review in reviews:
            # Airline Name
            airline = response.meta['airline']
            Airline = airline

            # Generate a unique ID for the review
            unique_id = uuid.uuid4()

            # OverallScore
            try:
                OverallScore = review.xpath('./div/span[1]/text()').extract_first()
            except:
                OverallScore = ''

            # Title
            try:
                title_text = review.xpath('././div/h2/text()').extract_first()
                Title = title_text.strip('""')
            except:
                Title = ''

            # OriginCountry
            try:
                OriginCountry = review.xpath('.//h3[@class="text_sub_header userStatusWrapper"]/text()')\
                    .re(r'\((.*?)\)')[0].strip()
            except:
                OriginCountry = ''

            # DatePub
            try:
                DatePub = review.xpath('././div/h3/time/text()').extract_first()
            except:
                DatePub = ''

            # Aircraft
            try:
                aircraft_text = review.xpath('.//td[@class="review-rating-header aircraft "]/../td[2]/text()').extract_first()
                Aircraft = aircraft_text.replace(',', " ")
            except:
                Aircraft = ''

            # TravelType
            try:
                TravelType = review.xpath('.//td[@class="review-rating-header type_of_traveller "]/../td[2]/text()').extract_first()
            except:
                TravelType = ''

            # CabinType
            try:
                CabinType = review.xpath('.//td[@class="review-rating-header cabin_flown "]/../td[2]/text()').extract_first()
            except:
                CabinType = ''

            # Route
            try:
                route_text = review.xpath('.//td[@class="review-rating-header route "]/../td[2]/text()').extract_first()
                Route = route_text.replace(';', '')
            except:
                Route = ''

            # DateFlown
            try:
                DateFlown = review.xpath('.//td[@class="review-rating-header date_flown "]/../td[2]/text()').extract_first()
            except:
                DateFlown = ''

            # SeatComfortRating
            try:
                SeatComfortRatingPrep = review.xpath('.//td[@class="review-rating-header seat_comfort"]/../td[2]/span/@class').extract()
                SeatComfortRating = SeatComfortRatingPrep.count('star fill')
            except:
                SeatComfortRating = ''

            # ServiceRating
            try:
                ServiceRatingPrep = review.xpath('.//td[@class="review-rating-header cabin_staff_service"]/../td[2]/span/@class').extract()
                ServiceRating = ServiceRatingPrep.count('star fill')
            except:
                ServiceRating = ''

            # FoodRating
            try:
                FoodRatingPrep = review.xpath('.//td[@class="review-rating-header food_and_beverages"]/../td[2]/span/@class').extract()
                FoodRating = FoodRatingPrep.count('star fill')
            except:
                FoodRating = ''

            # EntertainmentRating
            try:
                EntertainmentRatingPrep = review.xpath('.//td[@class="review-rating-header inflight_entertainment"]/../td[2]/span/@class').extract()
                EntertainmentRating = EntertainmentRatingPrep.count('star fill')
            except:
                EntertainmentRating = ''

            # GroundServiceRating
            try:
                GroundServiceRatingPrep = review.xpath('.//td[@class="review-rating-header ground_service"]/../td[2]/span/@class').extract()
                GroundServiceRating = GroundServiceRatingPrep.count('star fill')
            except:
                GroundServiceRating = ''

            # WifiRating
            try:
                WifiRatingPrep = review.xpath('.//td[@class="review-rating-header wifi_and_connectivity"]/../td[2]/span/@class').extract()
                WifiRating = WifiRatingPrep.count('star fill')
            except:
                WifiRating = ''

            # ValueRating
            try:
                ValueRatingPrep = review.xpath('.//td[@class="review-rating-header value_for_money"]/../td[2]/span/@class').extract()
                ValueRating = ValueRatingPrep.count('star fill')
            except:
                ValueRating = ''

            # Recommended
            Recommended = review.xpath('.//td[@class="review-value rating-yes"]/text()')
            if Recommended:
                Recommended = Recommended.extract_first()
            else:
                Recommended = 'no'

            # Review
            try:
                # Get the year which review was published (Verified reviews was introduced in the beginning of 2017.
                # Reviews before then have to be scraped with a different path)
                year_pub = DatePub[-4:]
                year_pub = datetime.datetime.strptime(year_pub, '%Y').year
                if year_pub > 2016:
                    review_text = review.xpath('.//div[@class="text_content "]/text()').extract()
                    if review_text:
                        # Check if the review starts with the ✅ emoji
                        if review_text[0].startswith('✅'):
                            Review = review_text[1].replace('&nbsp;&nbsp;', '').strip().split('| ')[1].strip().replace(';', '').replace('\r\n', ' ')
                        else:
                            Review = review_text[0].replace('&nbsp;&nbsp;', '').strip().split('| ')[1].strip().replace(';', '').replace('\r\n', ' ')
                    else:
                        Review = ''
                elif year_pub <= 2016:
                    review_text = review.xpath('.//div[@class="text_content "]/text()').extract()
                    if review_text:
                        Review = review_text
                    else:
                        ''
                else:
                    Review = ''
            except:
                Review = ''

            # TripVerified
            try:
                TripVerified = review.xpath('.//div[1]/strong/a/em/text()').extract()
            except:
                TripVerified = ''

            item = AirlineReviewsItem()
            item['unique_id'] = unique_id
            item['AirlineName'] = Airline
            item['OverallScore'] = OverallScore
            item['Title'] = Title
            item['OriginCountry'] = OriginCountry
            item['DatePub'] = DatePub
            item['Aircraft'] = Aircraft
            item['TravelType'] = TravelType
            item['CabinType'] = CabinType
            item['Route'] = Route
            item['DateFlown'] = DateFlown
            item['SeatComfortRating'] = SeatComfortRating
            item['ServiceRating'] = ServiceRating
            item['FoodRating'] = FoodRating
            item['EntertainmentRating'] = EntertainmentRating
            item['GroundServiceRating'] = GroundServiceRating
            item['WifiRating'] = WifiRating
            item['ValueRating'] = ValueRating
            item['Recommended'] = Recommended
            item['Review'] = Review
            item['TripVerified'] = TripVerified

            yield item
        pass
