# Problem Statement: AI-Powered Restaurant Recommendation System

## Overview
Build an AI-powered restaurant recommendation application inspired by Zomato.  
The system should combine structured restaurant data with a Large Language Model (LLM) to generate personalized recommendations based on user preferences.

## Objective
Design and implement an application that can:
- Accept user preferences such as location, budget, cuisine, and minimum rating
- Use a real-world restaurant dataset for recommendation logic
- Leverage an LLM to generate personalized, natural-language suggestions
- Present results in a clear, user-friendly format

## Data Source
Use the Zomato dataset available on Hugging Face:  
<https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation>

At a minimum, process the following fields:
- Restaurant name
- Location
- Cuisines
- Average cost / price range
- Rating
- Any relevant metadata useful for filtering or ranking

## Functional Workflow

### 1. Data Ingestion and Preprocessing
- Load the dataset
- Clean and normalize relevant fields
- Handle missing or inconsistent values
- Store the processed data in a structure suitable for filtering and ranking

### 2. User Preference Collection
Collect inputs such as:
- Location (e.g., Delhi, Bangalore)
- Budget (low, medium, high)
- Preferred cuisine (e.g., Italian, Chinese)
- Minimum rating threshold
- Additional preferences (optional), such as family-friendly or quick service

### 3. Candidate Selection Layer
- Filter restaurants based on user preferences
- Prepare a structured shortlist of relevant candidates
- Build a prompt payload from shortlisted restaurant data

### 4. LLM-Based Recommendation Engine
Use the LLM to:
- Rank shortlisted restaurants
- Generate concise explanations for each recommendation
- Optionally provide a final summary comparing top options

### 5. Result Presentation
Display top recommendations with:
- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated reasoning for why the restaurant matches user preferences

## Expected Outcome
A working recommendation system that combines deterministic filtering with LLM reasoning to provide useful, personalized restaurant suggestions.
