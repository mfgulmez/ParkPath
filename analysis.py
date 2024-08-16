import matplotlib.pyplot as plt

# Example data
confidence_levels = [0.5, 0.6, 0.7, 0.8, 0.9]
true_positives = [13, 12, 12, 11, 11]
false_positives = [0, 1, 1, 2, 2]
true_negatives = [15, 18, 17, 15, 12]
false_negatives = [3, 2, 3, 5, 8]

# Calculate metrics
precision = [tp / (tp + fp) for tp, fp in zip(true_positives, false_positives)]
recall = [tp / (tp + fn) for tp, fn in zip(true_positives, false_negatives)]
f1_score = [2 * (p * r) / (p + r) for p, r in zip(precision, recall)]
accuracy = [(tp + tn) / (tp + fp + tn + fn) for tp, fp, tn, fn in zip(true_positives, false_positives, true_negatives, false_negatives)]

# Plot Precision-Recall Curve
plt.figure()
plt.plot(recall, precision, marker='o')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()

# Plot F1 Score and Accuracy
plt.figure()
plt.plot(confidence_levels, f1_score, marker='o', label='F1 Score')
plt.plot(confidence_levels, accuracy, marker='o', label='Accuracy')
plt.xlabel('Confidence Level')
plt.ylabel('Score')
plt.title('F1 Score and Accuracy vs Confidence Level')
plt.legend()
plt.show()
