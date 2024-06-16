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
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        yield (word, sum(counts))

    def reducer_format(self, _, word_count_pairs):
        for word, count in word_count_pairs:
            yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
