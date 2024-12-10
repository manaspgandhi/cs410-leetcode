import json
import random

# Load the problems JSON
def load_problems(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        problems = json.load(file)
    return problems

# Generate a validation set
def generate_validation_set(problems, num_queries=10, num_expected_per_query=3):
    validation_set = []
    for _ in range(num_queries):
        # Randomly select problems to form the query
        selected_problems = random.sample(problems, num_expected_per_query)
        expected_titles = [problem["title"] for problem in selected_problems]
        
        # Create a query based on the selected problems' titles and topics
        query_terms = " ".join([problem["title"] for problem in selected_problems[:2]])  # Combine 2 titles
        query_terms += " " + " ".join(selected_problems[0]["topic_tags"])  # Add some topic tags

        # Add to the validation set
        validation_set.append({
            "query": query_terms,
            "expected_titles": expected_titles
        })
    return validation_set

# Save validation set to a JSON file
def save_validation_set(validation_set, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(validation_set, file, indent=4)

# Main workflow
if __name__ == "__main__":
    # Load the problems JSON
    problems_file_path = "detailed_problems_100.json"  # Replace with your problems file path
    problems = load_problems(problems_file_path)
    
    # Generate validation set
    num_queries = 20  # Number of test cases to generate
    validation_set = generate_validation_set(problems, num_queries=num_queries)

    # Save validation set to a file
    output_path = "validation_set.json"  # Replace with your desired file path
    save_validation_set(validation_set, output_path)

    print(f"Validation set created and saved to {output_path}")
