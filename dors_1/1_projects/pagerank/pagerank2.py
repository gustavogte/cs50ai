import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus: dict, page: str, damping_factor: float) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    ## Example for:
    # corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    ## Result for damping_factor = .85 and page "1.html"
    ## output = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

    t_model = dict()
    n_pages = len(corpus)

    # Initialize model with equal probabilities
    for item in corpus:
        p_corpus = (1 / n_pages) * (1 - damping_factor)
        t_model.update({item: (p_corpus)})
    # print(t_model)

    # Add probabilities to the existing links
    if corpus[page]:
        linked_pages = corpus[page]
        # print(linked_pages)
        n_links = len(linked_pages)
        link_prob = damping_factor / n_links
        for link in linked_pages:
            # print(link, t_model[link], link_prob)
            t_model[link] += link_prob
    else:
        # If no outgoing links, treat as linking to all pages equally
        # So if we get to a dead end with no links =>
        # treat it as if it links to all pages in the corpus, equally choose randomly.
        for item in corpus:
            t_model[item] += damping_factor / n_pages

    # print(t_model)
    return t_model


def sample_pagerank(corpus: dict, damping_factor: float, n: int) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    damping_factor = DAMPING
    n = SAMPLES

    page = random.choice(list(corpus.keys()))
    # print("Page 0: ", page)
    visits = list()
    n_copies = 1000 # optional for get_page() to create the list of elements with the transition_model, 100 is by default, 
    for _ in range(1, n):
        t_model = transition_model(corpus, page, damping_factor)
        # print(t_model)
        #page = get_page(t_model, n_copies)
        #page = get_page(t_model)
        page = get_page_2(t_model)
        # print(f"Page {sample}: ", page)
        visits.append(page)
    # print(visits)
    s_page_rank = dict()
    for key in corpus.keys():
        p_dict = visits.count(key) / n
        # print(key, p_dict)
        s_page_rank[key] = p_dict
    # print(s_page_rank)
    # print(sum(s_page_rank.values()))
    return s_page_rank

    # quit()
    # raise NotImplementedError


## GG
def get_page(model: dict, n:int = 100) -> str:

    data_sample = list()
    for item in model:
        copies = int(model[item] * n)
        # print(item)
        for _ in range(copies):
            # print(item, "x", copies)
            data_sample.append(item)
    #print(data_sample)
    return random.choice(data_sample)

def get_page_2(model: dict) -> str:
    model_keys = list(model.keys())
    model_values = list(model.values())
    
    return random.choices(model_keys, weights = model_values)[0]


def iterate_pagerank(corpus: dict, damping_factor: float) -> dict:
    # return value = dict {Key-page: value-PageRank}
    # sum values == 1
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print("\nIterate PageRank\n")
    d = DAMPING
    accurrate_factor = .001
    corpus_keys = list(corpus.keys())
    N = len(corpus_keys) 
   
    fix = (1 - d) / N 

    # First iteration => Initialize values 1 / N
    pages = dict()
    for page in corpus_keys:
        pages[page] = 1 / N      
    print(pages)
    print()

    x = 0
    while True:
        pages_old = pages
        print("\npages old\n", pages_old)
        print()
        for page in pages:
            links = corpus[page]
            n_links = len(links)
            p = fix
            for link in links:
                # Check if our page appears in corpus[page] (links)
                if page in links:
                    print(page, "->", link)
                    p += d * (pages[page] / n_links)
                    print(page, p)
                # If there are no links send to all pages with equal probability
                if n_links == 0:
                    p += d * (pages[page] / N)
            pages.update({page: p})
            pages_old.update({page: p})
        print(x, pages)
        # All pages must have an difference less than .001
        # Must store the previos iteration and the current to check the difference.
        x += 1 
        if x == 3:
            break

    # page with no links should be calculated as having one link for every page includint itself.
    # process go until PageRank changes less than .001
    quit()

if __name__ == "__main__":
    main()

## GG Notes
"""
Markov Models

Markov Assumption: 
- The current state depends on only a previous fixed number of previous events.

Markov Chain :
- Sequence of random variables where the distribution of each of the variables follow the Markov assumption.

Transition Model:
- How you change from one state to another


Hidden Markov Models
- You have observation or sensors instead of direct variables.


- Sensor Markov assumption:
    - depends only on the corresponding state.

"""
