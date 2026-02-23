---
chunk_id: technique::web::frontend::explicacion-css::loginform::centrar-elementos::002
domain: web
chunk_type: technique
---

# Normalización de estilos y maquetación centrada con CSS Flexbox

La calidad de una interfaz web depende de la eliminación de los estilos predeterminados del navegador y de la implementación de un modelo de caja consistente. Esto permite un control absoluto sobre el espaciado y el posicionamiento.



## 1. El Reset Universal y el Modelo de Caja
El primer paso de todo profesional es normalizar los márgenes y asegurar que el padding no altere las dimensiones calculadas de los elementos.

- **Selector Universal (`*`)**: Aplica las reglas a todos los elementos del DOM.
- **box-sizing: border-box**: Modifica el modelo de caja para que el `padding` y el `border` se incluyan dentro del ancho y alto especificados, evitando que los elementos se "inflen" involuntariamente.

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

```

## 2. Centrado Absoluto Moderno

Utilizar Flexbox elimina la complejidad de los cálculos manuales de márgenes o posiciones absolutas para centrar componentes.

* **height: 90vh**: Define que el contenedor ocupe el 90% de la altura de la ventana (Viewport Height).
* **display: flex**: Habilita el modelo de caja flexible.
* **justify-content: center**: Alinea el contenido en el eje horizontal (eje principal).
* **align-items: center**: Alinea el contenido en el eje vertical (eje cruzado).

```css
.main-container {
    height: 90vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f8f9fa;
}

```

## 3. Estilización de Contenedores (The "Card" Effect)

Para generar jerarquía visual y profundidad, se aplican bordes redondeados y sombreados suaves que separan el contenido del fondo.

* **border-radius**: Define la curvatura de las esquinas (12px es el estándar moderno para tarjetas).
* **box-shadow**: Aporta profundidad mediante sombras difusas (procurar opacidades bajas como `0.08` para un look limpio).
* **max-width**: Garantiza que el diseño sea responsivo, limitando el crecimiento del contenedor en pantallas de escritorio.

```css
.login-card {
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    width: 100%;
    max-width: 400px;
}

```
