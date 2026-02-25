---
chunk_id: technique::web::injection::insecure-deserialization::001
domain: web
chunk_type: reference
confidence: 5
reuse_level: 5
tags: [yososerial, serialization, transformers, javascript, deserialization, rce, gadgets, web-security]
---

# Deserialización Insegura: De Objetos a Ejecución de Código

La deserialización insegura ocurre cuando una aplicación utiliza datos suministrados por el usuario para reconstruir objetos en memoria sin la validación adecuada, permitiendo que un atacante manipule la lógica de la aplicación o ejecute comandos.



## 1. Conceptos Fundamentales

En el desarrollo moderno, las aplicaciones necesitan mover objetos complejos a través de medios que solo entienden bytes o texto.

* **Serialización (Empaquetado)**: Convierte un objeto vivo en memoria (Java, PHP, Python) en un formato transportable como JSON, XML o bytes binarios.
    * *Ejemplo*: `User(id=1, role="user")` -> `{"id":1, "role":"user"}`
* **Deserialización (Desempaquetado)**: El proceso inverso donde el flujo de datos se reconstruye en un objeto vivo para que el servidor pueda interactuar con sus métodos.



## 2. La Mentalidad del Atacante (The Gadget Chain)

Un atacante no ve la serialización como transporte, sino como una **inyección de estado**. El peligro reside en los "Objetos Mágicos" o métodos que se ejecutan automáticamente al instanciarse (ej. `__wakeup` en PHP, `readObject` en Java).

### Escenario de Explotación:
1.  **Identificación**: El atacante detecta datos serializados en cookies, parámetros URL o cabeceras (ej: firmas de Java `AC ED 00 05` o Base64).
2.  **Manipulación**: Se decodifica el objeto para alterar atributos (ej: cambiar `isAdmin: false` a `true`).
3.  **Inyección de Gadgets**: El atacante envía un objeto malicioso diseñado para que, al ser "desempaquetado", invoque funciones del sistema operativo. Esto se conoce como **Remote Code Execution (RCE)**.



## 3. Checklist de Auditoría Técnica

Para auditar esta vulnerabilidad, sigue este flujo:

| Paso | Acción Técnica |
| :--- | :--- |
| **1. Identificar** | ¿Es JSON, XML, YAML o un formato nativo de lenguaje (Pickle, Java Serialization)? |
| **2. Probar Integridad** | ¿Si modifico un byte, el servidor devuelve errores de stack trace detallados? |
| **3. Escalar** | Intentar modificar campos de tipo booleano o IDs de usuario dentro del objeto. |
| **4. Ejecutar** | Usar herramientas como `ysoserial` (Java) o `PHPGGC` (PHP) para generar payloads de RCE. |

## 4. Estrategias de Mitigación

Para neutralizar este vector de ataque, aplica la defensa en profundidad:

1.  **Evitar la Serialización Nativa**: Priorizar formatos de solo datos como JSON o XML plano que no permitan la instanciación de clases complejas.
2.  **Validación de Integridad**: Implementar firmas digitales (HMAC) o tokens (JWT) para asegurar que el objeto no ha sido modificado en tránsito.
3.  **Aislamiento**: Ejecutar el código de deserialización en entornos con privilegios mínimos para mitigar el impacto de un RCE.

> [!WARNING]
> La deserialización insegura es a menudo "invisible" en los escaneos automáticos. Requiere un análisis profundo de cómo el backend maneja el estado de la sesión y los objetos persistentes.
