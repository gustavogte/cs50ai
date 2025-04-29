import csv
import itertools
import sys


PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    names = set(people)
    ## GG print name
    # print("\nnames\n", names)
    # print()
    ## GG initialize loop to 1
    # loop = 1
    # Loop over all sets of people who might have the trait
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                ## GG print loop number and sets
                # print("Loop: ", loop, "----------------------------------------------------------")
                # print("2 genes: ", two_genes)
                # print("1 gene: ", one_gene)
                # print("trait: ", have_trait)

                # Update probabilities with new joint probability
                ## update probalities dict in main()

                p = joint_probability(people, one_gene, two_genes, have_trait)
                ## GG
                # print("probabilities", probabilities)
                ## GF
                update(probabilities, one_gene, two_genes, have_trait, p)

                ## GG
                # loop += 1
                # quit()

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    ## GG print data
    ## Print Formmated Data
    # people = data
    # for person in people:
    #    print(person, "[ name: ", people[person]["name"], "- mother: ", people[person]["mother"], "- father: ", people[person]["mother"],  "- trait: ", people[person]["trait"], "]")
    # quit()

    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(
    people: dict, one_gene: set, two_genes: set, have_trait: set
) -> float:
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # for person in people:
    #     print(person, people[person])
    p_family = 1
    for person in people:
        # print()
        name = people[person]["name"]
        # print("name: ", name)
        mother = people[person]["mother"]
        mother_genes = genes(mother, one_gene, two_genes)
        # print("mother: ", mother)
        # print("mother genes= ", mother_genes)
        father = people[person]["father"]
        father_genes = genes(father, one_gene, two_genes)
        # print("father: ", father)
        # print("father_genes= ", father_genes)
        # print("trait: ", people[person]["trait"])
        h_trait = trait(people[person]["name"], have_trait)
        # print("Have Trait: ", h_trait)
        genes_n = genes(people[person]["name"], one_gene, two_genes)
        # print("genes: ", genes_n)
        mutation_p = PROBS["mutation"]
        # print("mutation_p = ", mutation_p)

        if mother == None or father == None:
            p_n = PROBS["gene"][genes_n] * PROBS["trait"][genes_n][h_trait]
            # print("p_n = ", p_n)
            p_family *= p_n
            # print("p_family: ", p_family)
        else:
            ## GG Have parentes and pass genes
            father_pass_gene = father_genes / 2
            mother_pass_gene = mother_genes / 2

            ## GG Mutation
            father_pass_gene_dont_mutate = father_pass_gene * (1 - PROBS["mutation"])
            father_pass_gene_and_mutate = father_pass_gene * PROBS["mutation"]
            father_dont_pass_dont_mutate = (1 - father_pass_gene) * (
                1 - PROBS["mutation"]
            )
            father_dont_pass_and_mutate = (1 - father_pass_gene) * PROBS["mutation"]

            mother_pass_gene_dont_mutate = mother_pass_gene * (1 - PROBS["mutation"])
            mother_pass_gene_and_mutate = mother_pass_gene * PROBS["mutation"]
            mother_dont_pass_dont_mutate = (1 - mother_pass_gene) * (
                1 - PROBS["mutation"]
            )
            mother_dont_pass_and_mutate = (1 - mother_pass_gene) * PROBS["mutation"]

            if genes_n == 0:
                p = (
                    (father_pass_gene_and_mutate * mother_dont_pass_dont_mutate)
                    + (father_pass_gene_and_mutate * mother_pass_gene_and_mutate)
                    + (father_dont_pass_dont_mutate * mother_dont_pass_dont_mutate)
                    + (father_dont_pass_dont_mutate * mother_pass_gene_and_mutate)
                )
                p0 = p * PROBS["trait"][genes_n][h_trait]
                # print("p0 = ", p0)
                p_family *= p0
                # print("print_family: ", p_family)
            if genes_n == 1:
                p = (
                    (father_pass_gene_dont_mutate * mother_dont_pass_dont_mutate)
                    + (father_pass_gene_dont_mutate * mother_pass_gene_and_mutate)
                    + (father_pass_gene_and_mutate * mother_dont_pass_and_mutate)
                    + (father_dont_pass_and_mutate * mother_pass_gene_dont_mutate)
                    + (4 - 4)
                    + (father_pass_gene_dont_mutate * mother_dont_pass_and_mutate)
                    + (father_dont_pass_dont_mutate * mother_pass_gene_dont_mutate)
                    + (father_dont_pass_and_mutate * mother_dont_pass_dont_mutate)
                    + (father_dont_pass_and_mutate * mother_pass_gene_dont_mutate)
                )
                p1 = p * PROBS["trait"][genes_n][h_trait]
                # print("p1 = ", p1)
                p = p1
                p_family *= p1
                # print("print_family: ", p_family)
            if genes_n == 2:
                p = (
                    (father_pass_gene_dont_mutate * mother_pass_gene_dont_mutate)
                    + (father_dont_pass_and_mutate * mother_dont_pass_and_mutate)
                    + (father_dont_pass_and_mutate * mother_pass_gene_dont_mutate)
                    + (father_pass_gene_dont_mutate * mother_dont_pass_and_mutate)
                )
                p2 = p * PROBS["trait"][genes_n][h_trait]
                # print("p2 = ", p2)
                p = p2
                p_family *= p2
                # print("print_family: ", p_family)
    # print("return p_family", p_family)
    return p_family


## GG
def trait(name: str, have_trait: set) -> bool:
    ## GG
    # have_trait = {"James"}

    if name in have_trait:
        return True
    else:
        return False


## GG
def genes(name: str, one_gene: set, two_genes: set) -> int:
    ## GG
    # one_gene = {"Harry"}
    # two_genes = {"James"}

    if name in one_gene:
        return 1
    elif name in two_genes:
        return 2
    else:
        return 0


def update(
    probabilities: dict, one_gene: set, two_genes: set, have_trait: set, p: float
) -> None:
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            gene = 1
        elif person in two_genes:
            gene = 2
        else:
            gene = 0

        if person in have_trait:
            trait = True
        else:
            trait = False

        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        sum_p_genes = sum(probabilities[person]["gene"].values())
        sum_p_trait = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"]:
            value = probabilities[person]["gene"][gene]
            norm_value = value / sum_p_genes
            probabilities[person]["gene"][gene] = norm_value

        for trait in probabilities[person]["trait"]:
            value = probabilities[person]["trait"][trait]
            norm_value = value / sum_p_trait
            probabilities[person]["trait"][trait] = norm_value


if __name__ == "__main__":
    main()
