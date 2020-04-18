from random import *
import json
import requests
from bs4 import BeautifulSoup

def getFact():
	topics = ['9-11', 'Africa', 'Alaska', 'Alexander-The-Great', 'Amazon-Rainforest', 'Ancient-Greece', 'Roman', 'Animal-Testing', 'Animal', 'Anne-Frank', 'Antarctica', 'Apple', 'Argentina', 'Asia', 'Atomic-Bomb', 'Auschwitz', 'Australia', 'Autism', 'Baby', 'Bacteria', 'Banana', 'Barack-Obama', 'Bear', 'Beer', 'Benjamin-Franklin', 'Berlin-Wall', 'Bible', 'Big-Ben', 'Bill-Gates', 'Blood', 'Bolivia', 'Brain', 'Brazil', 'Breast-Cancer', 'Buddhism', 'Bullying', 'California', 'Canada', 'Cancer', 'Car', 'Cat', 'Chimpanzee', 'China', 'Chocolate', 'Christianity', 'Christmas', 'Christopher-Columbus', 'Civil-War', 'Cocaine', 'Cockroach', 'Coffee', 'Colombia', 'Cuba', 'D-Day', 'Death', 'Death-Penalty', 'Denmark', 'Depression', 'Desert', 'Dinosaur', 'Disney', 'Divorce', 'Dog', 'Dolphin', 'Drug', 'Earth', 'Earthquake', 'Egypt', 'Eiffel-Tower', 'Albert-Einstein', 'Elephant', 'Elvis-Presley', 'English', 'Eye', 'Facebook', 'Family-Guy', 'Fidel-Castro', 'Finland', 'Fish', 'Florida', 'Food', 'France', 'Fruit', 'Fun', 'George-Washington', 'Germany', 'Giraffe', 'Global-Warming', 'Gold', 'Golden-Gate-Bridge', 'Google', 'Harry-Potter', 'Hawaii', 'Health', 'Heart-Disease', 'Hinduism', 'History', 'Hitler', 'Holocaust', 'Horse', 'Iceland', 'India', 'Indonesia', 'Internet', 'Inventor', 'Ireland', 'Isaac-Newton', 'Islam', 'Israel', 'Italy', 'Japan', 'Jesus', 'JFK', 'Judaism', 'Kissing', 'Koala', 'Las-Vegas', 'Left-Handed', 'Leonardo-Da-Vinci', 'Life', 'Lightning', 'Abraham-Lincoln', 'Lion', 'London', 'Love', 'Marijuana', 'Marriage', 'Mars', 'Martin-Luther-King-Jr', 'Math', 'McDonalds', 'Men', 'Mexico', 'Mobile-Phone', 'Money', 'Monkey', 'Moon', 'Mount-Everest', 'Movie', 'Music', 'Nelson-Mandela', 'New-York', 'New-Zealand', 'North-Korea', 'Norway', 'Obesity', 'Ocean', 'Octopus', 'Panda', 'Paraguay', 'Penguin', 'Peru', 'Phobia', 'Pluto', 'Pollution', 'Poverty', 'Pregnancy', 'Psychology', 'Recycling', 'Russia', 'Saturn', 'Science', 'Shakespeare', 'Shark', 'Slavery', 'Sleep', 'Smoking', 'Snake','Soccer', 'Solar-System', 'South-Africa', 'South-Korea', 'Space', 'Spain', 'Spider', 'Statue-of-Liberty', 'Steve-Jobs', 'Strange', 'Suicide', 'Sun', 'Sustainable-Development', 'Sweden', 'Switzerland', 'Texas', 'The-Netherlands', 'The-Simpsons', 'Tiger', 'Titanic', 'Toilet', 'Twitter', 'UK', 'Unbelievable', 'Uranus', 'USA', 'Venezuela', 'Venus', 'Vietnam-War', 'Volcano', 'Water', 'Weird', 'Whale', 'Women', 'Womens-Rights', 'World-War-I', 'World-War-II', 'Body', 'Heart', 'YouTube', 'Zebra', 'Fact-Of-The-Day']
	#Add random fact
	link = "http://www.factslides.com/s-" + topics[randint(0, (len(topics)-1))]
	html = requests.get(link).text
	soup = BeautifulSoup(html, "html.parser")
	try:
		data = json.loads(soup.find('script', type='application/ld+json').text)
	except:
		getFact()
	else:
		data = data['articleBody']
		factList = data.split(". ")
		fact = factList[randint(0,(len(factList)-1))]
		return fact

