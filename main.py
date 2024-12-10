import spacy
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_md")  # Ensure this model is installed: python -m spacy download en_core_web_md

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
        similarities.append((idx, similarity))
    

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    recommended = [(problems[idx], score) for idx, score in similarities[:top_n]]
    return recommended

# Main workflow
if __name__ == "__main__":
    # Load the problems JSON
    file_path = "detailed_problems_100.json" 
    problems = load_problems(file_path)
    
    # User query
    query = input("Enter your query (e.g., 'geometry rectangle area'): ")
    
    # Get recommendations
    print("Fetching recommendations...")
    recommendations = recommend_problems(query, problems)
    
    # Print results with scores
    for idx, (problem, score) in enumerate(recommendations):
        print(f"\nRecommendation {idx + 1}:")
        print(f"Title: {problem['title']}")
        print(f"Difficulty: {problem['difficulty']}")
        print(f"Topic Tags: {', '.join(problem['topic_tags'])}")
        print(f"Content Snippet: {problem['content'][:300]}...")  
        print(f"Similarity Score: {score:.4f}")
