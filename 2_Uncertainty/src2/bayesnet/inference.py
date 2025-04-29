from model import model

# Calculate predictions 1
predictions = model.predict_proba({
## with evidence :     
    "train": "delayed"
})

# Print predictions for each node
print("\nwith evidence", "train delayed: ")
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")

# Calculate predictions 2
predictions = model.predict_proba({
## with evidence :
    "rain" : "heavy",    
    "train": "delayed"
})

# Print predictions for each node
print("\nwith evidence", "train delayed, and heavy rain: ")
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")
