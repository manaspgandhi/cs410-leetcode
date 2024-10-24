# CS 410 Leetcode Project

## Introduction
LeetCode is one of the most popular platforms for practicing technical coding interview questions. A common technique to solving leetcode questions is to recognize patterns and apply solution techniques that work for those patterns. However, finding relevant problems that aid in solving a given problem can be time-consuming and inefficient. 

This project aims to address this gap by automatically retrieving similar LeetCode problems when given a query problem. The system will allow users to find related problems that may help in understanding different problem-solving strategies, improving both learning and preparation for technical interviews.

## Problem Statement
It is very important to model a leetcode solution off of similar leetcode questions. These similar problems should share key features such as algorithms, data structures, or problem-solving techniques, and they should be helpful in guiding the user toward solving the target problem. Our system will explore various textual and structural features of problem descriptions to build an effective retrieval system for the leetcode problems.

## Data
The data will be acquired through public lists of LeetCode problems, including both the problem statements and the solutions. This data will be pre-processed to extract features from both the problem descriptions (e.g., keywords, tags, problem types) and the solutions (e.g., algorithms used, time complexity), and a similarity metric would be computed using these features.

## Approach
1. **Data Collection and Preprocessing:** We will collect problem and solution pairs from public LeetCode resources and preprocess the data by extracting features such as keywords, problem tags, and common algorithms.
2. **Feature Extraction:** Textual similarity between problem statements will be computed using techniques like TF-IDF, word embeddings (Word2Vec), and cosine similarity. Additionally, structural features like problem tags (e.g., dynamic programming, graph theory) will be considered.
3. **Similarity Metric Design:** We will design a custom similarity metric that combines textual features with problem metadata (tags, difficulty levels) to rank similar problems. This metric will prioritize problems that offer useful strategies or insight for solving the query problem.
4. **System Evaluation:** The effectiveness of our system will be evaluated through both quantitative and qualitative analysis. We will measure retrieval accuracy by comparing our system’s recommendations against user feedback and existing problem-solving resources.

## Challenges
One key challenge for our project is identifying the most useful features for similarity matching, because simple textual matching won't capture the algorithmic similarities between problems. To address this, we plan to integrate problem-solving strategies (extracted from solution descriptions) into our similarity metric. Another challenge will be evaluating the relevance of the recommended problems based on user's skill level.

## Conclusion and Future Work
This project will develop a system that enhances problem-solving on LeetCode by retrieving similar problems to a given query problem. After this class, we plan to expand the dataset by incorporating problems from other coding platforms and refining the similarity metric with user interaction data.