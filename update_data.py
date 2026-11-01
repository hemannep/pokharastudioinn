import json

with open('js/data.js', 'r') as f:
    content = f.read()

# Let's extract APARTMENTS_DATA and HERO_SLIDES, and append REVIEWS_DATA
reviews_data = [
  {
    "id": "rev-1",
    "author": "Laura & Thomas",
    "country": "United Kingdom",
    "avatar": "LT",
    "rating": 5,
    "date": "Stayed at Pokhara Home to Home Apartment",
    "apartment_name": "Pokhara Home to Home Apartment",
    "apartment_id": "23583417",
    "airbnb_url": "https://www.airbnb.com/rooms/23583417#reviews",
    "text": "Ekraj and Heman are outstanding Superhosts! The apartment is spotless, private, and located in such a peaceful area away from the loud music of Lakeside, yet only a quick 10-minute walk when you want restaurants. The kitchen had everything we needed to cook, and the mountain views from the rooftop are breathtaking. Would come back in a heartbeat!"
  },
  {
    "id": "rev-2",
    "author": "Marco Rossi",
    "country": "Italy",
    "avatar": "MR",
    "rating": 5,
    "date": "Stayed at Pokhara Family Home (★ 4.95)",
    "apartment_name": "Pokhara Family Home",
    "apartment_id": "37218276",
    "airbnb_url": "https://www.airbnb.com/rooms/37218276#reviews",
    "text": "We stayed as a family for two weeks. It felt just like our home in Pokhara. Fast reliable Wi-Fi for work, great pressure with continuous hot shower, and a lovely lush garden. Ekraj even safely kept our heavy backpacks while we went trekking to Annapurna Base Camp. 10/10 hospitality!"
  },
  {
    "id": "rev-3",
    "author": "Sophie Chen",
    "country": "Canada",
    "avatar": "SC",
    "rating": 5,
    "date": "Stayed at Peace Zone 1BR & Garden",
    "apartment_name": "Peace Zone 1BR • Kitchen & Garden",
    "apartment_id": "1039685991315991696",
    "airbnb_url": "https://www.airbnb.com/rooms/1039685991315991696#reviews",
    "text": "The ground floor apartment with garden is pure bliss! Super peaceful, wake up to birds singing and lush greenery. The apartment is brand new, spacious 400 sq. ft., and sparkling clean. Whenever I sent a WhatsApp message, Heman responded within seconds. Truly Superhost standard."
  },
  {
    "id": "rev-4",
    "author": "Julian & Emma",
    "country": "Germany",
    "avatar": "JE",
    "rating": 5,
    "date": "Stayed at Sunrise Apartment",
    "apartment_name": "Sunrise Apartment",
    "apartment_id": "30459121",
    "airbnb_url": "https://www.airbnb.com/rooms/30459121#reviews",
    "text": "Amazing bright studio filled with sunlight every morning! The kitchen is fully equipped with gas stove and fridge. We were working remotely and the fiber internet never dropped once. Close to grocery stores and fruit shops. You won't find a better value in Pokhara Lakeside."
  },
  {
    "id": "rev-5",
    "author": "Kenji Tanaka",
    "country": "Japan",
    "avatar": "KT",
    "rating": 5,
    "date": "Stayed at Pokhara Cosy Home Apartment",
    "apartment_name": "Pokhara’s Cosy Home Apartment",
    "apartment_id": "27266098",
    "airbnb_url": "https://www.airbnb.com/rooms/27266098#reviews",
    "text": "Warm and authentic hospitality. The bed was very comfortable and warm during chilly evenings. Located in a safe and quiet residential lane only 100 meters off the main street. Ekraj gave us the best tips for paragliding and local eateries."
  },
  {
    "id": "rev-6",
    "author": "Alexander Petrov",
    "country": "Switzerland",
    "avatar": "AP",
    "rating": 5,
    "date": "Stayed at Pokhara Studio Apartment",
    "apartment_name": "Pokhara Studio Apartment",
    "apartment_id": "27272742",
    "airbnb_url": "https://www.airbnb.com/rooms/27272742#reviews",
    "text": "The hiking hills start right behind the house! We loved doing morning walks up the trail, then having coffee on our private balcony. Sparkling clean bathroom with 24-hr hot water. Ekraj and Heman are the kindest hosts in Nepal."
  }
]

# append or update in js/data.js
if 'const REVIEWS_DATA =' in content:
    content = content[:content.find('const REVIEWS_DATA =')]
content += '\nconst REVIEWS_DATA = ' + json.dumps(reviews_data, indent=2) + ';\n'

with open('js/data.js', 'w') as f:
    f.write(content)

print('Updated js/data.js with REVIEWS_DATA!')
