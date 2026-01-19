import json

data = [
{"name": "John",  "age": 30,  "isMarried": True,
   "address": {
       "street": "123 Main St",
       "city": "New York",
       "state": "NY",
       "zipCode": "10001",
        "coordinates":
            { "latitude": 40.7128, "longitude": -74.0060 }
   },
   "phoneNumbers": [
        {"type": "home", "number": "555-1234" },
        {"type": "work", "number": "555-5678",
            "extensions": [
                  {"extNum": "1234",  "department": "Sales"},
                  {"extNum": "5678",  "department": "Support"}
              ]
            }
   ],
   "children": [
       {
           "name": "Jane",
           "age": 5,
           "isMarried": False,
           "toys": [
               {
                   "name": "Teddy Bear",  "color": "brown"},
               {  "name": "Barbie Doll",  "color": "pink" }
           ]
       },
       {
           "name": "Bob",
           "age": 7,
           "isMarried": False,
           "toys": [
               {  "name": "Lego Set",  "color": "multicolor"   },
               {  "name": "Transformers",  "color": ["red", "blue", "yellow"]   }
           ]
       }
   ]  }
]

with open('2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


