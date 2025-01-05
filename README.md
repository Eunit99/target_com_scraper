# [Target.com Product Reviews Scraper ](https://apify.com/eunit/target-reviews-scraper) 

[![Target.com Product Reviews Scraper](https://i.postimg.cc/Gt5VsBmf/image.png)](https://apify.com/eunit/target-reviews-scraper)

## Overview  
The [**Target.com Product Reviews Scraper**](https://apify.com/eunit/target-reviews-scraper) is a powerful tool designed to extract product reviews, ratings, and related details directly from Target.com. Whether you’re conducting market research, analyzing customer sentiment, or tracking product performance, this scraper provides structured, easy-to-use data in JSON format.  

## Features  
- Extracts detailed reviews, including:
  - Usernames, timestamps, and review text.
  - Star ratings and secondary ratings (e.g., quality scores).
  - Rating histograms and recommendation percentages.
- Outputs clean, structured JSON for seamless integration.
- Handles large datasets efficiently, saving time and effort.
- Easily customizable for specific scraping needs.  

## Example Output  
```json
{
  "secondary_rating": "quality\n4.6 out of 5",
  "rating_count": "832 star ratings",
  "rating_histogram": "5 stars\n85%\n4 stars\n9%\n3 stars\n3%\n2 stars\n1%\n1 star\n2%",
  "percent_recommended": "90% would recommend",
  "total_recommendations": "155 recommendations",
  "reviews": [
    {
      "title": "no more litter everywhere",
      "rating": "5 out of 5 stars",
      "username": "tryingnewskincareproducts",
      "time": "7 days ago",
      "text": "it did not take long to teach my kittens to use this enclosed litter box..."
    }
  ]
}
```

## Your feedback

We are always working on improving the performance of our Actors. So if you’ve got any technical feedback for the [Target.com Product Reviews Scraper](https://apify.com/eunit/target-reviews-scraper) Actor or simply found a bug, please create an issue on the [Actor’s Issues tab](https://console.apify.com/actors/nNMgUFvnZOKJfh06e/issues) in [Apify Console](https://console.apify.com/actors/nNMgUFvnZOKJfh06e).
