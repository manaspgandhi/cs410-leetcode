import requests
import json
import time

# REST API URL for fetching all problems
REST_URL = "https://leetcode.com/api/problems/all/"

# GraphQL API details
BASE_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

# GraphQL query for problem details
DETAIL_QUERY = """
query getProblemDetails($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    title
    content
    difficulty
    topicTags {
      name
    }
    isPaidOnly
    exampleTestcases
  }
}
"""

# Function to fetch all problems using the REST API
def fetch_all_problems(limit=100):
    response = requests.get(REST_URL)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print("Response Text:", response.text)
        return []

    data = response.json()
    problems = data.get("stat_status_pairs", [])

    # Process only the first `limit` problems
    parsed_problems = []
    for problem in problems[:limit]:
        parsed_problems.append({
            "title": problem.get("stat", {}).get("question__title"),
            "title_slug": problem.get("stat", {}).get("question__title_slug"),
            "difficulty": problem.get("difficulty", {}).get("level"),
            "paid_only": problem.get("paid_only", False)
        })

    return parsed_problems

# Function to fetch detailed problem information using the GraphQL API
def fetch_problem_details(title_slug):
    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json={
            "query": DETAIL_QUERY,
            "variables": {
                "titleSlug": title_slug
            }
        }
    )

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for {title_slug}")
        print("Response Text:", response.text)
        return None

    data = response.json()
    return data.get("data", {}).get("question", {})

if __name__ == "__main__":
    # Step 1: Fetch the first 100 problems from the REST API
    print("Fetching the first 100 problems...")
    all_problems = fetch_all_problems(limit=100)

    # Step 2: Fetch detailed data for each problem
    print("Fetching detailed problem information...")
    detailed_problems = []
    for i, problem in enumerate(all_problems):
        if problem["paid_only"]:  # Skip paid-only problems if necessary
            print(f"Skipping paid-only problem: {problem['title']}")
            continue

        print(f"Fetching details for: {problem['title']} ({i + 1}/{len(all_problems)})")
        details = fetch_problem_details(problem["title_slug"])
        if details:
            detailed_problem = {
                "title": details.get("title"),
                "difficulty": details.get("difficulty"),
                "content": details.get("content"),
                "topic_tags": [tag["name"] for tag in details.get("topicTags", [])],
                "example_testcases": details.get("exampleTestcases"),
            }
            detailed_problems.append(detailed_problem)

        time.sleep(0.5)  # Avoid hitting rate limits

    # Step 3: Save all detailed problems to a JSON file
    with open("detailed_problems_100.json", "w", encoding="utf-8") as f:
        json.dump(detailed_problems, f, indent=4)
    print(f"Saved detailed problems to detailed_problems_100.json")
