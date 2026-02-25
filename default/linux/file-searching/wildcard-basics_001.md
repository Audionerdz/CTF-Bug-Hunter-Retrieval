---
chunk_id: concept::linux::file-searching::wildcards::001
domain: linux
chunk_type: concept
category: linux
confidence: high
reuse_level: universal
tags: [wildcards, asterisk, find, pattern-matching, linux]
source_file: /home/ftpuser/uploads/WINGDATA/Comandos para busquedas de Directorios o archivos sensibles.md
---

# Búsquedas con Wildcards (Comodines)

Las búsquedas con asteriscos (`*`) se conocen técnicamente como búsquedas con **Wildcards** (comodines). El asterisco actúa como un "comodín" que representa **cualquier cantidad de caracteres** (incluyendo cero).

### 1. ¿Para qué sirven?

Sirven principalmente para tres escenarios en el mundo del pentesting:

* **Desconocimiento parcial:** Sabes que el archivo tiene la palabra "secret", pero no sabes si se llama `top_secret.txt`, `secret_keys` o `secrets.zip`.
    
* **Búsqueda por extensiones:** Quieres encontrar todos los archivos de un mismo tipo (ej. todos los `.lua` o todos los `.conf`).
    
* **Rapidez:** No quieres escribir el nombre larguísimo de un directorio.