# evaluator.py

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """Clean and normalize text."""

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_similarity(student_answer, model_answer):
    """Calculate similarity between student and model answers."""

    student_answer = clean_text(student_answer)
    model_answer = clean_text(model_answer)

    if not student_answer:
        return 0

    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform(
            [student_answer, model_answer]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return similarity

    except ValueError:
        return 0


def calculate_keyword_score(student_answer, keywords):
    """Calculate percentage of important keywords used."""

    student_answer = clean_text(student_answer)

    if not keywords:
        return 0

    matched = 0

    for keyword in keywords:

        keyword = clean_text(keyword)

        if keyword in student_answer:
            matched += 1

    score = matched / len(keywords)

    return score


def calculate_length_score(student_answer):

    words = student_answer.split()

    word_count = len(words)

    if word_count == 0:
        return 0

    if word_count < 5:
        return 0.3

    elif word_count < 15:
        return 0.6

    elif word_count < 30:
        return 0.8

    else:
        return 1.0


def evaluate_answer(student_answer, model_answer, keywords):

    similarity = calculate_similarity(
        student_answer,
        model_answer
    )

    keyword_score = calculate_keyword_score(
        student_answer,
        keywords
    )

    length_score = calculate_length_score(
        student_answer
    )

    final_score = (
        similarity * 0.50
        + keyword_score * 0.40
        + length_score * 0.10
    )

    score = round(final_score * 10, 1)

    if score >= 8:

        feedback = (
            "Excellent answer! Your answer is relevant "
            "and contains important concepts."
        )

    elif score >= 6:

        feedback = (
            "Good answer. Your answer is mostly relevant, "
            "but you can add more important points or examples."
        )

    elif score >= 4:

        feedback = (
            "Average answer. Try to explain the concept "
            "more clearly and include important keywords."
        )

    else:

        feedback = (
            "Your answer needs improvement. "
            "Study the concept and try to give a more "
            "complete and relevant answer."
        )

    return {
        "score": score,
        "similarity": round(similarity * 100, 1),
        "keyword_score": round(keyword_score * 100, 1),
        "feedback": feedback
    }