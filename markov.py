# markov.py — Order-2 Markov chain text generator with automatic timestamped file saving
import random
import sys
from collections import defaultdict
import datetime

def read_tokens(path):
    """Read text file and split into words."""
    text = open(path, encoding="utf-8").read().replace("\n", " ")
    return text.split()

def build_chain(tokens):
    """Build an order-2 Markov chain: (word1, word2) -> possible next words."""
    chain = defaultdict(list)
    for i in range(len(tokens) - 2):
        key = (tokens[i], tokens[i + 1])  # tuple of two consecutive words
        next_word = tokens[i + 2]
        chain[key].append(next_word)
    return chain

def generate(chain, length=50):
    """Generate new text using the chain."""
    if not chain:
        return ""
    
    # pick a random starting pair (key)
    current = random.choice(list(chain.keys()))
    w1, w2 = current
    output = [w1, w2]

    for _ in range(length - 2):
        possible_next = chain.get((w1, w2))
        if not possible_next:
            # dead end: pick a new random pair
            current = random.choice(list(chain.keys()))
            w1, w2 = current
            output.extend([w1, w2])
            continue

        next_word = random.choice(possible_next)
        output.append(next_word)

        # shift window
        w1, w2 = w2, next_word

    return " ".join(output)

if __name__ == "__main__":
    # Get input file and length from command line (or use defaults)
    path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    # Step 1: Read input and build Markov chain
    tokens = read_tokens(path)
    chain = build_chain(tokens)

    # Step 2: Generate text
    text = generate(chain, length)

    # Step 3: Print text to terminal
    print("\n--- Generated Text ---\n")
    print(text)

    # Step 4: Save text to a timestamped file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n--- Text saved to {filename} ---\n")


