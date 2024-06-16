import unidecode

# Lista de las palabras más usadas en español
most_common_words = [
    "de", "y", "el", "la", "en", "a", "que", "los", "se", "que", "un", "las", "con", "no", "por", "una",
    "para", "su", "es", "como", "me", "más", "le", "lo", "o", "pero", "sus", "si", "este", "sobre", "entre",
    "cuando", "también", "todo", "era", "fue", "esta", "ya", "son", "mi", "sin", "la", "años", "ser", "nos",
    "te", "qué", "dos", "está", "muy", "desde", "porque", "yo", "hasta", "había", "hay", "tiene", "ese", "todos",
    "hacer", "donde", "eso", "puede", "parte", "vida", "uno", "esa", "tiempo", "él", "ella", "sólo", "dijo", "cada",
    "vez", "ni", "otro", "después", "otros", "mismo", "hace", "ahora", "les", "estaba", "así", "bien", "e", "día",
    "año", "aunque", "durante", "país", "siempre", "otra", "tres", "algo", "ver", "mundo", "los", "tan", "antes", 
    "sí", "cómo", "casa", "nada", "trabajo", "estos", "momento", "quien", "están", "gran", "esto", "forma", "mayor", 
    "personas", "ellos", "nacional", "gobierno", "sino", "primera", "unos", "hacia", "tenía", "entonces", "hoy", 
    "lugar", "ante", "luego", "estado", "otras", "días", "tener", "pues", "va", "contra", "nunca", "casi", "tienen", 
    "según", "algunos", "una", "manera", "nuevo", "además", "hombre", "millones", "dar", "mucho", "veces", "menos", 
    "todas", "primer", "presidente", "decir", "mujer", "tu", "solo", "mientras", "cosas", "mí", "debe", "tanto", 
    "aquí", "estas", "ciudad", "fueron", "historia", "más", "sin embargo", "toda", "tras", "pueden", "dice", "tipo", 
    "las", "grupo", "cual", "social", "gente", "sistema", "desarrollo", "mejor", "noche", "misma", "estar", "lado", 
    "muchos", "sea", "cuenta", "mujeres", "agua", "importante", "aún", "dentro", "cuatro", "información", "mis", 
    "madre", "salud", "nuestro", "será"
]

# Función para cargar el archivo corregido y contar las palabras
def load_corrected_output(file_path):
    word_count = {}  # Diccionario para almacenar el conteo de palabras
    with open(file_path, 'r', encoding='utf-8') as f:  
        for line in f:  # Itera sobre cada línea del archivo
            word, count = line.strip().split(',')  # Divide la línea en palabra y conteo
            word = unidecode.unidecode(word.strip('"'))  # Elimina comillas y normaliza la palabra
            count = int(count)  
            word_count[word] = count  
    return word_count  # Retorna el diccionario con el conteo de palabras

# Función para calcular el porcentaje de coincidencia
def calculate_coincidence(word_count, common_words, top_n=200):
    # Ordena las palabras por su conteo en orden descendente
    sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    # Obtiene las primeras top_n palabras
    top_words = [word for word, count in sorted_words[:top_n]]
    # Cuenta cuántas de las top_n palabras están en la lista de las palabras más usadas
    coincidence_count = sum(1 for word in top_words if word in common_words)
    # Calcula el porcentaje de coincidencia
    percentage = (coincidence_count / top_n) * 100
    return percentage  # Retorna el porcentaje de coincidencia

if __name__ == "__main__":
    output_file = 'output_corregido.txt'  
    word_count = load_corrected_output(output_file)  # Carga el conteo de palabras del archivo
    # Calcula el porcentaje de coincidencia
    percentage = calculate_coincidence(word_count, most_common_words)  
    print(f"El porcentaje de coincidencia entre las 200 palabras más usadas y las palabras en el archivo es: {percentage:.2f}%")
