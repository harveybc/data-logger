from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# Compilar una expresión regular para encontrar palabras
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
        # Dividir la línea en palabras utilizando una expresión regular
        for word in WORD_RE.findall(line):
            # Emitir cada palabra con el conteo 1
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        # Sumar todos los conteos para cada palabra
        yield (word, sum(counts))

if __name__ == "__main__":
    MapReduce.run()
