---
chunk_id: technique::web::frontend::centrar-elementos::001
domain: web
chunk_type: technique
---

## Fase 2: El Diseño (CSS Flexbox) 🎨

Aquí es donde la mayoría se traba: **centrar elementos**. Usaremos `Flexbox`. Es la herramienta más potente para que tu login se vea igual en PC y celular.

Crea un archivo llamado `style.css`:

```css
/* 1. Reset: Limpiamos espacios que el navegador trae por defecto */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 2. Cuerpo y Fondo */
body {
    background: #f0f2f5;
    height: 100vh; /* Ocupa el 100% de la altura de la pantalla */
    display: flex;
    flex-direction: column;
}

/* 3. La Navbar */
.navbar {
    background: #ffffff;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between; /* Logo a la izquierda, links a la derecha */
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 20px;
}

/* 4. Centrado Mágico del Formulario */
.main-container {
    flex-grow: 1; /* Ocupa todo el espacio debajo de la navbar */
    display: flex;
    justify-content: center; /* Centrado horizontal */
    align-items: center;     /* Centrado vertical */
}

/* 5. La Tarjeta de Login */
.login-card {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
}

.input-group {
    margin-bottom: 1.5rem;
}

.input-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #555;
    font-weight: 600;
}

.input-group input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    outline: none;
}

/* Efecto visual al hacer clic en el input */
.input-group input:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0,123,255,0.2);
}

.btn-submit {
    width: 100%;
    padding: 0.8rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background 0.3s;
}

.btn-submit:hover {
    background: #0056b3;
}

```
