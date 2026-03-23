# pyfuzz

```
██████╗ ██╗   ██╗███████╗██╗   ██╗███████╗███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║╚══███╔╝╚══███╔╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║  ███╔╝   ███╔╝
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║ ███╔╝   ███╔╝
██║        ██║   ██║     ╚██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝
```

Web directory fuzzer escrito en Python.

---

## Uso

```bash
./pyfuzz.py [opciones] <uri>
```

## Argumentos

| Argumento | Descripción |
|---|---|
| `uri` | URL objetivo. Ej: `http://target.com` |
| `-w`, `--wordlist` | Uno o más archivos de wordlist. La lista final es la unión de todos los archivos (palabras únicas). |
| `-s`, `--start` | Comenzar desde una línea específica del wordlist. Por defecto: `0`. |
| `-R`, `--allow-redirects` | Seguir redirecciones `3xx`. |

## Ejemplos

**Fuzzing básico:**
```bash
./pyfuzz.py -w wordlist.txt http://target.com
```

**Múltiples wordlists:**
```bash
./pyfuzz.py -w wordlist.txt extra.txt http://target.com
```

**Continuar desde una línea específica:**
```bash
./pyfuzz.py -w wordlist.txt -s 500 http://target.com
```

**Seguir redirecciones:**
```bash
./pyfuzz.py -w wordlist.txt -R http://target.com
```

**Combinado:**
```bash
./pyfuzz.py -w wordlist.txt fuzz.txt -s 100 -R http://target.com
```

## Notas

- Cuando se pasan múltiples wordlists con `-w`, se deduplican automáticamente — la lista efectiva es la unión de todas las entradas únicas.
- `-s` es útil para retomar una sesión interrumpida sin volver a procesar entradas ya probadas.
