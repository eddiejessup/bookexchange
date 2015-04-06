import yaml
import urllib2


def load_yaml(link):
    try:
        stream = urllib2.urlopen(link)
    except ValueError:
        stream = open(link, 'r')
    return yaml.load(stream)


def parse_profile_yaml(profile_yaml):
    name = profile_yaml['name']
    email = profile_yaml['email']

    books_yaml = profile_yaml['books']
    books = []
    for book_yaml in books_yaml:
        books.append(Book(book_yaml))
    links_yaml = profile_yaml['links']
    return name, email, books, links_yaml


class Profile(object):
    def __init__(self, name, email, books, links):
        self.name = name
        self.email = email
        self.books = books
        self.links = links

    def search(self, query):
        for book in self.books:
            if book.match(query):
                return book

    def __str__(self):
        return '{} ({}), {} books, {} links'.format(
            self.name, self.email, len(self.books), len(self.links))


class Book(object):
    def __init__(self, ISBN, title, author, condition, status):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.condition = condition
        self.status = status

    def match(self, query):
        return self.ISBN in query

    def __str__(self):
        return '{} - {} (ISBN {}). Condition: {}. Status: {}'.format(
            self.author, self.title, self.ISBN, self.condition, self.status)


def link_profile_map_yaml(link):
    profile_yaml = load_yaml(link)
    profile_args = parse_profile_yaml(profile_yaml)
    return Profile(*profile_args)


def find_match_bfs(start_link, query, link_profile_map):
    links_dicovered = [start_link]
    links_to_visit = [start_link]
    while len(links_to_visit):
        current_link = links_to_visit.pop()
        current_profile = link_profile_map(current_link)
        matching_book = current_profile.search(query)
        if matching_book is not None:
            return current_profile, matching_book
        for new_link in current_profile.links:
            if new_link not in links_dicovered:
                links_to_visit.append(new_link)
                links_dicovered.append(new_link)
    return None, None
