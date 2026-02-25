---
chunk_id: technique::web::frontend::login-form-esqueleto::001
domain: web
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [html5, loginform, esqueleto, base]
---

## Fase 1: El Esqueleto (HTML Semántico) 🏗️

El HTML es la estructura. Si usas etiquetas genéricas (`div`), los buscadores y las IAs no entienden qué estás haciendo. Usaremos etiquetas con **significado**.

Crea un archivo llamado `index.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Login Profesional</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="navbar">
        <div class="logo">MiApp</div>
        <ul class="nav-links">
            <li><a href="#">Inicio</a></li>
            <li><a href="#">Nosotros</a></li>
            <li><a href="#" class="btn-nav">Registro</a></li>
        </ul>
    </nav>

    <main class="main-container">
        <section class="login-card">
            <form id="loginForm">
                <h2>Iniciar Sesión</h2>
                <p>Ingresa tus credenciales</p>

                <div class="input-group">
                    <label for="email">Correo Electrónico</label>
                    <input type="email" id="email" placeholder="tu@email.com" required>
                </div>

                <div class="input-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" placeholder="••••••••" required>
                </div>

                <button type="submit" class="btn-submit">Entrar</button>
                
                <p class="form-footer">
                    ¿No tienes cuenta? <a href="#" id="go-to-signup">Regístrate</a>
                </p>
            </form>
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>

```

---
