"""
A restaurant recommendation system.

Here are some example dictionaries.  These correspond to the information in
restaurants_small.txt.

Restaurant name to rating:
# dict of {str: int}
{'Georgie Porgie': 87,
 'Queen St. Cafe': 82,
 'Dumplings R Us': 71,
 'Mexican Grill': 85,
 'Deep Fried Everything': 52}

Price to list of restaurant names:
# dict of {str, list of str}
{'$': ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything'],
 '$$': ['Mexican Grill'],
 '$$$': ['Georgie Porgie'],
 '$$$$': []}

Cuisine to list of restaurant names:
# dict of {str, list of str}
{'Canadian': ['Georgie Porgie'],
 'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
 'Malaysian': ['Queen St. Cafe'],
 'Thai': ['Queen St. Cafe'],
 'Chinese': ['Dumplings R Us'],
 'Mexican': ['Mexican Grill']}

With this data, for a price of '$' and cuisines of ['Chinese', 'Thai'], we
would produce this list:

    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
"""

# The file containing the restaurant data.
FILENAME = 'restaurants.txt'


def recommend(price, cuisines_list, file=FILENAME):
    """(file open for reading, str, list of str) -> list of [int, str] list

    Find restaurants in file that are priced according to price and that are
    tagged with any of the items in cuisines_list.  Return a list of lists of
    the form [rating%, restaurant name], sorted by rating%.
    """

    # Read the file and build the data structures.
    # - a dict of {restaurant name: rating%}
    # - a dict of {price: list of restaurant names}
    # - a dict of {cusine: list of restaurant names}
    name_to_rating, price_to_names, cuisine_to_names = read_restaurants(file)

    # Look for price or cuisines first?
    # Price: look up the list of restaurant names for the requested price.
    names_matching_price = price_to_names[price]

    # Now we have a list of restaurants in the right price range.
    # Need a new list of restaurants that serve one of the cuisines.
    names_final = filter_by_cuisine(names_matching_price,
                                    cuisine_to_names,
                                    cuisines_list)

    # Now we have a list of restaurants that are in the right price range and
    # serve the requested cuisine.
    # Need to look at ratings and sort this list.
    result = build_rating_list(name_to_rating, names_final)

    # We're done!  Return that sorted list.
    return result


def build_rating_list(name_to_rating, names_final):
    """ (dict of {str: int}, list of str) -> list of list of [int, str]

    Return a list of [rating%, restaurant name], sorted by rating%

    >>> name_to_rating = {'Georgie Porgie': 87,
     'Queen St. Cafe': 82,
     'Dumplings R Us': 71,
     'Mexican Grill': 85,
     'Deep Fried Everything': 52}
    >>> names = ['Queen St. Cafe', 'Dumplings R Us']
    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
    """
    return [[name_to_rating[name], name] for name in names_final]


def filter_by_cuisine(names_matching_price, cuisine_to_names, cuisines_list):
    """ (list of str, dict of {str: list of str}, list of str) -> list of str

    >>> names = ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything']
    >>> cuis = {'Canadian': ['Georgie Porgie'],
     'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
     'Malaysian': ['Queen St. Cafe'],
     'Thai': ['Queen St. Cafe'],
     'Chinese': ['Dumplings R Us'],
     'Mexican': ['Mexican Grill']}
    >>> cuisines = ['Chinese', 'Thai']
    >>> filter_by_cuisine(names, cuis, cuisines)
    ['Queen St. Cafe', 'Dumplings R Us']
    """

    # my solution is a list comprehension version of this:
    # names_matching_cuisine = []

    # for c in cuisines_list:
    #     for n in names_matching_price:
    #         if n in cuisine_to_names[c]:
    #             names_matching_cuisine.append(n)

    names_matching_cuisine = [name for name in names_matching_price
                              for cuisine in cuisines_list
                              if name in cuisine_to_names[cuisine]]

    return names_matching_cuisine


def read_restaurants(file):
    """ (file) -> (dict, dict, dict)

    Return a tuple of three dictionaries based on the information in the file:

    - a dict of {restaurant name: rating%}
    - a dict of {price: list of restaurant names}
    - a dict of {cusine: list of restaurant names}
    """

    with open(file) as f:
        file_list = f.read().splitlines()

    # extract resaurant details in order from file_list
    restaurant_names = file_list[::5]
    restaurant_ratings = file_list[1::5]
    restaurant_prices = file_list[2::5]
    restaurant_cuisines = [item.split(',') for item in file_list[3::5]]

    # create dict of {restaurant name: rating%}
    name_to_rating = dict(zip(restaurant_names, restaurant_ratings))

    # create dict of {price: list of restaurant names}
    price_to_names = {'$': [], '$$': [], '$$$': [], '$$$$': []}
    restaurant_price_tuples = list(zip(restaurant_names, restaurant_prices))
    for restaurant in restaurant_price_tuples:
        price_to_names[restaurant[1]].append(restaurant[0])

    # create dict of {cusine: list of restaurant names}
    cuisine_to_names = {}
    restaurant_cuisine_tuples = list(zip(restaurant_names,
                                         restaurant_cuisines))
    for r in restaurant_cuisine_tuples:
        for c in r[1]:
            if c in cuisine_to_names.keys():
                cuisine_to_names[c].append(r[0])
            else:
                cuisine_to_names[c] = [r[0]]

    return (name_to_rating, price_to_names, cuisine_to_names)
