"""
Text Splitter Utility for SayAs

Splits long text into manageable chunks for TTS processing.
Handles sentence boundaries intelligently.
"""

import re
from typing import List


# Default maximum characters per chunk (safe limit for Chatterbox with voice cloning)
DEFAULT_MAX_CHUNK_SIZE = 800

# Sentence-ending punctuation
SENTENCE_ENDINGS = re.compile(r'([.!?。！？])\s*')

# Abbreviations that don't end sentences (lowercase)
ABBREVIATIONS = frozenset([
    'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr', 'vs', 'etc', 'inc', 'ltd',
    'co', 'corp', 'vol', 'rev', 'gen', 'col', 'lt', 'sgt', 'capt', 'cmdr',
    'adm', 'pvt', 'cpl', 'maj', 'st', 'ave', 'blvd', 'rd', 'ct', 'ln',
    'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'am', 'pm', 'a.m', 'p.m'
])


def is_abbreviation(word: str) -> bool:
    """Check if a word is a known abbreviation."""
    return word.lower().rstrip('.') in ABBREVIATIONS


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences, respecting abbreviations.
    
    Args:
        text: Input text to split
        
    Returns:
        List of sentences
    """
    sentences = []
    current_pos = 0
    
    # Find all potential sentence endings
    for match in SENTENCE_ENDINGS.finditer(text):
        end_pos = match.end()
        punct = match.group(1)
        
        # Look back to find the word before the punctuation
        word_match = re.search(r'\b(\w+)\s*$', text[current_pos:match.start()])
        if word_match:
            word = word_match.group(1)
            # If it's an abbreviation, skip this split
            if is_abbreviation(word):
                continue
        
        # Extract sentence
        sentence = text[current_pos:end_pos].strip()
        if sentence:
            sentences.append(sentence)
        current_pos = end_pos
    
    # Add remaining text
    remaining = text[current_pos:].strip()
    if remaining:
        sentences.append(remaining)
    
    return sentences


def split_text(text: str, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE) -> List[str]:
    """
    Split long text into chunks that fit within the character limit.
    
    Tries to split at sentence boundaries when possible.
    
    Args:
        text: Input text to split
        max_chunk_size: Maximum characters per chunk (default: 800)
        
    Returns:
        List of text chunks
    """
    # If text is already short enough, return as-is
    if len(text) <= max_chunk_size:
        return [text]
    
    # Split into sentences first
    sentences = split_into_sentences(text)
    
    # Group sentences into chunks
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_len = len(sentence) + 1  # +1 for space
        
        # If single sentence is too long, split it by words
        if sentence_len > max_chunk_size:
            # First, save current chunk if any
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            
            # Split long sentence by words
            words = sentence.split()
            word_chunk = []
            word_length = 0
            
            for word in words:
                word_len = len(word) + 1
                if word_length + word_len > max_chunk_size:
                    if word_chunk:
                        chunks.append(' '.join(word_chunk))
                    word_chunk = [word]
                    word_length = len(word)
                else:
                    word_chunk.append(word)
                    word_length += word_len
            
            if word_chunk:
                current_chunk = word_chunk
                current_length = word_length
        
        # If adding this sentence exceeds limit, save current chunk
        elif current_length + sentence_len > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_len
        else:
            current_chunk.append(sentence)
            current_length += sentence_len
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def create_silence(duration: float = 0.5, sample_rate: int = 22050) -> 'torch.Tensor':
    """
    Create a silence tensor of specified duration.
    
    Args:
        duration: Duration in seconds (default: 0.5)
        sample_rate: Audio sample rate (default: 22050)
        
    Returns:
        Tensor of silence (zeros)
    """
    import torch
    samples = int(duration * sample_rate)
    return torch.zeros(1, samples)


def stitch_audio_segments(
    segments: List['torch.Tensor'],
    sample_rate: int = 22050,
    silence_duration: float = 0.5
) -> 'torch.Tensor':
    """
    Stitch multiple audio segments together with silence gaps.
    
    Args:
        segments: List of audio tensors to concatenate
        sample_rate: Audio sample rate
        silence_duration: Duration of silence between segments (seconds)
        
    Returns:
        Combined audio tensor
    """
    import torch
    
    if not segments:
        return torch.zeros(1, 0)
    
    if len(segments) == 1:
        return segments[0]
    
    # Create silence tensor
    silence = create_silence(silence_duration, sample_rate)
    
    # Combine segments with silence between them
    result_parts = []
    for i, segment in enumerate(segments):
        result_parts.append(segment)
        # Add silence after each segment except the last
        if i < len(segments) - 1:
            result_parts.append(silence)
    
    return torch.cat(result_parts, dim=-1)


def estimate_duration(text: str, chars_per_second: float = 15.0) -> float:
    """
    Estimate the duration of speech for given text.
    
    Args:
        text: Input text
        chars_per_second: Average characters per second (default: 15.0)
        
    Returns:
        Estimated duration in seconds
    """
    return len(text) / chars_per_second


if __name__ == "__main__":
    # Test the splitter
    test_text = """
    This is a long text. It has multiple sentences! Does it work correctly?
    Mr. Smith went to Washington. He arrived at 5 p.m. sharp. The meeting was held on St. James Ave.
    Dr. Jones met him there. They discussed various topics, etc. This is another sentence!
    """ * 10
    
    print(f"Original length: {len(test_text)} characters")
    
    chunks = split_text(test_text, max_chunk_size=200)
    
    print(f"\nSplit into {len(chunks)} chunks:\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({len(chunk)} chars):")
        display = chunk[:100] + "..." if len(chunk) > 100 else chunk
        print(f"  {display}")
        print()
