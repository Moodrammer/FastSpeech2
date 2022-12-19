from typing import Optional

def phonetise(sentence:str, language: Optional[str]="ar"):
  """converts orthographical text into its original phonemes according to language
  rules using espeak-phonemizer
  Args:
    sentence (str): orthographical text to be phonetized
    language (Optional[str]): language to convert orthographical text based on 
                              its rules (default value is `ar`)
  Returns:
    str: phonemes contributes to form the orthographical text.
  """
  import os
  stream = os.popen(f'echo {sentence} | espeak-phonemizer -v {language} --no-stress -p " "')
  phonemes = stream.read().strip().replace('ɹ', 'r').replace('s̪', 's').replace('t̪', 't').replace('β ', 'b').replace('bb', 'bː')
  return phonemes