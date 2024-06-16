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
                reducer_final=self.reducer_final
            )
        ]

    def mapper(self, _, line):
        # Decode the line to ensure it handles different encodings
        try:
            line = line.decode('utf-8')
        except AttributeError:
            # If already decoded (Python 3), pass
            pass
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        total = sum(counts)
        print(f"DEBUG: Reducer - word: {word}, total: {total}")
        yield (word, total)

    def reducer_final(self, word, counts):
        print(f"DEBUG: Reducer Final - word: {word}, counts: {counts}")
        for count in counts:
            yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
