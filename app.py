# Bismillah al-Rahmaan al-Raheem
# Ali Shah | Nov. 08, 2020
# WEB1.1 Assignment 3: More Forms

from flask import Flask, request, render_template
from PIL import Image, ImageFilter
from pprint import PrettyPrinter
import json
import os
import random
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

################################################################################
# COMPLIMENTS ROUTES
################################################################################

list_of_compliments = [
    'awesome',
    'beatific',
    'blithesome',
    'conscientious',
    'coruscant',
    'erudite',
    'exquisite',
    'fabulous',
    'fantastic',
    'gorgeous',
    'indubitable',
    'ineffable',
    'magnificent',
    'outstanding',
    'propitioius',
    'remarkable',
    'spectacular',
    'splendiferous',
    'stupendous',
    'super',
    'upbeat',
    'wondrous',
    'zoetic'
]

@app.route('/compliments')
def compliments():
    """Shows the user a form to get compliments."""
    return render_template('compliments_form.html')

@app.route('/compliments_results')
def compliments_results():
    """Show the user some compliments."""

    # Get user inputs from compliments_form.html
    users_name = request.args.get('users_name')
    wants_compliments = request.args.get('wants_compliments')
    num_compliments = int(request.args.get('num_compliments'))

    # Shorthand if-statement to set translate wants_compliments from str to bool
    wants_compliments = True if wants_compliments == 'yes' else False

    # Randomly generate a subset from list_of_compliments
    random_compliments = random.sample(list_of_compliments, num_compliments)

    context = {
        'users_name': users_name,
        'wants_compliments': wants_compliments,
        'random_compliments': random_compliments
    }

    return render_template('compliments_results.html', **context)

################################################################################
# ANIMAL FACTS ROUTE
################################################################################

animals_and_facts = {
    'koala': "Koala fingerprints are so close to humans' that they could taint crime scenes.",
    'parrot': "Parrots will selflessly help each other out.",
    'mantis shrimp': "The mantis shrimp has the world's fastest punch.",
    'lion': "Female lions do 90 percent of the hunting.",
    'narwhal': "Narwhal tusks are really an \"inside out\" tooth."
}

@app.route('/animal_facts')
def animal_facts():
    """Show a form to choose an animal and receive facts."""

    # Generate list of keys and get user input from animal_facts.html
    animals = animals_and_facts.keys()
    users_animals = request.args.getlist('animal')

    context = {
        'animals': animals,
        'users_animals': users_animals,
        'animals_and_facts': animals_and_facts,
    }

    return render_template('animal_facts.html', **context)

################################################################################
# IMAGE FILTER ROUTE
################################################################################

filter_types_dict = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR,
    'detail': ImageFilter.DETAIL,
    'edge-enhance': ImageFilter.EDGE_ENHANCE,
    'emboss': ImageFilter.EMBOSS,
    'sharpen': ImageFilter.SHARPEN,
    'smooth': ImageFilter.SMOOTH
}

def save_image(image, filter_type):
    """Save the image, then return the full file path of the saved image."""

    # Append the filter type at the beginning (in case the user wants to 
    # apply multiple filters to 1 image, there won't be a name conflict)
    new_file_name = f'{filter_type}_{image.filename}'
    image.filename = new_file_name

    # Construct full file path
    file_path = os.path.join(app.root_path, 'static/images', new_file_name)

    # Save the image
    image.save(file_path)

    return file_path

def apply_filter(file_path, filter_name):
    """Apply a Pillow filter to a saved image."""
    img = Image.open(file_path)
    img.thumbnail((500, 500))
    img = img.filter(filter_types_dict.get(filter_name))
    img.save(file_path)

@app.route('/image_filter', methods=['GET', 'POST'])
def image_filter():
    """Filter an image uploaded by the user using the Pillow library."""

    filters = filter_types_dict.keys()

    if request.method == 'GET':
        context = {'filters': filters}
        return render_template('image_filter.html', **context)
    else:  # If request method is 'POST'

        # Save user's image to new file path and apply filter on it
        filter = request.form.get('filter_type')
        image = request.files.get('users_image')
        file_path = save_image(image, filter)
        apply_filter(file_path, filter)

        # Filtered image's URL
        image_url = f'/static/images/{image.filename}'

        context = {
            'filters': filters,
            'image_url': image_url
        }

        return render_template('image_filter.html', **context)

################################################################################
# GIF SEARCH ROUTE
################################################################################

API_KEY = 'LIVDSRZULELA'
TENOR_URL = 'https://api.tenor.com/v1/search'
pp = PrettyPrinter(indent=2)

@app.route('/gif_search', methods=['GET', 'POST'])
def gif_search():
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""

    if request.method == 'GET':
        return render_template('gif_search.html')
    else:  # If request method is 'POST'

        # Save user's GIF search parameters
        search_query = request.form.get('search_query')
        quantity = request.form.get('quantity')

        params = {
            'key': API_KEY,
            'q': search_query,
            'limit': quantity
        }

        # Call API and save the result GIFs
        response = requests.get(TENOR_URL, params=params)
        gifs = json.loads(response.content).get('results')

        context = {'gifs': gifs}

        # Uncomment to see the result JSON
        # pp.pprint(gifs)

        return render_template('gif_search.html', **context)

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
