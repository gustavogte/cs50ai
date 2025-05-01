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
    """
    Iteratively update PageRank values until convergence.
    Returns a dictionary where keys are page names and values are
    their estimated PageRank (values between 0 and 1).
    """
    accuracy_factor = 0.001
    N = len(corpus)
    ## Use list comprehensions instead
    # page_ranks = dict()
    # for page in corpus:
    #     page_ranks[page] = 1 / N
    ### This is faster beacuse it faster because list comprehensions are implemented in C under the hood and optimized internally:
    page_ranks = {page: 1 / N for page in corpus}
    iteration = 0

    while True:
        new_page_ranks = pagerank(corpus, page_ranks, damping_factor)

        # Compute max difference to check convergence
        max_difference = 0
        for page in corpus:
            diff = abs(new_page_ranks[page] - page_ranks[page])
            if diff > max_difference:
                max_difference = diff

        # Debug info
        print(f"Iteration: {iteration}")
        print("Old Page Ranks:", page_ranks)
        print("New Page Ranks:", new_page_ranks)
        print("Max Difference:", max_difference)
        print()

        if max_difference <= accuracy_factor:
            break

        page_ranks = new_page_ranks
        iteration += 1

    return page_ranks


def pagerank(corpus:dict, ranks:dict, damping_factor:float) -> dict:
    """
    Compute one iteration of PageRank values.
    """
    N = len(corpus)
    new_ranks = dict()

    for page in corpus:
        total_ranks = 0
        for page_links in corpus:
            links = corpus[page_links]
            if not links:
                total_ranks += ranks[page_links] / N
            elif page in links:
                total_ranks += ranks[page_links] / len(links)

        new_ranks[page] = (1 - damping_factor) / N + damping_factor * total_ranks

    return new_ranks


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
