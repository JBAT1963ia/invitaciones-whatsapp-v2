from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
import os

app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-12345'

# Archivo para almacenar datos
DATA_FILE = 'invitaciones.json'

def load_data():
    """Cargar datos desde archivo JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    """Guardar datos en archivo JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎉 Sistema de Invitaciones WhatsApp</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                margin: 0; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                padding: 20px; 
            }
            .container { 
                background: white; 
                border-radius: 20px; 
                padding: 40px; 
                text-align: center; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
                max-width: 500px; 
                width: 100%; 
            }
            h1 { color: #25D366; font-size: 2.5em; margin-bottom: 20px; }
            p { font-size: 1.2em; color: #666; margin-bottom: 30px; }
            .btn { 
                background: #25D366; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 8px; 
                display: inline-block; 
                margin: 10px; 
                font-size: 18px; 
                transition: background 0.3s; 
            }
            .btn:hover { background: #128C7E; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #545b62; }
            .status { 
                background: #e8f5e8; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 20px 0; 
                color: #2d5a2d; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Sistema de Invitaciones WhatsApp</h1>
            <div class="status">
                <strong>✅ Sistema funcionando correctamente</strong><br>
                Versión con Dashboard de Administración
            </div>
            <p>Crea invitaciones profesionales para WhatsApp con confirmación automática</p>
            <a href="/admin" class="btn">📝 Crear Invitación</a>
            <a href="/dashboard" class="btn btn-secondary">📊 Ver Confirmaciones</a>
            <a href="/api/test" class="btn btn-secondary">🧪 Probar API</a>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    # Cargar datos
    data = load_data()
    
    # Calcular estadísticas
    total_invitaciones = len(data)
    confirmadas = 0
    parciales = 0
    declinadas = 0
    pendientes = 0
    total_personas_confirmadas = 0
    
    invitaciones_list = []
    
    for inv_id, inv in data.items():
        if inv['confirmado']:
            if inv['numero_confirmados'] == inv['numero_invitados']:
                confirmadas += 1
                estado = 'Confirmado'
                estado_class = 'confirmed'
            elif inv['numero_confirmados'] > 0:
                parciales += 1
                estado = 'Parcial'
                estado_class = 'partial'
            else:
                declinadas += 1
                estado = 'Declinado'
                estado_class = 'declined'
            total_personas_confirmadas += inv['numero_confirmados']
        else:
            pendientes += 1
            estado = 'Pendiente'
            estado_class = 'pending'
        
        invitaciones_list.append({
            'id': inv_id,
            'nombre_evento': inv['nombre_evento'],
            'nombre_invitado': inv['nombre_invitado'],
            'numero_invitados': inv['numero_invitados'],
            'numero_confirmados': inv['numero_confirmados'],
            'estado': estado,
            'estado_class': estado_class,
            'comentarios': inv.get('comentarios', ''),
            'fecha_confirmacion': inv.get('fecha_confirmacion', ''),
            'fecha_evento': inv['fecha_evento']
        })
    
    # Ordenar por fecha de creación (más recientes primero)
    invitaciones_list.sort(key=lambda x: x['id'], reverse=True)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 Dashboard - Confirmaciones</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                padding: 20px; 
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                padding: 30px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .header h1 {{ color: #25D366; font-size: 2em; margin-bottom: 10px; }}
            .stats {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px; 
            }}
            .stat-card {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 12px; 
                text-align: center; 
            }}
            .stat-number {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
            .confirmed {{ color: #28a745; }}
            .partial {{ color: #ffc107; }}
            .declined {{ color: #dc3545; }}
            .pending {{ color: #6c757d; }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }}
            .table th {{ background: #f8f9fa; font-weight: 600; }}
            .status-badge {{ 
                padding: 4px 8px; 
                border-radius: 4px; 
                font-size: 0.8em; 
                font-weight: bold; 
            }}
            .status-badge.confirmed {{ background: #d4edda; color: #155724; }}
            .status-badge.partial {{ background: #fff3cd; color: #856404; }}
            .status-badge.declined {{ background: #f8d7da; color: #721c24; }}
            .status-badge.pending {{ background: #e2e3e5; color: #383d41; }}
            .back-btn {{ 
                background: #6c757d; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block; 
                margin-bottom: 20px; 
            }}
            .refresh-btn {{ 
                background: #25D366; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block; 
                margin-left: 10px; 
            }}
            .no-data {{ text-align: center; padding: 40px; color: #6c757d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al inicio</a>
            <a href="/dashboard" class="refresh-btn">🔄 Actualizar</a>
            
            <div class="header">
                <h1>📊 Dashboard de Confirmaciones</h1>
                <p>Resumen de todas las invitaciones y confirmaciones</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_invitaciones}</div>
                    <div>Total Invitaciones</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number confirmed">{confirmadas}</div>
                    <div>Confirmadas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number partial">{parciales}</div>
                    <div>Parciales</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number declined">{declinadas}</div>
                    <div>Declinadas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number pending">{pendientes}</div>
                    <div>Pendientes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number confirmed">{total_personas_confirmadas}</div>
                    <div>Total Personas</div>
                </div>
            </div>
            
            {'''
            <table class="table">
                <thead>
                    <tr>
                        <th>Evento</th>
                        <th>Invitado</th>
                        <th>Invitados</th>
                        <th>Confirmados</th>
                        <th>Estado</th>
                        <th>Comentarios</th>
                        <th>Enlace</th>
                    </tr>
                </thead>
                <tbody>''' + ''.join([f'''
                    <tr>
                        <td><strong>{inv['nombre_evento']}</strong><br><small>{inv['fecha_evento']}</small></td>
                        <td>{inv['nombre_invitado']}</td>
                        <td>{inv['numero_invitados']}</td>
                        <td>{inv['numero_confirmados']}</td>
                        <td><span class="status-badge {inv['estado_class']}">{inv['estado']}</span></td>
                        <td>{inv['comentarios'] if inv['comentarios'] else '-'}</td>
                        <td><a href="/confirmar/{inv['id']}" target="_blank">Ver</a></td>
                    </tr>''' for inv in invitaciones_list]) + '''
                </tbody>
            </table>''' if invitaciones_list else '''
            <div class="no-data">
                <h3>📭 No hay invitaciones aún</h3>
                <p>Crea tu primera invitación para ver las confirmaciones aquí.</p>
                <a href="/admin" class="refresh-btn">📝 Crear Invitación</a>
            </div>'''}
        </div>
    </body>
    </html>
    '''

@app.route('/admin')
def admin():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crear Invitación - WhatsApp</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                padding: 20px; 
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                padding: 30px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { color: #25D366; font-size: 2em; margin-bottom: 10px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
            input, textarea { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e1e1e1; 
                border-radius: 8px; 
                font-size: 16px; 
            }
            input:focus, textarea:focus { outline: none; border-color: #25D366; }
            .btn { 
                background: #25D366; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                font-size: 18px; 
                cursor: pointer; 
                width: 100%; 
            }
            .btn:hover { background: #128C7E; }
            .result { 
                margin-top: 30px; 
                padding: 20px; 
                background: #f8f9fa; 
                border-radius: 8px; 
                display: none; 
            }
            .message-template { 
                background: #e8f5e8; 
                padding: 15px; 
                border-radius: 8px; 
                margin: 10px 0; 
                white-space: pre-wrap; 
                font-family: monospace; 
            }
            .back-btn { 
                background: #6c757d; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block; 
                margin-bottom: 20px; 
            }
            .dashboard-btn { 
                background: #17a2b8; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                display: inline-block; 
                margin-left: 10px; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Volver al inicio</a>
            <a href="/dashboard" class="dashboard-btn">📊 Ver Confirmaciones</a>
            
            <div class="header">
                <h1>📱 Crear Invitación WhatsApp</h1>
                <p>Genera invitaciones con confirmación automática</p>
            </div>
            
            <form id="invitationForm">
                <div class="form-group">
                    <label>Nombre del evento *</label>
                    <input type="text" id="nombreEvento" required placeholder="Ej: Cumpleaños de María">
                </div>
                
                <div class="form-group">
                    <label>Fecha del evento *</label>
                    <input type="datetime-local" id="fechaEvento" required>
                </div>
                
                <div class="form-group">
                    <label>Lugar del evento *</label>
                    <input type="text" id="lugarEvento" required placeholder="Dirección completa">
                </div>
                
                <div class="form-group">
                    <label>Nombre del invitado *</label>
                    <input type="text" id="nombreInvitado" required placeholder="Nombre de la persona o familia">
                </div>
                
                <div class="form-group">
                    <label>Número de personas incluidas *</label>
                    <input type="number" id="numeroInvitados" required min="1" value="1">
                </div>
                
                <button type="submit" class="btn">🎉 Crear Invitación</button>
            </form>
            
            <div id="result" class="result">
                <h3>✅ ¡Invitación creada exitosamente!</h3>
                <p><strong>Enlace de confirmación:</strong></p>
                <p id="enlaceConfirmacion"></p>
                
                <h4>📱 Mensaje para WhatsApp:</h4>
                <div id="mensajeWhatsapp" class="message-template"></div>
                
                <button onclick="copyMessage()" class="btn" style="margin-top: 15px;">📋 Copiar Mensaje</button>
                <a href="/dashboard" class="btn" style="margin-top: 10px; background: #17a2b8;">📊 Ver en Dashboard</a>
            </div>
        </div>
        
        <script>
            document.getElementById('invitationForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = {
                    nombre_evento: document.getElementById('nombreEvento').value,
                    fecha_evento: document.getElementById('fechaEvento').value,
                    lugar_evento: document.getElementById('lugarEvento').value,
                    nombre_invitado: document.getElementById('nombreInvitado').value,
                    numero_invitados: parseInt(document.getElementById('numeroInvitados').value)
                };
                
                try {
                    const response = await fetch('/api/invitaciones', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        const baseUrl = window.location.origin;
                        const enlaceConfirmacion = `${baseUrl}/confirmar/${result.id}`;
                        
                        document.getElementById('enlaceConfirmacion').textContent = enlaceConfirmacion;
                        
                        const fecha = new Date(formData.fecha_evento).toLocaleDateString('es-ES', {
                            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
                        });
                        
                        const mensaje = `¡Hola! 🎉

Soy Alfredo y te invito a ${formData.nombre_evento} que se realizará el ${fecha} en ${formData.lugar_evento}.

**Detalles de tu invitación:**
👥 Número de invitados incluidos: ${formData.numero_invitados}

Por favor confirma tu asistencia haciendo clic en el enlace:
🔗 ${enlaceConfirmacion}

Opciones disponibles:
✅ Confirmar asistencia (todos los invitados)
✅ Confirmar asistencia parcial (menos invitados)
❌ Declinar invitación

¡Espero verte pronto!`;
                        
                        document.getElementById('mensajeWhatsapp').textContent = mensaje;
                        document.getElementById('result').style.display = 'block';
                        
                        // Scroll to result
                        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Error al crear la invitación: ' + error.message);
                }
            });
            
            function copyMessage() {
                const mensaje = document.getElementById('mensajeWhatsapp').textContent;
                navigator.clipboard.writeText(mensaje).then(() => {
                    alert('¡Mensaje copiado al portapapeles!');
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/confirmar/<invitation_id>')
def confirmar(invitation_id):
    # Cargar datos
    data = load_data()
    
    if invitation_id not in data:
        return '<h1>Invitación no encontrada</h1>', 404
    
    invitacion = data[invitation_id]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Confirmar Asistencia - {invitacion['nombre_evento']}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                padding: 20px; 
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                padding: 30px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .event-info {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 12px; 
                margin-bottom: 30px; 
            }}
            .btn {{ 
                padding: 15px 25px; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px; 
                cursor: pointer; 
                margin: 10px 5px; 
                min-width: 200px; 
                display: block; 
                width: 100%; 
            }}
            .btn-success {{ background: #28a745; color: white; }}
            .btn-warning {{ background: #ffc107; color: #212529; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            .btn:hover {{ opacity: 0.9; }}
            .form-group {{ margin: 20px 0; }}
            input, textarea {{ 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e1e1e1; 
                border-radius: 8px; 
            }}
            .result {{ 
                margin-top: 20px; 
                padding: 20px; 
                border-radius: 8px; 
                display: none; 
            }}
            .success {{ background: #d4edda; color: #155724; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 {invitacion['nombre_evento']}</h1>
                <p>Confirma tu asistencia</p>
            </div>
            
            <div class="event-info">
                <h3>📅 Detalles del Evento</h3>
                <p><strong>Fecha:</strong> {invitacion['fecha_evento']}</p>
                <p><strong>Lugar:</strong> {invitacion['lugar_evento']}</p>
                <p><strong>Invitado:</strong> {invitacion['nombre_invitado']}</p>
                <p><strong>Personas incluidas:</strong> {invitacion['numero_invitados']}</p>
            </div>
            
            <div style="text-align: center;">
                <h3>¿Confirmas tu asistencia?</h3>
                
                <button class="btn btn-success" onclick="confirmarCompleta()">
                    ✅ Sí, confirmo asistencia completa ({invitacion['numero_invitados']} personas)
                </button>
                
                <button class="btn btn-warning" onclick="mostrarParcial()">
                    ⚠️ Asistencia parcial (menos personas)
                </button>
                
                <button class="btn btn-danger" onclick="declinar()">
                    ❌ No podré asistir
                </button>
            </div>
            
            <div id="parcialForm" style="display: none; margin-top: 20px;">
                <div class="form-group">
                    <label>¿Cuántas personas asistirán?</label>
                    <input type="number" id="numeroConfirmados" min="1" max="{invitacion['numero_invitados']}" value="1">
                </div>
                <button class="btn btn-warning" onclick="confirmarParcial()">Confirmar Asistencia Parcial</button>
            </div>
            
            <div class="form-group">
                <label>Comentarios adicionales (opcional):</label>
                <textarea id="comentarios" placeholder="Algún comentario o mensaje..."></textarea>
            </div>
            
            <div id="result" class="result"></div>
        </div>
        
        <script>
            function confirmarCompleta() {{
                confirmarAsistencia({invitacion['numero_invitados']}, 'confirmado');
            }}
            
            function mostrarParcial() {{
                document.getElementById('parcialForm').style.display = 'block';
            }}
            
            function confirmarParcial() {{
                const numero = document.getElementById('numeroConfirmados').value;
                confirmarAsistencia(parseInt(numero), 'parcial');
            }}
            
            function declinar() {{
                confirmarAsistencia(0, 'declinado');
            }}
            
            async function confirmarAsistencia(numeroConfirmados, estado) {{
                const comentarios = document.getElementById('comentarios').value;
                
                try {{
                    const response = await fetch('/api/invitaciones/{invitation_id}/confirmar', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            numero_confirmados: numeroConfirmados,
                            comentarios: comentarios,
                            estado: estado
                        }})
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        let mensaje = '';
                        if (estado === 'confirmado') {{
                            mensaje = '✅ ¡Perfecto! Tu asistencia ha sido confirmada para todas las personas.';
                        }} else if (estado === 'parcial') {{
                            mensaje = `⚠️ Tu asistencia parcial ha sido confirmada para ${{numeroConfirmados}} persona(s).`;
                        }} else {{
                            mensaje = '❌ Hemos registrado que no podrás asistir. ¡Gracias por avisar!';
                        }}
                        
                        document.getElementById('result').innerHTML = `
                            <div class="success">
                                <h3>${{mensaje}}</h3>
                                <p>El organizador ha sido notificado de tu respuesta.</p>
                            </div>
                        `;
                        document.getElementById('result').style.display = 'block';
                        
                        // Ocultar botones
                        document.querySelector('.container > div:nth-child(3)').style.display = 'none';
                        document.getElementById('parcialForm').style.display = 'none';
                    }} else {{
                        alert('Error: ' + result.error);
                    }}
                }} catch (error) {{
                    alert('Error al confirmar: ' + error.message);
                }}
            }}
        </script>
    </body>
    </html>
    '''

# API Endpoints
@app.route('/api/invitaciones', methods=['POST'])
def crear_invitacion():
    try:
        data_request = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre_evento', 'fecha_evento', 'lugar_evento', 'nombre_invitado', 'numero_invitados']
        for field in required_fields:
            if field not in data_request:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Generar ID único
        invitation_id = str(uuid.uuid4())
        
        # Crear invitación
        invitacion = {
            'id': invitation_id,
            'nombre_evento': data_request['nombre_evento'],
            'fecha_evento': data_request['fecha_evento'],
            'lugar_evento': data_request['lugar_evento'],
            'nombre_invitado': data_request['nombre_invitado'],
            'numero_invitados': data_request['numero_invitados'],
            'fecha_creacion': datetime.utcnow().isoformat(),
            'confirmado': False,
            'numero_confirmados': 0,
            'comentarios': '',
            'fecha_confirmacion': None
        }
        
        # Cargar datos existentes
        data = load_data()
        data[invitation_id] = invitacion
        
        # Guardar datos
        if save_data(data):
            return jsonify({
                'id': invitation_id,
                'mensaje': 'Invitación creada exitosamente'
            }), 201
        else:
            return jsonify({'error': 'Error al guardar la invitación'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invitaciones/<invitation_id>/confirmar', methods=['POST'])
def confirmar_asistencia(invitation_id):
    try:
        # Cargar datos
        data = load_data()
        
        if invitation_id not in data:
            return jsonify({'error': 'Invitación no encontrada'}), 404
        
        data_request = request.get_json()
        
        # Actualizar confirmación
        data[invitation_id]['confirmado'] = True
        data[invitation_id]['numero_confirmados'] = data_request.get('numero_confirmados', 0)
        data[invitation_id]['comentarios'] = data_request.get('comentarios', '')
        data[invitation_id]['fecha_confirmacion'] = datetime.utcnow().isoformat()
        
        # Guardar datos
        if save_data(data):
            return jsonify({'mensaje': 'Confirmación registrada exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al guardar la confirmación'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invitaciones', methods=['GET'])
def listar_invitaciones():
    """API para obtener todas las invitaciones"""
    try:
        data = load_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'OK',
        'mensaje': '¡API funcionando correctamente!',
        'timestamp': datetime.utcnow().isoformat(),
        'platform': 'Render.com - Versión con Dashboard',
        'storage': 'Archivos JSON (sin base de datos)',
        'features': ['Dashboard de administración', 'Estadísticas en tiempo real', 'Gestión completa de confirmaciones']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

