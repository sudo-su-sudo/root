"""
Persona Persistence Layer

Extends the orchestrator persistence system to handle AI persona storage and retrieval.
Enables long-term persona memory across sessions.
"""

import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pathlib import Path

from .persona import Persona


class PersonaPersistence:
    """Handles persistent storage of AI personas"""
    
    def __init__(self, db_path: str = "orchestrator_data.db"):
        """
        Initialize persona persistence layer
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create persona tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Personas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                persona_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                persona_type TEXT NOT NULL,
                persona_data TEXT NOT NULL,
                version TEXT,
                created_at TIMESTAMP,
                last_active TIMESTAMP,
                conversation_count INTEGER DEFAULT 0
            )
        ''')
        
        # Persona state history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persona_state_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_id TEXT,
                state_snapshot TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (persona_id) REFERENCES personas(persona_id)
            )
        ''')
        
        # Summoning protocols table (for quick access to protocols)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summoning_protocols (
                persona_id TEXT PRIMARY KEY,
                protocol_text TEXT NOT NULL,
                compact_protocol TEXT,
                generated_at TIMESTAMP,
                FOREIGN KEY (persona_id) REFERENCES personas(persona_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_persona(self, persona: Persona, persona_id: Optional[str] = None) -> str:
        """
        Save persona to database
        
        Args:
            persona: Persona instance to save
            persona_id: Optional custom ID, defaults to sanitized name
            
        Returns:
            The persona_id used
        """
        if persona_id is None:
            # Generate ID from name
            persona_id = persona.core.name.lower().replace(' ', '_')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Serialize persona
            persona_data = persona.to_json()
            
            # Insert or update
            cursor.execute('''
                INSERT OR REPLACE INTO personas
                (persona_id, name, persona_type, persona_data, version, created_at, last_active, conversation_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                persona_id,
                persona.core.name,
                persona.core.persona_type.value,
                persona_data,
                persona.core.version,
                persona.core.created_at,
                persona.last_active,
                persona.conversation_count
            ))
            
            conn.commit()
            return persona_id
            
        except Exception as e:
            print(f"Error saving persona: {e}")
            raise
        finally:
            conn.close()
    
    def load_persona(self, persona_id: str) -> Optional[Persona]:
        """
        Load persona from database
        
        Args:
            persona_id: Persona identifier
            
        Returns:
            Persona instance or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT persona_data FROM personas
                WHERE persona_id = ?
            ''', (persona_id,))
            
            row = cursor.fetchone()
            if row:
                persona = Persona.from_json(row[0])
                return persona
            return None
            
        except Exception as e:
            print(f"Error loading persona: {e}")
            return None
        finally:
            conn.close()
    
    def save_summoning_protocol(self, persona_id: str, persona: Persona):
        """
        Generate and save summoning protocols for a persona
        
        Args:
            persona_id: Persona identifier
            persona: Persona instance
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            full_protocol = persona.generate_summoning_protocol(include_state=True)
            compact_protocol = persona.generate_compact_protocol()
            
            cursor.execute('''
                INSERT OR REPLACE INTO summoning_protocols
                (persona_id, protocol_text, compact_protocol, generated_at)
                VALUES (?, ?, ?, ?)
            ''', (
                persona_id,
                full_protocol,
                compact_protocol,
                datetime.now(timezone.utc)
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"Error saving summoning protocol: {e}")
            raise
        finally:
            conn.close()
    
    def get_summoning_protocol(self, persona_id: str, compact: bool = False) -> Optional[str]:
        """
        Retrieve summoning protocol for a persona
        
        Args:
            persona_id: Persona identifier
            compact: If True, return compact protocol
            
        Returns:
            Protocol text or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Use parameterized query with whitelisted column selection
            if compact:
                cursor.execute('''
                    SELECT compact_protocol FROM summoning_protocols
                    WHERE persona_id = ?
                ''', (persona_id,))
            else:
                cursor.execute('''
                    SELECT protocol_text FROM summoning_protocols
                    WHERE persona_id = ?
                ''', (persona_id,))
            
            row = cursor.fetchone()
            return row[0] if row else None
            
        finally:
            conn.close()
    
    def save_state_snapshot(self, persona_id: str, state: Dict[str, Any]):
        """
        Save a snapshot of persona state for history tracking
        
        Args:
            persona_id: Persona identifier
            state: State dictionary to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO persona_state_history
                (persona_id, state_snapshot, timestamp)
                VALUES (?, ?, ?)
            ''', (
                persona_id,
                json.dumps(state),
                datetime.now(timezone.utc)
            ))
            
            conn.commit()
            
        finally:
            conn.close()
    
    def list_personas(self) -> List[Dict[str, Any]]:
        """
        List all saved personas
        
        Returns:
            List of persona metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT persona_id, name, persona_type, version, created_at, last_active, conversation_count
                FROM personas
                ORDER BY last_active DESC
            ''')
            
            personas = [
                {
                    'persona_id': row[0],
                    'name': row[1],
                    'persona_type': row[2],
                    'version': row[3],
                    'created_at': row[4],
                    'last_active': row[5],
                    'conversation_count': row[6]
                }
                for row in cursor.fetchall()
            ]
            
            return personas
            
        finally:
            conn.close()
    
    def delete_persona(self, persona_id: str) -> bool:
        """
        Delete a persona and all related data
        
        Args:
            persona_id: Persona identifier
            
        Returns:
            True if deleted successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM persona_state_history WHERE persona_id = ?', (persona_id,))
            cursor.execute('DELETE FROM summoning_protocols WHERE persona_id = ?', (persona_id,))
            cursor.execute('DELETE FROM personas WHERE persona_id = ?', (persona_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting persona: {e}")
            return False
        finally:
            conn.close()
    
    def update_persona_activity(self, persona_id: str):
        """
        Update last_active timestamp and increment conversation count
        
        Args:
            persona_id: Persona identifier
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE personas
                SET last_active = ?,
                    conversation_count = conversation_count + 1
                WHERE persona_id = ?
            ''', (datetime.now(timezone.utc), persona_id))
            
            conn.commit()
            
        finally:
            conn.close()
    
    def export_persona(self, persona_id: str, include_history: bool = True) -> Optional[Dict[str, Any]]:
        """
        Export persona with optional state history
        
        Args:
            persona_id: Persona identifier
            include_history: Whether to include state history
            
        Returns:
            Complete persona export or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get persona
            cursor.execute('''
                SELECT persona_data FROM personas
                WHERE persona_id = ?
            ''', (persona_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            export = {
                'persona_id': persona_id,
                'persona_data': json.loads(row[0]),
                'exported_at': datetime.now(timezone.utc).isoformat()
            }
            
            # Get summoning protocol
            cursor.execute('''
                SELECT protocol_text, compact_protocol FROM summoning_protocols
                WHERE persona_id = ?
            ''', (persona_id,))
            
            protocol_row = cursor.fetchone()
            if protocol_row:
                export['summoning_protocol'] = protocol_row[0]
                export['compact_protocol'] = protocol_row[1]
            
            # Get state history if requested
            if include_history:
                cursor.execute('''
                    SELECT state_snapshot, timestamp FROM persona_state_history
                    WHERE persona_id = ?
                    ORDER BY timestamp DESC
                ''', (persona_id,))
                
                export['state_history'] = [
                    {
                        'state': json.loads(row[0]),
                        'timestamp': row[1]
                    }
                    for row in cursor.fetchall()
                ]
            
            return export
            
        finally:
            conn.close()
