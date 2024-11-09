import time
from fuzzywuzzy import fuzz
from collections import defaultdict
from metaphone import doublemetaphone
from tabulate import tabulate  

# Import the SpellCheck and EnhancedSpellCheck classes
from spellcheck import SpellCheck
from enhanced_spellcheck import EnhancedSpellCheck

# Function to calculate the main metrics
def calculate_main_metrics(invalid_recognized_misspelled, valid_recognized_misspelled,
                           valid_recognized_correct, invalid_recognized_correct):
    recall = invalid_recognized_misspelled / (invalid_recognized_misspelled + valid_recognized_misspelled)
    precision = invalid_recognized_misspelled / (invalid_recognized_misspelled + invalid_recognized_correct)
    accuracy = (invalid_recognized_misspelled + valid_recognized_correct) / (
            invalid_recognized_misspelled + valid_recognized_misspelled + valid_recognized_correct + invalid_recognized_correct)
    return recall, precision, accuracy

# Function to evaluate a spell-checker
def evaluate_spell_checker(spell_checker, correct_sentence, misspell_sentence, invalid_count):
    start_time = time.time()
    spell_checker.check(misspell_sentence)
    corrected_sentence = spell_checker.correct()
    end_time = time.time()

    # Calculate time taken
    time_taken = end_time - start_time
    speed = len(misspell_sentence.split()) / time_taken

    # Calculate metrics
    invalids_remaining = sum(1 for word in corrected_sentence.split() if word not in correct_sentence.split())
    accuracy, precision, recall = calculate_metrics(invalid_count, invalids_remaining)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "speed": speed,
        "invalids_remaining": invalids_remaining
    }

# Function to calculate metrics based on corrected results
def calculate_metrics(invalid_count, invalids_remaining):
    accuracy = (invalid_count - invalids_remaining) / invalid_count
    precision = accuracy  
    recall = accuracy  
    return accuracy, precision, recall

# Function to compare two spell-checkers and output average metrics in table format
def compare_spell_checkers(spell_checker1, spell_checker2, sentences, correct_sentences):
    results1 = {"accuracy": [], "precision": [], "recall": [], "speed": [], "invalids_remaining": []}
    results2 = {"accuracy": [], "precision": [], "recall": [], "speed": [], "invalids_remaining": []}

    for idx, (misspelled, correct) in enumerate(zip(sentences, correct_sentences)):
        # Evaluate the first spell-checker
        result1 = evaluate_spell_checker(spell_checker1, correct, misspelled, len(correct.split()))
        for key in results1:
            results1[key].append(result1[key])

        # Evaluate the second spell-checker
        result2 = evaluate_spell_checker(spell_checker2, correct, misspelled, len(correct.split()))
        for key in results2:
            results2[key].append(result2[key])

    # Calculate averages for both spell-checkers
    avg_results1 = {key: sum(results1[key]) / len(results1[key]) for key in results1}
    avg_results2 = {key: sum(results2[key]) / len(results2[key]) for key in results2}

    # Prepare data for the table
    table_data = [
        ["Metric", "Original Spell-Checker ", "Enhanced Spell-Checker"],
        ["Invalids Remaining", avg_results1["invalids_remaining"] *100, avg_results2["invalids_remaining"] * 100],
        ["Accuracy (%)", avg_results1["accuracy"] * 100, avg_results2["accuracy"] * 100],
        ["Speed (words/sec)", avg_results1["speed"], avg_results2["speed"]],
        ["Precision (%)", avg_results1["precision"] * 100, avg_results2["precision"] * 100],
        ["Recall (%)", avg_results1["recall"] * 100, avg_results2["recall"] * 100],
        
        
    ]

    # Print the table
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

# Example usage with test sentences
sentences = [
    "The arrea was marked by tall trees and flowing rivers",
    "They walked through the narow street to find their way home",
    "He is glad to witnss such a wide view",
    "It is crucial to have suffient light in the room",
    "The pilot navigated the narow path through the clouds",
    "We had to rearrange the furniture to make the area more spacious",
    "A soft light shone through the window as the sun set",
    "Her voice was both calm and peacful",
    "The lake was glistening under the bright afternoon light",
    "I apprecite all the help you have given me",
    "The narrow alley was dimly lit but safe",
    "He is wide awake even though it's past midnight",
    "They decided to take a wide turn to avoid obstacles",
    "Their strategy was quite narrow in scope",
    "Glad to have met you at the conference",
    "The temprature is expected to rise gradually",
    "It is importnt to stay informed about local events",
    "He was able to witnss the event from a prime location",
    "Their dedication to the cause was remarkable and commendable",
    "The narrow beam of light illuminated the path ahead"
]

correct_sentences = [
    "The area was marked by tall trees and flowing rivers",
    "They walked through the narrow street to find their way home",
    "He is glad to witness such a wide view",
    "It is crucial to have sufficient light in the room",
    "The pilot navigated the narrow path through the clouds",
    "We had to rearrange the furniture to make the area more spacious",
    "A soft light shone through the window as the sun set",
    "Her voice was both calm and peaceful",
    "The lake was glistening under the bright afternoon light",
    "I appreciate all the help you have given me",
    "The narrow alley was dimly lit but safe",
    "He is wide awake even though it's past midnight",
    "They decided to take a wide turn to avoid obstacles",
    "Their strategy was quite narrow in scope",
    "Glad to have met you at the conference",
    "The temperature is expected to rise gradually",
    "It is important to stay informed about local events",
    "He was able to witness the event from a prime location",
    "Their dedication to the cause was remarkable and commendable",
    "The narrow beam of light illuminated the path ahead"
]

# Initialize spell-checkers
spell_checker1 = SpellCheck("words.txt")  # Original spell-checker
spell_checker2 = EnhancedSpellCheck("words.txt")  # Enhanced spell-checker

# Compare both spell-checkers and output average values
compare_spell_checkers(spell_checker1, spell_checker2, sentences, correct_sentences)
