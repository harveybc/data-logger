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
        # Decode the line to ensure it handles different encodings
        try:
            line = line.decode('utf-8')
        except AttributeError:
            # If already decoded (Python 3), pass
            pass
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        yield (word, sum(counts))

    def reducer_format(self, word, count):
        # Format the output as "word,count"
        yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
