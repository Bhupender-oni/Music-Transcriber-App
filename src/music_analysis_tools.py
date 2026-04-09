"""
Musical Tools & Analysis Module
Comprehensive analysis tools for Indian Classical Music
"""

import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path

class MusicalTools:
    """Advanced musical analysis tools for Indian classical music"""
    
    def __init__(self):
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
            'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
            'A#': 466.16, 'B': 493.88
        }
        
        self.indian_notes = {
            'S': 0,      # Shadaj (Root) = C
            'r': 1,      # Komal Rishabh = C#
            'R': 2,      # Shuddh Rishabh = D
            'g': 3,      # Komal Gandhar = D#
            'G': 4,      # Shuddh Gandhar = E
            'M': 5,      # Shuddh Madhyam = F
            'M#': 6,     # Tivra Madhyam = F#
            'P': 7,      # Pancham = G
            'd': 8,      # Komal Dhaivat = G#
            'D': 9,      # Shuddh Dhaivat = A
            'n': 10,     # Komal Nishad = A#
            'N': 11      # Shuddh Nishad = B
        }
        
        self.thaat_map = {
            'Bilawal': ['S', 'R', 'G', 'M', 'P', 'D', 'N'],
            'Kalyan': ['S', 'R', 'G', 'M#', 'P', 'D', 'N'],
            'Khamaj': ['S', 'R', 'G', 'M', 'P', 'D', 'n'],
            'Bhairav': ['S', 'r', 'G', 'M', 'P', 'd', 'N'],
            'Marwa': ['S', 'r', 'G', 'M#', 'P', 'D', 'N'],
            'Puriya': ['S', 'r', 'G', 'M#', 'P', 'D', 'n'],
            'Todi': ['S', 'r', 'g', 'M#', 'P', 'd', 'N'],
            'Asavari': ['S', 'R', 'g', 'M', 'P', 'd', 'n'],
            'Bhairavi': ['S', 'r', 'g', 'M', 'P', 'd', 'n'],
            'Kafi': ['S', 'R', 'g', 'M', 'P', 'D', 'n']
        }

    def analyze_raga_characteristics(self, raga_name: str, raga_data: Dict) -> Dict:
        """
        Analyze raga characteristics
        
        Returns:
            Detailed analysis of raga properties
        """
        characteristics = {
            'name': raga_name,
            'notes_count': len(raga_data.get('notes_used', [])),
            'shuddha_notes': len(raga_data.get('shuddha_notes', [])),
            'komal_notes': len(raga_data.get('komal_notes', [])),
            'vadi_note': raga_data.get('vadi', 'Unknown'),
            'samvadi_note': raga_data.get('samvadi', 'Unknown'),
            'thaat': raga_data.get('thaat', 'Unknown'),
            'time_of_day': raga_data.get('time', 'Not specified'),
            'mood': raga_data.get('mood', 'Not specified'),
            'best_instruments': raga_data.get('best_instruments', []),
            'difficulty': raga_data.get('difficulty_level', 'Unknown'),
            'performance_context': raga_data.get('performance_time', 'Concert'),
            'ascending_notes': len(raga_data.get('aaroh', [])),
            'descending_notes': len(raga_data.get('avaroh', []))
        }
        
        return characteristics

    def identify_raga_from_notes(self, notes_sequence: List[str]) -> List[Tuple[str, float]]:
        """
        Identify probable raga from a sequence of notes
        
        Args:
            notes_sequence: List of notes detected in the music
            
        Returns:
            List of probable ragas with confidence scores
        """
        # Load raga database
        try:
            with open('data/raga_database_extended.json', 'r') as f:
                db = json.load(f)
        except:
            with open('data/raga_database.json', 'r') as f:
                db = json.load(f)
        
        matches = {}
        unique_notes = list(set(notes_sequence))
        
        for raga_name, raga_info in db.get('ragas', {}).items():
            raga_notes = set(raga_info.get('notes_used', []))
            if not raga_notes:
                raga_notes = set(raga_info.get('aaroh', []) + raga_info.get('avaroh', []))
            
            # Check note match percentage
            common_notes = len(unique_notes & raga_notes)
            if common_notes > 0:
                match_score = common_notes / max(len(unique_notes), len(raga_notes))
                matches[raga_name] = match_score
        
        # Sort by match score
        sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
        return sorted_matches[:5]  # Return top 5 matches

    def analyze_note_frequency(self, notes_sequence: List[str]) -> Dict:
        """
        Analyze frequency distribution of notes
        
        Args:
            notes_sequence: List of notes
            
        Returns:
            Frequency distribution analysis
        """
        from collections import Counter
        
        note_counts = Counter(notes_sequence)
        total_notes = len(notes_sequence)
        
        analysis = {
            'total_notes_sung': total_notes,
            'unique_notes': len(note_counts),
            'note_frequencies': {},
            'most_common_note': note_counts.most_common(1)[0][0] if note_counts else None,
            'least_common_note': note_counts.most_common()[-1][0] if note_counts else None,
            'note_distribution': {}
        }
        
        for note, count in note_counts.items():
            percentage = (count / total_notes) * 100
            analysis['note_frequencies'][note] = count
            analysis['note_distribution'][note] = f"{percentage:.1f}%"
        
        return analysis

    def detect_ornamentation_types(self, pitch_contour: np.ndarray) -> Dict:
        """
        Detect types of ornamentation in the music
        
        Returns:
            Types and count of ornamentations
        """
        ornamentations = {
            'meend': 0,        # Smooth glide between notes
            'khatka': 0,       # Quick grace note
            'murki': 0,        # Rapid note sequence
            'gamak': 0,        # Oscillation on a note
            'jhala': 0,        # Rapid stringed flourish
            'kan': 0,          # Grace note before main note
            'alaap': 'Not quantified'  # Elaborate melodic development
        }
        
        # Detect meend (gradual pitch change)
        pitch_diff = np.diff(pitch_contour[~np.isnan(pitch_contour)])
        smooth_transitions = np.sum(np.abs(pitch_diff) < 50) / len(pitch_diff) if len(pitch_diff) > 0 else 0
        ornamentations['meend'] = int(smooth_transitions * 100)
        
        # Detect rapid note changes (murki, khatka)
        rapid_changes = np.sum(np.abs(pitch_diff) > 100) / len(pitch_diff) if len(pitch_diff) > 0 else 0
        ornamentations['khatka'] = int(rapid_changes * 50)
        ornamentations['murki'] = int(rapid_changes * 30)
        
        return ornamentations

    def analyze_raga_time_appropriateness(self, raga_name: str, current_time: str) -> Dict:
        """
        Check if raga is appropriate for current time
        
        Args:
            raga_name: Name of the raga
            current_time: Current time (e.g., "Morning", "Evening", "Night")
            
        Returns:
            Appropriateness analysis
        """
        time_mapping = {
            'Morning': ['Morning', 'Early Morning', 'Dawn'],
            'Afternoon': ['Afternoon', 'Late Morning', 'Midday'],
            'Evening': ['Evening', 'Sunset'],
            'Night': ['Night', 'Late Night', 'Midnight']
        }
        
        appropriate_times = []
        for period, variants in time_mapping.items():
            appropriate_times.extend(variants)
        
        return {
            'raga': raga_name,
            'current_period': current_time,
            'is_appropriate': True,  # Would check against raga_data in real implementation
            'best_times': appropriate_times
        }

    def analyze_instrument_suitability(self, raga_name: str, raga_data: Dict) -> Dict:
        """
        Analyze which instruments are best suited for the raga
        
        Returns:
            Instrument recommendations
        """
        recommended_instruments = raga_data.get('best_instruments', [])
        
        instrument_characteristics = {
            'Sitar': ['Melodic expression', 'Ornamentation', 'Resonance'],
            'Sarod': ['Deep tone', 'Shuddha notes', 'Expression'],
            'Sarangi': ['Vocal imitation', 'Meend', 'Gamak'],
            'Bansuri': ['Romantic', 'Light raags', 'Sweet tone'],
            'Vocal': ['Alaap', 'Khayal', 'Expression'],
            'Violin': ['Komal notes', 'Meend', 'Tender mood'],
            'Veena': ['South Indian', 'Classical', 'Serious'],
            'Flute': ['Light', 'Krishna raags', 'Morning'],
            'Shehnai': ['Festival', 'Devotional', 'Bright'],
            'Harmonium': ['Accompaniment', 'Drone']
        }
        
        return {
            'raga': raga_name,
            'recommended_instruments': recommended_instruments,
            'instrument_details': [
                {'instrument': inst, 'characteristics': instrument_characteristics.get(inst, [])}
                for inst in recommended_instruments
            ]
        }

    def analyze_raga_structure(self, raga_data: Dict) -> Dict:
        """
        Analyze raga's ascending and descending patterns
        
        Returns:
            Structure analysis
        """
        aaroh = raga_data.get('aaroh', [])
        avaroh = raga_data.get('avaroh', [])
        pakad = raga_data.get('pakad', [])
        
        return {
            'ascending_pattern': ' - '.join(aaroh),
            'descending_pattern': ' - '.join(avaroh),
            'characteristic_phrase': ' - '.join(pakad),
            'ascending_notes_count': len(aaroh),
            'descending_notes_count': len(avaroh),
            'total_unique_notes': len(set(aaroh + avaroh)),
            'is_symmetric': set(aaroh) == set(avaroh),
            'asymmetry_type': 'Ascending' if len(aaroh) > len(avaroh) else 'Descending' if len(avaroh) > len(aaroh) else 'Symmetric'
        }

    def analyze_raga_mood_characteristics(self, raga_name: str, raga_data: Dict) -> Dict:
        """
        Detailed mood and emotional analysis
        
        Returns:
            Mood characteristics
        """
        mood_text = raga_data.get('mood', '')
        moods = [m.strip() for m in mood_text.split(',')]
        
        mood_intensity = {
            'Romantic': 8, 'Peaceful': 7, 'Serious': 8, 'Joyful': 9,
            'Devotional': 9, 'Contemplative': 6, 'Energetic': 8,
            'Mysterious': 7, 'Tender': 7, 'Sacred': 9, 'Light': 5,
            'Deep': 8, 'Melancholic': 7, 'Festive': 9
        }
        
        intensity_scores = [mood_intensity.get(mood, 5) for mood in moods]
        avg_intensity = np.mean(intensity_scores) if intensity_scores else 5
        
        return {
            'raga': raga_name,
            'moods': moods,
            'emotional_intensity': round(avg_intensity, 1),
            'best_for': ' & '.join(moods),
            'listening_context': raga_data.get('performance_time', 'Concert performance')
        }

    def compare_ragas(self, raga1_name: str, raga2_name: str, ragas_db: Dict) -> Dict:
        """
        Compare two ragas
        
        Returns:
            Comparison analysis
        """
        raga1 = ragas_db.get(raga1_name, {})
        raga2 = ragas_db.get(raga2_name, {})
        
        notes1 = set(raga1.get('notes_used', []) or (raga1.get('aaroh', []) + raga1.get('avaroh', [])))
        notes2 = set(raga2.get('notes_used', []) or (raga2.get('aaroh', []) + raga2.get('avaroh', [])))
        
        common_notes = notes1 & notes2
        different_notes = (notes1 ^ notes2)
        
        return {
            'raga1': raga1_name,
            'raga2': raga2_name,
            'total_notes_raga1': len(notes1),
            'total_notes_raga2': len(notes2),
            'common_notes': list(common_notes),
            'different_notes': list(different_notes),
            'similarity_percentage': (len(common_notes) / max(len(notes1), len(notes2))) * 100,
            'raga1_thaat': raga1.get('thaat', 'Unknown'),
            'raga2_thaat': raga2.get('thaat', 'Unknown'),
            'same_thaat': raga1.get('thaat') == raga2.get('thaat')
        }

    def analyze_tala_structure(self, tala_name: str, tala_data: Dict) -> Dict:
        """
        Analyze rhythmic pattern structure
        
        Returns:
            Tala analysis
        """
        beats = tala_data.get('beats', [])
        total_beats = sum(beats) if beats else 0
        
        return {
            'tala_name': tala_name,
            'beat_structure': beats,
            'total_beats_in_cycle': total_beats,
            'number_of_sections': len(beats),
            'time_signature': f"{total_beats}/4" if total_beats else "Unknown",
            'description': tala_data.get('description', ''),
            'usage': tala_data.get('usage', '')
        }


class RagaMusicDatabase:
    """Comprehensive Indian classical music database"""
    
    @staticmethod
    def load_extended_database() -> Dict:
        """Load extended raga database with detailed information"""
        try:
            with open('data/raga_database_extended.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            try:
                with open('data/raga_database.json', 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                return {'ragas': {}}

    @staticmethod
    def search_ragas_by_time(time_period: str) -> List[str]:
        """Search ragas suitable for a specific time of day"""
        db = RagaMusicDatabase.load_extended_database()
        matching_ragas = []
        
        for raga_name, raga_info in db.get('ragas', {}).items():
            raga_time = raga_info.get('time', '').lower()
            if time_period.lower() in raga_time:
                matching_ragas.append(raga_name)
        
        return matching_ragas

    @staticmethod
    def search_ragas_by_mood(mood: str) -> List[str]:
        """Search ragas by emotional mood"""
        db = RagaMusicDatabase.load_extended_database()
        matching_ragas = []
        
        for raga_name, raga_info in db.get('ragas', {}).items():
            raga_mood = raga_info.get('mood', '').lower()
            if mood.lower() in raga_mood:
                matching_ragas.append(raga_name)
        
        return matching_ragas

    @staticmethod
    def get_raga_difficulty_progression() -> Dict:
        """Get ragas organized by difficulty level"""
        db = RagaMusicDatabase.load_extended_database()
        progression = {
            'Beginner': [],
            'Intermediate': [],
            'Advanced': []
        }
        
        for raga_name, raga_info in db.get('ragas', {}).items():
            difficulty = raga_info.get('difficulty_level', 'Intermediate')
            if difficulty in progression:
                progression[difficulty].append(raga_name)
        
        return progression


# Export tools
__all__ = ['MusicalTools', 'RagaMusicDatabase']
