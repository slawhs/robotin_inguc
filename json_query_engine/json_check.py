from os import path
from jsonpath_ng.ext import parse
import json

with open(path.join('data', 'places.json')) as f:
    json_dict = json.load(f)

# Definir la expresión JSONPath
jsonpath_expr = parse("$.places[?(@.name == 'M1')].coordinates")

# Ejecutar la consulta JSONPath
result = jsonpath_expr.find(json_dict)

# Mostrar los resultados
coordinates = [match.value for match in result]
print(coordinates)