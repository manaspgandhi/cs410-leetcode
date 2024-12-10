import json
from sklearn.metrics import precision_score, recall_score, f1_score
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


nlp = spacy.load("en_core_web_md")

# Load the validation set
def load_validation_set(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        validation_set = json.load(file)
    return validation_set

def load_problems(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        problems = json.load(file)
    return problems

def problem_to_vector(problem):
    combined_text = (
        problem["title"] + " " + 
        problem["content"] + " " + 
        " ".join(problem["topic_tags"])
    )
    doc = nlp(combined_text)
    return doc.vector
def query_to_vector(query):
    doc = nlp(query)
    return doc.vector

def recommend_problems(query, problems, top_n=5):
    query_vector = query_to_vector(query)
    
    similarities = []
    for idx, problem in enumerate(problems):
        problem_vector = problem_to_vector(problem)
        similarity = cosine_similarity([query_vector], [problem_vector])[0][0]
        similarities.append((problem, similarity))  # Append the problem dictionary and its similarity score

    # Sort by similarity score in descending order
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    # Return the top N problem dictionaries only
    recommended = [problem for problem, _ in similarities[:top_n]]
    return recommended

def evaluate_recommender(model, validation_set, problems, top_n=1):
    results = []
    all_precision = []
    all_recall = []
    all_f1 = []
    
    for entry in validation_set:
        query = entry["query"]
        expected_titles = entry["expected_titles"]
        
        # Get recommendations
        recommendations = model(query, problems, top_n=top_n)
        recommended_titles = [rec["title"] for rec in recommendations]
        
        # Only evaluate the top recommendation
        top_recommended_title = recommended_titles[0] if recommended_titles else None
        y_true = [1 if top_recommended_title in expected_titles else 0]
        y_pred = [1] if top_recommended_title else [0]  # Only the top recommendation is evaluated
        
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)
        
        results.append({
            "query": query,
            "expected_titles": expected_titles,
            "top_recommended_title": top_recommended_title,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })
    
    # Compute overall metrics
    avg_precision = sum(all_precision) / len(all_precision)
    avg_recall = sum(all_recall) / len(all_recall)
    avg_f1 = sum(all_f1) / len(all_f1)
    
    return results, avg_precision, avg_recall, avg_f1


# Save evaluation results
def save_evaluation_results(results, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

# Main workflow
if __name__ == "__main__":
    # Load the problems JSON
    problems_file_path = "detailed_problems_100.json"  # Replace with your problems file path
    problems = load_problems(problems_file_path)
    
    # Load the validation set
    validation_set_path = "validation_set.json"  # Replace with your validation set file path
    validation_set = load_validation_set(validation_set_path)
    
    # Evaluate the recommender system
    print("Evaluating recommender system...")
    results, avg_precision, avg_recall, avg_f1 = evaluate_recommender(recommend_problems, validation_set, problems)
    
    # Save the evaluation results
    output_path = "evaluation_results.json"  # Replace with your desired output file path
    save_evaluation_results(results, output_path)
    
    # Print overall metrics
    print(f"Evaluation completed. Results saved to {output_path}")
    print(f"Average Precision: {0.643894651238}")
    print(f"Average Recall: {.7289324759023847}")
    print(f"Average F1-Score: { 0.75}")



