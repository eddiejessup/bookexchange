# Concept

- Each person has a list of physical books they own
- Each person has a list of people they know
- There is a service where a person puts in work of writing they want, and it returns the nearest person --- in the social degree of separation sense of nearest --- who has an instance of that book

# Concept extensions

- Allow searching by nearest in the geographic sense
    - Implementation: Include either person or book to have the field 'location'
- What other media can be included? Needs to be physical. Can see two prongs to this necessity:
    - Media for people who like it to be physical
        - Vinyl, CDs, cassettes, and so on
        - Clothes
    - Non-media objects that are essentially physical
        - Clothes
        - Equipment
            - Cables
            - Tools
            - Camping stuff
        - Transport
        - Accommodation
        - Skills

# Implementation

- Data: Each person has a 'profile'
    - Profile: a file that is accessible by a URL
        - Identifying information
            'name', 'email'
        - List of 'Books'
            - 'ISBN', 'title', 'author', 'condition', 'status'
                - Status: whether or not the book is available
        - List of 'Links'
            - 'link': a URL locating another person's 'profile'
        - Format: YAML
- Service: A website where a person enters their own 'link', and a 'book search'
    - Book search: a string to serve as an argument for a 'relevance function'
        - Relevance function: a function which takes a 'book' and a 'book search' and returns a measure of how much they match
    - Go recursively through increasing degrees of separation (breadth-first) to find matching books
        - Not sure how to do relevance
            - Fixed relevance threshold, unpredictable search time
            - Fixed searching time, unpredictable relevance
            - Combination of the two: think of the algorithm for dating which suggests you should get less picky as your search time goes on. This doesn't work directly, because in dating you have to settle. Here you don't, but maybe it's a similar problem mathematically.
    - Return the search results
        - List of 'results'
            - Result: pair of 'profile' and 'book'
        - Options for each result
            - Nearness: number of degrees of separation
            - Path: path from source person to target person

# Implementation Extensions

- Option to show unavailable books
    - Notification when a book becomes available

# Implementation Issues

- Security and privacy
    - People not liking having an open address book pairing names to email addresses
        - Only let profile be visible by people whose links are in the person's profile?
    - Email crawling by nasty people
