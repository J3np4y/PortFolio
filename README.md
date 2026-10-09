# Portafolio profesional · Oscar Cimas Bravo

**Ver el portafolio publicado:** [https://j3np4y.github.io/PortFolio/](https://j3np4y.github.io/PortFolio/)

Web estática, adaptable a móvil y sin dependencias de build. Resume la experiencia backend, el stack y los proyectos WebGL y Nexora. El CV PDF actualizado se sirve desde el propio sitio para que el botón de descarga funcione directamente.

## Verlo en local

Abre `index.html` en el navegador o sirve la carpeta con cualquier servidor estático.

## Publicarlo con GitHub Pages

El sitio se publica desde la rama `main`, en la carpeta `/ (root)`. La configuración está en `Settings > Pages` (`Deploy from a branch`).

## Contenido y mantenimiento

- `index.html`: propuesta de valor, resumen para selección, trayectoria, casos de estudio de Nexora y WebGL, stack y contacto.
- `styles.css`: estilos adaptables y preferencias de movimiento reducido.
- `CV-Oscar-Cimas-Bravo.pdf`: CV descargable, enlazado con el atributo `download`.
- `generate-cv.py`: generador del PDF con la biblioteca estándar de Python.
- Los resultados se limitan a pruebas y capacidades verificadas; Nexora se identifica como prototipo educativo, no listo para producción.

Para regenerar el PDF, ejecuta `python generate-cv.py`. El PDF público omite el teléfono y las referencias personales del DOCX fuente; para modificar su contenido, edita el script. Los enlaces de descarga conservan el mismo nombre de archivo.
