#!/usr/bin/env python3
"""
Unified Messaging Service for 9Router
Integrates Twilio (SMS/WhatsApp) and Telegram with full media support
"""

import os
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    LINK = "link"

class Platform(Enum):
    TWILIO_SMS = "twilio_sms"
    TWILIO_WHATSAPP = "twilio_whatsapp"
    TELEGRAM = "telegram"

@dataclass
class Message:
    platform: Platform
    content: str
    media_url: Optional[str] = None
    media_type: Optional[MessageType] = None
    recipient: Optional[str] = None
    sender: Optional[str] = None
    timestamp: datetime = None
    metadata: Dict = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}

class DatabaseBridge:
    """Bridge to access 9Router SQLite database"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connected to database: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def get_provider_connections(self) -> List[Dict]:
        """Get all provider connections from database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM providerConnections")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting provider connections: {e}")
            return []
    
    def get_api_keys(self) -> List[Dict]:
        """Get all API keys from database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM apiKeys WHERE isActive = 1")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting API keys: {e}")
            return []
    
    def get_usage_history(self, limit: int = 10) -> List[Dict]:
        """Get recent usage history"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM usageHistory ORDER BY timestamp DESC LIMIT {limit}")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting usage history: {e}")
            return []
    
    def get_daily_usage(self, date: str = None) -> Dict:
        """Get daily usage statistics"""
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM usageDaily WHERE dateKey = ?", (date,))
            row = cursor.fetchone()
            
            if row:
                data = json.loads(row['data'])
                return data
            return {}
        except Exception as e:
            logger.error(f"Error getting daily usage: {e}")
            return {}
    
    def get_combos(self) -> List[Dict]:
        """Get all model combos"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM combos")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting combos: {e}")
            return []

class MediaHandler:
    """Handle media file storage and retrieval"""
    
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different media types
        (self.storage_dir / "images").mkdir(exist_ok=True)
        (self.storage_dir / "videos").mkdir(exist_ok=True)
        (self.storage_dir / "files").mkdir(exist_ok=True)
        (self.storage_dir / "links").mkdir(exist_ok=True)
    
    def save_media(self, media_data: bytes, media_type: MessageType, filename: str = None) -> str:
        """Save media file and return the path"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{media_type.value}"
            
            if media_type == MessageType.IMAGE:
                subdir = "images"
                ext = ".jpg"
            elif media_type == MessageType.VIDEO:
                subdir = "videos"
                ext = ".mp4"
            elif media_type == MessageType.FILE:
                subdir = "files"
                ext = ".bin"
            else:
                subdir = "files"
                ext = ".bin"
            
            filepath = self.storage_dir / subdir / f"{filename}{ext}"
            
            with open(filepath, 'wb') as f:
                f.write(media_data)
            
            logger.info(f"Saved media file: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving media: {e}")
            return None
    
    def get_media(self, filepath: str) -> bytes:
        """Retrieve media file"""
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error retrieving media: {e}")
            return None
    
    def save_link(self, url: str, metadata: Dict = None) -> str:
        """Save link information"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            link_file = self.storage_dir / "links" / f"{timestamp}.json"
            
            link_data = {
                "url": url,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }
            
            with open(link_file, 'w') as f:
                json.dump(link_data, f, indent=2)
            
            logger.info(f"Saved link: {url}")
            return str(link_file)
            
        except Exception as e:
            logger.error(f"Error saving link: {e}")
            return None

class TwilioService:
    """Twilio integration for SMS and WhatsApp"""
    
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}"
        
    def send_message(self, to: str, content: str, media_url: str = None, platform: Platform = Platform.TWILIO_SMS) -> bool:
        """Send message via Twilio"""
        try:
            endpoint = "/Messages.json"
            url = f"{self.base_url}{endpoint}"
            
            # Determine platform-specific parameters
            if platform == Platform.TWILIO_WHATSAPP:
                from_number = f"whatsapp:{self.phone_number}"
                to_number = f"whatsapp:{to}"
            else:
                from_number = self.phone_number
                to_number = to
            
            data = {
                "From": from_number,
                "To": to_number,
                "Body": content
            }
            
            if media_url:
                data["MediaUrl"] = media_url
            
            response = requests.post(
                url,
                data=data,
                auth=(self.account_sid, self.auth_token)
            )
            
            if response.status_code == 201:
                logger.info(f"Twilio message sent successfully to {to}")
                return True
            else:
                logger.error(f"Twilio API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Twilio message: {e}")
            return False
    
    def receive_message(self, data: Dict) -> Message:
        """Process incoming Twilio message"""
        try:
            platform = Platform.TWILIO_WHATSAPP if 'whatsapp' in data.get('From', '') else Platform.TWILIO_SMS
            
            message = Message(
                platform=platform,
                content=data.get('Body', ''),
                sender=data.get('From', ''),
                recipient=data.get('To', ''),
                media_url=data.get('MediaUrl0', None),
                timestamp=datetime.now()
            )
            
            # Determine media type if media URL is present
            if message.media_url:
                if any(ext in message.media_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    message.media_type = MessageType.IMAGE
                elif any(ext in message.media_url.lower() for ext in ['.mp4', '.mov', '.avi']):
                    message.media_type = MessageType.VIDEO
                else:
                    message.media_type = MessageType.FILE
            
            return message
            
        except Exception as e:
            logger.error(f"Error processing Twilio message: {e}")
            return None

class TelegramService:
    """Telegram bot with full media support"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, chat_id: str, content: str, parse_mode: str = "HTML") -> bool:
        """Send text message via Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": content,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                logger.info(f"Telegram message sent successfully to {chat_id}")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_photo(self, chat_id: str, photo: str, caption: str = "") -> bool:
        """Send photo via Telegram"""
        try:
            url = f"{self.base_url}/sendPhoto"
            data = {
                "chat_id": chat_id,
                "photo": photo,
                "caption": caption
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                logger.info(f"Telegram photo sent successfully to {chat_id}")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram photo: {e}")
            return False
    
    def send_video(self, chat_id: str, video: str, caption: str = "") -> bool:
        """Send video via Telegram"""
        try:
            url = f"{self.base_url}/sendVideo"
            data = {
                "chat_id": chat_id,
                "video": video,
                "caption": caption
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                logger.info(f"Telegram video sent successfully to {chat_id}")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram video: {e}")
            return False
    
    def send_document(self, chat_id: str, document: str, caption: str = "") -> bool:
        """Send document via Telegram"""
        try:
            url = f"{self.base_url}/sendDocument"
            data = {
                "chat_id": chat_id,
                "document": document,
                "caption": caption
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                logger.info(f"Telegram document sent successfully to {chat_id}")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram document: {e}")
            return False
    
    def get_updates(self, offset: int = 0, timeout: int = 0) -> List[Dict]:
        """Get updates from Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                "offset": offset,
                "timeout": timeout
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json().get('result', [])
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting Telegram updates: {e}")
            return []
    
    def process_update(self, update: Dict) -> Message:
        """Process incoming Telegram update"""
        try:
            message_data = update.get('message', {})
            
            # Extract basic message info
            chat_id = message_data.get('chat', {}).get('id')
            sender = message_data.get('from', {}).get('username')
            text = message_data.get('text', '')
            
            # Check for different types of content
            photo = message_data.get('photo')
            video = message_data.get('video')
            document = message_data.get('document')
            
            media_url = None
            media_type = None
            
            if photo:
                # Get the largest photo
                largest_photo = photo[-1]
                media_url = largest_photo.get('file_id')
                media_type = MessageType.IMAGE
            elif video:
                media_url = video.get('file_id')
                media_type = MessageType.VIDEO
            elif document:
                media_url = document.get('file_id')
                media_type = MessageType.FILE
            
            # Check for links in text
            if text and not media_url:
                if 'http' in text.lower():
                    media_type = MessageType.LINK
            
            message = Message(
                platform=Platform.TELEGRAM,
                content=text,
                media_url=media_url,
                media_type=media_type,
                recipient=str(chat_id),
                sender=sender,
                timestamp=datetime.now(),
                metadata={"update_id": update.get('update_id')}
            )
            
            return message
            
        except Exception as e:
            logger.error(f"Error processing Telegram update: {e}")
            return None

class MessagingService:
    """Unified messaging service combining all platforms"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_bridge = None
        self.media_handler = None
        self.twilio_service = None
        self.telegram_service = None
        
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all services"""
        try:
            # Initialize database bridge
            db_path = self.config.get('database_path', '9router-data/db/data.sqlite')
            self.db_bridge = DatabaseBridge(db_path)
            self.db_bridge.connect()
            
            # Initialize media handler
            storage_dir = self.config.get('media_storage_dir', '9router-data/media')
            self.media_handler = MediaHandler(storage_dir)
            
            # Initialize Twilio if credentials provided
            twilio_config = self.config.get('twilio', {})
            if twilio_config.get('account_sid') and twilio_config.get('auth_token'):
                self.twilio_service = TwilioService(
                    account_sid=twilio_config['account_sid'],
                    auth_token=twilio_config['auth_token'],
                    phone_number=twilio_config.get('phone_number', '')
                )
                logger.info("Twilio service initialized")
            
            # Initialize Telegram if token provided
            telegram_config = self.config.get('telegram', {})
            if telegram_config.get('bot_token'):
                self.telegram_service = TelegramService(bot_token=telegram_config['bot_token'])
                logger.info("Telegram service initialized")
            
            logger.info("Messaging service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing services: {e}")
    
    def get_9router_data(self, data_type: str) -> Any:
        """Get data from 9Router database"""
        try:
            if data_type == "providers":
                return self.db_bridge.get_provider_connections()
            elif data_type == "api_keys":
                return self.db_bridge.get_api_keys()
            elif data_type == "usage":
                return self.db_bridge.get_usage_history()
            elif data_type == "daily_usage":
                return self.db_bridge.get_daily_usage()
            elif data_type == "combos":
                return self.db_bridge.get_combos()
            else:
                logger.warning(f"Unknown data type: {data_type}")
                return None
        except Exception as e:
            logger.error(f"Error getting 9Router data: {e}")
            return None
    
    def send_message(self, platform: Platform, recipient: str, content: str, media: str = None) -> bool:
        """Send message through specified platform"""
        try:
            if platform == Platform.TELEGRAM and self.telegram_service:
                if media:
                    # Determine media type and send accordingly
                    if media.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        return self.telegram_service.send_photo(recipient, media, content)
                    elif media.endswith(('.mp4', '.mov', '.avi')):
                        return self.telegram_service.send_video(recipient, media, content)
                    else:
                        return self.telegram_service.send_document(recipient, media, content)
                else:
                    return self.telegram_service.send_message(recipient, content)
            
            elif (platform == Platform.TWILIO_SMS or platform == Platform.TWILIO_WHATSAPP) and self.twilio_service:
                return self.twilio_service.send_message(recipient, content, media, platform)
            
            else:
                logger.error(f"Platform {platform} not configured")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def process_incoming_message(self, message: Message) -> Dict:
        """Process incoming message and generate response"""
        try:
            # Get relevant 9Router data based on message content
            response_data = {}
            
            if "provider" in message.content.lower():
                response_data['providers'] = self.get_9router_data("providers")
            elif "usage" in message.content.lower():
                response_data['usage'] = self.get_9router_data("usage")
            elif "combo" in message.content.lower():
                response_data['combos'] = self.get_9router_data("combos")
            elif "api" in message.content.lower() or "key" in message.content.lower():
                response_data['api_keys'] = self.get_9router_data("api_keys")
            else:
                # Default: send summary
                response_data = {
                    'providers': self.get_9router_data("providers"),
                    'usage': self.get_9router_data("daily_usage"),
                    'combos': self.get_9router_data("combos")
                }
            
            # Format response based on platform
            formatted_response = self._format_response(response_data, message.platform)
            
            return {
                'success': True,
                'response': formatted_response,
                'data': response_data
            }
            
        except Exception as e:
            logger.error(f"Error processing incoming message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _format_response(self, data: Dict, platform: Platform) -> str:
        """Format response based on platform"""
        try:
            if platform == Platform.TELEGRAM:
                return self._format_telegram_response(data)
            else:
                return self._format_twilio_response(data)
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Error formatting response"
    
    def _format_telegram_response(self, data: Dict) -> str:
        """Format response for Telegram (supports HTML)"""
        response = "<b>📊 9Router Data Summary</b>\n\n"
        
        if 'providers' in data:
            providers = data['providers']
            response += f"<b>🔌 Providers:</b> {len(providers)} active\n"
            for provider in providers[:3]:  # Show first 3
                response += f"  • {provider.get('name', 'Unknown')} ({provider.get('provider', 'Unknown')})\n"
        
        if 'usage' in data:
            usage = data['usage']
            if usage:
                response += f"\n<b>📈 Recent Usage:</b>\n"
                for record in usage[:3]:
                    response += f"  • {record.get('model', 'Unknown')}: {record.get('promptTokens', 0)} tokens\n"
        
        if 'combos' in data:
            combos = data['combos']
            response += f"\n<b>🎯 Combos:</b> {len(combos)} available\n"
            for combo in combos[:3]:
                response += f"  • {combo.get('name', 'Unknown')}\n"
        
        return response
    
    def _format_twilio_response(self, data: Dict) -> str:
        """Format response for Twilio (plain text)"""
        response = "9Router Data Summary:\n\n"
        
        if 'providers' in data:
            providers = data['providers']
            response += f"Providers: {len(providers)} active\n"
            for provider in providers[:3]:
                response += f"- {provider.get('name', 'Unknown')} ({provider.get('provider', 'Unknown')})\n"
        
        if 'usage' in data:
            usage = data['usage']
            if usage:
                response += f"\nRecent Usage:\n"
                for record in usage[:3]:
                    response += f"- {record.get('model', 'Unknown')}: {record.get('promptTokens', 0)} tokens\n"
        
        if 'combos' in data:
            combos = data['combos']
            response += f"\nCombos: {len(combos)} available\n"
            for combo in combos[:3]:
                response += f"- {combo.get('name', 'Unknown')}\n"
        
        return response
    
    def cleanup(self):
        """Cleanup resources"""
        if self.db_bridge:
            self.db_bridge.disconnect()
        logger.info("Messaging service cleanup completed")

# Configuration template
def get_config_template():
    """Get configuration template for the messaging service"""
    return {
        "database_path": "9router-data/db/data.sqlite",
        "media_storage_dir": "9router-data/media",
        "twilio": {
            "account_sid": "YOUR_TWILIO_ACCOUNT_SID",
            "auth_token": "YOUR_TWILIO_AUTH_TOKEN",
            "phone_number": "YOUR_TWILIO_PHONE_NUMBER"
        },
        "telegram": {
            "bot_token": "YOUR_TELEGRAM_BOT_TOKEN"
        }
    }

if __name__ == "__main__":
    # Example usage
    config = get_config_template()
    
    # Override with environment variables if available
    config['twilio']['account_sid'] = os.environ.get('TWILIO_ACCOUNT_SID', config['twilio']['account_sid'])
    config['twilio']['auth_token'] = os.environ.get('TWILIO_AUTH_TOKEN', config['twilio']['auth_token'])
    config['twilio']['phone_number'] = os.environ.get('TWILIO_PHONE_NUMBER', config['twilio']['phone_number'])
    config['telegram']['bot_token'] = os.environ.get('TELEGRAM_BOT_TOKEN', config['telegram']['bot_token'])
    
    service = MessagingService(config)
    
    try:
        # Test database connection
        providers = service.get_9router_data("providers")
        print(f"Found {len(providers)} provider connections")
        
        # Example: Send Telegram message (if configured)
        # service.send_message(Platform.TELEGRAM, "chat_id", "Test message from 9Router")
        
    finally:
        service.cleanup()