Task 2 focuses on self-learning algorithm implementation for intelligent resume-job matching. Based on Task 1's OOP class structure (Job, Resume, Skill), this task realizes text-based similarity calculation and automatic keyword extraction, providing core data support for the system's intelligent matching function.

Core Algorithm Implementation

1. Selected Algorithm: TF-IDF (Main Function)

TF-IDF (Term Frequency-Inverse Document Frequency) is used to calculate the similarity between resume content and job description, and output the final matching score.

Implementation Steps:

• Text Preprocessing: Perform word segmentation (using jieba), remove stop words, and clean special symbols for both job description and resume text.

• Vector Construction: Calculate TF (term frequency) and IDF (inverse document frequency) of words in the corpus, and construct text vectors for resumes and jobs respectively.

• Similarity Calculation: Use cosine similarity to compute the similarity between the resume vector and the job vector, and map it to a 0-100 matching score.

2. Expansion Algorithm: TextRank (Auxiliary Function)

As an expansion function, TextRank is used to automatically extract high-weight keywords from job description text.

Implementation Steps:

• Build a text graph based on the co-occurrence relationship of words in the job description.

• Iteratively calculate the weight of each node (word) to sort and extract top-N keywords.

• Optimize the matching calculation dimension by using only keywords for subsequent TF-IDF matching, improving calculation efficiency and accuracy.

Key Features

• Modular Design: Separate text preprocessing, TF-IDF calculation, and TextRank extraction into independent modules for easy maintenance.

• Data Compatibility: Adapt to Task 1's Job/Resume class structure, directly reading internal text attributes (e.g., job.description, resume.content).

• Error Handling: Add exception handling for empty text, invalid word segmentation results, and ensure algorithm stability.

Environment Setup

1. Install Python 3.8+.
2. Install flask


How to Run

1. Run TF-IDF Matching Calculation
Execute the main matching script, input resume and job data (from Task 1 class instances), and get the matching score

2. Run TextRank Keyword Extraction
Extract keywords from a specified job description text
   

   
