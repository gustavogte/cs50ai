from model import model

# Calculate probability for a given observation
print("\nProbability of no rain, no maintence, train on time, meeting attended: ")

probability = model.probability([["none", "no", "on time", "attend"]])

print(probability)


# Calculate probability for a given observation
print("\nProbability of no rain, no maintence, train on time, meeting missed: ")

probability = model.probability([["none", "no", "on time", "miss"]])

print(probability)
