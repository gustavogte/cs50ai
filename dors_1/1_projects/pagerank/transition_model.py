DAMPING = 0.85


def main():

    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    #corpus = {"A": {"B", "C"}, "B": {"C", "A"}, "C": {"A"}}
    #corpus = {"A": {"B", "C"}, "B": {"C"}, "C": {"A"}}
    ## Result for damping_factor = .85 and page "1.html"  
    ## output = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

    corpus_pages = list(corpus.keys())
    page = corpus_pages[0]
    #page = None
    damping_factor = DAMPING

    transition_model(corpus, damping_factor, page)

def transition_model(corpus: dict, damping_factor: float, page: str = None) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    print("Corpus :\n", corpus)
    print("type:", type(corpus))
    print()
    print("\nModel\n")

    t_model = dict()
    n_pages = len(corpus)
    # Initialize mode with equal probabilities
    for item in corpus:
        p_corpus = (1 / len(corpus.keys())) * (1 - damping_factor) 
        print(item, p_corpus)
        t_model.update({item:(p_corpus)})
    
        for link in corpus[item]:
            p_links = (1 / len(corpus[item])) * damping_factor
            print("           -->",link, p_links)
            if item == page:
                print("        Here we go ....")
                print()
    if corpus[page]:
        linked_pages = corpus[page]
        n_links = len(linked_pages)
        link_prob = damping_factor / n_links
        for link in linked_pages:
            t_model[link] += link_prob

    else:
    # If no outgoing links, treat as linking to all pages equally
    # So if we get to a dead end with no links =>
    # treat it as if it links to all pages in the corpus, equally choose randomly.
        for item in corpus:
            t_model[item] += damping_factor / n_pages


    print()
    print(t_model)

    if page is not None:
        print("\nSelected page: ", page)
        print("\nLinked pages = ", corpus[page], "# ", len(corpus[page]))  

if __name__ == "__main__":
    main()
