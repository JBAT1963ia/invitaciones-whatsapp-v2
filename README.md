# 🎉 Sistema de Invitaciones WhatsApp - Render

## ✅ Versión Optimizada para Render.com

Sistema completo de invitaciones por WhatsApp con confirmación automática, optimizado específicamente para Render.com (100% GRATIS).

## 🚀 Características

- ✅ **Hosting gratuito** en Render.com (750 horas/mes)
- ✅ **Aplicación Flask** completa y optimizada
- ✅ **Base de datos SQLite** integrada
- ✅ **Interfaz responsive** para móviles
- ✅ **SSL automático** incluido
- ✅ **Sin tarjeta de crédito** requerida

## 📁 Estructura del Proyecto

```
invitaciones_render/
├── app.py              # Aplicación Flask principal
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```

## 🎯 Funcionalidades

### Para el Organizador:
- **Página principal**: `/` - Inicio del sistema
- **Panel de administración**: `/admin` - Crear invitaciones
- **Generar mensajes** automáticos para WhatsApp
- **Enlaces únicos** de confirmación

### Para los Invitados:
- **Página de confirmación**: `/confirmar/{ID}` - Confirmar asistencia
- **Opciones flexibles**: completa, parcial o declinar
- **Comentarios adicionales** opcionales
- **Confirmación instantánea**

## 🌐 URLs Disponibles

- **Inicio**: `/` - Página principal con estado del sistema
- **Admin**: `/admin` - Crear invitaciones
- **Confirmación**: `/confirmar/{ID}` - Para invitados
- **API Test**: `/api/test` - Verificar funcionamiento

## 🔧 API Endpoints

- `POST /api/invitaciones` - Crear nueva invitación
- `POST /api/invitaciones/{id}/confirmar` - Confirmar asistencia
- `GET /api/test` - Verificar funcionamiento

## 🚀 Despliegue en Render

### Configuración recomendada:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment**: Python 3
- **Plan**: Free (gratis)

### Variables de entorno (automáticas):
- `PORT` - Puerto asignado por Render
- Render maneja automáticamente el puerto y host

## 📱 Ejemplo de Uso

1. **Crear invitación** en `/admin`
2. **Copiar mensaje** generado automáticamente:
   ```
   ¡Hola! 🎉
   
   Te invito a [Evento] que se realizará el [Fecha] en [Lugar].
   
   **Detalles de tu invitación:**
   👥 Número de invitados incluidos: [X]
   
   Por favor confirma tu asistencia:
   🔗 https://tu-app.onrender.com/confirmar/abc123
   
   ¡Espero verte pronto!
   ```
3. **Enviar por WhatsApp** a los invitados
4. **Los invitados confirman** fácilmente
5. **Ver confirmaciones** en tiempo real

## 🎨 Diseño

- **Colores**: Gradiente moderno (azul-púrpura)
- **Tema WhatsApp**: Verde #25D366 para botones
- **Responsive**: Funciona perfectamente en móviles
- **Iconos emoji**: Interfaz amigable y moderna

## ✅ Ventajas de Render

1. **100% Gratuito** - 750 horas/mes (más que suficiente)
2. **SSL incluido** - HTTPS automático
3. **Dominio gratuito** - .onrender.com
4. **Fácil despliegue** - Conecta GitHub y listo
5. **Confiable** - Uptime excelente
6. **Sin tarjeta** - No requiere información de pago

## 🔧 Optimizaciones para Render

- **Puerto dinámico** - Se adapta al puerto asignado
- **Host 0.0.0.0** - Acepta conexiones externas
- **Gunicorn incluido** - Servidor de producción
- **Debug desactivado** - Optimizado para producción
- **Dependencias mínimas** - Solo lo esencial

## 🎊 Garantía de Funcionamiento

Esta versión está específicamente optimizada para Render:
- ✅ Estructura correcta para Flask
- ✅ Configuración de puerto automática
- ✅ Dependencias estables
- ✅ HTML integrado (sin archivos externos)
- ✅ Base de datos SQLite funcional

¡Tu sistema funcionará perfectamente en Render! 🚀

