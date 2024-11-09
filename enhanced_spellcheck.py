from fuzzywuzzy import fuzz
from collections import defaultdict
from metaphone import doublemetaphone  

class EnhancedSpellCheck:
    
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
        if word[:2] == candidate[:2]:  # Check prefix
            prefix_suffix_score += 5
        if word[-2:] == candidate[-2:]:  # Check suffix
            prefix_suffix_score += 5
        
        # Phonetic similarity using Metaphone
        phonetic_score = 0
        word_metaphone = doublemetaphone(word)[0]  # Get the primary Metaphone code for the word
        candidate_metaphone = doublemetaphone(candidate)[0]  # Get the primary Metaphone code for the candidate
        if word_metaphone == candidate_metaphone:
            phonetic_score += 10  # Bonus for matching phonetic representations

        # Frequency score for high-frequency words
        frequency_score = 0
        if candidate in self.high_frequency_words:
            frequency_score += 50  # Give a significant bonus to high-frequency words
        
        # Total score is a combination of all features
        total_score = levenshtein_score + prefix_suffix_score + phonetic_score + frequency_score
        return total_score

    def suggestions(self):
        words_to_check = self.string_to_check.split()
        suggestions = defaultdict(list)
        
        for word in words_to_check:
            if word.lower() in self.dictionary:
                continue  # No correction needed if the word is correct

            word_suggestions = []
            for candidate in self.dictionary:
                # Calculate the combined similarity score for each dictionary word
                score = self.similarity_score(word.lower(), candidate)
                
                # Filter suggestions by similarity threshold
                if score >= 70:  # Threshold for acceptable similarity 
                    word_suggestions.append((candidate, score))

            # Rank suggestions by score and keep only the top suggestion(s)
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
            # Use the top suggestion if available, else keep the original word
            best_suggestion = word_suggestions.get(word, [word])[0]
            corrected_text.append(best_suggestion)

        return " ".join(corrected_text)

# Example usage
input_sentences = [
    "The arrea was marked by tall trees and flowing rivers",
    "They walked through the narow street to find their way home",
    "He is glad to witness such a wide view"
]

spell_checker = EnhancedSpellCheck("words.txt")

for sentence in input_sentences:
    spell_checker.check(sentence)
    corrected_text = spell_checker.correct()
    print(f"Original sentence: {sentence}")
    print(f"Corrected sentence: {corrected_text}\n")


