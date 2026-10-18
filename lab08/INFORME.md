# Laboratorio 08 Django REST Framework

FarmaPoint

Integrantes: Dario Maza, Sheila Aguirre y Jose Contreras.

Fecha de revisión: 17 de octubre de 2026.


La revisión original del PDF era una propuesta sin ejecución ni capturas. El repositorio consultado hoy ya tenía una implementación parcial. Se conservó ese trabajo y se completaron los recursos y comprobaciones que el PDF exige, sin presentar los resultados anteriores como pruebas de esta ejecución.


Se usó una base SQLite de demostración separada: una categoría, tres productos, tres clientes, tres ventas, seis detalles, tres zonas, tres farmacias y tres evaluaciones. Todos los registros llevan LAB08. Las pruebas automatizadas usan otra base temporal independiente.


Las imágenes de código son capturas de un visor de los archivos reales, con líneas numeradas. Las imágenes de resultados son capturas de JSON producido por peticiones HTTP efectivas al servidor local. Las salidas de serialización proceden de un script Python con Django inicializado, equivalente al código ejecutable en manage.py shell. No se presentan estas imágenes como una terminal ni como Postman.


Las pantallas navegables de DRF se capturaron directamente en Edge. Se adjunta una colección Postman con variables y encadenamiento de IDs para repetir el CRUD. Si se exige estrictamente una captura dentro de Postman o Thunder Client, debe repetirse allí; la evidencia incluida utiliza otro cliente HTTP.


La configuración es local y la API conserva AllowAny de DRF. Las operaciones de escritura de los recursos CRUD no requieren autenticación. Esta entrega no certifica seguridad de producción ni añade facturación, permisos por rol o escritura anidada de ventas.


La copia pública fue preparada desde main para publicar únicamente el trabajo del Lab 08. Los cambios locales previos de Semana 7 se conservaron en la carpeta original y se probaron por separado. Por eso se informan 25 pruebas en publicación y 32 en el entorno local.



## Ejercicio 01 Instalar DRF e identificar recursos


Se revisó main en GitHub al 17 de octubre de 2026, revisión 8c901e4. Esta versión ya incorporaba Django REST Framework, ProductoQuerySet.con_stock(), serializers, vistas genéricas y ViewSets. Se integró en la copia local preservando las modificaciones previas de las semanas 6 y 7. Se verificó Django 5.2.17 y DRF 3.18.3, con rest_framework en INSTALLED_APPS.


Producto se utiliza como recurso simple y Venta como recurso relacionado. Zona, Farmacia y EvaluacionUbicacion cubren la investigación de ubicaciones. La API reutiliza los modelos y no añade tablas. La configuración permite elegir una SQLite separada mediante FARMAPOINT_DB. manage.py check no reportó problemas y makemigrations --check --dry-run no detectó cambios.


**Justificación.** DRF incorpora acceso JSON sin sustituir la interfaz HTML ni el Admin. El PDF de partida afirmaba que no había un QuerySet personalizado: esa descripción se actualizó porque el repositorio de hoy sí lo contiene.


![E01_C01_modelos](evidencias/E01_C01_modelos.png)


![E01_C02_settings](evidencias/E01_C02_settings.png)


![E01_C03_requirements](evidencias/E01_C03_requirements.png)



## Ejercicio 02 ModelSerializer y serialización


ProductoSerializer define id, nombre, descripcion, precio, stock, categoria y categoria_nombre. El identificador categoria permite escribir la relación; categoria_nombre es de solo lectura y obtiene el nombre mediante source="categoria.nombre".


Se serializó un producto y después los tres productos ficticios con many=True. Los resultados reales están en E02_C02_objeto.json y E02_C03_queryset.json. La colección se consultó con select_related("categoria") para evitar consultas adicionales por cada nombre de categoría.


**Justificación.** El serializer convierte instancias del ORM en tipos representables por el renderizador JSON. many=True indica una colección; no cambia los registros ni sustituye una consulta.


![E02_C01_serializer](evidencias/E02_C01_serializer.png)


![E02_C02_objeto](evidencias/E02_C02_objeto.png)


![E02_C03_queryset](evidencias/E02_C03_queryset.png)



## Ejercicio 03 Deserialización y validación


validate_precio rechaza valores iguales o menores que cero. La entrada válida usó precio 2.50, stock 1 y una categoría existente. is_valid() devolvió True; validated_data incluyó un Decimal y la instancia relacionada. save() creó un objeto y se comprobó su existencia dentro de una transacción.


La prueba inválida envió precio 0: is_valid() devolvió False y errors incluyó el campo precio. La creación válida se revirtió explícitamente al terminar la demostración, de modo que no dejó un producto temporal. Los datos que fallan validación nunca se guardaron.


**Justificación.** La validación del serializer protege las entradas de la API antes de persistirlas. No constituye una restricción universal de la base de datos para escrituras que omitan el serializer.


![E03_C01_validacion](evidencias/E03_C01_validacion.png)


![E03_C02_valido](evidencias/E03_C02_valido.png)


![E03_C03_invalido](evidencias/E03_C03_invalido.png)



## Ejercicio 04 Vistas genéricas


Se conservaron ProductoListCreateAPIView y ProductoRetrieveUpdateDestroyAPIView del repositorio. La primera resuelve GET y POST de colección; la segunda resuelve GET, PUT, PATCH y DELETE de un producto. Ambas utilizan ProductoSerializer y cargan la categoría con select_related.


Se comprobaron GET /api/v1/basico/productos/ y GET /api/v1/basico/productos/1/, ambos con HTTP 200. Las rutas HTML existentes permanecieron disponibles.


**Justificación.** El prefijo basico conserva la etapa de vistas genéricas para demostrar el ejercicio. La API principal usa el router en otra dirección; ninguna URL queda registrada dos veces para las mismas operaciones.


![E04_C01_vistas](evidencias/E04_C01_vistas.png)


![E04_C02_urls](evidencias/E04_C02_urls.png)


![E04_C03_lista](evidencias/E04_C03_lista.png)


![E04_C04_detalle](evidencias/E04_C04_detalle.png)



## Ejercicio 05 ModelViewSet y DefaultRouter


La API principal utiliza DefaultRouter y registra categorías, productos, farmacias, ventas, zonas y evaluaciones. Los cuatro primeros recursos proceden de la revisión pública; zonas y evaluaciones se incorporaron para cubrir la investigación descrita en el PDF.


GET /api/v1/ devolvió HTTP 200 con los seis recursos. Las operaciones de productos están en /api/v1/productos/ y /api/v1/productos/<id>/. Se conserva el prefijo versionado del repositorio actual en lugar de cambiarlo al /api/ orientativo del documento.


**Justificación.** ModelViewSet agrupa las acciones CRUD y el router genera los patrones de lista y detalle. La separación por prefijos permite comparar la etapa genérica con la implementación principal sin conflictos de resolución.


![E05_C01_viewset](evidencias/E05_C01_viewset.png)


![E05_C02_router](evidencias/E05_C02_router.png)


![E05_C03_api_root](evidencias/E05_C03_api_root.png)



## Ejercicio 06 CRUD y códigos HTTP


Se ejecutaron peticiones HTTP reales a productos mediante urllib contra el servidor local de demostración. Se registró método, URL, cuerpo enviado, código y respuesta. El producto temporal creado por POST fue el mismo que se modificó y eliminó.


Resultados: GET lista 200; GET detalle 200; POST válido 201; POST con precio 0, 400; PATCH stock, 200; DELETE, 204 sin cuerpo; GET posterior al mismo ID, 404. También se comprobó en el ORM que el registro borrado ya no existía.


**Justificación.** Las capturas corresponden a un visor de resultados HTTP, no a Postman ni Thunder Client. Se adjunta una colección importable de Postman para reproducir el recorrido si el docente exige esa interfaz concreta. La API devuelve datos; los templates generan páginas HTML.


![E06_C01_get_lista](evidencias/E06_C01_get_lista.png)


![E06_C02_get_detalle](evidencias/E06_C02_get_detalle.png)


![E06_C03_post_valido](evidencias/E06_C03_post_valido.png)


![E06_C04_post_invalido](evidencias/E06_C04_post_invalido.png)


![E06_C05_patch](evidencias/E06_C05_patch.png)


![E06_C06_delete](evidencias/E06_C06_delete.png)


![E06_C07_no_encontrado](evidencias/E06_C07_no_encontrado.png)



## Ejercicio 07 Solo lectura con relación anidada


VentaReadSerializer incluye ClienteSerializer y una colección de DetalleVentaReadSerializer. Cada detalle incorpora ProductoSerializer, cantidad, precio unitario y subtotal. VentaReadOnlyViewSet publica lista y detalle y rechaza POST con HTTP 405.


Se serializaron las mismas tres ventas, con seis detalles y sus productos, antes y después de optimizar. La versión sin precarga realizó 19 consultas y la optimizada 4. Ambas respuestas fueron iguales. Se usa select_related("cliente") y prefetch_related("detalles__producto__categoria").


**Justificación.** Se incluyó categoría en la precarga porque ProductoSerializer muestra categoria_nombre. La medición evalúa serializer.data completo; no mide solamente list(queryset), que omitiría los accesos anidados y produciría una comparación engañosa.


![E07_C01_serializer_anidado](evidencias/E07_C01_serializer_anidado.png)


![E07_C02_queryset_optimizado](evidencias/E07_C02_queryset_optimizado.png)


![E07_C03_consultas_antes](evidencias/E07_C03_consultas_antes.png)


![E07_C04_consultas_despues](evidencias/E07_C04_consultas_despues.png)


![E07_C05_respuesta_api](evidencias/E07_C05_respuesta_api.png)



## Ejercicio 08 Búsqueda ordenamiento filtro y acción


ProductoViewSet usa SearchFilter sobre nombre, descripción y categoría; OrderingFilter permite nombre, precio y stock. El parámetro disponible selecciona productos con o sin existencias. La acción con-stock reutiliza ProductoQuerySet.con_stock() y también respeta los filtros.


La búsqueda Analgesico devolvió dos registros; el orden por precio mostró 5.50, 8.90 y 12.00; búsqueda y orden combinados devolvieron 5.50 y 12.00. La acción con-stock devolvió los dos productos cuyo stock es positivo. Farmacia filtra el campo estado con comparación sin distinguir mayúsculas.


**Justificación.** Los filtros componen consultas reutilizables. Se conserva la acción con-stock existente y se añade activas para Farmacia en el ejercicio 13, cubriendo ambas variantes del repositorio y del PDF.


![E08_C01_filtros](evidencias/E08_C01_filtros.png)


![E08_C02_filtro_estado](evidencias/E08_C02_filtro_estado.png)


![E08_C03_action](evidencias/E08_C03_action.png)


![E08_C04_search](evidencias/E08_C04_search.png)


![E08_C05_ordering](evidencias/E08_C05_ordering.png)


![E08_C06_combinacion](evidencias/E08_C06_combinacion.png)


![E08_C07_action_resultado](evidencias/E08_C07_action_resultado.png)



## Ejercicio 09 Recursos de la investigación propia


La investigación de ubicaciones utiliza Zona, Farmacia y EvaluacionUbicacion. Zona describe distrito, población, flujo y accesibilidad. Farmacia registra nombre, tipo, distancia y estado. EvaluacionUbicacion guarda competencia, centros de salud, alquiler, ventas estimadas y viabilidad.


Farmacia y EvaluacionUbicacion tienen ForeignKey a Zona: una zona puede tener muchas farmacias y evaluaciones. La base de demostración contiene tres registros de cada modelo. La base local no tenía farmacias al revisarla; los valores Activa, Inactiva y ACTIVA se introdujeron expresamente como datos ficticios.


**Justificación.** Se conservan además las siete entidades del módulo comercial. No se duplican modelos para implementar la API. La tabla de equivalencias documenta los recursos, relaciones, validaciones y QuerySets utilizados.


![E09_C01_modelos](evidencias/E09_C01_modelos.png)


![E09_C02_relaciones](evidencias/E09_C02_relaciones.png)


![E09_C03_tabla_equivalencias](evidencias/E09_C03_tabla_equivalencias.png)



## Ejercicio 10 Serializers de la investigación


Se implementaron ZonaSerializer, FarmaciaSerializer y EvaluacionUbicacionSerializer. Farmacia recibe la zona por su identificador y muestra zona_nombre de solo lectura. EvaluacionUbicacion presenta una ZonaSerializer anidada y se expone únicamente para lectura.


FarmaciaSerializer valida distancia_metros > 0. La entrada de 100 metros devolvió is_valid=True; la de 0 metros devolvió False y un error del campo. Se mantienen las opciones Alta, Media y Baja del modelo de evaluación y los tipos definidos en el ORM.


**Justificación.** Cada serializer define la representación de su recurso. La validación del campo numérico se realiza antes de crear o actualizar. Un campo anidado read_only no permite escribir automáticamente el objeto relacionado.


![E10_C01_serializers](evidencias/E10_C01_serializers.png)


![E10_C02_validacion_valida](evidencias/E10_C02_validacion_valida.png)


![E10_C03_validacion_invalida](evidencias/E10_C03_validacion_invalida.png)



## Ejercicio 11 ViewSets y códigos HTTP de investigación


ZonaViewSet y FarmaciaViewSet ofrecen operaciones CRUD mediante ModelViewSet. Sus registros se añadieron al mismo DefaultRouter utilizado por la API principal. Los detalles se obtienen mediante el identificador de cada recurso.


Las peticiones HTTP a farmacias produjeron 200 en GET, 201 al crear, 400 con distancia 0, 204 al eliminar el registro temporal y 404 al consultar ese ID eliminado. El CRUD de zonas y el PATCH de ambos recursos se comprobaron además en pruebas automatizadas que verifican los valores persistidos.


**Justificación.** Los códigos permiten distinguir una operación válida, un dato rechazado y un recurso inexistente. DELETE se ejecutó solo sobre el registro creado para la prueba. La eliminación de zonas conserva las reglas CASCADE ya definidas por el modelo.


![E11_C01_viewsets](evidencias/E11_C01_viewsets.png)


![E11_C02_router](evidencias/E11_C02_router.png)


![E11_C03_http_200](evidencias/E11_C03_http_200.png)


![E11_C04_http_201](evidencias/E11_C04_http_201.png)


![E11_C05_http_400](evidencias/E11_C05_http_400.png)


![E11_C06_http_404](evidencias/E11_C06_http_404.png)


![E11_C07_http_204](evidencias/E11_C07_http_204.png)



## Ejercicio 12 Recurso anidado y optimización


EvaluacionUbicacionReadOnlyViewSet usa EvaluacionUbicacionSerializer con la zona anidada. get_queryset() aplica select_related("zona") y un orden estable por clave primaria. La API responde con la evaluación y la información de su zona en el mismo JSON.


Sobre las tres evaluaciones ficticias, la serialización completa realizó 4 consultas sin optimizar y 1 con select_related. Se comprobó igualdad de respuestas. GET de evaluación devolvió 200; POST devolvió 405. Las pruebas automatizadas también rechazan PATCH y DELETE.


**Justificación.** La relación es una ForeignKey y puede resolverse con una unión SQL. Esto evita la consulta adicional de zona por cada evaluación y mantiene la salida de solo lectura.


![E12_C01_serializer](evidencias/E12_C01_serializer.png)


![E12_C02_queryset](evidencias/E12_C02_queryset.png)


![E12_C03_antes](evidencias/E12_C03_antes.png)


![E12_C04_despues](evidencias/E12_C04_despues.png)


![E12_C05_respuesta](evidencias/E12_C05_respuesta.png)



## Ejercicio 13 Filtros y acción en investigación


FarmaciaViewSet permite búsqueda por nombre, tipo, estado y nombre de zona, y orden por nombre, distancia o estado. get_queryset() aplica ?estado= mediante estado__iexact. La acción activas reutiliza FarmaciaQuerySet.activas().


La búsqueda Botica devolvió tres registros, ordenados por distancia en 150, 300 y 450 metros. ?estado=activa devolvió dos. /activas/?search=Botica&ordering=distancia_metros devolvió las activas de 150 y 450 metros. La prueba automatizada verifica también que una condición contradictoria estado=Inactiva en /activas/ devuelve una lista vacía.


**Justificación.** La acción pasa por filter_queryset y conserva la paginación si se configura más adelante. La regla del QuerySet evita repetir la lógica de selección de farmacias activas.


![E13_C01_filtros](evidencias/E13_C01_filtros.png)


![E13_C02_queryset](evidencias/E13_C02_queryset.png)


![E13_C03_action](evidencias/E13_C03_action.png)


![E13_C04_search](evidencias/E13_C04_search.png)


![E13_C05_ordering](evidencias/E13_C05_ordering.png)


![E13_C06_filtro_parametro](evidencias/E13_C06_filtro_parametro.png)


![E13_C07_action_resultado](evidencias/E13_C07_action_resultado.png)



## Ejercicio 14 Documentación verificación y publicación


Se actualizaron los README y los documentos de evidencia del Lab 08, las dependencias y las instrucciones de ejecución. El informe contiene los tres integrantes solicitados. Se revisaron los cambios y se publicaron con autorización expresa del usuario en main.


El código se publicó en el commit c5144bd377d45efcff114b49ab1e0249ed589071. La copia de publicación, basada en main, ejecutó 25 pruebas correctas. La copia local conservó los cambios adicionales de Semana 7 y ejecutó 32 pruebas correctas. Ambas comprobaciones de esquema finalizaron sin cambios. Las diferencias de cantidad corresponden a esas pruebas locales adicionales.


**Justificación.** Las capturas incluyen el estado previo, commit y push reales. La publicación excluye bases SQLite, respaldos, entornos virtuales y archivos temporales. El informe y las evidencias se incorporan en un segundo commit documental para no alterar la referencia del código verificado.


![E14_C01_requirements](evidencias/E14_C01_requirements.png)


![E14_C02_readme](evidencias/E14_C02_readme.png)


![E14_C03_git_status](evidencias/E14_C03_git_status.png)


![E14_C04_commit_push](evidencias/E14_C04_commit_push.png)


![E14_pruebas](evidencias/E14_pruebas.png)



## Conclusiones


FarmaPoint expone seis recursos mediante una API versionada. Productos, categorías, zonas y farmacias admiten CRUD; ventas y evaluaciones son de solo lectura y muestran relaciones anidadas. Los serializers rechazan precios y distancias no positivos antes de guardar.

Las comprobaciones HTTP produjeron los códigos 200, 201, 400, 404, 204 y 405 en los escenarios documentados. La igualdad de los JSON antes y después de precargar relaciones confirma que la optimización reduce consultas sin cambiar la información presentada.

Se conservaron el HTML y Django Admin. Los QuerySets personalizados se reutilizan mediante acciones y filtros combinables. El código del laboratorio está publicado y cuenta con pruebas automatizadas; la configuración continúa siendo de desarrollo local.


## Repositorio
https://github.com/SAguirreT/django_project

Commit de código: c5144bd377d45efcff114b49ab1e0249ed589071