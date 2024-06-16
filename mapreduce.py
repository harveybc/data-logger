from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"\w+")

class MapReduce(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer,
                reducer_final=self.reducer_format
            )
        ]

    def mapper(self, _, line):
        print(f"DEBUG: Mapper input line: {line}")
        try:
            line = line.decode('utf-8')
            print(f"DEBUG: Decoded line: {line}")
        except AttributeError:
            print(f"DEBUG: Line already decoded: {line}")
            # Already decoded in Python 3
            pass
        for word in WORD_RE.findall(line):
            print(f"DEBUG: Mapper yield: {word.lower()}, 1")
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        total = sum(counts)
        print(f"DEBUG: Reducer - word: {word}, total: {total}")
        yield (word.encode('utf-8'), total)

    def reducer_format(self, _, word_count_pairs):
        for word, count in word_count_pairs:
            word = word.decode('utf-8')  # Ensure word is a string
            print(f"DEBUG: Reducer Final - word: {word}, count: {count}")
            yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
