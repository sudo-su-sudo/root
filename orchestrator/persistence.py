"""
Persistence Layer for Learning Orchestrator

Handles saving and loading orchestrator state to/from SQLite database.
"""

import sqlite3
import json
import pickle
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class OrchestratorPersistence:
    """Handles persistent storage of orchestrator state"""
    
    def __init__(self, db_path: str = "orchestrator_data.db"):
        """
        Initialize persistence layer
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                last_accessed TIMESTAMP,
                last_saved TIMESTAMP
            )
        ''')
        
        # Orchestrator state table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orchestrator_state (
                user_id TEXT PRIMARY KEY,
                state_data BLOB,
                framework_data TEXT,
                decisions_count INTEGER,
                patterns_count INTEGER,
                last_update TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_sessions(user_id)
            )
        ''')
        
        # Decision history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decision_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                situation TEXT,
                chosen_option TEXT,
                rejected_options TEXT,
                reasoning TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_sessions(user_id)
            )
        ''')
        
        # Learning patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_sessions(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user_session(self, user_id: str) -> bool:
        """
        Create a new user session
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            True if created, False if already exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_sessions (user_id, created_at, last_accessed, last_saved)
                VALUES (?, ?, ?, ?)
            ''', (user_id, datetime.now(), datetime.now(), datetime.now()))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # User already exists
            return False
        finally:
            conn.close()
    
    def update_last_accessed(self, user_id: str):
        """Update last accessed timestamp for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions
            SET last_accessed = ?
            WHERE user_id = ?
        ''', (datetime.now(), user_id))
        
        conn.commit()
        conn.close()
    
    def save_orchestrator(self, user_id: str, orchestrator: Any) -> bool:
        """
        Save orchestrator state to database
        
        Args:
            user_id: User identifier
            orchestrator: LearningOrchestrator instance
            
        Returns:
            True if saved successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Serialize the orchestrator state
            state_data = pickle.dumps(orchestrator)
            
            # Extract framework data for easier querying
            framework_data = json.dumps({
                'goals': orchestrator.framework.goals,
                'values': orchestrator.framework.values,
                'intent': orchestrator.framework.intent,
                'mental_model': orchestrator.framework.mental_model
            })
            
            # Count decisions and patterns
            decisions_count = len(orchestrator.preference_learner.decision_history)
            patterns_count = len(orchestrator.preference_learner.reasoning_patterns)
            
            # Insert or update
            cursor.execute('''
                INSERT OR REPLACE INTO orchestrator_state
                (user_id, state_data, framework_data, decisions_count, patterns_count, last_update)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, state_data, framework_data, decisions_count, patterns_count, datetime.now()))
            
            # Update last saved timestamp
            cursor.execute('''
                UPDATE user_sessions
                SET last_saved = ?
                WHERE user_id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error saving orchestrator: {e}")
            return False
        finally:
            conn.close()
    
    def load_orchestrator(self, user_id: str) -> Optional[Any]:
        """
        Load orchestrator state from database
        
        Args:
            user_id: User identifier
            
        Returns:
            LearningOrchestrator instance or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT state_data FROM orchestrator_state
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                # Deserialize orchestrator
                orchestrator = pickle.loads(row[0])
                self.update_last_accessed(user_id)
                return orchestrator
            return None
            
        except Exception as e:
            print(f"Error loading orchestrator: {e}")
            return None
        finally:
            conn.close()
    
    def save_decision(self, user_id: str, situation: str, chosen: str, 
                      rejected: str, reasoning: str):
        """Save individual decision to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO decision_history
            (user_id, situation, chosen_option, rejected_options, reasoning, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, situation, chosen, rejected, reasoning, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get session info
        cursor.execute('''
            SELECT created_at, last_accessed, last_saved
            FROM user_sessions
            WHERE user_id = ?
        ''', (user_id,))
        
        session_row = cursor.fetchone()
        
        # Get orchestrator stats
        cursor.execute('''
            SELECT decisions_count, patterns_count, last_update
            FROM orchestrator_state
            WHERE user_id = ?
        ''', (user_id,))
        
        state_row = cursor.fetchone()
        
        conn.close()
        
        if not session_row:
            return {}
        
        stats = {
            'created_at': session_row[0],
            'last_accessed': session_row[1],
            'last_saved': session_row[2],
            'decisions_count': state_row[0] if state_row else 0,
            'patterns_count': state_row[1] if state_row else 0,
            'last_update': state_row[2] if state_row else None
        }
        
        return stats
    
    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Export all user data as JSON"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get decisions
        cursor.execute('''
            SELECT situation, chosen_option, rejected_options, reasoning, timestamp
            FROM decision_history
            WHERE user_id = ?
            ORDER BY timestamp
        ''', (user_id,))
        
        decisions = [
            {
                'situation': row[0],
                'chosen': row[1],
                'rejected': row[2],
                'reasoning': row[3],
                'timestamp': row[4]
            }
            for row in cursor.fetchall()
        ]
        
        # Get framework
        cursor.execute('''
            SELECT framework_data FROM orchestrator_state
            WHERE user_id = ?
        ''', (user_id,))
        
        framework_row = cursor.fetchone()
        framework = json.loads(framework_row[0]) if framework_row else {}
        
        conn.close()
        
        return {
            'user_id': user_id,
            'exported_at': datetime.now().isoformat(),
            'framework': framework,
            'decisions': decisions
        }
    
    def import_user_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Import user data from JSON"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Import decisions
            for decision in data.get('decisions', []):
                cursor.execute('''
                    INSERT INTO decision_history
                    (user_id, situation, chosen_option, rejected_options, reasoning, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    decision['situation'],
                    decision['chosen'],
                    decision['rejected'],
                    decision['reasoning'],
                    decision.get('timestamp', datetime.now())
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def list_users(self) -> list:
        """List all user sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, created_at, last_accessed, last_saved
            FROM user_sessions
            ORDER BY last_accessed DESC
        ''')
        
        users = [
            {
                'user_id': row[0],
                'created_at': row[1],
                'last_accessed': row[2],
                'last_saved': row[3]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return users
    
    def delete_user(self, user_id: str) -> bool:
        """Delete all data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM decision_history WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM learning_patterns WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM orchestrator_state WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()
