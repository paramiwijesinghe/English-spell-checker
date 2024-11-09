import time
from fuzzywuzzy import fuzz
from collections import defaultdict
from metaphone import doublemetaphone

class SpellCheck:
    def __init__(self, word_dict_file=None):
        # Load the dictionary and preprocess it
        with open(word_dict_file, 'r') as file:
            data = file.read().split(",")
            self.dictionary = list(set(word.strip().lower() for word in data))

        # Predefined list of common words
        self.high_frequency_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'on', 'with', 'as',
            'at', 'by', 'this', 'from', 'you', 'not', 'but', 'his', 'they', 'say', 'her', 'she', 'or', 'an'
        }

    def check(self, string_to_check):
        self.string_to_check = string_to_check

    def similarity_score(self, word, candidate):
        # Levenshtein distance (fuzz.ratio)
        levenshtein_score = fuzz.ratio(word, candidate)

        # Prefix/Suffix matching
        prefix_suffix_score = 0
        if word[:2] == candidate[:2]:  # Prefix match
            prefix_suffix_score += 5
        if word[-2:] == candidate[-2:]:  # Suffix match
            prefix_suffix_score += 5

        # Phonetic similarity using Metaphone
        phonetic_score = 0
        word_metaphone = doublemetaphone(word)[0]
        candidate_metaphone = doublemetaphone(candidate)[0]
        if word_metaphone == candidate_metaphone:
            phonetic_score += 10  # Matching phonetic codes

        # High-frequency word bonus
        frequency_score = 0
        if candidate in self.high_frequency_words:
            frequency_score += 50

        # Total score from all features
        total_score = levenshtein_score + prefix_suffix_score + phonetic_score + frequency_score
        return total_score

    def suggestions(self):
        words_to_check = self.string_to_check.split()
        suggestions = defaultdict(list)

        for word in words_to_check:
            if word.lower() in self.dictionary:
                continue  # No correction needed

            word_suggestions = []
            for candidate in self.dictionary:
                # Calculate similarity score
                score = self.similarity_score(word.lower(), candidate)

                # Filter based on score threshold
                if score >= 70:
                    word_suggestions.append((candidate, score))

            # Sort and store the top suggestion
            if word_suggestions:
                sorted_suggestions = sorted(word_suggestions, key=lambda x: x[1], reverse=True)
                suggestions[word] = [suggestion[0] for suggestion in sorted_suggestions[:1]]  # Top suggestion only

        return suggestions

    def correct(self):
        words_to_check = self.string_to_check.split()
        corrected_text = []

        # Get suggestions for each word
        word_suggestions = self.suggestions()

        for word in words_to_check:
            # Use the top suggestion if available
            best_suggestion = word_suggestions.get(word, [word])[0]
            corrected_text.append(best_suggestion)

        return " ".join(corrected_text)

    def calculate_metrics(self, ground_truth_sentences):
        # Calculate performance metrics
        total_words = 0
        correct_corrections = 0
        total_corrections = 0
        start_time = time.time()

        for i, sentence in enumerate(ground_truth_sentences):
            self.check(sentence["input"])
            corrected_text = self.correct()
            corrected_words = corrected_text.split()
            total_words += len(corrected_words)

            # Count correct corrections
            original_words = sentence["input"].split()
            ground_truth_words = sentence["corrected"].split()
            total_corrections += len(ground_truth_words)

            for j in range(min(len(corrected_words), len(ground_truth_words))):
                if corrected_words[j] == ground_truth_words[j]:
                    correct_corrections += 1

        # Calculate metrics
        accuracy = (correct_corrections / total_corrections)*100 if total_corrections else 0
        precision = (correct_corrections / total_corrections)*100 if total_corrections else 0
        recall = (correct_corrections / total_words)*100 if total_words else 0
        end_time = time.time()
        speed = total_words / (end_time - start_time)  # Words per second

        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"Speed: {speed:.2f} words/sec")

# Example usage
input_sentences = [
    {"input": "The arrea was marked by tall trees and flowing rivers", "corrected": "The area was marked by tall trees and flowing rivers"},
    {"input": "They walked through the narow street to find their way home", "corrected": "They walked through the narrow street to find their way home"},
    {"input": "He is glad to witnss such a wide view", "corrected": "He is glad to witness such a wide view"},
    {"input": "It is crucial to have suffient light in the room", "corrected": "It is crucial to have sufficient light in the room"},
    {"input": "The pilot navigated the narow path through the clouds", "corrected": "The pilot navigated the narrow path through the clouds"},
    {"input": "We had to rearrange the furniture to make the area more spacious", "corrected": "We had to rearrange the furniture to make the area more spacious"},
    {"input": "A soft light shone through the window as the sun set", "corrected": "A soft light shone through the window as the sun set"},
    {"input": "Her voice was both calm and peacful", "corrected": "Her voice was both calm and peaceful"},
    {"input": "The lake was glistening under the bright afternoon light", "corrected": "The lake was glistening under the bright afternoon light"},
    {"input": "I apprecite all the help you have given me", "corrected": "I appreciate all the help you have given me"},
    {"input": "The narrow alley was dimly lit but safe", "corrected": "The narrow alley was dimly lit but safe"},
    {"input": "He is wide awake even though it's past midnight", "corrected": "He is wide awake even though it's past midnight"},
    {"input": "They decided to take a wide turn to avoid obstacles", "corrected": "They decided to take a wide turn to avoid obstacles"},
    {"input": "Their strategy was quite narrow in scope", "corrected": "Their strategy was quite narrow in scope"},
    {"input": "Glad to have met you at the conference", "corrected": "Glad to have met you at the conference"},
    {"input": "The temprature is expected to rise gradually", "corrected": "The temperature is expected to rise gradually"},
    {"input": "It is importnt to stay informed about local events", "corrected": "It is important to stay informed about local events"},
    {"input": "He was able to witnss the event from a prime location", "corrected": "He was able to witness the event from a prime location"},
    {"input": "Their dedication to the cause was remarkable and commendable", "corrected": "Their dedication to the cause was remarkable and commendable"},
    {"input": "The narrow beam of light illuminated the path ahead", "corrected": "The narrow beam of light illuminated the path ahead"}
]


spell_checker = SpellCheck("words.txt")

for sentence in input_sentences:
    spell_checker.check(sentence["input"])
    corrected_text = spell_checker.correct()
    print(f"Original sentence: {sentence['input']}")
    print(f"Corrected sentence: {corrected_text}\n")

# Call metrics calculation function
spell_checker.calculate_metrics(input_sentences)
