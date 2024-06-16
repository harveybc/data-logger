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
        if isinstance(line, bytes):
            line = line.decode('utf-8')  # Decode bytes to str
        print(f"DEBUG: Mapper input line (type: {type(line)}): {line}")
        for word in WORD_RE.findall(line):
            print(f"DEBUG: Mapper yield: {word.lower()}, 1")
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        total = sum(counts)
        print(f"DEBUG: Reducer - word: {word} (type: {type(word)}), total: {total}")
        yield (word, total)

    def reducer_format(self, _, word_count_pairs):
        for word, count in word_count_pairs:
            if isinstance(word, bytes):
                word = word.decode('utf-8')  # Ensure word is a string
            print(f"DEBUG: Reducer Final - word: {word}, count: {count}")
            yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
