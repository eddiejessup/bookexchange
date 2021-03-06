from string import uppercase, lowercase, digits
import numpy.random
from numpy.random import choice
import search

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


def random_book():
    return search.Book(random_ISBN(), random_title(), random_name(),
                       random_condition(), random_status())


def random_empty_profile():
    name = random_name()
    email = make_email(name)
    return search.Profile(name, email, books=[], links=[])


def random_empty_iso_profiles(n_profs):
    profiles = {}
    for i_prof in range(n_profs):
        profile = random_empty_profile()
        link = make_link(profile.name)
        profiles[link] = profile
    return profiles


def random_empty_profile_network(n_profs, p):
    profiles = random_empty_iso_profiles(n_profs)
    link_list = profiles.keys()
    for i_1 in range(len(link_list)):
        link_1 = link_list[i_1]
        for i_2 in range(i_1 + 1, len(link_list)):
            if numpy.random.random() < p:
                link_2 = link_list[i_2]
                profiles[link_1].links.append(link_2)
                profiles[link_2].links.append(link_1)
    return profiles


def make_link_profile_map_dict(profiles):
    def link_profile_map_dict(link):
        return profiles[link]
    return link_profile_map_dict


def test_search(n_profs, p):
    profiles = random_empty_profile_network(n_profs, p)
    for profile in profiles.values():
        profile.books = [random_book() for _ in range(6)]
    link_profile_map = make_link_profile_map_dict(profiles)
    start_link = choice(profiles.keys())
    destination_link = choice(profiles.keys())
    destination_profile = link_profile_map(destination_link)
    destination_book = choice(destination_profile.books)
    query = destination_book.ISBN
    results = search.find_match_bfs(start_link, query, link_profile_map)
    return profiles, results


def nth_adjacent_link(start_link, profiles, n):
    adjacent_link = profiles[start_link].links[0]
    if n == 1:
        return adjacent_link
    else:
        return nth_adjacent_link(adjacent_link, profiles, n - 1)


def test_search_known(n_profs, p):
    profiles = random_empty_profile_network(n_profs, p)
    for profile in profiles.values():
        profile.books = [random_book() for _ in range(6)]

    start_link = choice(profiles.keys())
    target_link = nth_adjacent_link(start_link, profiles, 2)
    target_profile, path = search.find_match_bfs_known(start_link, target_link, profiles)
    print(start_link, target_link)
    return target_profile, path
