#!/usr/bin/env python3
"""
REST API for 9Router Messaging Service
Provides endpoints for Twilio and Telegram integration
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from messaging_service import MessagingService, Platform, MessageType, get_config_template
from werkzeug.utils import secure_filename
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG = get_config_template()
CONFIG['database_path'] = os.environ.get('DATABASE_PATH', '9router-data/db/data.sqlite')
CONFIG['media_storage_dir'] = os.environ.get('MEDIA_STORAGE_DIR', '9router-data/media')
CONFIG['twilio']['account_sid'] = os.environ.get('TWILIO_ACCOUNT_SID', '')
CONFIG['twilio']['auth_token'] = os.environ.get('TWILIO_AUTH_TOKEN', '')
CONFIG['twilio']['phone_number'] = os.environ.get('TWILIO_PHONE_NUMBER', '')
CONFIG['telegram']['bot_token'] = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Initialize messaging service
messaging_service = MessagingService(CONFIG)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'doc', 'docx', 'zip', 'rar'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': '9Router Messaging API',
        'platforms_configured': {
            'twilio': bool(CONFIG['twilio']['account_sid']),
            'telegram': bool(CONFIG['telegram']['bot_token'])
        }
    })

@app.route('/api/data/providers', methods=['GET'])
def get_providers():
    """Get provider connections from 9Router database"""
    try:
        providers = messaging_service.get_9router_data("providers")
        return jsonify({
            'success': True,
            'data': providers,
            'count': len(providers)
        })
    except Exception as e:
        logger.error(f"Error getting providers: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/api-keys', methods=['GET'])
def get_api_keys():
    """Get API keys from 9Router database"""
    try:
        api_keys = messaging_service.get_9router_data("api_keys")
        # Mask sensitive data
        masked_keys = []
        for key in api_keys:
            masked_key = key.copy()
            if 'key' in masked_key:
                original_key = masked_key['key']
                masked_key['key'] = original_key[:8] + '...' + original_key[-4:]
            masked_keys.append(masked_key)
        
        return jsonify({
            'success': True,
            'data': masked_keys,
            'count': len(masked_keys)
        })
    except Exception as e:
        logger.error(f"Error getting API keys: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/usage', methods=['GET'])
def get_usage():
    """Get usage history from 9Router database"""
    try:
        limit = request.args.get('limit', 10, type=int)
        usage = messaging_service.get_9router_data("usage")
        limited_usage = usage[:limit] if usage else []
        
        return jsonify({
            'success': True,
            'data': limited_usage,
            'count': len(limited_usage)
        })
    except Exception as e:
        logger.error(f"Error getting usage: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/daily-usage', methods=['GET'])
def get_daily_usage():
    """Get daily usage statistics"""
    try:
        date = request.args.get('date')
        daily_usage = messaging_service.get_9router_data("daily_usage")
        
        return jsonify({
            'success': True,
            'data': daily_usage,
            'date': date or 'today'
        })
    except Exception as e:
        logger.error(f"Error getting daily usage: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/combos', methods=['GET'])
def get_combos():
    """Get model combos from 9Router database"""
    try:
        combos = messaging_service.get_9router_data("combos")
        return jsonify({
            'success': True,
            'data': combos,
            'count': len(combos)
        })
    except Exception as e:
        logger.error(f"Error getting combos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send/telegram', methods=['POST'])
def send_telegram_message():
    """Send message via Telegram"""
    try:
        data = request.json
        chat_id = data.get('chat_id')
        content = data.get('content', '')
        media_url = data.get('media_url')
        
        if not chat_id:
            return jsonify({
                'success': False,
                'error': 'chat_id is required'
            }), 400
        
        success = messaging_service.send_message(
            Platform.TELEGRAM,
            chat_id,
            content,
            media_url
        )
        
        return jsonify({
            'success': success,
            'message': 'Message sent successfully' if success else 'Failed to send message'
        })
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send/twilio', methods=['POST'])
def send_twilio_message():
    """Send message via Twilio"""
    try:
        data = request.json
        to = data.get('to')
        content = data.get('content', '')
        media_url = data.get('media_url')
        platform = data.get('platform', 'sms')
        
        if not to:
            return jsonify({
                'success': False,
                'error': 'to is required'
            }), 400
        
        platform_enum = Platform.TWILIO_WHATSAPP if platform == 'whatsapp' else Platform.TWILIO_SMS
        
        success = messaging_service.send_message(
            platform_enum,
            to,
            content,
            media_url
        )
        
        return jsonify({
            'success': success,
            'message': 'Message sent successfully' if success else 'Failed to send message'
        })
    except Exception as e:
        logger.error(f"Error sending Twilio message: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload/media', methods=['POST'])
def upload_media():
    """Upload media file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        media_type = request.form.get('media_type', 'file')
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if file and allowed_file(file.filename):
            # Determine media type
            if media_type == 'image':
                message_type = MessageType.IMAGE
            elif media_type == 'video':
                message_type = MessageType.VIDEO
            else:
                message_type = MessageType.FILE
            
            # Save file
            file_data = file.read()
            filepath = messaging_service.media_handler.save_media(
                file_data,
                message_type,
                secure_filename(file.filename)
            )
            
            if filepath:
                return jsonify({
                    'success': True,
                    'filepath': filepath,
                    'media_type': media_type
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to save media file'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400
            
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/media/<path:filename>', methods=['GET'])
def get_media(filename):
    """Get media file"""
    try:
        # Determine which subdirectory to look in
        media_type = request.args.get('type', 'files')
        storage_dir = messaging_service.media_handler.storage_dir
        
        if media_type == 'image':
            filepath = storage_dir / "images" / filename
        elif media_type == 'video':
            filepath = storage_dir / "videos" / filename
        else:
            filepath = storage_dir / "files" / filename
        
        if filepath.exists():
            return send_file(str(filepath))
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting media: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/telegram/webhook', methods=['POST'])
def telegram_webhook():
    """Telegram webhook endpoint"""
    try:
        update = request.json
        
        if not update:
            return jsonify({'success': False, 'error': 'No update data'}), 400
        
        # Process the update
        message = messaging_service.telegram_service.process_update(update)
        
        if message:
            # Process the message and generate response
            response = messaging_service.process_incoming_message(message)
            
            if response['success']:
                # Send response back to user
                messaging_service.send_message(
                    Platform.TELEGRAM,
                    message.recipient,
                    response['response']
                )
            
            return jsonify({
                'success': True,
                'message': 'Webhook processed successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to process update'
            }), 400
            
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/twilio/webhook', methods=['POST'])
def twilio_webhook():
    """Twilio webhook endpoint"""
    try:
        # Get form data from Twilio
        data = request.form.to_dict()
        
        if not data:
            return jsonify({'success': False, 'error': 'No webhook data'}), 400
        
        # Process the incoming message
        message = messaging_service.twilio_service.receive_message(data)
        
        if message:
            # Process the message and generate response
            response = messaging_service.process_incoming_message(message)
            
            if response['success']:
                # Send response back via Twilio
                # Determine platform
                platform = Platform.TWILIO_WHATSAPP if 'whatsapp' in data.get('From', '') else Platform.TWILIO_SMS
                
                messaging_service.send_message(
                    platform,
                    message.sender,
                    response['response']
                )
            
            # Return TwiML response
            return "<?xml version='1.0' encoding='UTF-8'?><Response></Response>", 200, {'Content-Type': 'application/xml'}
        else:
            return "<?xml version='1.0' encoding='UTF-8'?><Response></Response>", 200, {'Content-Type': 'application/xml'}
            
    except Exception as e:
        logger.error(f"Error processing Twilio webhook: {e}")
        return "<?xml version='1.0' encoding='UTF-8'?><Response></Response>", 200, {'Content-Type': 'application/xml'}

@app.route('/api/links', methods=['POST'])
def save_link():
    """Save link information"""
    try:
        data = request.json
        url = data.get('url')
        metadata = data.get('metadata', {})
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'url is required'
            }), 400
        
        filepath = messaging_service.media_handler.save_link(url, metadata)
        
        if filepath:
            return jsonify({
                'success': True,
                'filepath': filepath,
                'url': url
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save link'
            }), 500
            
    except Exception as e:
        logger.error(f"Error saving link: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/links', methods=['GET'])
def get_links():
    """Get saved links"""
    try:
        links_dir = messaging_service.media_handler.storage_dir / "links"
        links = []
        
        if links_dir.exists():
            for link_file in links_dir.glob("*.json"):
                with open(link_file, 'r') as f:
                    link_data = json.load(f)
                    links.append(link_data)
        
        return jsonify({
            'success': True,
            'data': links,
            'count': len(links)
        })
    except Exception as e:
        logger.error(f"Error getting links: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

def cleanup():
    """Cleanup function"""
    messaging_service.cleanup()

if __name__ == '__main__':
    port = int(os.environ.get('MESSAGING_API_PORT', 5000))
    logger.info(f"Starting Messaging API on port {port}")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    finally:
        cleanup()