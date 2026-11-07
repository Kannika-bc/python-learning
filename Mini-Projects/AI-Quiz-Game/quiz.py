import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fetch_quiz_questions():
    prompt = """
    Generate 5 multiple-choice quiz questions about Python programming.

    Each question must have:
    - A prompt
    - Exactly 4 options
    - One correct answer (A, B, C, or D)

    Return ONLY valid JSON in this format:

    {
        "questions": [
            {
                "prompt": "What is Python?",
                "options": [
                    "A. Programming language",
                    "B. Database",
                    "C. Operating system",
                    "D. Browser"
                ],
                "answer": "A"
            }
        ]
    }
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "user", 
                 "content": prompt}
                 ],
            max_tokens=5000,
            temperature=0.8)

        result=response.choices[0].message.content
        try:
          data=json.loads(result)

        except json.JSONDecodeError:
          print("Error decoding JSON response:", result)
          return []

        return data["questions"]
    
    except Exception as e:
        print("Error fetching quiz questions:", e)
        return []


# quetions=[
#   {
#     "prompt": "What is the capital of France?",
#     "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
#     "answer": "C"
#   },
#   {
#     "prompt": "What is the largest planet in our solar system?",
#     "options": ["A. Earth", "B. Jupiter", "C. Saturn", "D. Mars"],
#     "answer": "B"
#   },
#   {
#     "prompt": "What is the chemical symbol for gold?",
#     "options": ["A. Go", "B. Gd", "C. Au", "D. Ag"],
#     "answer": "C"
#   },
#   {
#     "prompt": "Who painted the Mona Lisa?",
#     "options": ["A. Vincent van Gogh", "B. Pablo Picasso", "C. Leonardo da Vinci", "D. Michelangelo"],
#     "answer": "C"
#   }
# ]

def run_quiz():
    quetions=fetch_quiz_questions()
    score=0
    for quetion in  quetions:
        print(quetion["prompt"])
        for option in quetion["options"]:
            print(option)

        answer=input("Enter your answer (A, B, C, or D): ")
        if answer.upper() == quetion["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is {quetion['answer']}.")

    print(f"You got {score} out of {len(quetions)} correct.")

if __name__ == "__main__":
    run_quiz()
