from string import uppercase, lowercase, digits
import numpy.random
from numpy.random import choice
from search import Profile, Book, find_match_bfs

uppercase = list(uppercase)
lowercase = list(lowercase)
lowercase = list(lowercase)
digits = list(digits)


def random_proper_noun(n_char):
    return '{}{}'.format(choice(uppercase),
                         ''.join(choice(lowercase, size=n_char - 1)))


def random_name():
    return '{}_{}'.format(random_proper_noun(5), random_proper_noun(5))


def make_email(name):
    return '{}@gmail.com'.format(name)


def random_ISBN():
    return ''.join(choice(digits, size=10))


def random_title():
    return '{} the {}'.format(random_proper_noun(7), random_proper_noun(4))


def random_condition():
    return choice(['Excellent', 'Very Good', 'Good', 'Acceptable'])


def random_status():
    return choice(['Available', 'Not Available'], p=[0.9, 0.1])


def make_link(name):
    return 'http://www.{}.{}/profile.yaml'.format(
        name, choice(['co.uk', 'com', 'org']))


def random_iso_profile(n_books_max):
    name = random_name()
    email = make_email(name)
    books = [Book(random_ISBN(), random_title(), random_name(),
                  random_condition(), random_status())
             for _ in range(numpy.random.randint(1, n_books_max))]
    return Profile(name, email, books, links=[])


def random_iso_profiles(n_profs, n_books_max):
    profiles = {}
    for i_prof in range(n_profs):
        profile = random_iso_profile(n_books_max)
        link = make_link(profile.name)
        profiles[link] = profile
    return profiles


def random_profile_network(n_profs, n_books_max, p):
    profiles = random_iso_profiles(n_profs, n_books_max)
    link_list = profiles.keys()
    for i_1 in range(len(link_list)):
        link_1 = link_list[i_1]
        for i_2 in range(i_1 + 1, len(link_list)):
            if numpy.random.random() < p:
                link_2 = link_list[i_2]
                profiles[link_1].links.append(link_2)
                profiles[link_2].links.append(link_1)
    return profiles


def make_dict_link_profile_map(profiles):
    def link_profile_map(link):
        return profiles[link]
    return link_profile_map


def test_search(n_profs, n_books_max, p):
    profiles = random_profile_network(n_profs, n_books_max, p)
    link_profile_map = make_dict_link_profile_map(profiles)
    start_link = choice(profiles.keys())
    destination_link = choice(profiles.keys())
    destination_profile = link_profile_map(destination_link)
    destination_book = choice(destination_profile.books)
    query = destination_book.ISBN
    results = find_match_bfs(start_link, query, link_profile_map)
    return results
