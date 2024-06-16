from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"\w+")

class MapReduce(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer
            )
        ]

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        yield (self.decode_unicode(word), sum(counts))

    def decode_unicode(self, text):
        # Decodificar caracteres Unicode a su forma legible
        return text.encode('latin1').decode('utf-8')

    def reducer_final(self, word, count):
        yield (word, count)

    def reducer_format(self, word, count):
        # Formatear la salida como "palabra,contador"
        yield None, f"{word},{count}"

if __name__ == "__main__":
    MapReduce.run()
