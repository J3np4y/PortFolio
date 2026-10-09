# Portafolio profesional · Oscar Cimas Bravo

**Ver el portafolio publicado:** [https://j3np4y.github.io/PortFolio/](https://j3np4y.github.io/PortFolio/)

Web estática, adaptable a móvil y sin dependencias de build. Resume la experiencia profesional, el stack y los proyectos publicados en GitHub. El CV PDF se sirve desde el propio sitio para que el botón de descarga funcione directamente.

## Verlo en local

Abre `index.html` en el navegador o sirve la carpeta con cualquier servidor estático.

## Publicarlo con GitHub Pages

El sitio se publica desde la rama `j3np4y-portafolio-profesional`, en la carpeta `/ (root)`. Para cambiar la rama de publicación, ve a `Settings > Pages` y selecciona `Deploy from a branch`.

## Contenido y mantenimiento

- `index.html`: propuesta de valor, resumen para selección, trayectoria, casos de estudio, stack y contacto.
- `styles.css`: estilos adaptables y preferencias de movimiento reducido.
- `CV-Oscar-Cimas-Bravo.pdf`: CV descargable, enlazado con el atributo `download`.
- `generate-cv.py`: generador del PDF con la biblioteca estándar de Python.
- Los casos de estudio distinguen métricas técnicas verificables de métricas de negocio que no están publicadas.

Para regenerar el PDF, ejecuta `python generate-cv.py`. Para actualizar el CV, edita su contenido en ese script; los enlaces de descarga conservan el mismo nombre de archivo.
