# Guía Linux — Semana 1 (Fundamentos + Organización de Proyectos)

## 📂 Estructura de Carpetas (Nextia)
Se creó la siguiente estructura con `mkdir -p`:

proyectos/
└── nextia/
├── marketing/
│ ├── docs/
│ ├── branding/
│ ├── datasets/
│ ├── reports/
│ ├── scripts/
│ ├── notebooks/
│ ├── web/
│ ├── seo_sem/
│ └── media/
│ ├── images/
│ └── videos/


## 🔑 Comandos Aprendidos
- `pwd` → ver ruta actual.
- `ls` → listar archivos/carpetas.
- `cd <carpeta>` → moverse entre directorios.
- `cd ..` → subir un nivel.
- `mkdir -p` → crear carpetas con estructura completa.
- `tree` → visualizar árbol de carpetas.

## 🚨 Nota Importante
- Cuando ya estás dentro de una carpeta, usa `tree` directo.  
- Si quieres ver desde afuera, `cd ..` y luego `tree nombre_carpeta`.

## 📝 Resumen
Hasta ahora aprendiste a:  
1. Crear una estructura organizada para proyectos.  
2. Navegar con `cd` y verificar rutas con `pwd`.  
3. Visualizar tu proyecto con `tree`.  

Bro, buenísimo 🙌, vamos a hacer un compendio completo de lo que llevamos hasta ahora:
👉 comandos que usamos, código que ejecutaste, explicaciones claras, y un resumen al final de cada bloque.
Así lo guardas en tu docs/ y queda como tu manual interno.

📚 Guía Linux — Organización de Proyectos Nextia
1️⃣ Crear carpeta principal del proyecto

Primero, nos movimos al directorio donde queríamos trabajar (tu usuario):

cd ~


cd ~ → te lleva a tu home directory (carpeta principal del usuario).

Creamos una carpeta raíz llamada proyectos:

mkdir proyectos


mkdir → crea carpetas.

Ahora tienes la carpeta base donde vivirán todos tus proyectos.

📌 Resumen: Aprendiste a crear tu carpeta base proyectos/ en tu directorio principal.

2️⃣ Crear la estructura de Nextia completa

Nos movimos dentro de proyectos:

cd ~/proyectos


Ejecutamos este bloque para crear toda la estructura de carpetas (Nextia):

mkdir -p nextia/marketing/{docs,branding,datasets,reports,scripts,notebooks,web,seo_sem,media/{images,videos}} \
nextia/shop/{docs,products,orders,customers,media/{images,videos}} \
nextia/trading/{docs,strategies,data,scripts,token/{docs,contracts,tests,media}} \
nextia/common/{templates,research}


mkdir -p → crea carpetas y subcarpetas de golpe (sin error si ya existen).

{} → agrupa carpetas hermanas.

\ → permite que el comando ocupe varias líneas sin romperse.

📌 Resumen: Con un solo comando creaste todo el árbol de Nextia: marketing, shop, trading, common, y sus subcarpetas organizadas.

3️⃣ Verificar dónde estás

Para saber siempre tu ubicación en la terminal usamos:

pwd


Significa Print Working Directory.

Te muestra la ruta completa en la que estás trabajando.

📌 Resumen: pwd es tu brújula, nunca te pierdes con él.

4️⃣ Ver y listar carpetas

Para ver el contenido de la carpeta actual:

ls


Para ver con más detalles (permisos, tamaños, fechas):

ls -l


Para incluir archivos ocultos (que empiezan con .):

ls -a


📌 Resumen: Con ls tienes diferentes visores de carpetas: simple, detallado y completo.

5️⃣ Navegar entre carpetas

Entrar a una carpeta:

cd nombre_de_carpeta


Subir un nivel:

cd ..


Volver directo al home:

cd ~


📌 Resumen: cd es como tu teletransporte.

cd carpeta → entras.

cd .. → subes.

cd ~ → vuelves al inicio.

6️⃣ Ver estructura como árbol

Instalamos y usamos tree (si no lo tenías):

sudo apt install tree


Para visualizar tu proyecto:

tree nextia


Opciones útiles:

tree -a              # muestra también archivos ocultos
tree -L 2            # muestra hasta 2 niveles de profundidad
tree -I "backups"    # ignora ciertas carpetas


📌 Resumen: tree te da la visión de tu proyecto como un mapa jerárquico.

7️⃣ Guardar tu guía dentro de Nextia

Nos movimos a marketing/docs:

cd ~/proyectos/nextia/marketing/docs


Creamos un archivo para registrar esta enseñanza:

nano linux_basico.md


Pegamos el contenido (como este documento) y guardamos:

CTRL + O → Guardar.

CTRL + X → Salir.

📌 Resumen: Ahora tienes tu manual interno en Markdown para consultar en cualquier momento.

✅ Resumen Global hasta aquí

Creaste tu carpeta raíz proyectos/.

Levantaste toda la estructura completa de Nextia (marketing, shop, trading, common).

Aprendiste a moverte (cd), ver dónde estás (pwd), listar (ls) y visualizar jerarquías (tree).

Documentaste todo en un archivo linux_basico.md dentro de marketing/docs.
